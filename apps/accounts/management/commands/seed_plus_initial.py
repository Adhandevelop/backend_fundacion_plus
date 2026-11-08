from django.core.management.base import BaseCommand
from django.db import transaction

from apps.accounts.models import Role
from apps.cases.models import CaseCategory, CaseStatus
from apps.communications.models import SiteSetting
from apps.news.models import NewsCategory


class Command(BaseCommand):
    help = 'Inicializa los catálogos oficiales de la sección 08 de base de datos.md (roles, estados_caso, configuracion_plataforma).'

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

        # 3. Tipos de caso iniciales
        tipos_data = [
            ('Infraestructura y Vías', 'infraestructura', 'Afectaciones viales y espacio público'),
            ('Servicios Públicos y Agua', 'servicios_publicos', 'Acueducto, energía y saneamiento'),
            ('Educación y Juventud', 'educacion', 'Situaciones escolares y comunitarias'),
            ('Salud y Bienestar', 'salud', 'Atención comunitaria y prevención'),
            ('Ambiente y Riesgo', 'ambiente', 'Gestión ambiental y prevención de riesgos'),
        ]
        for nombre, categoria, desc in tipos_data:
            CaseCategory.objects.get_or_create(
                categoria=categoria,
                nombre=nombre,
                defaults={'descripcion': desc, 'activo': True},
            )

        # 4. Categorías de noticias
        for name in ('Comunicados Oficiales', 'Trabajo Territorial', 'Jornadas Sociales', 'Veeduría Ciudadana'):
            NewsCategory.objects.get_or_create(name=name)

        # 5. Configuración plataforma (sección 08 de base de datos.md)
        configs = [
            ('institucion.nombre', 'Corporacion Pluralismo Social'),
            ('mapa.srid', 4326),
            ('iniciativas.max_destacadas', 4),
        ]
        for clave, valor in configs:
            SiteSetting.objects.get_or_create(clave=clave, defaults={'valor': valor})

        self.stdout.write(self.style.SUCCESS('Catálogos de base de datos.md sincronizados correctamente.'))
