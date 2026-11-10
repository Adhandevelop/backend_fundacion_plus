from django.contrib import admin
from apps.dynamic_forms.models import (
    Formulario,
    FormularioEnvio,
    FormularioNotificacion,
    FormularioOpcion,
    FormularioPregunta,
    FormularioRespuesta,
    FormularioToken,
    FormularioVersion,
)


class FormularioPreguntaInline(admin.TabularInline):
    model = FormularioPregunta
    extra = 0


@admin.register(Formulario)
class FormularioAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'slug', 'estado', 'numero_version_publicada', 'revision_edicion', 'fecha_creacion']
    search_fields = ['titulo', 'slug']
    list_filter = ['estado', 'requiere_documento', 'permite_multiples_envios']
    inlines = [FormularioPreguntaInline]


@admin.register(FormularioVersion)
class FormularioVersionAdmin(admin.ModelAdmin):
    list_display = ['formulario', 'numero_version', 'es_vigente', 'publicado_en']
    list_filter = ['es_vigente']


@admin.register(FormularioEnvio)
class FormularioEnvioAdmin(admin.ModelAdmin):
    list_display = ['id', 'formulario', 'version', 'correo_declarado', 'estado_vinculacion', 'fecha_envio']
    list_filter = ['estado_vinculacion', 'fecha_envio']
    search_fields = ['correo_declarado', 'nombres_declarados', 'apellidos_declarados']


@admin.register(FormularioRespuesta)
class FormularioRespuestaAdmin(admin.ModelAdmin):
    list_display = ['envio', 'codigo_pregunta', 'enunciado_congelado']


@admin.register(FormularioToken)
class FormularioTokenAdmin(admin.ModelAdmin):
    list_display = ['correo', 'proposito', 'usado', 'fecha_expiracion']
    list_filter = ['proposito', 'usado']
    search_fields = ['correo']


@admin.register(FormularioNotificacion)
class FormularioNotificacionAdmin(admin.ModelAdmin):
    list_display = ['correo_destino', 'asunto', 'estado', 'fecha_creacion']
    list_filter = ['estado']
