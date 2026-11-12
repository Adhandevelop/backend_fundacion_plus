from decimal import Decimal
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import Role
from apps.audit.models import AuditCase, AuditLog
from apps.cases.models import Case, CaseCategory, CaseStatus, FollowedCase
from apps.initiatives.models import (
    Initiative,
    InitiativeActivity,
    InitiativeCaseLink,
    InitiativeCommunity,
    InitiativeEdition,
    InitiativeMedia,
    InitiativeMetric,
)
from apps.news.models import NewsArticle, NewsCategory
from apps.territories.models import Community, Department, Municipality
from core.gis import make_geojson_point


class CasesMapAndPlatformIntegrationTests(APITestCase):
    """
    Pruebas integrales extremo a extremo sobre el esquema de 30 tablas de base de datos.md:
    territorios (departamentos, municipios, comunidades), casos, estados_caso, tipos_caso,
    asignaciones_casos, seguimientos, historial_estados, comentarios, mensajes_privados,
    propuestas_iniciativas, iniciativas, iniciativa_ediciones, iniciativa_indicadores,
    iniciativa_actividades, iniciativa_casos y auditoria_*.
    """

    def setUp(self):
        User = get_user_model()
        self.citizen = User.objects.create_user(
            email='ciudadano@plus.org',
            password='Password123!',
            nombres='Pedro',
            apellidos='Pérez',
            role_name=Role.Nombre.CIUDADANO,
        )
        self.other_citizen = User.objects.create_user(
            email='otro@plus.org',
            password='Password123!',
            nombres='María',
            apellidos='López',
            role_name=Role.Nombre.CIUDADANO,
        )
        self.responsible = User.objects.create_user(
            email='representante@plus.org',
            password='Password123!',
            nombres='Luis',
            apellidos='Representante',
            role_name=Role.Nombre.REPRESENTANTE,
        )
        self.admin = User.objects.create_user(
            email='admin@plus.org',
            password='Password123!',
            nombres='Admin',
            apellidos='PLUS',
            role_name=Role.Nombre.ADMINISTRADOR,
        )

        # Catálogo de estados de caso (sección 08 de base de datos.md)
        CaseStatus.get_by_name('pendiente')
        CaseStatus.get_by_name('en_revision')
        CaseStatus.get_by_name('en_proceso')
        CaseStatus.get_by_name('resuelto')
        CaseStatus.get_by_name('cerrado')

        # Territorios (sección 01 de base de datos.md) - Meta y Villavicencio
        self.department = Department.objects.create(
            codigo_dane='50',
            nombre='Meta',
        )
        self.municipality = Municipality.objects.create(
            departamento=self.department,
            codigo_dane='50001',
            nombre='Villavicencio',
        )
        self.community = Community.objects.create(
            municipio=self.municipality,
            nombre='Vereda Vanguardia',
            tipo=Community.TipoComunidad.VEREDA,
            activo=True,
        )
        self.category = CaseCategory.objects.create(
            nombre='Infraestructura Vial',
            categoria='infraestructura',
            descripcion='Vías terciarias y puentes comunitarios',
            activo=True,
        )

    def test_full_case_lifecycle_map_privacy_and_tracking(self):
        # 1. Ciudadano registra un caso georreferenciado (SRID 4326)
        self.client.force_authenticate(user=self.citizen)
        create_resp = self.client.post(
            '/api/v1/citizen/cases/',
            {
                'titulo': 'Deterioro crítico de vía terciaria en El Saladito',
                'descripcion': 'Derrumbe afecta el paso escolar en la vereda.',
                'tipo_caso': str(self.category.id),
                'comunidad': str(self.community.id),
                'latitud': '3.485432',
                'longitud': '-76.614876',
                'direccion_referencia': 'Kilómetro 4 vía a la escuela rural',
            },
            format='json',
        )
        self.assertEqual(create_resp.status_code, status.HTTP_201_CREATED)
        case_id = create_resp.data['id']
        codigo = create_resp.data['codigo']
        self.assertTrue(codigo.startswith('PLUS-'))
        self.assertEqual(create_resp.data['estado_publicacion'], Case.EstadoPublicacion.PENDIENTE)
        self.assertEqual(create_resp.data['estado_nombre'], CaseStatus.Nombre.PENDIENTE)

        # 2. Un caso pendiente NO aparece en el mapa público
        self.client.force_authenticate(user=None)
        map_resp = self.client.get('/api/v1/public/cases/map/')
        self.assertEqual(map_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(map_resp.data['count'], 0)

        # 3. Administrador aprueba la publicación y asigna prioridad alta
        self.client.force_authenticate(user=self.admin)
        mod_resp = self.client.post(
            f'/api/v1/admin/cases/{case_id}/moderate/',
            {
                'estado_publicacion': 'aprobado',
                'prioridad': 'alta',
                'motivo': 'Verificado por comité territorial.',
            },
            format='json',
        )
        self.assertEqual(mod_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(mod_resp.data['estado_publicacion'], 'aprobado')
        self.assertEqual(mod_resp.data['prioridad'], 'alta')
        self.assertGreaterEqual(AuditCase.objects.filter(caso_id=case_id).count(), 1)

        # 4. El mapa público ahora incluye el caso con coordenadas generalizadas (2 decimales) y sin datos personales
        self.client.force_authenticate(user=None)
        map_after = self.client.get('/api/v1/public/cases/map/?bbox=-77.0,3.0,-76.0,4.0')
        self.assertEqual(map_after.status_code, status.HTTP_200_OK)
        self.assertEqual(map_after.data['count'], 1)
        feature = map_after.data['features'][0]
        self.assertEqual(feature['properties']['codigo'], codigo)
        self.assertEqual(feature['geometry']['coordinates'], [-76.61, 3.49])
        self.assertNotIn('usuario', feature['properties'])

        # 5. Administrador asigna representante al caso -> pasa a 'en_revision'
        self.client.force_authenticate(user=self.admin)
        assign_resp = self.client.post(
            f'/api/v1/admin/cases/{case_id}/assign/',
            {'id_responsable': str(self.responsible.id)},
            format='json',
        )
        self.assertEqual(assign_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(assign_resp.data['estado_nombre'], 'en_revision')

        # 6. Representante registra un seguimiento interno y uno público, y resuelve el caso
        self.client.force_authenticate(user=self.responsible)
        self.client.post(
            f'/api/v1/admin/cases/{case_id}/updates/',
            {
                'descripcion': 'Coordinación interna con maquinaria municipal.',
                'visible_publicamente': False,
            },
            format='json',
        )
        self.client.post(
            f'/api/v1/admin/cases/{case_id}/updates/',
            {
                'descripcion': 'Visita técnica realizada con la junta de acción comunal.',
                'visible_publicamente': True,
            },
            format='json',
        )

        # Resolver sin motivo debe fallar validación
        bad_resolve = self.client.post(
            f'/api/v1/admin/cases/{case_id}/status/',
            {'estado': 'resuelto', 'motivo': ''},
            format='json',
        )
        self.assertEqual(bad_resolve.status_code, status.HTTP_400_BAD_REQUEST)

        ok_resolve = self.client.post(
            f'/api/v1/admin/cases/{case_id}/status/',
            {'estado': 'resuelto', 'motivo': 'Vía intervenida y paso escolar habilitado.'},
            format='json',
        )
        self.assertEqual(ok_resolve.status_code, status.HTTP_200_OK)
        self.assertEqual(ok_resolve.data['estado_nombre'], 'resuelto')

        # 7. El detalle público solo muestra el seguimiento con visible_publicamente=True
        self.client.force_authenticate(user=None)
        pub_detail = self.client.get(f'/api/v1/public/cases/{codigo}/')
        self.assertEqual(pub_detail.status_code, status.HTTP_200_OK)
        self.assertEqual(len(pub_detail.data['public_updates']), 1)
        self.assertIn('Visita técnica', pub_detail.data['public_updates'][0]['descripcion'])

    def test_private_messages_and_moderated_public_comments(self):
        case = Case.objects.create(
            usuario=self.citizen,
            tipo_caso=self.category,
            comunidad=self.community,
            estado=CaseStatus.get_by_name('pendiente'),
            titulo='Caso de prueba de comunicación',
            descripcion='Descripción del caso',
            ubicacion=make_geojson_point(-76.53, 3.45),
            estado_publicacion=Case.EstadoPublicacion.APROBADO,
        )

        # Ciudadano autor envía un mensaje privado
        self.client.force_authenticate(user=self.citizen)
        msg_resp = self.client.post(
            f'/api/v1/citizen/cases/{case.id}/messages/',
            {'contenido': 'Mensaje privado para el equipo de PLUS.'},
            format='json',
        )
        self.assertEqual(msg_resp.status_code, status.HTTP_201_CREATED)

        # Otro ciudadano NO puede leer los mensajes privados del caso
        self.client.force_authenticate(user=self.other_citizen)
        forbidden_msg = self.client.get(f'/api/v1/citizen/cases/{case.id}/messages/')
        self.assertEqual(forbidden_msg.status_code, status.HTTP_403_FORBIDDEN)

        # Otro ciudadano comenta públicamente -> entra como 'pendiente'
        comm_resp = self.client.post(
            f'/api/v1/citizen/cases/{case.id}/comments/',
            {'contenido': 'Respaldamos la solicitud desde la vereda.'},
            format='json',
        )
        self.assertEqual(comm_resp.status_code, status.HTTP_201_CREATED)
        comment_id = comm_resp.data['id']

        self.client.force_authenticate(user=None)
        detail_before = self.client.get(f'/api/v1/public/cases/{case.codigo}/')
        self.assertEqual(len(detail_before.data['approved_comments']), 0)

        # Administrador aprueba el comentario -> ahora es visible públicamente
        self.client.force_authenticate(user=self.admin)
        mod_comm = self.client.post(
            f'/api/v1/admin/comments/{comment_id}/moderate/',
            {'estado_moderacion': 'aprobado'},
            format='json',
        )
        self.assertEqual(mod_comm.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(user=None)
        detail_after = self.client.get(f'/api/v1/public/cases/{case.codigo}/')
        self.assertEqual(len(detail_after.data['approved_comments']), 1)

    def test_initiatives_editions_metrics_proposals_and_home(self):
        self.client.force_authenticate(user=self.admin)
        init_resp = self.client.post(
            '/api/v1/admin/initiatives/',
            {
                'titulo': 'Dulcemanía Comunitaria',
                'subtitulo': 'Alegría y acompañamiento para la niñez',
                'descripcion_corta': 'Jornadas recreativas en comunidades rurales.',
                'descripcion': 'Detalle completo de la iniciativa Dulcemanía.',
                'categoria': 'Temporada',
                'estado': 'en_curso',
                'estado_publicacion': 'publicada',
                'destacada': True,
                'orden_destacado': 1,
            },
            format='json',
        )
        self.assertEqual(init_resp.status_code, status.HTTP_201_CREATED)
        initiative = Initiative.objects.get(pk=init_resp.data['id'])
        edicion = initiative.get_or_create_current_edition()

        InitiativeMedia.objects.create(
            iniciativa=initiative,
            tipo='imagen',
            ruta_archivo='/media/initiatives/dulcemania_portada.jpg',
            es_portada=True,
            orden=1,
        )
        InitiativeMetric.objects.create(
            edicion=edicion,
            nombre='Niños beneficiados',
            valor=Decimal('180.00'),
            unidad='niños',
            tipo_medicion='real',
            orden=1,
        )
        InitiativeCommunity.objects.create(
            edicion=edicion,
            comunidad=self.community,
            observaciones='Jornada principal realizada en la escuela rural.',
        )
        InitiativeActivity.objects.create(
            edicion=edicion,
            responsable=self.responsible,
            comunidad=self.community,
            titulo='Jornada Dulcemanía El Saladito',
            fecha_inicio='2026-10-31T09:00:00Z',
            lugar='Cancha múltiple El Saladito',
            ubicacion=make_geojson_point(-76.61, 3.48),
            estado=InitiativeActivity.Estado.REALIZADA,
        )

        # Vincular caso a la edición (iniciativa_casos)
        case = Case.objects.create(
            usuario=self.citizen,
            tipo_caso=self.category,
            comunidad=self.community,
            estado=CaseStatus.get_by_name('resuelto'),
            titulo='Adecuación de parque infantil',
            descripcion='Solicitud atendida durante la jornada.',
            estado_publicacion='aprobado',
        )
        InitiativeCaseLink.objects.create(
            edicion=edicion,
            caso=case,
            tipo_vinculo='resultado',
        )

        news_cat = NewsCategory.objects.create(nombre='Jornadas Sociales', slug='jornadas-sociales')
        NewsArticle.objects.create(
            titulo='Éxito en la jornada Dulcemanía en El Saladito',
            resumen='Más de 180 niños participaron en la jornada comunitaria.',
            contenido='Contenido completo de la noticia institucional.',
            categoria=news_cat,
            iniciativa_relacionada=initiative,
            autor=self.admin,
            estado_publicacion=NewsArticle.EstadoPublicacion.PUBLICADA,
            destacada=True,
        )

        # Postulación pública de iniciativa (propuestas_iniciativas) validando consentimiento
        self.client.force_authenticate(user=None)
        prop_resp = self.client.post(
            '/api/v1/public/event-proposals/',
            {
                'comunidad': str(self.community.id),
                'nombre_contacto': 'Junta de Acción Comunal',
                'telefono_contacto': '3001234567',
                'acepta_tratamiento_datos': True,
                'iniciativa_solicitada': str(initiative.id),
                'titulo': 'Solicitud de jornada navideña en El Saladito',
                'descripcion': 'Solicitamos acompañamiento para novena comunitaria.',
            },
            format='json',
        )
        self.assertEqual(prop_resp.status_code, status.HTTP_201_CREATED)

        home_resp = self.client.get('/api/v1/public/home/')
        self.assertEqual(home_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(home_resp.data['featured_initiatives']), 1)
        self.assertEqual(home_resp.data['featured_initiatives'][0]['titulo'], 'Dulcemanía Comunitaria')
        self.assertEqual(
            home_resp.data['featured_initiatives'][0]['portada'],
            '/media/initiatives/dulcemania_portada.jpg',
        )
        self.assertEqual(len(home_resp.data['recent_news']), 1)
        self.assertGreaterEqual(AuditLog.objects.count(), 1)

    def test_endpoints_v1_2_expansions_and_contracts(self):
        """
        Verifica los contratos de endpoints.md (AMP-01..12, CAT-01..08, ME-01..05, CIT-01..08,
        ADM-01..11, MAP-01..10, PUB-02..11, REP-01..02, AUD-01..02).
        """
        # 1. Catálogos (CAT-01..08)
        self.client.force_authenticate(user=None)
        self.assertEqual(self.client.get('/api/v1/catalogs/departments/').status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get('/api/v1/catalogs/municipalities/').status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get('/api/v1/catalogs/communities/').status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get('/api/v1/catalogs/basins/').status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get('/api/v1/catalogs/case-types/').status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get('/api/v1/catalogs/case-categories/').status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get('/api/v1/catalogs/case-statuses/').status_code, status.HTTP_200_OK)
        opts_resp = self.client.get('/api/v1/catalogs/case-options/')
        self.assertEqual(opts_resp.status_code, status.HTTP_200_OK)
        self.assertIn('prioridades', opts_resp.data)
        self.assertIn('audiencias_seguimiento', opts_resp.data)

        # 2. Perfil y preferencias (ME-01..05)
        self.client.force_authenticate(user=self.citizen)
        me_patch = self.client.patch(
            '/api/v1/me/',
            {
                'telefono': '3159876543',
                'id_departamento': str(self.department.id),
                'id_municipio': str(self.municipality.id),
                'id_comunidad': str(self.community.id),
            },
            format='json',
        )
        self.assertEqual(me_patch.status_code, status.HTTP_200_OK)
        self.assertEqual(me_patch.data['telefono'], '3159876543')
        self.assertEqual(str(me_patch.data['perfil']['id_comunidad']), str(self.community.id))

        pref_patch = self.client.patch(
            '/api/v1/me/preferences/',
            {'notificar_novedades_casos': False, 'suscrito_boletin': True},
            format='json',
        )
        self.assertEqual(pref_patch.status_code, status.HTTP_200_OK)
        self.assertFalse(pref_patch.data['notificar_novedades_casos'])
        self.assertTrue(pref_patch.data['suscrito_boletin'])

        # 3. Creación de caso en /api/v1/me/cases/ con impacto (AMP-06, CIT-02)
        case_resp = self.client.post(
            '/api/v1/me/cases/',
            {
                'titulo': 'Falta de agua potable en escuela veredal',
                'descripcion': 'El acueducto rural presenta daños en la bocatoma.',
                'id_tipo_caso': str(self.category.id),
                'id_comunidad': str(self.community.id),
                'latitud': '3.481234',
                'longitud': '-76.612345',
                'familias_afectadas': 45,
                'meses_afectacion': 3,
                'acepta_tratamiento_datos': True,
            },
            format='json',
        )
        self.assertEqual(case_resp.status_code, status.HTTP_201_CREATED)
        case_id = case_resp.data['id']
        self.assertEqual(case_resp.data['familias_afectadas'], 45)

        # 4. Solicitud de corrección por admin (ADM-07) y respuesta ciudadana con aporte (CIT-08)
        self.client.force_authenticate(user=self.admin)
        corr_resp = self.client.post(
            f'/api/v1/admin/cases/{case_id}/correction-requests/',
            {
                'motivo': 'Por favor adjuntar detalle del sector exacto de la bocatoma.',
                'campos_solicitados': ['direccion_referencia', 'evidencias'],
            },
            format='json',
        )
        self.assertEqual(corr_resp.status_code, status.HTTP_201_CREATED)
        corr_id = corr_resp.data['id_solicitud']

        self.client.force_authenticate(user=self.citizen)
        contrib_resp = self.client.post(
            f'/api/v1/me/cases/{case_id}/contributions/',
            {
                'id_solicitud_correccion': corr_id,
                'tipo_aporte': 'respuesta_correccion',
                'mensaje': 'La bocatoma queda a 300 metros arriba del puente de piedra.',
                'campos_actualizados': {'direccion_referencia': '300m arriba del puente de piedra'},
            },
            format='json',
        )
        self.assertEqual(contrib_resp.status_code, status.HTTP_201_CREATED)

        # 5. Seguimientos con 3 niveles de audiencia (AMP-07: publico, autor, interno)
        self.client.force_authenticate(user=self.admin)
        self.client.post(
            f'/api/v1/admin/cases/{case_id}/updates/',
            {'titulo': 'Nota interna', 'descripcion': 'Solo visible para staff.', 'audiencia': 'interno'},
            format='json',
        )
        self.client.post(
            f'/api/v1/admin/cases/{case_id}/updates/',
            {'titulo': 'Aviso al ciudadano', 'descripcion': 'Visible para el autor.', 'audiencia': 'autor'},
            format='json',
        )

        # El autor ve el seguimiento con audiencia='autor', pero NO el 'interno' (CIT-05)
        self.client.force_authenticate(user=self.citizen)
        timeline_resp = self.client.get(f'/api/v1/me/cases/{case_id}/timeline/')
        self.assertEqual(timeline_resp.status_code, status.HTTP_200_OK)
        audiencias_autor = [u['audiencia'] for u in timeline_resp.data['seguimientos']]
        self.assertIn('ciudadano', audiencias_autor)
        self.assertNotIn('interno', audiencias_autor)

        # 6. Cierre narrativo de caso (ADM-10) y aprobación para mapa público
        self.client.force_authenticate(user=self.admin)
        self.client.post(
            f'/api/v1/admin/cases/{case_id}/moderate/',
            {'estado_publicacion': 'aprobado', 'prioridad': 'alta'},
            format='json',
        )
        resolve_resp = self.client.post(
            f'/api/v1/admin/cases/{case_id}/resolve/',
            {
                'titulo': 'Bocatoma reparada con la comunidad',
                'descripcion': 'Se instaló nueva tubería de conducción y filtro.',
                'resultado_resumen': 'Suministro de agua restablecido para 45 familias.',
                'publicar_en_mapa': True,
            },
            format='json',
        )
        self.assertEqual(resolve_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resolve_resp.data['estado_nombre'], 'resuelto')
        self.assertEqual(
            resolve_resp.data['resultado_resumen'],
            'Suministro de agua restablecido para 45 familias.',
        )

        # 7. Casos seguidos por el ciudadano (MAP-08..10)
        self.client.force_authenticate(user=self.citizen)
        follow_post = self.client.post(f'/api/v1/me/followed-cases/{case_id}/')
        self.assertIn(follow_post.status_code, (status.HTTP_200_OK, status.HTTP_201_CREATED))
        follow_list = self.client.get('/api/v1/me/followed-cases/')
        self.assertEqual(follow_list.status_code, status.HTTP_200_OK)
        self.assertEqual(len(follow_list.data['results']), 1)

        # 8. Boletín institucional (PUB-11)
        self.client.force_authenticate(user=None)
        sub_resp = self.client.post(
            '/api/v1/public/newsletter/subscribe/',
            {
                'correo': 'boletin@comunidad.org',
                'nombre': 'Líder Comunitario',
                'intereses': ['territorio', 'iniciativas'],
                'acepta_tratamiento_datos': True,
            },
            format='json',
        )
        self.assertEqual(sub_resp.status_code, status.HTTP_201_CREATED)

        # 9. Reportes y exportación CSV (REP-01..02) y Auditoría unificada (AUD-01..02)
        self.client.force_authenticate(user=self.admin)
        rep_resp = self.client.get('/api/v1/admin/reports/cases/')
        self.assertEqual(rep_resp.status_code, status.HTTP_200_OK)
        self.assertIn('kpis', rep_resp.data)

        csv_resp = self.client.get('/api/v1/admin/reports/cases/export/')
        self.assertEqual(csv_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(csv_resp['Content-Type'], 'text/csv; charset=utf-8')

        aud_resp = self.client.get('/api/v1/admin/audit/events/')
        self.assertEqual(aud_resp.status_code, status.HTTP_200_OK)
        self.assertIn('kpis', aud_resp.data)
        self.assertGreaterEqual(aud_resp.data['count'], 1)

    def test_p22_initiative_case_links_filters_and_candidates(self):
        """
        P22:
        - GET /api/v1/admin/initiative-case-links/?edicion={uuid} filtra server-side por edición.
        - GET /api/v1/admin/initiative-case-links/?caso={uuid} y ?tipo_vinculo=...
        - GET /api/v1/admin/initiative-case-links/candidates/ lista casos aprobados con búsqueda y paginación.
        - Si se pasa ?edicion={uuid}, excluye los casos ya vinculados a esa edición.
        - Soporta alias ?id_edicion= y action /eligible-cases/.
        """
        self.client.force_authenticate(user=self.admin)

        # Crear iniciativa y dos ediciones
        init_resp = self.client.post(
            '/api/v1/admin/initiatives/',
            {
                'titulo': 'Iniciativa P22 Test',
                'subtitulo': 'Subtítulo',
                'descripcion_corta': 'Corta',
                'descripcion': 'Larga',
                'categoria': 'Comunitaria',
                'estado': 'en_curso',
                'estado_publicacion': 'publicada',
            },
            format='json',
        )
        self.assertEqual(init_resp.status_code, status.HTTP_201_CREATED)
        initiative = Initiative.objects.get(pk=init_resp.data['id'])
        edicion_1 = initiative.get_or_create_current_edition()
        edicion_2 = InitiativeEdition.objects.create(
            iniciativa=initiative,
            anio=2027,
            nombre_edicion='Edición 2027',
            descripcion='Segunda edición',
        )

        # Crear dos casos aprobados
        caso_1 = Case.objects.create(
            usuario=self.citizen,
            tipo_caso=self.category,
            comunidad=self.community,
            estado=CaseStatus.get_by_name('en_proceso'),
            titulo='Caso Pavimentación Calle 5',
            descripcion='Detalles de pavimentación requerida.',
            estado_publicacion=Case.EstadoPublicacion.APROBADO,
        )
        caso_2 = Case.objects.create(
            usuario=self.other_citizen,
            tipo_caso=self.category,
            comunidad=self.community,
            estado=CaseStatus.get_by_name('en_proceso'),
            titulo='Caso Parque La Esperanza',
            descripcion='Recuperación de juegos infantiles.',
            estado_publicacion=Case.EstadoPublicacion.APROBADO,
        )

        # Vincular caso_1 a edicion_1
        link_resp = self.client.post(
            '/api/v1/admin/initiative-case-links/',
            {
                'edicion': str(edicion_1.id),
                'caso': str(caso_1.id),
                'tipo_vinculo': 'hallazgo',
                'observaciones': 'Detectado en visita técnica preliminar.',
            },
            format='json',
        )
        self.assertEqual(link_resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(link_resp.data['caso_codigo'], caso_1.codigo)
        self.assertEqual(link_resp.data['caso_titulo'], 'Caso Pavimentación Calle 5')

        # 1. Filtro por edicion (edicion_1 debe traer 1, edicion_2 debe traer 0)
        list_e1 = self.client.get(f'/api/v1/admin/initiative-case-links/?edicion={edicion_1.id}')
        self.assertEqual(list_e1.status_code, status.HTTP_200_OK)
        results_e1 = list_e1.data.get('results', list_e1.data)
        self.assertEqual(len(results_e1), 1)
        self.assertEqual(results_e1[0]['caso'], caso_1.id)

        # Alias id_edicion
        list_alias = self.client.get(f'/api/v1/admin/initiative-case-links/?id_edicion={edicion_1.id}')
        self.assertEqual(list_alias.status_code, status.HTTP_200_OK)
        results_alias = list_alias.data.get('results', list_alias.data)
        self.assertEqual(len(results_alias), 1)

        # Filtro con edicion_2 (vacío)
        list_e2 = self.client.get(f'/api/v1/admin/initiative-case-links/?edicion={edicion_2.id}')
        self.assertEqual(list_e2.status_code, status.HTTP_200_OK)
        results_e2 = list_e2.data.get('results', list_e2.data)
        self.assertEqual(len(results_e2), 0)

        # Error de validación con UUID inválido
        list_err = self.client.get('/api/v1/admin/initiative-case-links/?edicion=invalid-uuid')
        self.assertEqual(list_err.status_code, status.HTTP_400_BAD_REQUEST)

        # 2. Endpoint de candidatos (/candidates/):
        # Sin edicion, debe listar ambos casos aprobados
        cand_all = self.client.get('/api/v1/admin/initiative-case-links/candidates/')
        self.assertEqual(cand_all.status_code, status.HTTP_200_OK)
        results_all = cand_all.data.get('results', cand_all.data)
        cand_all_ids = [str(c['id']) for c in results_all]
        self.assertIn(str(caso_1.id), cand_all_ids)
        self.assertIn(str(caso_2.id), cand_all_ids)

        # Con ?edicion={edicion_1.id}, debe excluir caso_1 y listar caso_2
        cand_e1 = self.client.get(f'/api/v1/admin/initiative-case-links/candidates/?edicion={edicion_1.id}')
        self.assertEqual(cand_e1.status_code, status.HTTP_200_OK)
        results_cand_e1 = cand_e1.data.get('results', cand_e1.data)
        cand_e1_ids = [str(c['id']) for c in results_cand_e1]
        self.assertNotIn(str(caso_1.id), cand_e1_ids)
        self.assertIn(str(caso_2.id), cand_e1_ids)

        # Búsqueda textual ?search=Esperanza
        cand_search = self.client.get(f'/api/v1/admin/initiative-case-links/candidates/?edicion={edicion_1.id}&search=Esperanza')
        self.assertEqual(cand_search.status_code, status.HTTP_200_OK)
        results_search = cand_search.data.get('results', cand_search.data)
        self.assertEqual(len(results_search), 1)
        self.assertEqual(results_search[0]['id'], str(caso_2.id))

        # Alias /eligible-cases/
        cand_alias = self.client.get(f'/api/v1/admin/initiative-case-links/eligible-cases/?edicion={edicion_1.id}')
        self.assertEqual(cand_alias.status_code, status.HTTP_200_OK)
        results_cand_alias = cand_alias.data.get('results', cand_alias.data)
        cand_alias_ids = [str(c['id']) for c in results_cand_alias]
        self.assertNotIn(str(caso_1.id), cand_alias_ids)
        self.assertIn(str(caso_2.id), cand_alias_ids)

    def test_p23_initiative_activity_eligible_responsibles_and_geopoint(self):
        """
        P23:
        - Selector de responsables elegibles: GET /api/v1/admin/initiative-activities/eligible-responsibles/
        - Excluye ciudadanos y usuarios inactivos; retorna administradores, representantes y moderadores.
        - Validación de responsable en InitiativeActivity: rechaza ciudadanos (400), acepta roles institucionales.
        - DTO de coordenadas PostGIS Point SRID 4326:
          * Acepta GeoJSON {"type": "Point", "coordinates": [-76.53, 3.45], "srid": 4326}
          * Acepta {"lat": 3.45, "lng": -76.53}
          * Acepta campos directos latitud/longitud
          * Rechaza SRID diferente de 4326 con 400
          * Rechaza coordenadas fuera de Colombia con 400
          * Lectura retorna formato GeoJSON estándar con srid 4326
        """
        self.client.force_authenticate(user=self.admin)

        # 1. Selector de responsables elegibles
        resp_res = self.client.get('/api/v1/admin/initiative-activities/eligible-responsibles/')
        self.assertEqual(resp_res.status_code, status.HTTP_200_OK)
        users_list = resp_res.data.get('results', resp_res.data)
        user_ids = [str(u['id']) for u in users_list]
        self.assertIn(str(self.admin.id), user_ids)
        self.assertIn(str(self.responsible.id), user_ids)
        self.assertNotIn(str(self.citizen.id), user_ids)
        self.assertNotIn(str(self.other_citizen.id), user_ids)

        # Filtro por rol
        rep_filter = self.client.get('/api/v1/admin/initiative-activities/eligible-responsibles/?rol=representante')
        self.assertEqual(rep_filter.status_code, status.HTTP_200_OK)
        rep_results = rep_filter.data.get('results', rep_filter.data)
        self.assertTrue(all(u['rol_nombre'] == 'representante' for u in rep_results))

        # Alias en /initiatives/
        ini_resp_res = self.client.get('/api/v1/admin/initiatives/eligible-responsibles/')
        self.assertEqual(ini_resp_res.status_code, status.HTTP_200_OK)

        # Preparar iniciativa y edición
        init_resp = self.client.post(
            '/api/v1/admin/initiatives/',
            {
                'titulo': 'Iniciativa Actividades P23',
                'subtitulo': 'Subtítulo',
                'descripcion_corta': 'Corta',
                'descripcion': 'Larga',
                'categoria': 'Comunitaria',
                'estado': 'en_curso',
                'estado_publicacion': 'publicada',
            },
            format='json',
        )
        self.assertEqual(init_resp.status_code, status.HTTP_201_CREATED)
        initiative = Initiative.objects.get(pk=init_resp.data['id'])
        edicion = initiative.get_or_create_current_edition()

        # 2. Validación de responsable: rechazar ciudadano
        bad_act_resp = self.client.post(
            '/api/v1/admin/initiative-activities/',
            {
                'edicion': str(edicion.id),
                'responsable': str(self.citizen.id),
                'titulo': 'Actividad no autorizada',
                'fecha_inicio': '2026-11-20T10:00:00Z',
            },
            format='json',
        )
        self.assertEqual(bad_act_resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('responsable', bad_act_resp.data.get('errors', bad_act_resp.data))

        # 3. GeoPoint: rechazar SRID inválido
        srid_err_resp = self.client.post(
            '/api/v1/admin/initiative-activities/',
            {
                'edicion': str(edicion.id),
                'responsable': str(self.responsible.id),
                'titulo': 'Actividad SRID Inválido',
                'fecha_inicio': '2026-11-20T10:00:00Z',
                'ubicacion': {
                    'type': 'Point',
                    'srid': 3857,
                    'coordinates': [-76.53, 3.45],
                },
            },
            format='json',
        )
        self.assertEqual(srid_err_resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('ubicacion', srid_err_resp.data.get('errors', srid_err_resp.data))

        # 4. GeoPoint: rechazar coordenadas fuera de Colombia
        bounds_err_resp = self.client.post(
            '/api/v1/admin/initiative-activities/',
            {
                'edicion': str(edicion.id),
                'responsable': str(self.responsible.id),
                'titulo': 'Actividad Fuera de Colombia',
                'fecha_inicio': '2026-11-20T10:00:00Z',
                'ubicacion': {
                    'type': 'Point',
                    'srid': 4326,
                    'coordinates': [2.35, 48.85],  # París
                },
            },
            format='json',
        )
        self.assertEqual(bounds_err_resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('ubicacion', bounds_err_resp.data.get('errors', bounds_err_resp.data))

        # 5. Creación exitosa con GeoJSON Point SRID 4326
        ok_act_1 = self.client.post(
            '/api/v1/admin/initiative-activities/',
            {
                'edicion': str(edicion.id),
                'responsable': str(self.responsible.id),
                'titulo': 'Taller de Huertas Comunitarias',
                'descripcion': 'Taller práctico de siembra y compostaje.',
                'fecha_inicio': '2026-11-25T09:00:00Z',
                'lugar': 'Kiosko Comunal',
                'ubicacion': {
                    'type': 'Point',
                    'srid': 4326,
                    'coordinates': [-76.5320, 3.4510],
                },
            },
            format='json',
        )
        self.assertEqual(ok_act_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ok_act_1.data['responsable_nombre'], self.responsible.full_name)
        self.assertIsNotNone(ok_act_1.data['ubicacion'])
        self.assertEqual(ok_act_1.data['ubicacion']['type'], 'Point')
        self.assertEqual(ok_act_1.data['ubicacion']['srid'], 4326)
        self.assertAlmostEqual(ok_act_1.data['ubicacion']['coordinates'][0], -76.5320, places=3)
        self.assertAlmostEqual(ok_act_1.data['ubicacion']['coordinates'][1], 3.4510, places=3)

        # 6. Creación exitosa con DTO {'lat': ..., 'lng': ...}
        ok_act_2 = self.client.post(
            '/api/v1/admin/initiative-activities/',
            {
                'edicion': str(edicion.id),
                'id_responsable': str(self.admin.id),
                'titulo': 'Feria Gastronómica Campesina',
                'fecha_inicio': '2026-11-26T10:00:00Z',
                'ubicacion': {
                    'lat': 3.4600,
                    'lng': -76.5200,
                },
            },
            format='json',
        )
        self.assertEqual(ok_act_2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ok_act_2.data['ubicacion']['type'], 'Point')
        self.assertAlmostEqual(ok_act_2.data['ubicacion']['coordinates'][0], -76.5200, places=3)
        self.assertAlmostEqual(ok_act_2.data['ubicacion']['coordinates'][1], 3.4600, places=3)

        # 7. Filtro server-side por edición en GET /initiative-activities/?edicion=
        filter_resp = self.client.get(f'/api/v1/admin/initiative-activities/?edicion={edicion.id}')
        self.assertEqual(filter_resp.status_code, status.HTTP_200_OK)
        act_results = filter_resp.data.get('results', filter_resp.data)
        self.assertGreaterEqual(len(act_results), 2)

    def test_admin_my_cases_created_by_me_and_followed_cases(self):
        """
        Contrato "Mis Casos" para cuentas administrativas:
        1. Creados por mí: POST /api/v1/admin/cases/ registra creado_por y devuelve creado_por_nombre.
        2. Filtro ?created_by_me=true en GET /api/v1/admin/cases/ retorna solo casos creados por el admin autenticado.
        3. Seguidos institucional: GET/POST/DELETE /api/v1/admin/followed-cases/
           - Exclusivo institucional (IsResponsibleOrAdmin, 403 para ciudadano).
           - Seguir activa el registro; DELETE lo desactiva lógicamente (activo=False, fecha_baja).
           - Volver a seguir reactiva el registro existente.
        """
        self.client.force_authenticate(user=self.admin)

        # 1. Crear un caso como administrador
        case_resp = self.client.post(
            '/api/v1/admin/cases/',
            {
                'titulo': 'Caso Institucional Admin 1',
                'descripcion': 'Descripción del caso creado por admin.',
                'tipo_caso': str(self.category.id),
                'comunidad': str(self.community.id),
                'prioridad': 'alta',
                'estado_publicacion': 'aprobado',
            },
            format='json',
        )
        self.assertEqual(case_resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(case_resp.data['creado_por'], str(self.admin.id))
        self.assertEqual(case_resp.data['creado_por_nombre'], self.admin.full_name)
        admin_case_id = case_resp.data['id']

        # 2. Filtrar ?created_by_me=true
        my_cases_resp = self.client.get('/api/v1/admin/cases/?created_by_me=true')
        self.assertEqual(my_cases_resp.status_code, status.HTTP_200_OK)
        results = my_cases_resp.data.get('results', my_cases_resp.data)
        my_case_ids = [c['id'] for c in results]
        self.assertIn(admin_case_id, my_case_ids)
        for c in results:
            self.assertEqual(c['creado_por'], str(self.admin.id))

        # 3. Casos seguidos institucionales (/api/v1/admin/followed-cases/)
        # Crear otro caso aprobado que el admin NO creó
        other_case = Case.objects.create(
            usuario=self.citizen,
            tipo_caso=self.category,
            comunidad=self.community,
            estado=CaseStatus.get_by_name('en_proceso'),
            titulo='Caso Ciudadano para Seguir',
            descripcion='Caso público para verificar seguimiento institucional.',
            estado_publicacion=Case.EstadoPublicacion.APROBADO,
        )

        # Seguir caso vía POST /admin/followed-cases/{case_id}/
        follow_resp = self.client.post(f'/api/v1/admin/followed-cases/{other_case.id}/')
        self.assertEqual(follow_resp.status_code, status.HTTP_200_OK)
        self.assertTrue(follow_resp.data['activo'])
        self.assertEqual(follow_resp.data['id_caso'], str(other_case.id))

        # Listar seguidos: GET /admin/followed-cases/
        list_followed = self.client.get('/api/v1/admin/followed-cases/')
        self.assertEqual(list_followed.status_code, status.HTTP_200_OK)
        followed_results = list_followed.data.get('results', list_followed.data)
        followed_ids = [f['id_caso'] for f in followed_results]
        self.assertIn(str(other_case.id), followed_ids)

        # Consultar detalle de seguimiento
        detail_follow = self.client.get(f'/api/v1/admin/followed-cases/{other_case.id}/')
        self.assertEqual(detail_follow.status_code, status.HTTP_200_OK)
        self.assertTrue(detail_follow.data['followed'])

        # Dejar de seguir: DELETE /admin/followed-cases/{case_id}/
        unfollow_resp = self.client.delete(f'/api/v1/admin/followed-cases/{other_case.id}/')
        self.assertEqual(unfollow_resp.status_code, status.HTTP_204_NO_CONTENT)

        # Verificar baja lógica: activo=False, fecha_baja poblada
        follow_record = FollowedCase.objects.get(usuario=self.admin, caso=other_case)
        self.assertFalse(follow_record.activo)
        self.assertIsNotNone(follow_record.fecha_baja)

        # Ya no aparece en el listado activo
        list_after = self.client.get('/api/v1/admin/followed-cases/')
        self.assertEqual(list_after.status_code, status.HTTP_200_OK)
        after_ids = [f['id_caso'] for f in list_after.data.get('results', list_after.data)]
        self.assertNotIn(str(other_case.id), after_ids)

        # Volver a seguir reactiva el registro
        refollow_resp = self.client.post('/api/v1/admin/followed-cases/', {'caso': str(other_case.id)}, format='json')
        self.assertEqual(refollow_resp.status_code, status.HTTP_200_OK)
        follow_record.refresh_from_db()
        self.assertTrue(follow_record.activo)
        self.assertIsNone(follow_record.fecha_baja)

        # Exclusividad: cuenta ciudadana recibe 403 Forbidden en /admin/followed-cases/
        self.client.force_authenticate(user=self.citizen)
        cit_resp = self.client.get('/api/v1/admin/followed-cases/')
        self.assertEqual(cit_resp.status_code, status.HTTP_403_FORBIDDEN)

        # 4. Historial de moderación de comentarios (P14)
        self.client.force_authenticate(user=self.admin)
        from apps.communications.models import CaseComment
        comm = CaseComment.objects.create(
            caso=other_case,
            usuario=self.citizen,
            contenido='Comentario para prueba de historial.',
            estado_moderacion='pendiente',
        )
        # Moderar comentario para generar evento en auditoria_eventos
        self.client.post(
            f'/api/v1/admin/comments/{comm.id}/moderation/',
            {
                'estado_moderacion': 'aprobado',
                'motivo': 'Aprobado tras revisión comunitaria.',
            },
            format='json',
        )
        hist_resp = self.client.get(f'/api/v1/admin/comments/{comm.id}/history/')
        self.assertEqual(hist_resp.status_code, status.HTTP_200_OK)
        hist_results = hist_resp.data.get('results', hist_resp.data.get('history', []))
        self.assertGreaterEqual(len(hist_results), 1)
        self.assertEqual(hist_results[0]['decision'], 'aprobado')
        self.assertEqual(hist_results[0]['actor_nombre'], self.admin.full_name)
        self.assertEqual(hist_results[0]['motivo'], 'Aprobado tras revisión comunitaria.')
