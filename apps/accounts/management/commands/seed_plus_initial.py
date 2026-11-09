from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from apps.accounts.models import Role
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

        # 3. Tipos de caso iniciales (AMP-05 naturaleza)
        tipos_data = [
            ('Infraestructura y Vías', 'infraestructura', 'problematica', 'Afectaciones viales y espacio público'),
            ('Servicios Públicos y Agua', 'servicios_publicos', 'servicio', 'Acueducto, energía y saneamiento'),
            ('Educación y Juventud', 'educacion', 'necesidad', 'Situaciones escolares y comunitarias'),
            ('Salud y Bienestar', 'salud', 'necesidad', 'Atención comunitaria y prevención'),
            ('Ambiente y Riesgo', 'ambiente', 'riesgo', 'Gestión ambiental y prevención de riesgos'),
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
            ('institucion.nombre', 'Corporacion Pluralismo Social'),
            ('mapa.srid', 4326),
            ('iniciativas.max_destacadas', 4),
        ]
        for clave, valor in configs:
            SiteSetting.objects.get_or_create(clave=clave, defaults={'valor': valor})

        self.stdout.write(self.style.SUCCESS('Catálogos de base de datos.md y endpoints.md sincronizados correctamente.'))
