from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction
from rest_framework.authtoken.models import Token

from apps.accounts.models import Role, User, UserPreference, UserProfile
from apps.cases.models import CaseCategory, CaseStatus
from apps.communications.models import LegalDocument, SiteSetting
from apps.news.models import NewsCategory


class Command(BaseCommand):
    help = 'Inicializa los catálogos oficiales de base de datos.md y endpoints.md (roles, estados_caso, tipos_caso, categorias_noticias, documentos_legales, configuracion_plataforma).'

    @transaction.atomic
    def handle(self, *args, **options):
        # 1. Roles oficiales de base de datos.md (sección 08)
        roles_data = [
            ('administrador', 'Administracion general de PLUS'),
            ('representante', 'Representacion y gestion territorial'),
            ('moderador', 'Revision de publicaciones y comentarios'),
            ('ciudadano', 'Usuario que reporta casos y propone iniciativas'),
        ]
        for nombre, desc in roles_data:
            Role.objects.get_or_create(nombre=nombre, defaults={'descripcion': desc})

        # 2. Estados de caso oficiales de base de datos.md (sección 08)
        estados_data = [
            ('pendiente', 'Caso recibido pendiente de gestion', 1),
            ('en_revision', 'Caso en verificacion', 2),
            ('en_proceso', 'Caso en seguimiento', 3),
            ('resuelto', 'Caso solucionado', 4),
            ('cerrado', 'Caso archivado o cerrado', 5),
        ]
        for nombre, desc, orden in estados_data:
            CaseStatus.objects.get_or_create(
                nombre=nombre,
                defaults={'descripcion': desc, 'orden': orden},
            )

        # 3. Tipos de caso iniciales (AMP-12 naturaleza: problematica | proyecto_iniciativa | otro)
        tipos_data = [
            ('Infraestructura y Vías', 'infraestructura', 'problematica', 'Afectaciones viales y espacio público'),
            ('Servicios Públicos y Agua', 'servicios_publicos', 'problematica', 'Acueducto, energía y saneamiento'),
            ('Educación y Juventud', 'educacion', 'proyecto_iniciativa', 'Situaciones escolares y comunitarias'),
            ('Salud y Bienestar', 'salud', 'problematica', 'Atención comunitaria y prevención'),
            ('Ambiente y Riesgo', 'ambiente', 'problematica', 'Gestión ambiental y prevención de riesgos'),
        ]
        for nombre, categoria, naturaleza, desc in tipos_data:
            CaseCategory.objects.update_or_create(
                categoria=categoria,
                nombre=nombre,
                defaults={'naturaleza': naturaleza, 'descripcion': desc, 'activo': True},
            )

        # 4. Categorías de noticias (AMP-01)
        news_cats = [
            ('Institucional', 'institucional', 'Noticias y comunicados institucionales de PLUS'),
            ('Territorio', 'territorio', 'Trabajo comunitario y presencia territorial'),
            ('Iniciativas', 'iniciativas', 'Avances de programas e iniciativas sociales'),
            ('Impacto Social', 'impacto-social', 'Resultados y casos resueltos con las comunidades'),
            ('Convocatorias', 'convocatorias', 'Invitaciones y jornadas abiertas a la ciudadanía'),
            ('Comunicados Oficiales', 'comunicados-oficiales', 'Pronunciamientos oficiales de la fundación'),
        ]
        for nombre, slug, desc in news_cats:
            NewsCategory.objects.get_or_create(
                slug=slug,
                defaults={'nombre': nombre, 'descripcion': desc, 'activa': True},
            )

        # 5. Documentos legales iniciales (AMP-09 / AMP-12)
        legal_docs = [
            (
                'terminos_condiciones',
                '1.0',
                'Términos y condiciones de uso de la plataforma PLUS',
                'Términos y condiciones oficiales para la participación ciudadana y uso responsable de la plataforma PLUS.',
            ),
            (
                'tratamiento_datos',
                '1.0',
                'Política de tratamiento de datos personales conforme a Ley 1581 de 2012',
                'Autorización expresa para el tratamiento de datos personales conforme a la Ley 1581 de 2012.',
            ),
            (
                'boletin',
                '1.0',
                'Política de suscripción al boletín institucional PLUS',
                'Consentimiento informado para el envío de boletines y novedades institucionales de PLUS.',
            ),
        ]
        for tipo, version, titulo, contenido in legal_docs:
            LegalDocument.objects.get_or_create(
                tipo=tipo,
                version=version,
                defaults={'titulo': titulo, 'contenido': contenido, 'vigente': True},
            )

        # 6. Configuración plataforma (sección 08 de base de datos.md)
        configs = [
            ('institucion.nombre', 'Corporación Pluralismo Social'),
            ('mapa.srid', 4326),
            ('iniciativas.max_destacadas', 4),
            ('SUPERADMIN_EMAILS', ['admin@plus.org', 'superadmin@plus.org']),
            (
                'INSTITUTION_HERO',
                {
                    'image_url': '/media/site/hero/home_hero_default.jpg',
                    'url': '/media/site/hero/home_hero_default.jpg',
                    'relative_url': '/media/site/hero/home_hero_default.jpg',
                    'api_media_url': '/api/v1/public/media/site/hero/home_hero_default.jpg',
                    'alt_text': 'Comunidad y equipo de la Fundación PLUS en territorio',
                    'version': '1',
                    'corporation_name': 'Corporación Pluralismo Social',
                    'acronym': 'PLUS',
                },
            ),
        ]
        for clave, valor in configs:
            SiteSetting.objects.get_or_create(clave=clave, defaults={'valor': valor})

        # 7. Territorios de Colombia (departamentos, municipios principales y comunidades)
        call_command('seed_territories')

        # 8. Usuarios iniciales (1 Administrador y 1 Ciudadano)
        admin_role = Role.objects.get(nombre='administrador')
        citizen_role = Role.objects.get(nombre='ciudadano')

        initial_users = [
            {
                'correo': 'admin@plus.org',
                'password': 'AdminPlus2026!',
                'nombres': 'Administrador',
                'apellidos': 'PLUS',
                'telefono': '3000000001',
                'rol': admin_role,
            },
            {
                'correo': 'ciudadano@plus.org',
                'password': 'CiudadanoPlus2026!',
                'nombres': 'María Fernanda',
                'apellidos': 'López',
                'telefono': '3000000002',
                'rol': citizen_role,
            },
        ]
        for udata in initial_users:
            user = User.objects.filter(correo__iexact=udata['correo']).first()
            if not user:
                user = User.objects.create_user(
                    correo=udata['correo'],
                    password=udata['password'],
                    nombres=udata['nombres'],
                    apellidos=udata['apellidos'],
                    telefono=udata['telefono'],
                    rol=udata['rol'],
                    estado=User.Estado.ACTIVO,
                )
            else:
                user.rol = udata['rol']
                user.estado = User.Estado.ACTIVO
                user.set_password(udata['password'])
                user.save()
            UserProfile.objects.get_or_create(usuario=user)
            UserPreference.objects.get_or_create(usuario=user)
            Token.objects.get_or_create(user=user)

        # 9. Formulario dinámico de prueba publicado (censo-comunitario-meta)
        try:
            from apps.dynamic_forms.models import (
                Formulario,
                FormularioOpcion,
                FormularioPregunta,
                FormularioVersion,
            )
            admin_user = User.objects.filter(correo='admin@plus.org').first()
            demo_slug = 'censo-comunitario-meta'
            demo_form, created = Formulario.objects.get_or_create(
                slug=demo_slug,
                defaults={
                    'titulo': 'Censo de Necesidades Comunitarias del Meta 2026',
                    'descripcion': 'Consulta participativa sobre prioridades de servicios públicos e infraestructura en comunidades del Meta.',
                    'estado': Formulario.Estado.PUBLICADO,
                    'requiere_documento': True,
                    'permite_multiples_envios': False,
                    'numero_version_publicada': 1,
                    'revision_edicion': 1,
                    'creado_por': admin_user,
                },
            )
            if created or not demo_form.versiones.exists():
                version, _ = FormularioVersion.objects.get_or_create(
                    formulario=demo_form,
                    numero_version=1,
                    defaults={
                        'es_vigente': True,
                        'titulo_congelado': demo_form.titulo,
                        'descripcion_congelada': demo_form.descripcion,
                        'requiere_documento': True,
                        'permite_multiples_envios': False,
                        'publicado_por': admin_user,
                    },
                )
                p1, _ = FormularioPregunta.objects.get_or_create(
                    version=version,
                    codigo='barrio_sector',
                    defaults={
                        'enunciado': '¿En qué barrio, vereda o sector reside actualmente?',
                        'tipo_campo': FormularioPregunta.TipoCampo.TEXTO_CORTO,
                        'es_obligatorio': True,
                        'orden': 1,
                        'configuracion_validacion': {'min_length': 3, 'max_length': 150},
                    },
                )
                p2, _ = FormularioPregunta.objects.get_or_create(
                    version=version,
                    codigo='servicios_afectados',
                    defaults={
                        'enunciado': '¿Qué servicios presentan mayores fallas o intermitencias?',
                        'tipo_campo': FormularioPregunta.TipoCampo.SELECCION_MULTIPLE,
                        'es_obligatorio': True,
                        'orden': 2,
                        'configuracion_validacion': {'min_items': 1, 'max_items': 4},
                    },
                )
                for o_val, o_lbl, o_ord in [
                    ('acueducto', 'Agua potable y acueducto', 1),
                    ('alcantarillado', 'Alcantarillado y aguas residuales', 2),
                    ('energia', 'Energía eléctrica', 3),
                    ('vias', 'Vías y transporte público', 4),
                ]:
                    FormularioOpcion.objects.get_or_create(
                        pregunta=p2,
                        valor=o_val,
                        defaults={'etiqueta': o_lbl, 'orden': o_ord},
                    )

                p3, _ = FormularioPregunta.objects.get_or_create(
                    version=version,
                    codigo='descripcion_necesidad',
                    defaults={
                        'enunciado': 'Describa brevemente la principal problemática o necesidad:',
                        'tipo_campo': FormularioPregunta.TipoCampo.TEXTO_LARGO,
                        'es_obligatorio': True,
                        'orden': 3,
                        'configuracion_validacion': {'min_length': 10, 'max_length': 2000},
                    },
                )
                p4, _ = FormularioPregunta.objects.get_or_create(
                    version=version,
                    codigo='desea_participar',
                    defaults={
                        'enunciado': '¿Desea participar en las mesas de trabajo y veeduría social?',
                        'tipo_campo': FormularioPregunta.TipoCampo.BOOLEANO,
                        'es_obligatorio': False,
                        'orden': 4,
                    },
                )
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Aviso al inicializar formulario de demostración: {e}'))

        self.stdout.write(
            self.style.SUCCESS(
                'Catálogos, usuarios iniciales (admin@plus.org y ciudadano@plus.org) y formulario de prueba sincronizados correctamente.'
            )
        )
