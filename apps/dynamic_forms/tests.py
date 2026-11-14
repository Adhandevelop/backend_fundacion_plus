import uuid
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import Role, User
from apps.audit.models import AuditLog
from apps.communications.models import LegalDocument
from apps.dynamic_forms.models import (
    Formulario,
    FormularioEnvio,
    FormularioNotificacion,
    FormularioPregunta,
    FormularioToken,
    FormularioVersion,
)


class DynamicFormsModuleTests(APITestCase):
    """
    Suite de pruebas integrales para el módulo de Formularios Dinámicos de PLUS:
    - Autorización y capacidad can_manage_forms.
    - Ciclo de vida y versionado inmutable del formulario (borrador, publicar, cerrar, reabrir, archivar, duplicar).
    - Concurrencia optimista y estabilidad de códigos.
    - Validación rigurosa de respuestas, tipos y documento legal vigente.
    - Obligatoriedad de Idempotency-Key y respuesta neutral anti-enumeración.
    - Creación de cuenta ciudadana pendiente y token uniuso SHA-256.
    - Activación de cuenta y fijación de clave (login_required).
    - Portal ciudadano "Mis Formularios" (IsCitizenOnly).
    - Consulta detallada y exportación CSV sanitizada para administradores.
    """

    def setUp(self):
        # Roles
        self.admin_role, _ = Role.objects.get_or_create(nombre=Role.Nombre.ADMINISTRADOR)
        self.citizen_role, _ = Role.objects.get_or_create(nombre=Role.Nombre.CIUDADANO)
        self.moderator_role, _ = Role.objects.get_or_create(nombre=Role.Nombre.MODERADOR)

        # Usuarios
        self.admin_user = User.objects.create_user(
            username='admin_forms',
            email='admin_forms@plus.org',
            password='AdminPassword123!',
            rol=self.admin_role,
            is_staff=True,
        )
        self.moderator_user = User.objects.create_user(
            username='mod_forms',
            email='mod_forms@plus.org',
            password='ModPassword123!',
            rol=self.moderator_role,
            is_staff=True,
        )
        self.citizen_user = User.objects.create_user(
            username='ciudadano_forms',
            email='ciudadano_forms@plus.org',
            password='CitizenPassword123!',
            rol=self.citizen_role,
        )

        # Documento legal vigente de tratamiento de datos
        self.legal_doc = LegalDocument.get_current('tratamiento_datos')

    def test_can_manage_forms_exposed_in_me_endpoint(self):
        # 1. Administrador tiene can_manage_forms = True
        self.client.force_authenticate(user=self.admin_user)
        res_adm = self.client.get('/api/v1/me/')
        self.assertEqual(res_adm.status_code, status.HTTP_200_OK)
        self.assertTrue(res_adm.data.get('can_manage_forms'))
        self.assertTrue(res_adm.data['permissions'].get('can_manage_forms'))

        # 2. Moderador tiene can_manage_forms = False
        self.client.force_authenticate(user=self.moderator_user)
        res_mod = self.client.get('/api/v1/me/')
        self.assertEqual(res_mod.status_code, status.HTTP_200_OK)
        self.assertFalse(res_mod.data.get('can_manage_forms'))

        # 3. Ciudadano tiene can_manage_forms = False
        self.client.force_authenticate(user=self.citizen_user)
        res_ciu = self.client.get('/api/v1/me/')
        self.assertEqual(res_ciu.status_code, status.HTTP_200_OK)
        self.assertFalse(res_ciu.data.get('can_manage_forms'))

    def test_admin_form_lifecycle_and_versioning(self):
        self.client.force_authenticate(user=self.admin_user)

        # 1. Crear borrador de formulario con preguntas y opciones
        create_payload = {
            'slug': 'encuesta-servicios-meta',
            'titulo': 'Encuesta de Servicios Públicos en el Meta',
            'descripcion': 'Diagnóstico de cobertura y calidad de agua y energía.',
            'requiere_documento': True,
            'permite_multiples_envios': False,
            'preguntas': [
                {
                    'codigo': 'barrio_residencia',
                    'enunciado': '¿En qué sector o barrio reside?',
                    'tipo_campo': 'texto_corto',
                    'es_obligatorio': True,
                    'orden': 1,
                    'configuracion_validacion': {'min_length': 3, 'max_length': 100},
                },
                {
                    'codigo': 'servicio_fallas',
                    'enunciado': '¿Qué servicio presenta mayores fallas?',
                    'tipo_campo': 'seleccion_unica',
                    'es_obligatorio': True,
                    'orden': 2,
                    'opciones': [
                        {'valor': 'agua', 'etiqueta': 'Acueducto y Agua Potable', 'orden': 1},
                        {'valor': 'energia', 'etiqueta': 'Energía Eléctrica', 'orden': 2},
                    ],
                },
                {
                    'codigo': 'calificacion_general',
                    'enunciado': 'Califique el servicio de 1 a 5:',
                    'tipo_campo': 'numero',
                    'es_obligatorio': False,
                    'orden': 3,
                    'configuracion_validacion': {'min_value': 1, 'max_value': 5, 'integer_only': True},
                },
            ],
        }

        res_create = self.client.post('/api/v1/admin/forms/', create_payload, format='json')
        self.assertEqual(res_create.status_code, status.HTTP_201_CREATED)
        form_id = res_create.data['id']
        self.assertEqual(res_create.data['estado'], 'borrador')
        self.assertEqual(res_create.data['numero_version_publicada'], 0)
        self.assertEqual(res_create.data['revision_edicion'], 0)

        # 2. Publicar primera versión
        res_pub = self.client.post(f'/api/v1/admin/forms/{form_id}/publish/')
        self.assertEqual(res_pub.status_code, status.HTTP_200_OK)
        self.assertEqual(res_pub.data['numero_version'], 1)
        self.assertEqual(res_pub.data['estado'], 'publicado')

        form = Formulario.objects.get(pk=form_id)
        self.assertEqual(form.numero_version_publicada, 1)
        self.assertEqual(form.versiones.count(), 1)
        v1 = form.versiones.first()
        self.assertTrue(v1.es_vigente)
        self.assertEqual(v1.preguntas.count(), 3)

        # 3. Cerrar y reabrir
        res_close = self.client.post(f'/api/v1/admin/forms/{form_id}/close/')
        self.assertEqual(res_close.status_code, status.HTTP_200_OK)
        self.assertEqual(res_close.data['estado'], 'cerrado')

        res_reopen = self.client.post(f'/api/v1/admin/forms/{form_id}/reopen/')
        self.assertEqual(res_reopen.status_code, status.HTTP_200_OK)
        self.assertEqual(res_reopen.data['estado'], 'publicado')

        # 4. Duplicar formulario
        res_dup = self.client.post(f'/api/v1/admin/forms/{form_id}/duplicate/')
        self.assertEqual(res_dup.status_code, status.HTTP_201_CREATED)
        self.assertIn('-copia', res_dup.data['slug'])
        self.assertEqual(res_dup.data['estado'], 'borrador')

    def test_mandatory_idempotency_key_and_public_submission(self):
        # Preparar un formulario publicado
        self.client.force_authenticate(user=self.admin_user)
        form = Formulario.objects.create(
            slug='censo-villavicencio',
            titulo='Censo Comunitario Villavicencio',
            estado=Formulario.Estado.BORRADOR,
            requiere_documento=True,
            permite_multiples_envios=False,
            creado_por=self.admin_user,
        )
        p1 = FormularioPregunta.objects.create(
            formulario_borrador=form,
            codigo='sector_barrio',
            enunciado='Indique su barrio de residencia',
            tipo_campo=FormularioPregunta.TipoCampo.TEXTO_CORTO,
            es_obligatorio=True,
            orden=1,
        )
        p2 = FormularioPregunta.objects.create(
            formulario_borrador=form,
            codigo='acepta_reunion',
            enunciado='¿Desea participar en la asamblea comunitaria?',
            tipo_campo=FormularioPregunta.TipoCampo.BOOLEANO,
            es_obligatorio=True,
            orden=2,
        )
        # Publicar versión 1
        res_pub = self.client.post(f'/api/v1/admin/forms/{form.id}/publish/')
        self.assertEqual(res_pub.status_code, status.HTTP_200_OK)

        # Desautenticar para probar flujo público ciudadano
        self.client.credentials()
        self.client.logout()

        # 1. Consulta pública del formulario
        res_get = self.client.get('/api/v1/public/forms/censo-villavicencio/')
        self.assertEqual(res_get.status_code, status.HTTP_200_OK)
        self.assertEqual(res_get.data['slug'], 'censo-villavicencio')
        self.assertEqual(res_get.data['version_activa']['numero_version'], 1)
        preguntas = res_get.data['version_activa']['preguntas']
        p1_id = preguntas[0]['id']
        p2_id = preguntas[1]['id']

        submit_payload = {
            'datos_identificacion': {
                'nombres': 'Andrea',
                'apellidos': 'Gómez',
                'correo': 'andrea.gomez@gmail.com',
                'telefono': '3201234567',
                'tipo_documento': 'CC',
                'numero_documento': '1121543210',
            },
            'acepta_politica_datos': True,
            'id_documento_legal': str(self.legal_doc.id),
            'respuestas': [
                {'id_pregunta': p1_id, 'valor_texto': 'Ciudad Porfía Sector 2'},
                {'id_pregunta': p2_id, 'valor_booleano': True},
            ],
        }

        # 2. Rechazo por falta de Idempotency-Key
        res_fail_key = self.client.post('/api/v1/public/forms/censo-villavicencio/submit/', submit_payload, format='json')
        self.assertEqual(res_fail_key.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Idempotency-Key', str(res_fail_key.data))

        # 3. Envío exitoso con Idempotency-Key
        idempotency_key = str(uuid.uuid4())
        res_submit = self.client.post(
            '/api/v1/public/forms/censo-villavicencio/submit/',
            submit_payload,
            format='json',
            HTTP_IDEMPOTENCY_KEY=idempotency_key,
        )
        self.assertEqual(res_submit.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res_submit.data['estado'], 'recibido')
        envio_id = res_submit.data['id_envio']

        # Verificar que se creó cuenta inactiva para Andrea
        andrea_user = User.objects.filter(correo='andrea.gomez@gmail.com').first()
        self.assertIsNotNone(andrea_user)
        self.assertFalse(andrea_user.is_active)

        # Verificar que se creó token seguro de activación
        token_entry = FormularioToken.objects.filter(correo='andrea.gomez@gmail.com').first()
        self.assertIsNotNone(token_entry)
        self.assertEqual(token_entry.proposito, FormularioToken.Proposito.ACTIVAR_CUENTA)
        self.assertFalse(token_entry.usado)

        # 4. Reenvío idempotente seguro (mismo Idempotency-Key devuelve el mismo ID de envío)
        res_reentry = self.client.post(
            '/api/v1/public/forms/censo-villavicencio/submit/',
            submit_payload,
            format='json',
            HTTP_IDEMPOTENCY_KEY=idempotency_key,
        )
        self.assertEqual(res_reentry.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res_reentry.data['id_envio'], envio_id)

        # 5. Envío duplicado con diferente Idempotency-Key (cuando permite_multiples_envios es False)
        # Debe responder de forma neutral sin duplicar registros en base de datos
        res_dup = self.client.post(
            '/api/v1/public/forms/censo-villavicencio/submit/',
            submit_payload,
            format='json',
            HTTP_IDEMPOTENCY_KEY=str(uuid.uuid4()),
        )
        self.assertEqual(res_dup.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res_dup.data['estado'], 'recibido')
        self.assertEqual(FormularioEnvio.objects.filter(correo_declarado='andrea.gomez@gmail.com').count(), 1)

    def test_activation_flow_and_citizen_submission_view(self):
        # 1. Crear un formulario y envío pendiente de activación
        form = Formulario.objects.create(
            slug='encuesta-cultura',
            titulo='Encuesta de Cultura y Deporte',
            estado=Formulario.Estado.PUBLICADO,
            creado_por=self.admin_user,
        )
        version = FormularioVersion.objects.create(
            formulario=form,
            numero_version=1,
            es_vigente=True,
            titulo_congelado=form.titulo,
        )
        p = FormularioPregunta.objects.create(
            version=version,
            codigo='disciplina_interes',
            enunciado='¿Qué disciplina practica?',
            tipo_campo=FormularioPregunta.TipoCampo.TEXTO_CORTO,
        )

        andrea = User.objects.create_user(
            email='andrea.cultura@gmail.com',
            username='andrea_cultura',
            nombres='Andrea',
            apellidos='Cultura',
            rol=self.citizen_role,
            is_active=False,
        )

        envio = FormularioEnvio.objects.create(
            formulario=form,
            version=version,
            estado_vinculacion=FormularioEnvio.EstadoVinculacion.PENDIENTE_ACTIVACION,
            nombres_declarados='Andrea',
            apellidos_declarados='Cultura',
            correo_declarado='andrea.cultura@gmail.com',
        )

        from apps.dynamic_forms.services import FormularioTokenService
        raw_token, token_obj = FormularioTokenService.create_token(
            usuario=andrea,
            correo='andrea.cultura@gmail.com',
            proposito=FormularioToken.Proposito.ACTIVAR_CUENTA,
        )

        # 2. Andrea activa su cuenta mediante POST /activation/verify/
        verify_res = self.client.post(
            '/api/v1/public/forms/activation/verify/',
            {
                'token': raw_token,
                'nueva_contrasena': 'ClaveNueva2026*',
            },
            format='json',
        )
        self.assertEqual(verify_res.status_code, status.HTTP_200_OK)
        self.assertTrue(verify_res.data.get('login_required'))
        self.assertEqual(verify_res.data.get('estado'), 'activada')

        # Andrea ahora está activa
        andrea.refresh_from_db()
        self.assertTrue(andrea.is_active)
        self.assertTrue(andrea.check_password('ClaveNueva2026*'))

        # El envío ahora está vinculado a su cuenta
        envio.refresh_from_db()
        self.assertEqual(envio.estado_vinculacion, FormularioEnvio.EstadoVinculacion.VINCULADO)
        self.assertEqual(envio.usuario, andrea)

        # 3. Andrea inicia sesión y consulta "Mis Formularios"
        self.client.force_authenticate(user=andrea)
        res_me_list = self.client.get('/api/v1/me/forms/submissions/')
        self.assertEqual(res_me_list.status_code, status.HTTP_200_OK)
        self.assertEqual(res_me_list.data['count'], 1)
        self.assertEqual(res_me_list.data['results'][0]['formulario']['slug'], 'encuesta-cultura')

        res_me_detail = self.client.get(f'/api/v1/me/forms/submissions/{envio.id}/')
        self.assertEqual(res_me_detail.status_code, status.HTTP_200_OK)
        self.assertEqual(res_me_detail.data['formulario_titulo'], 'Encuesta de Cultura y Deporte')

        # 4. Un administrador recibe 403 Forbidden al intentar entrar a endpoints ciudadanos
        self.client.force_authenticate(user=self.admin_user)
        res_blocked = self.client.get('/api/v1/me/forms/submissions/')
        self.assertEqual(res_blocked.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_submission_detail_and_csv_export(self):
        self.client.force_authenticate(user=self.admin_user)

        form = Formulario.objects.create(
            slug='export-test',
            titulo='Formulario de Exportación',
            estado=Formulario.Estado.PUBLICADO,
            creado_por=self.admin_user,
        )
        version = FormularioVersion.objects.create(
            formulario=form,
            numero_version=1,
            es_vigente=True,
            titulo_congelado=form.titulo,
        )
        p = FormularioPregunta.objects.create(
            version=version,
            codigo='comentario',
            enunciado='Comentarios generales',
            tipo_campo=FormularioPregunta.TipoCampo.TEXTO_CORTO,
        )

        envio = FormularioEnvio.objects.create(
            formulario=form,
            version=version,
            estado_vinculacion=FormularioEnvio.EstadoVinculacion.VINCULADO,
            nombres_declarados='Carlos',
            apellidos_declarados='Prueba',
            correo_declarado='carlos.prueba@plus.org',
            telefono_declarado='3119876543',
            tipo_documento_declarado='CC',
            numero_documento_declarado='1020304050',
        )

        from apps.dynamic_forms.models import FormularioRespuesta
        FormularioRespuesta.objects.create(
            envio=envio,
            pregunta=p,
            codigo_pregunta='comentario',
            tipo_campo_congelado='texto_corto',
            valor_texto='=1+1 intento de inyeccion csv',
        )

        # 1. Consulta individual detallada de envío por admin
        res_det = self.client.get(f'/api/v1/admin/forms/{form.id}/submissions/{envio.id}/')
        self.assertEqual(res_det.status_code, status.HTTP_200_OK)
        self.assertEqual(res_det.data['datos_identificacion_completos']['correo'], 'carlos.prueba@plus.org')

        # 2. Exportación CSV
        res_csv = self.client.get(f'/api/v1/admin/forms/{form.id}/submissions-export/?version=1')
        self.assertEqual(res_csv.status_code, status.HTTP_200_OK)
        self.assertIn('text/csv', res_csv.headers['Content-Type'])
        self.assertIn('attachment', res_csv.headers['Content-Disposition'])

        csv_text = res_csv.content.decode('utf-8-sig')
        self.assertIn('carlos.prueba@plus.org', csv_text)
        # Verificar mitigación de inyección CSV: celda iniciada por '=' debe anteponer apóstrofe
        self.assertIn("'=1+1 intento de inyeccion csv", csv_text)

        # Verificar registro de auditoría
        audit_entry = AuditLog.objects.filter(
            modulo='formularios_dinamicos',
            accion='export',
            usuario=self.admin_user,
        ).first()
        self.assertIsNotNone(audit_entry)

    def test_p25_admin_submissions_list_and_edge_cases(self):
        """
        P25: Validación de robustez en GET /api/v1/admin/forms/{id}/submissions/:
        - Formulario con cero envíos (retorna 200 con results: []).
        - Envío anónimo pendiente de activación (sin teléfono o con telefono_declarado=None).
        - Envío vinculado a cuenta ciudadana.
        - Resolución transparente tanto por UUID como por slug del formulario.
        - Manejo seguro de 404 para identificadores no existentes (nunca 500).
        """
        self.client.force_authenticate(user=self.admin_user)

        # 1. Crear formulario nuevo sin ningún envío
        form = Formulario.objects.create(
            slug='arreglo-vial',
            titulo='Reporte de Arreglo Vial Comunitario',
            estado=Formulario.Estado.PUBLICADO,
            creado_por=self.admin_user,
        )
        version = FormularioVersion.objects.create(
            formulario=form,
            numero_version=1,
            es_vigente=True,
        )

        # Caso A: Cero envíos registrados
        res_zero = self.client.get(f'/api/v1/admin/forms/{form.id}/submissions/?page=1&page_size=20')
        self.assertEqual(res_zero.status_code, status.HTTP_200_OK)
        self.assertEqual(res_zero.data['count'], 0)
        self.assertEqual(res_zero.data['results'], [])

        # También debe funcionar si se consulta por slug
        res_zero_slug = self.client.get(f'/api/v1/admin/forms/{form.slug}/submissions/?page=1&page_size=20')
        self.assertEqual(res_zero_slug.status_code, status.HTTP_200_OK)
        self.assertEqual(res_zero_slug.data['count'], 0)
        self.assertEqual(res_zero_slug.data['results'], [])

        # Caso B: Envío anónimo pendiente de activación con telefono_declarado=None y sin cédula
        envio_anon = FormularioEnvio.objects.create(
            formulario=form,
            version=version,
            usuario=None,
            estado_vinculacion=FormularioEnvio.EstadoVinculacion.PENDIENTE_ACTIVACION,
            nombres_declarados='Vecino',
            apellidos_declarados='Anónimo',
            correo_declarado='vecino.anonimo@barrio.org',
            telefono_declarado=None,  # Simula NULL en base de datos
            tipo_documento_declarado='',
            numero_documento_declarado='',
        )

        res_anon = self.client.get(f'/api/v1/admin/forms/{form.id}/submissions/?page=1&page_size=20')
        self.assertEqual(res_anon.status_code, status.HTTP_200_OK)
        self.assertEqual(res_anon.data['count'], 1)
        sub_anon_data = res_anon.data['results'][0]
        self.assertEqual(sub_anon_data['id'], str(envio_anon.id))
        self.assertEqual(sub_anon_data['estado_vinculacion'], 'pendiente_activacion')
        self.assertEqual(sub_anon_data['ciudadano']['telefono_enmascarado'], '***')
        self.assertIsNone(sub_anon_data['ciudadano']['documento_enmascarado'])
        self.assertIn('@barrio.org', sub_anon_data['ciudadano']['correo_enmascarado'])

        # Caso C: Envío vinculado a cuenta ciudadana con teléfono completo y documento
        envio_vinc = FormularioEnvio.objects.create(
            formulario=form,
            version=version,
            usuario=self.admin_user,
            estado_vinculacion=FormularioEnvio.EstadoVinculacion.VINCULADO,
            nombres_declarados='Ciudadano',
            apellidos_declarados='Ejemplar',
            correo_declarado='ciudadano.ejemplar@plus.org',
            telefono_declarado='3109876543',
            tipo_documento_declarado='CC',
            numero_documento_declarado='1020304050',
        )

        res_two = self.client.get(f'/api/v1/admin/forms/{form.id}/submissions/?page=1&page_size=20')
        self.assertEqual(res_two.status_code, status.HTTP_200_OK)
        self.assertEqual(res_two.data['count'], 2)
        results = res_two.data['results']
        ids = [r['id'] for r in results]
        self.assertIn(str(envio_anon.id), ids)
        self.assertIn(str(envio_vinc.id), ids)

        # Verificar enmascaramiento correcto de teléfono y documento
        sub_vinc_data = next(r for r in results if r['id'] == str(envio_vinc.id))
        self.assertEqual(sub_vinc_data['ciudadano']['telefono_enmascarado'], '310****543')
        self.assertEqual(sub_vinc_data['ciudadano']['documento_enmascarado'], 'CC ***4050')

        # Caso D: Consulta con slug para formulario con envíos
        res_slug = self.client.get(f'/api/v1/admin/forms/arreglo-vial/submissions/?page=1&page_size=20')
        self.assertEqual(res_slug.status_code, status.HTTP_200_OK)
        self.assertEqual(res_slug.data['count'], 2)

        # Caso E: Consulta con identificador no existente retorna 404 limpio
        res_404_slug = self.client.get('/api/v1/admin/forms/formulario-inexistente/submissions/')
        self.assertEqual(res_404_slug.status_code, status.HTTP_404_NOT_FOUND)
        res_404_uuid = self.client.get('/api/v1/admin/forms/00000000-0000-0000-0000-000000000000/submissions/')
        self.assertEqual(res_404_uuid.status_code, status.HTTP_404_NOT_FOUND)
