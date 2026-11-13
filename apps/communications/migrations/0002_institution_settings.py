from django.db import migrations


def create_initial_institution_settings(apps, schema_editor):
    SiteSetting = apps.get_model('communications', 'SiteSetting')
    defaults = {
        'institucion.sigla': 'PLUS',
        'institucion.representante_nombre': 'JUAN DAVID MARTINEZ BOLAÑO',
        'institucion.representante_cargo': 'CEO de la Corporación Pluralismo Social',
        'institucion.mision': (
            'Fortalecer la participación ciudadana, la veeduría social y el acompañamiento '
            'territorial de las comunidades mediante gestión transparente e iniciativas de impacto.'
        ),
    }
    for key, value in defaults.items():
        SiteSetting.objects.get_or_create(
            clave=key,
            defaults={'valor': value},
        )


def remove_initial_institution_settings(apps, schema_editor):
    SiteSetting = apps.get_model('communications', 'SiteSetting')
    SiteSetting.objects.filter(
        clave__in=[
            'institucion.sigla',
            'institucion.representante_nombre',
            'institucion.representante_cargo',
            'institucion.mision',
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('communications', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_institution_settings, remove_initial_institution_settings),
    ]
