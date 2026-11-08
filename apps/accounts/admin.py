from django.contrib import admin
from apps.accounts.models import ResponsibleScopeAssignment, Role, User
from apps.audit.models import (
    AuditAccess,
    AuditCase,
    AuditLog,
    AuditPermission,
    AuditSecurity,
)
from apps.cases.models import Case, CaseAssignment, CaseCategory, CaseEvidence, CaseStatus
from apps.communications.models import (
    CaseComment,
    CaseMessage,
    EventProposal,
    SiteSetting,
)
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
from apps.notifications.models import Notification
from apps.territories.models import Community, Department, Municipality
from apps.tracking.models import CaseStatusHistory, CaseUpdate


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('correo', 'nombres', 'apellidos', 'rol', 'estado', 'fecha_registro')
    search_fields = ('correo', 'nombres', 'apellidos')
    list_filter = ('rol', 'estado')


@admin.register(ResponsibleScopeAssignment)
class ResponsibleScopeAssignmentAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'comunidad', 'tipo_caso', 'activo', 'fecha_asignacion')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('codigo_dane', 'nombre')


@admin.register(Municipality)
class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ('codigo_dane', 'nombre', 'departamento')
    list_filter = ('departamento',)


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'municipio', 'activo')
    list_filter = ('tipo', 'municipio', 'activo')


@admin.register(CaseCategory)
class CaseCategoryAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'activo')


@admin.register(CaseStatus)
class CaseStatusAdmin(admin.ModelAdmin):
    list_display = ('orden', 'nombre', 'descripcion')


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'titulo', 'tipo_caso', 'comunidad', 'estado', 'prioridad', 'estado_publicacion', 'fecha_creacion')
    list_filter = ('estado_publicacion', 'estado', 'prioridad', 'tipo_caso')
    search_fields = ('codigo', 'titulo', 'descripcion')


@admin.register(CaseAssignment)
class CaseAssignmentAdmin(admin.ModelAdmin):
    list_display = ('caso', 'responsable', 'asignador', 'activo', 'fecha_asignacion')


@admin.register(CaseEvidence)
class CaseEvidenceAdmin(admin.ModelAdmin):
    list_display = ('caso', 'tipo_archivo', 'ruta_archivo', 'fecha_subida')


@admin.register(CaseUpdate)
class CaseUpdateAdmin(admin.ModelAdmin):
    list_display = ('caso', 'usuario', 'visible_publicamente', 'fecha_seguimiento')


@admin.register(CaseStatusHistory)
class CaseStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('caso', 'estado_anterior', 'estado_nuevo', 'usuario', 'fecha_cambio')


@admin.register(CaseComment)
class CaseCommentAdmin(admin.ModelAdmin):
    list_display = ('caso', 'usuario', 'estado_moderacion', 'fecha_creacion')


@admin.register(CaseMessage)
class CaseMessageAdmin(admin.ModelAdmin):
    list_display = ('caso', 'remitente', 'destinatario', 'fecha_envio', 'fecha_lectura')


@admin.register(EventProposal)
class EventProposalAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'nombre_contacto', 'estado', 'fecha_creacion')


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('clave', 'fecha_actualizacion')


@admin.register(Initiative)
class InitiativeAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'estado', 'estado_publicacion', 'destacada', 'orden_destacado')


@admin.register(InitiativeEdition)
class InitiativeEditionAdmin(admin.ModelAdmin):
    list_display = ('iniciativa', 'anio', 'nombre_edicion', 'estado')


@admin.register(InitiativeActivity)
class InitiativeActivityAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'edicion', 'comunidad', 'estado', 'fecha_inicio')


@admin.register(InitiativeMedia)
class InitiativeMediaAdmin(admin.ModelAdmin):
    list_display = ('iniciativa', 'edicion', 'tipo', 'es_portada', 'orden')


@admin.register(InitiativeMetric)
class InitiativeMetricAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'valor', 'unidad', 'edicion', 'tipo_medicion')


@admin.register(InitiativeCommunity)
class InitiativeCommunityAdmin(admin.ModelAdmin):
    list_display = ('edicion', 'comunidad')


@admin.register(InitiativeCaseLink)
class InitiativeCaseLinkAdmin(admin.ModelAdmin):
    list_display = ('edicion', 'caso', 'tipo_vinculo', 'fecha_vinculacion')


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'publication_status', 'is_featured', 'published_at')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo', 'titulo', 'leida', 'fecha_creacion')


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('fecha_evento', 'usuario', 'accion', 'modulo', 'tabla_afectada', 'resultado')
    readonly_fields = [f.name for f in AuditLog._meta.fields]


@admin.register(AuditAccess)
class AuditAccessAdmin(admin.ModelAdmin):
    list_display = ('fecha_evento', 'correo_intentado', 'tipo_evento', 'resultado', 'direccion_ip')
    readonly_fields = [f.name for f in AuditAccess._meta.fields]


@admin.register(AuditCase)
class AuditCaseAdmin(admin.ModelAdmin):
    list_display = ('fecha_accion', 'caso', 'usuario', 'tipo_accion', 'estado_anterior', 'estado_nuevo')
    readonly_fields = [f.name for f in AuditCase._meta.fields]


@admin.register(AuditPermission)
class AuditPermissionAdmin(admin.ModelAdmin):
    list_display = ('fecha_cambio', 'usuario_afectado', 'usuario_responsable', 'tipo_cambio')
    readonly_fields = [f.name for f in AuditPermission._meta.fields]


@admin.register(AuditSecurity)
class AuditSecurityAdmin(admin.ModelAdmin):
    list_display = ('fecha_evento', 'tipo_evento', 'nivel_severidad', 'atendido')
    readonly_fields = [f.name for f in AuditSecurity._meta.fields]
