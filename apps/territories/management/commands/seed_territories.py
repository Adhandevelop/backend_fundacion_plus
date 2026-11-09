from django.core.management.base import BaseCommand
from django.db import transaction

from apps.territories.models import Community, Department, Municipality


class Command(BaseCommand):
    help = 'Carga los 32 departamentos de Colombia + Bogotá D.C. (códigos DANE), municipios principales y comunidades comunitarias.'

    @transaction.atomic
    def handle(self, *args, **options):
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

        self.stdout.write(f'  ✓ {len(dep_map)} departamentos sincronizados.')

        self.stdout.write('==> Cargando municipios principales...')
        municipios_data = [
            # Antioquia (05)
            ('05', '05001', 'Medellín'),
            ('05', '05088', 'Bello'),
            ('05', '05360', 'Itagüí'),
            ('05', '05266', 'Envigado'),
            ('05', '05615', 'Rionegro'),
            ('05', '05631', 'Sabaneta'),
            ('05', '05380', 'La Estrella'),
            ('05', '05129', 'Caldas'),
            ('05', '05212', 'Copacabana'),
            ('05', '05308', 'Girardota'),
            ('05', '05045', 'Apartadó'),
            ('05', '05837', 'Turbo'),
            ('05', '05147', 'Carepa'),
            ('05', '05172', 'Chigorodó'),
            ('05', '05440', 'Marinilla'),
            ('05', '05318', 'Guarne'),
            ('05', '05154', 'Caucasia'),
            ('05', '05893', 'Yarumal'),
            ('05', '05658', 'Santa Fe de Antioquia'),
            ('05', '05031', 'Amalfi'),
            # Atlántico (08)
            ('08', '08001', 'Barranquilla'),
            ('08', '08758', 'Soledad'),
            ('08', '08433', 'Malambo'),
            # Bogotá (11)
            ('11', '11001', 'Bogotá, D.C.'),
            # Bolívar (13)
            ('13', '13001', 'Cartagena de Indias'),
            ('13', '13430', 'Magangué'),
            # Boyacá (15)
            ('15', '15001', 'Tunja'),
            ('15', '15238', 'Duitama'),
            ('15', '15759', 'Sogamoso'),
            # Caldas (17)
            ('17', '17001', 'Manizales'),
            ('17', '17380', 'La Dorada'),
            # Cauca (19)
            ('19', '19001', 'Popayán'),
            ('19', '19698', 'Santander de Quilichao'),
            # Cesar (20)
            ('20', '20001', 'Valledupar'),
            ('20', '20011', 'Aguachica'),
            # Córdoba (23)
            ('23', '23001', 'Montería'),
            ('23', '23417', 'Lorica'),
            # Cundinamarca (25)
            ('25', '25754', 'Soacha'),
            ('25', '25175', 'Chía'),
            ('25', '25899', 'Zipaquirá'),
            ('25', '25269', 'Facatativá'),
            ('25', '25290', 'Fusagasugá'),
            ('25', '25307', 'Girardot'),
            # Chocó (27)
            ('27', '27001', 'Quibdó'),
            ('27', '27361', 'Istmina'),
            # Huila (41)
            ('41', '41001', 'Neiva'),
            ('41', '41551', 'Pitalito'),
            # La Guajira (44)
            ('44', '44001', 'Riohacha'),
            ('44', '44430', 'Maicao'),
            # Magdalena (47)
            ('47', '47001', 'Santa Marta'),
            ('47', '47189', 'Ciénaga'),
            # Meta (50)
            ('50', '50001', 'Villavicencio'),
            ('50', '50006', 'Acacías'),
            # Nariño (52)
            ('52', '52001', 'Pasto'),
            ('52', '52835', 'Tumaco'),
            ('52', '52356', 'Ipiales'),
            # Norte de Santander (54)
            ('54', '54001', 'Cúcuta'),
            ('54', '54498', 'Ocaña'),
            # Quindío (63)
            ('63', '63001', 'Armenia'),
            ('63', '63130', 'Calarcá'),
            # Risaralda (66)
            ('66', '66001', 'Pereira'),
            ('66', '66170', 'Dosquebradas'),
            # Santander (68)
            ('68', '68001', 'Bucaramanga'),
            ('68', '68307', 'Floridablanca'),
            ('68', '68081', 'Barrancabermeja'),
            ('68', '68276', 'Girón'),
            ('68', '68547', 'Piedecuesta'),
            # Sucre (70)
            ('70', '70001', 'Sincelejo'),
            # Tolima (73)
            ('73', '73001', 'Ibagué'),
            ('73', '73268', 'Espinal'),
            # Valle del Cauca (76)
            ('76', '76001', 'Cali'),
            ('76', '76109', 'Buenaventura'),
            ('76', '76520', 'Palmira'),
            ('76', '76834', 'Tuluá'),
            ('76', '76147', 'Cartago'),
            ('76', '76111', 'Buga'),
            ('76', '76364', 'Jamundí'),
            ('76', '76892', 'Yumbo'),
            # Arauca (81)
            ('81', '81001', 'Arauca'),
            # Casanare (85)
            ('85', '85001', 'Yopal'),
            # Putumayo (86)
            ('86', '86001', 'Mocoa'),
            ('86', '86568', 'Puerto Asís'),
            # San Andrés y Providencia (88)
            ('88', '88001', 'San Andrés'),
            # Amazonas (91)
            ('91', '91001', 'Leticia'),
            # Guainía (94)
            ('94', '94001', 'Inírida'),
            # Guaviare (95)
            ('95', '95001', 'San José del Guaviare'),
            # Vaupés (97)
            ('97', '97001', 'Mitú'),
            # Vichada (99)
            ('99', '99001', 'Puerto Carreño'),
        ]

        mun_map = {}
        for dep_code, mun_code, mun_name in municipios_data:
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

        self.stdout.write(f'  ✓ {len(mun_map)} municipios sincronizados.')

        self.stdout.write('==> Cargando comunidades (comunas, corregimientos, veredas y barrios)...')
        comunidades_data = [
            # Medellín (05001) - Comunas
            ('05001', 'Comuna 1 - Popular', 'comuna', 'Zona Nororiental de Medellín'),
            ('05001', 'Comuna 2 - Santa Cruz', 'comuna', 'Zona Nororiental de Medellín'),
            ('05001', 'Comuna 3 - Manrique', 'comuna', 'Zona Nororiental de Medellín'),
            ('05001', 'Comuna 4 - Aranjuez', 'comuna', 'Zona Nororiental de Medellín'),
            ('05001', 'Comuna 5 - Castilla', 'comuna', 'Zona Noroccidental de Medellín'),
            ('05001', 'Comuna 6 - Doce de Octubre', 'comuna', 'Zona Noroccidental de Medellín'),
            ('05001', 'Comuna 7 - Robledo', 'comuna', 'Zona Noroccidental de Medellín'),
            ('05001', 'Comuna 8 - Villa Hermosa', 'comuna', 'Zona Centro Oriental de Medellín'),
            ('05001', 'Comuna 9 - Buenos Aires', 'comuna', 'Zona Centro Oriental de Medellín'),
            ('05001', 'Comuna 10 - La Candelaria', 'comuna', 'Zona Centro de Medellín'),
            ('05001', 'Comuna 11 - Laureles - Estadio', 'comuna', 'Zona Centro Occidental de Medellín'),
            ('05001', 'Comuna 12 - La América', 'comuna', 'Zona Centro Occidental de Medellín'),
            ('05001', 'Comuna 13 - San Javier', 'comuna', 'Zona Centro Occidental de Medellín'),
            ('05001', 'Comuna 14 - El Poblado', 'comuna', 'Zona Suroriental de Medellín'),
            ('05001', 'Comuna 15 - Guayabal', 'comuna', 'Zona Suroccidental de Medellín'),
            ('05001', 'Comuna 16 - Belén', 'comuna', 'Zona Suroccidental de Medellín'),
            # Medellín - Corregimientos
            ('05001', 'Corregimiento San Cristóbal', 'corregimiento', 'Sector rural occidental'),
            ('05001', 'Corregimiento San Antonio de Prado', 'corregimiento', 'Sector rural suroccidental'),
            ('05001', 'Corregimiento Santa Elena', 'corregimiento', 'Sector rural oriental tradicional'),
            ('05001', 'Corregimiento Altavista', 'corregimiento', 'Sector rural suroccidental'),
            ('05001', 'Corregimiento San Sebastián de Palmitas', 'corregimiento', 'Sector rural noroccidental'),
            # Medellín - Veredas y Barrios comunitarios
            ('05001', 'Vereda La Loma', 'vereda', 'Vereda en corregimiento San Cristóbal'),
            ('05001', 'Vereda El Salado', 'vereda', 'Vereda en corregimiento San Antonio de Prado'),
            ('05001', 'Vereda Travesías', 'vereda', 'Vereda en corregimiento San Cristóbal'),
            ('05001', 'Vereda Media Luna', 'vereda', 'Vereda en corregimiento Santa Elena'),
            ('05001', 'Barrio Moravia', 'barrio', 'Barrio histórico de participación comunitaria'),
            ('05001', 'Barrio San Javier', 'barrio', 'Barrio emblemático Comuna 13'),
            ('05001', 'Barrio Belén Rincón', 'barrio', 'Sector Comuna 16'),
            ('05001', 'Barrio Santo Domingo Savio', 'barrio', 'Sector Comuna 1 Popular'),
            # Bello (05088)
            ('05088', 'Comuna 1 - París', 'comuna', 'Zona occidental de Bello'),
            ('05088', 'Barrio Niquía', 'barrio', 'Sector residencial y comercial de Bello'),
            ('05088', 'Corregimiento San Félix', 'corregimiento', 'Zona rural alta de Bello'),
            # Itagüí (05360)
            ('05360', 'Barrio Santa María', 'barrio', 'Sector popular de Itagüí'),
            ('05360', 'Corregimiento El Manzanillo', 'corregimiento', 'Zona rural de Itagüí'),
            # Envigado (05266)
            ('05266', 'Barrio El Dorado', 'barrio', 'Sector tradicional de Envigado'),
            ('05266', 'Vereda Las Palmas', 'vereda', 'Zona rural alta de Envigado'),
            ('05266', 'Vereda El Escobero', 'vereda', 'Zona rural ecológica de Envigado'),
            # Rionegro (05615)
            ('05615', 'Vereda Abreo', 'vereda', 'Sector rural de Rionegro'),
            ('05615', 'Vereda El Tablazo', 'vereda', 'Sector aeropuerto / rural'),
            ('05615', 'Barrio El Porvenir', 'barrio', 'Sector urbano consolidado'),
            # Bogotá (11001) - Localidades/Sectores
            ('11001', 'Localidad Suba', 'sector', 'Sector noroccidental de Bogotá'),
            ('11001', 'Localidad Kennedy', 'sector', 'Sector suroccidental de Bogotá'),
            ('11001', 'Localidad Ciudad Bolívar', 'sector', 'Sector sur comunitario de Bogotá'),
            ('11001', 'Localidad Usme', 'sector', 'Sector sur y rural de Bogotá'),
            ('11001', 'Localidad Santa Fe', 'sector', 'Sector centro histórico de Bogotá'),
            # Cali (76001) - Comunas
            ('76001', 'Comuna 6 - Petecuy', 'comuna', 'Sector nororiental de Cali'),
            ('76001', 'Comuna 14 - Aguablanca', 'comuna', 'Sector oriente de Cali'),
            ('76001', 'Comuna 20 - Siloé', 'comuna', 'Sector de ladera occidental'),
            ('76001', 'Corregimiento Pance', 'corregimiento', 'Zona rural ambiental de Cali'),
        ]

        count_comunidades = 0
        for mun_code, com_name, com_tipo, com_desc in comunidades_data:
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

        self.stdout.write(f'  ✓ {count_comunidades} comunidades sincronizadas.')
        self.stdout.write(self.style.SUCCESS('Territorios oficiales de Colombia inicializados con éxito.'))
