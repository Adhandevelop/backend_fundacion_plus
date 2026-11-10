from django.core.management.base import BaseCommand
from django.db import transaction

from apps.territories.models import Community, Department, Municipality


class Command(BaseCommand):
    help = 'Carga el territorio del Meta (código DANE 50), sus 29 municipios oficiales y sus comunidades.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all-colombia',
            action='store_true',
            help='Carga todos los departamentos de Colombia en lugar de solo Meta.',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        only_meta = not options.get('all_colombia', False)

        if only_meta:
            self.stdout.write('==> Configuración activa: Exclusivamente territorio del META...')
            # Limpiar departamentos y municipios no pertenecientes al Meta si no tienen casos vinculados
            non_meta_deps = Department.objects.exclude(codigo_dane='50')
            for dep in non_meta_deps:
                try:
                    Community.objects.filter(municipio__departamento=dep, casos__isnull=True).delete()
                    Municipality.objects.filter(departamento=dep, comunidades__casos__isnull=True).delete()
                    dep.delete()
                except Exception:
                    pass

            departamentos_data = [
                ('50', 'Meta'),
            ]
        else:
            self.stdout.write('==> Cargando departamentos de Colombia (DANE)...')
            departamentos_data = [
                ('05', 'Antioquia'),
                ('08', 'Atlántico'),
                ('11', 'Bogotá, D.C.'),
                ('13', 'Bolívar'),
                ('15', 'Boyacá'),
                ('17', 'Caldas'),
                ('19', 'Cauca'),
                ('20', 'Cesar'),
                ('23', 'Córdoba'),
                ('25', 'Cundinamarca'),
                ('27', 'Chocó'),
                ('41', 'Huila'),
                ('44', 'La Guajira'),
                ('47', 'Magdalena'),
                ('50', 'Meta'),
                ('52', 'Nariño'),
                ('54', 'Norte de Santander'),
                ('63', 'Quindío'),
                ('66', 'Risaralda'),
                ('68', 'Santander'),
                ('70', 'Sucre'),
                ('73', 'Tolima'),
                ('76', 'Valle del Cauca'),
                ('81', 'Arauca'),
                ('85', 'Casanare'),
                ('86', 'Putumayo'),
                ('88', 'San Andrés y Providencia'),
                ('91', 'Amazonas'),
                ('94', 'Guainía'),
                ('95', 'Guaviare'),
                ('97', 'Vaupés'),
                ('99', 'Vichada'),
            ]

        dep_map = {}
        for codigo, nombre in departamentos_data:
            dep, _ = Department.objects.update_or_create(
                codigo_dane=codigo,
                defaults={'nombre': nombre},
            )
            dep_map[codigo] = dep

        self.stdout.write(f'  ✓ {len(dep_map)} departamento(s) sincronizado(s): {", ".join(d.nombre for d in dep_map.values())}')

        self.stdout.write('==> Cargando los 29 municipios oficiales del departamento del Meta (DANE 50xxx)...')
        municipios_meta = [
            ('50', '50001', 'Villavicencio'),
            ('50', '50006', 'Acacías'),
            ('50', '50110', 'Barranca de Upía'),
            ('50', '50124', 'Cabuyaro'),
            ('50', '50150', 'Castilla la Nueva'),
            ('50', '50223', 'San Luis de Cubarral'),
            ('50', '50226', 'Cumaral'),
            ('50', '50245', 'El Calvario'),
            ('50', '50251', 'El Castillo'),
            ('50', '50270', 'El Dorado'),
            ('50', '50287', 'Fuente de Oro'),
            ('50', '50313', 'Granada'),
            ('50', '50318', 'Guamal'),
            ('50', '50325', 'Mapiripán'),
            ('50', '50330', 'Mesetas'),
            ('50', '50350', 'La Macarena'),
            ('50', '50370', 'Uribe'),
            ('50', '50400', 'Lejanías'),
            ('50', '50450', 'Puerto Concordia'),
            ('50', '50568', 'Puerto Gaitán'),
            ('50', '50573', 'Puerto López'),
            ('50', '50577', 'Puerto Lleras'),
            ('50', '50590', 'Puerto Rico'),
            ('50', '50606', 'Restrepo'),
            ('50', '50680', 'San Carlos de Guaroa'),
            ('50', '50683', 'San Juan de Arama'),
            ('50', '50686', 'San Juanito'),
            ('50', '50689', 'San Martín'),
            ('50', '50711', 'Vista Hermosa'),
        ]

        mun_map = {}
        for dep_code, mun_code, mun_name in municipios_meta:
            dep_obj = dep_map.get(dep_code)
            if not dep_obj:
                continue
            mun, _ = Municipality.objects.update_or_create(
                codigo_dane=mun_code,
                defaults={
                    'departamento': dep_obj,
                    'nombre': mun_name,
                },
            )
            mun_map[mun_code] = mun

        self.stdout.write(f'  ✓ {len(mun_map)} municipios del Meta sincronizados.')

        self.stdout.write('==> Cargando comunidades de Villavicencio y municipios del Meta (comunas, corregimientos, veredas y barrios)...')
        comunidades_meta = [
            # =========================================================
            # VILLAVICENCIO (50001) - 8 COMUNAS URBANAS
            # =========================================================
            ('50001', 'Comuna 1 - Centro', 'comuna', 'Sector centro y fundacional de Villavicencio'),
            ('50001', 'Comuna 2 - Barzal', 'comuna', 'Sector institucional y residencial (Barzal, Buque, Siete de Agosto)'),
            ('50001', 'Comuna 3 - Porvenir', 'comuna', 'Sector popular y comercial (Porvenir, Santa Inés, 20 de Julio)'),
            ('50001', 'Comuna 4 - Esperanza', 'comuna', 'Sector residencial norte (La Esperanza, Morichal, Jordán)'),
            ('50001', 'Comuna 5 - Popular', 'comuna', 'Sector oriente de Villavicencio (El Estero, Popular, Ricaurte)'),
            ('50001', 'Comuna 6 - San Benito', 'comuna', 'Sector suroriental (San Benito, Cantarrana)'),
            ('50001', 'Comuna 7 - La Rosita', 'comuna', 'Sector nororiental en expansión (La Rosita, Esperanza etapas)'),
            ('50001', 'Comuna 8 - Porfía', 'comuna', 'Sector suroccidental de alta densidad (Ciudad Porfía, Catumare, Montecarlo)'),

            # =========================================================
            # VILLAVICENCIO (50001) - 7 CORREGIMIENTOS RURALES
            # =========================================================
            ('50001', 'Corregimiento 1', 'corregimiento', 'Sector cordillera y vía Bogotá (Pipiral, Servitá, Quebrada Honda)'),
            ('50001', 'Corregimiento 2', 'corregimiento', 'Sector norte rural (Puente Abadía, La Argentina, La Cecilia)'),
            ('50001', 'Corregimiento 3', 'corregimiento', 'Sector rural aeropuerto y salida a Restrepo (Vanguardia, Cairo)'),
            ('50001', 'Corregimiento 4', 'corregimiento', 'Sector agrícola y ganadero (Apiay, Barcelona, Vegas del Guayuriba)'),
            ('50001', 'Corregimiento 5', 'corregimiento', 'Sector industrial y rural vía Puerto López (Pompeya, Las Mercedes)'),
            ('50001', 'Corregimiento 6', 'corregimiento', 'Sector turístico y miradores (Buenavista, La Cuncia, Bella Suiza)'),
            ('50001', 'Corregimiento 7', 'corregimiento', 'Sector rural sur (Cocuy, Guayuriba)'),

            # =========================================================
            # VILLAVICENCIO (50001) - VEREDAS
            # =========================================================
            ('50001', 'Vereda Vanguardia', 'vereda', 'Vereda sector aeropuerto de Villavicencio'),
            ('50001', 'Vereda Apiay', 'vereda', 'Vereda sector Apiay y base aérea'),
            ('50001', 'Vereda Buenavista', 'vereda', 'Vereda mirador cordillera occidental'),
            ('50001', 'Vereda La Cuncia', 'vereda', 'Vereda turística vía Acacías'),
            ('50001', 'Vereda Pompeya', 'vereda', 'Vereda sector rural oriente vía Puerto López'),
            ('50001', 'Vereda Pipiral', 'vereda', 'Vereda histórica cañón del Guatiquía / antigua vía Bogotá'),
            ('50001', 'Vereda Barcelona', 'vereda', 'Vereda sector agrícola suroriente'),
            ('50001', 'Vereda Servitá', 'vereda', 'Vereda alta de ladera'),
            ('50001', 'Vereda La Argentina', 'vereda', 'Vereda rural norte'),
            ('50001', 'Vereda El Cairo', 'vereda', 'Vereda sector norte vía Restrepo'),
            ('50001', 'Vereda Puente Abadía', 'vereda', 'Vereda turística río Guatiquía'),

            # =========================================================
            # VILLAVICENCIO (50001) - BARRIOS PRINCIPALES
            # =========================================================
            ('50001', 'Barrio Ciudad Porfía', 'barrio', 'Barrio emblemático y comunitario de la Comuna 8'),
            ('50001', 'Barrio El Porvenir', 'barrio', 'Barrio comercial tradicional Comuna 3'),
            ('50001', 'Barrio El Barzal', 'barrio', 'Barrio de servicios médicos e institucional Comuna 2'),
            ('50001', 'Barrio La Esperanza', 'barrio', 'Barrio residencial Comuna 4'),
            ('50001', 'Barrio Siete de Agosto', 'barrio', 'Barrio gastronómico y comercial Comuna 2'),
            ('50001', 'Barrio San Benito', 'barrio', 'Barrio tradicional Comuna 6'),
            ('50001', 'Barrio Morichal', 'barrio', 'Barrio residencial Comuna 4'),
            ('50001', 'Barrio Catumare', 'barrio', 'Barrio residencial Comuna 8'),
            ('50001', 'Barrio Montecarlo', 'barrio', 'Barrio en desarrollo Comuna 8'),
            ('50001', 'Barrio Santa Inés', 'barrio', 'Barrio céntrico Comuna 3'),
            ('50001', 'Barrio San Antonio', 'barrio', 'Barrio tradicional Comuna 5'),
            ('50001', 'Barrio Kirpas', 'barrio', 'Barrio sector oriente Comuna 4'),
            ('50001', 'Barrio Popular', 'barrio', 'Barrio popular Comuna 5'),
            ('50001', 'Barrio Doce de Octubre', 'barrio', 'Barrio céntrico Comuna 3'),

            # =========================================================
            # ACACÍAS (50006)
            # =========================================================
            ('50006', 'Barrio Centro', 'barrio', 'Sector céntrico y comercial de Acacías'),
            ('50006', 'Barrio Mancera', 'barrio', 'Barrio residencial de Acacías'),
            ('50006', 'Barrio Cooperativo', 'barrio', 'Barrio tradicional de Acacías'),
            ('50006', 'Barrio Las Colinas', 'barrio', 'Barrio en expansión de Acacías'),
            ('50006', 'Vereda Dinamarca', 'vereda', 'Vereda turística y rural de Acacías'),
            ('50006', 'Vereda Chichimene', 'vereda', 'Sector petrolero y agropecuario de Acacías'),
            ('50006', 'Vereda Manzanares', 'vereda', 'Zona rural agropecuaria'),
            ('50006', 'Vereda La Esmeralda', 'vereda', 'Sector rural de Acacías'),

            # =========================================================
            # GRANADA (50313)
            # =========================================================
            ('50313', 'Barrio Centro', 'barrio', 'Casco urbano principal de Granada'),
            ('50313', 'Barrio Belén', 'barrio', 'Barrio tradicional de Granada'),
            ('50313', 'Barrio El Jardín', 'barrio', 'Sector residencial de Granada'),
            ('50313', 'Vereda Puerto Caldas', 'vereda', 'Sector ribereño río Ariari'),
            ('50313', 'Vereda Canaguaro', 'vereda', 'Vereda agrícola de Granada'),

            # =========================================================
            # CUMARAL (50226)
            # =========================================================
            ('50226', 'Barrio Centro', 'barrio', 'Zona céntrica de Cumaral'),
            ('50226', 'Vereda Guacavía', 'vereda', 'Sector límite fluvial y agrícola'),
            ('50226', 'Vereda Caney Alto', 'vereda', 'Sector rural alto de Cumaral'),

            # =========================================================
            # RESTREPO (50606)
            # =========================================================
            ('50606', 'Barrio Centro', 'barrio', 'Casco urbano de Restrepo'),
            ('50606', 'Vereda Salinas', 'vereda', 'Sector histórico salinero de Restrepo'),
            ('50606', 'Vereda Caney Medio', 'vereda', 'Sector rural de Restrepo'),

            # =========================================================
            # PUERTO LÓPEZ (50573)
            # =========================================================
            ('50573', 'Barrio Centro', 'barrio', 'Centro del Ombligo de Colombia'),
            ('50573', 'Vereda Pachaquiaro', 'vereda', 'Centro poblado y vereda rural'),
            ('50573', 'Vereda Puerto Guadalupe', 'vereda', 'Sector ribereño río Meta'),

            # =========================================================
            # PUERTO GAITÁN (50568)
            # =========================================================
            ('50568', 'Barrio Centro', 'barrio', 'Casco urbano de Puerto Gaitán'),
            ('50568', 'Resguardo Indígena Wacoyo', 'resguardo_indigena', 'Comunidad indígena sikuani'),
            ('50568', 'Vereda Rubiales', 'vereda', 'Sector rural y de producción'),

            # =========================================================
            # SAN MARTÍN (50689)
            # =========================================================
            ('50689', 'Barrio Centro', 'barrio', 'Sector histórico y Cuadrillas de San Martín'),
            ('50689', 'Vereda Camoa', 'vereda', 'Sector rural y ganadero'),

            # =========================================================
            # CASTILLA LA NUEVA (50150)
            # =========================================================
            ('50150', 'Barrio Centro', 'barrio', 'Casco urbano de Castilla la Nueva'),
            ('50150', 'Vereda San Lorenzo', 'vereda', 'Sector agroindustrial'),
            ('50150', 'Vereda Toro Sentado', 'vereda', 'Sector rural'),
        ]

        count_comunidades = 0
        for mun_code, com_name, com_tipo, com_desc in comunidades_meta:
            mun_obj = mun_map.get(mun_code)
            if not mun_obj:
                continue
            Community.objects.update_or_create(
                municipio=mun_obj,
                tipo=com_tipo,
                nombre=com_name,
                defaults={
                    'descripcion': com_desc,
                    'activo': True,
                },
            )
            count_comunidades += 1

        self.stdout.write(f'  ✓ {count_comunidades} comunidades del Meta sincronizadas.')
        self.stdout.write(self.style.SUCCESS('Territorio del META (departamento, 29 municipios y comunidades) inicializado con éxito.'))
