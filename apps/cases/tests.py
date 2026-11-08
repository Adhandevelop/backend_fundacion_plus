from decimal import Decimal
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import Role
from apps.audit.models import AuditCase, AuditLog
from apps.cases.models import Case, CaseCategory, CaseStatus
from apps.initiatives.models import (
    Initiative,
    InitiativeActivity,
    InitiativeCaseLink,
    InitiativeCommunity,
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

        # Territorios (sección 01 de base de datos.md)
        self.department = Department.objects.create(
            codigo_dane='76',
            nombre='Valle del Cauca',
        )
        self.municipality = Municipality.objects.create(
            departamento=self.department,
            codigo_dane='76001',
            nombre='Cali',
        )
        self.community = Community.objects.create(
            municipio=self.municipality,
            nombre='Vereda El Saladito',
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

        news_cat = NewsCategory.objects.create(name='Jornadas Sociales')
        NewsArticle.objects.create(
            title='Éxito en la jornada Dulcemanía en El Saladito',
            summary='Más de 180 niños participaron en la jornada comunitaria.',
            content='Contenido completo de la noticia institucional.',
            category=news_cat,
            related_initiative=initiative,
            author=self.admin,
            publication_status=NewsArticle.PublicationStatus.PUBLISHED,
            is_featured=True,
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
