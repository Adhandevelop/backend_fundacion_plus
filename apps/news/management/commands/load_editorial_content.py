from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.accounts.models import Role, User
from apps.initiatives.models import (
    Initiative,
    InitiativeEdition,
    InitiativeMetric,
)
from apps.news.models import NewsArticle, NewsCategory, NewsMedia


class Command(BaseCommand):
    help = 'P11: Carga editorial específica, controlada e idempotente de categorías, noticias e iniciativas institucionales.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--publish',
            action='store_true',
            help='Publicar directamente los contenidos aprobados en lugar de dejarlos en borrador.',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        publish = options.get('publish', True)
        self.stdout.write(self.style.NOTICE('==> Iniciando carga editorial de PLUS...'))

        # Obtener un autor institucional (admin o primer usuario activo)
        author = User.objects.filter(
            rol__nombre=Role.Nombre.ADMINISTRADOR,
            estado=User.Estado.ACTIVO,
        ).first() or User.objects.filter(estado=User.Estado.ACTIVO).first()

        if not author:
            self.stdout.write(self.style.ERROR('No se encontró un usuario activo en el sistema para autoría editorial.'))
            return

        # 1. Categorías de Noticias
        cat_comunidad, _ = NewsCategory.objects.get_or_create(
            slug='comunidad',
            defaults={
                'nombre': 'Comunidad y Participación',
                'descripcion': 'Noticias sobre liderazgo comunitario, encuentros y participación ciudadana en el Meta.',
                'activa': True,
            },
        )
        cat_ambiente, _ = NewsCategory.objects.get_or_create(
            slug='medio-ambiente',
            defaults={
                'nombre': 'Medio Ambiente y Territorio',
                'descripcion': 'Acciones de conservación, gestión de cuencas y protección ambiental.',
                'activa': True,
            },
        )
        cat_proyectos, _ = NewsCategory.objects.get_or_create(
            slug='proyectos-sociales',
            defaults={
                'nombre': 'Proyectos y Gestión Social',
                'descripcion': 'Avance de proyectos de infraestructura, bienestar y desarrollo social.',
                'activa': True,
            },
        )

        self.stdout.write(self.style.SUCCESS('  ✓ Categorías de noticias sincronizadas.'))

        # 2. Noticias Institucionales
        noticias_data = [
            {
                'titulo': 'Lanzamiento del Programa de Monitoreo Territorial en el Departamento del Meta',
                'slug': 'lanzamiento-monitoreo-territorial-meta',
                'extracto': 'La Fundación PLUS presenta su plataforma digital para la radicación y seguimiento comunitario de casos territoriales.',
                'contenido': (
                    'Con la participación activa de representantes comunitarios, autoridades locales y líderes veredales '
                    'del Meta, la Fundación PLUS dio inicio a la implementación de su herramienta integral de vigilancia comunitaria. '
                    'El sistema permitirá canalizar solicitudes, vigilar recursos y acompañar el desarrollo sostenible de nuestras comunidades.'
                ),
                'categoria': cat_comunidad,
                'destacada': True,
            },
            {
                'titulo': 'Jornadas de Limpieza y Recuperación en la Cuenca del Río Guatiquía',
                'slug': 'recuperacion-cuenca-rio-guatiquia',
                'extracto': 'Comunidades ribereñas y voluntarios se unen para proteger las fuentes hídricas de Villavicencio.',
                'contenido': (
                    'Durante el fin de semana se recolectaron más de 3 toneladas de residuos en las márgenes del río Guatiquía. '
                    'La iniciativa comunitaria contó con talleres de sensibilización sobre manejo de aguas residuales y reforestación con especies nativas.'
                ),
                'categoria': cat_ambiente,
                'destacada': True,
            },
            {
                'titulo': 'Avances en Infraestructura Veredal y Vías Terciarias en Puerto López',
                'slug': 'avances-infraestructura-puerto-lopez',
                'extracto': 'Veeduría ciudadana reporta avances significativos en el mantenimiento vial del sector rural.',
                'contenido': (
                    'A través de la articulación con comités veredales, se ha verificado el mejoramiento de los tramos críticos '
                    'que facilitan el transporte de cosechas y el tránsito seguro de las familias rurales en Puerto López.'
                ),
                'categoria': cat_proyectos,
                'destacada': False,
            },
        ]

        for item in noticias_data:
            slug = item.pop('slug')
            article, created = NewsArticle.objects.get_or_create(
                slug=slug,
                defaults={
                    'autor': author,
                    'estado_publicacion': NewsArticle.EstadoPublicacion.PUBLICADA if publish else NewsArticle.EstadoPublicacion.BORRADOR,
                    'fecha_publicacion': timezone.now() if publish else None,
                    **item,
                },
            )
            if not created and publish and article.estado_publicacion != NewsArticle.EstadoPublicacion.PUBLICADA:
                article.estado_publicacion = NewsArticle.EstadoPublicacion.PUBLICADA
                if not article.fecha_publicacion:
                    article.fecha_publicacion = timezone.now()
                article.save(update_fields=['estado_publicacion', 'fecha_publicacion', 'fecha_actualizacion'])

        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(noticias_data)} noticias institucionales cargadas/sincronizadas.'))

        # 3. Iniciativas y Programas
        iniciativas_data = [
            {
                'titulo': 'Vigilancia y Protección de Cuencas Hídricas del Meta',
                'slug': 'proteccion-cuencas-hidricas-meta',
                'subtitulo': 'Monitoreo colaborativo y restauración ecológica',
                'descripcion_corta': 'Programa comunitario para la veeduría y preservación de ríos y afluentes estratégicos en el Meta.',
                'descripcion': (
                    'Esta iniciativa articula comunidades locales, instituciones educativas y expertos ambientales '
                    'para vigilar la calidad del agua, alertar oportunamente sobre factores de degradación y promover acciones de siembra y cuidado.'
                ),
                'categoria': 'Conservación',
                'destacada': True,
                'orden_destacado': 1,
            },
            {
                'titulo': 'Comunidades Conectadas y Transparentes',
                'slug': 'comunidades-conectadas-transparentes',
                'subtitulo': 'Capacitación y veeduría ciudadana participativa',
                'descripcion_corta': 'Fortalecimiento de capacidades para el liderazgo y seguimiento transparente de proyectos locales.',
                'descripcion': (
                    'Espacios de formación práctica en derecho de petición, radicación efectiva de inquietudes comunitarias '
                    'y seguimiento riguroso al cumplimiento de compromisos institucionales en comunas y veredas.'
                ),
                'categoria': 'Participación',
                'destacada': True,
                'orden_destacado': 2,
            },
        ]

        for ini in iniciativas_data:
            slug = ini.pop('slug')
            initiative, created = Initiative.objects.get_or_create(
                slug=slug,
                defaults={
                    'creador': author,
                    'estado_publicacion': Initiative.EstadoPublicacion.PUBLICADA if publish else Initiative.EstadoPublicacion.BORRADOR,
                    'fecha_publicacion': timezone.now() if publish else None,
                    **ini,
                },
            )
            # Asegurar al menos una edición vigente para la iniciativa
            edicion, _ = InitiativeEdition.objects.get_or_create(
                iniciativa=initiative,
                anio=timezone.now().year,
                defaults={
                    'nombre_edicion': f'Edición {timezone.now().year}',
                    'temporada': 'Anual',
                    'descripcion': f'Acciones operativas y despliegue territorial para la vigencia {timezone.now().year}.',
                    'estado': InitiativeEdition.Estado.EN_CURSO,
                },
            )
            # Indicadores de la edición
            InitiativeMetric.objects.get_or_create(
                edicion=edicion,
                nombre='Familias vinculadas',
                defaults={
                    'valor': 350,
                    'unidad': 'familias',
                    'descripcion': 'Número total de familias participantes en talleres y jornadas comunitarias.',
                    'orden': 1,
                },
            )
            InitiativeMetric.objects.get_or_create(
                edicion=edicion,
                nombre='Jornadas territoriales',
                defaults={
                    'valor': 12,
                    'unidad': 'jornadas',
                    'descripcion': 'Jornadas de campo y encuentros comunitarios realizados.',
                    'orden': 2,
                },
            )

        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(iniciativas_data)} iniciativas con ediciones y métricas sincronizadas.'))
        self.stdout.write(self.style.SUCCESS('==> Carga editorial completada exitosamente.'))
