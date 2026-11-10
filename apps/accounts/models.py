import uuid
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models import Q
from django.utils import timezone


class Role(models.Model):
    """
    Tabla SQL: plus.roles
    Catálogo oficial en base de datos.md:
    - 'administrador'
    - 'representante'
    - 'moderador'
    - 'ciudadano'
    """

    class Nombre(models.TextChoices):
        ADMINISTRADOR = 'administrador', 'Administración general de PLUS'
        REPRESENTANTE = 'representante', 'Representación y gestión territorial'
        MODERADOR = 'moderador', 'Revisión de publicaciones y comentarios'
        CIUDADANO = 'ciudadano', 'Usuario que reporta casos y propone iniciativas'

    # Alias de compatibilidad para código existente
    Code = Nombre

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_rol',
    )
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'roles'
        ordering = ['nombre']

    @property
    def id_rol(self):
        return self.id

    @property
    def code(self):
        return self.nombre

    def __str__(self):
        return self.nombre


ROLE_ALIAS_MAP = {
    'ADMIN': Role.Nombre.ADMINISTRADOR,
    'SUPERADMIN': Role.Nombre.ADMINISTRADOR,
    'ADMINISTRADOR': Role.Nombre.ADMINISTRADOR,
    'RESPONSIBLE': Role.Nombre.REPRESENTANTE,
    'REPRESENTANTE': Role.Nombre.REPRESENTANTE,
    'EDITOR': Role.Nombre.MODERADOR,
    'MODERADOR': Role.Nombre.MODERADOR,
    'CITIZEN': Role.Nombre.CIUDADANO,
    'CIUDADANO': Role.Nombre.CIUDADANO,
}

ROLE_PERMISSIONS_MAP = {
    Role.Nombre.CIUDADANO: {
        'casos': ['crear', 'ver_propios', 'subir_evidencia', 'comentar', 'mensajes_privados'],
        'propuestas': ['crear', 'ver_propias'],
        'notificaciones': ['ver_propias'],
    },
    Role.Nombre.REPRESENTANTE: {
        'casos': ['crear', 'ver_asignados', 'seguimiento', 'cambiar_estado', 'subir_evidencia', 'mensajes_privados'],
        'iniciativas': ['ver', 'registrar_actividades'],
        'notificaciones': ['ver_propias'],
    },
    Role.Nombre.MODERADOR: {
        'casos': ['revisar_publicacion', 'moderar_comentarios'],
        'iniciativas': ['crear', 'editar', 'publicar', 'multimedia', 'indicadores'],
        'propuestas': ['revisar'],
    },
    Role.Nombre.ADMINISTRADOR: {
        'all': ['*'],
        'usuarios': ['crear', 'editar', 'cambiar_rol', 'asignar_ambito'],
        'territorios': ['crear', 'editar', 'eliminar'],
        'casos': ['*'],
        'iniciativas': ['*'],
        'auditoria': ['consultar'],
        'configuracion': ['*'],
    },
}


def normalize_role_name(role_input: str) -> str:
    if not role_input:
        return Role.Nombre.CIUDADANO
    upper = str(role_input).strip().upper()
    if upper in ROLE_ALIAS_MAP:
        return ROLE_ALIAS_MAP[upper]
    return str(role_input).strip().lower()


class UserManager(BaseUserManager):
    """Manager para plus.usuarios compatible con create_user() y create_superuser()."""

    def get_by_natural_key(self, username):
        return self.get(correo__iexact=username)

    def create_user(
        self,
        username=None,
        email=None,
        password=None,
        nombres=None,
        apellidos=None,
        first_name=None,
        last_name=None,
        rol=None,
        role_name=None,
        is_staff=False,
        is_superuser=False,
        **extra_fields,
    ):
        correo = self.normalize_email(email or extra_fields.pop('correo', None) or username)
        if not correo:
            raise ValueError('El correo electrónico es obligatorio.')
        if '@' not in correo:
            correo = f'{correo}@plus.org'

        resolved_nombres = nombres or first_name or extra_fields.pop('nombres', None) or correo.split('@')[0]
        resolved_apellidos = apellidos or last_name or extra_fields.pop('apellidos', None) or 'PLUS'

        if rol is None:
            target_role_name = normalize_role_name(
                role_name or ('administrador' if (is_staff or is_superuser) else 'ciudadano')
            )
            rol, _ = Role.objects.get_or_create(
                nombre=target_role_name,
                defaults={'descripcion': dict(Role.Nombre.choices).get(target_role_name, target_role_name)},
            )

        estado = extra_fields.pop('estado', 'activo')
        if extra_fields.pop('is_active', True) is False:
            estado = 'inactivo'

        telefono = extra_fields.pop('telefono', None) or extra_fields.pop('phone_number', None)

        user = self.model(
            correo=correo.lower().strip(),
            nombres=resolved_nombres,
            apellidos=resolved_apellidos,
            rol=rol,
            telefono=telefono,
            estado=estado,
        )
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        user = self.create_user(username=username, email=email, password=password, **extra_fields)
        user._is_superuser_override = True
        try:
            from apps.communications.models import SiteSetting
            setting, _ = SiteSetting.objects.get_or_create(
                clave='SUPERADMIN_EMAILS',
                defaults={'valor': ['admin@plus.org', 'superadmin@plus.org']},
            )
            emails = list(setting.valor) if isinstance(setting.valor, list) else []
            if user.correo.lower().strip() not in [e.lower().strip() for e in emails if isinstance(e, str)]:
                emails.append(user.correo.lower().strip())
                setting.valor = emails
                setting.save()
        except Exception:
            pass
        return user


class User(AbstractBaseUser):
    """
    Tabla SQL: plus.usuarios
    Mapea 1:1 a las columnas de base de datos.md sin agregar columnas extra.
    """

    class Estado(models.TextChoices):
        ACTIVO = 'activo', 'Activo'
        SUSPENDIDO = 'suspendido', 'Suspendido'
        INACTIVO = 'inactivo', 'Inactivo'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_usuario',
    )
    rol = models.ForeignKey(
        Role,
        on_delete=models.RESTRICT,
        db_column='id_rol',
        related_name='usuarios',
    )
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo = models.EmailField(max_length=150, unique=True)
    password = models.TextField(db_column='contrasena_hash')
    telefono = models.CharField(max_length=20, null=True, blank=True)
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.ACTIVO,
    )
    fecha_registro = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(default=timezone.now)

    # plus.usuarios no tiene columna last_login
    last_login = None

    objects = UserManager()

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombres', 'apellidos']

    class Meta:
        db_table = 'usuarios'
        ordering = ['-fecha_registro']
        indexes = [
            models.Index(fields=['rol'], name='ix_usuarios_rol'),
        ]

    @property
    def id_usuario(self):
        return self.id

    @property
    def username(self) -> str:
        return self.correo

    @property
    def email(self) -> str:
        return self.correo

    @property
    def first_name(self) -> str:
        return self.nombres

    @first_name.setter
    def first_name(self, value: str):
        self.nombres = value

    @property
    def last_name(self) -> str:
        return self.apellidos

    @last_name.setter
    def last_name(self, value: str):
        self.apellidos = value

    @property
    def full_name(self) -> str:
        return f'{self.nombres} {self.apellidos}'.strip()

    @property
    def is_active(self) -> bool:
        return self.estado == self.Estado.ACTIVO

    @is_active.setter
    def is_active(self, value: bool):
        self.estado = self.Estado.ACTIVO if value else self.Estado.INACTIVO

    @property
    def is_staff(self) -> bool:
        return self.rol_id is not None and self.rol.nombre in (
            Role.Nombre.ADMINISTRADOR,
            Role.Nombre.MODERADOR,
        )

    @property
    def is_superadmin(self) -> bool:
        if getattr(self, '_is_superuser_override', False):
            return True
        if not self.is_authenticated or not self.is_active:
            return False
        if self.get_primary_role() != Role.Nombre.ADMINISTRADOR:
            return False
        try:
            from apps.communications.models import SiteSetting
            setting = SiteSetting.objects.filter(clave='SUPERADMIN_EMAILS').first()
            if setting and isinstance(setting.valor, list):
                allowed = [e.lower().strip() for e in setting.valor if isinstance(e, str)]
                if self.correo.lower().strip() in allowed:
                    return True
        except Exception:
            pass
        return self.correo.lower().strip() in {'admin@plus.org', 'superadmin@plus.org'}

    @property
    def can_manage_homepage(self) -> bool:
        return self.is_superadmin

    @property
    def can_manage_forms(self) -> bool:
        if not self.is_authenticated or not self.is_active:
            return False
        return self.get_primary_role() == Role.Nombre.ADMINISTRADOR

    @property
    def is_superuser(self) -> bool:
        return self.is_superadmin

    def has_perm(self, perm, obj=None):
        return self.is_active and self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_active and self.is_staff

    def get_role_codes(self) -> list[str]:
        if not self.rol_id:
            return [Role.Nombre.CIUDADANO]
        return [self.rol.nombre]

    def get_primary_role(self) -> str:
        if not self.rol_id:
            return Role.Nombre.CIUDADANO
        return self.rol.nombre

    def has_any_role(self, *role_names: str) -> bool:
        if not self.is_authenticated or not self.is_active:
            return False
        normalized_targets = {normalize_role_name(r) for r in role_names}
        current = normalize_role_name(self.get_primary_role())
        if current == Role.Nombre.ADMINISTRADOR:
            return True
        return current in normalized_targets

    def has_role(self, role_name: str) -> bool:
        return self.has_any_role(role_name)

    def get_aggregated_permissions(self) -> dict:
        role_name = normalize_role_name(self.get_primary_role())
        perms = dict(ROLE_PERMISSIONS_MAP.get(role_name, ROLE_PERMISSIONS_MAP[Role.Nombre.CIUDADANO]))
        perms['can_manage_homepage'] = self.can_manage_homepage
        perms['can_manage_forms'] = self.can_manage_forms
        return perms

    def save(self, *args, **kwargs):
        self.correo = self.correo.lower().strip()
        self.fecha_actualizacion = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.nombres} {self.apellidos} <{self.correo}>'


class ResponsibleScopeAssignment(models.Model):
    """
    Tabla SQL: plus.asignaciones_responsables
    Vincula a un representante/responsable con una comunidad y/o un tipo de caso.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_asignacion',
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        db_column='id_usuario',
        related_name='asignaciones_ambito',
    )
    comunidad = models.ForeignKey(
        'territories.Community',
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        db_column='id_comunidad',
        related_name='responsables_asignados',
    )
    tipo_caso = models.ForeignKey(
        'cases.CaseCategory',
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        db_column='id_tipo_caso',
        related_name='responsables_asignados',
    )
    fecha_asignacion = models.DateTimeField(default=timezone.now)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'asignaciones_responsables'
        ordering = ['-fecha_asignacion']
        indexes = [
            models.Index(fields=['usuario', 'activo'], name='ix_asignacion_ambito_usuario'),
            models.Index(fields=['comunidad'], name='ix_asignacion_resp_comunidad'),
            models.Index(fields=['tipo_caso'], name='ix_asignacion_resp_tipo'),
        ]

    def __str__(self):
        return f'Ámbito de {self.usuario.correo}: comunidad={self.comunidad_id}, tipo={self.tipo_caso_id}'


class UserProfile(models.Model):
    """
    Tabla SQL (AMP-04): plus.perfiles_usuarios
    Relación 1:1 con plus.usuarios para fotografía y territorio de residencia.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_perfil',
    )
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        db_column='id_usuario',
        related_name='perfil',
    )
    ruta_foto = models.TextField(null=True, blank=True)
    departamento = models.ForeignKey(
        'territories.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_departamento',
        related_name='perfiles_usuarios',
    )
    municipio = models.ForeignKey(
        'territories.Municipality',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_municipio',
        related_name='perfiles_usuarios',
    )
    comunidad = models.ForeignKey(
        'territories.Community',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_comunidad',
        related_name='perfiles_usuarios',
    )
    fecha_actualizacion = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'perfiles_usuarios'

    def save(self, *args, **kwargs):
        if self.comunidad_id and not self.municipio_id:
            self.municipio = self.comunidad.municipio
        if self.municipio_id and not self.departamento_id:
            self.departamento = self.municipio.departamento
        self.fecha_actualizacion = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Perfil de {self.usuario.correo}'


class UserPreference(models.Model):
    """
    Tabla SQL (AMP-04): plus.preferencias_usuarios
    Relación 1:1 con plus.usuarios para preferencias de notificaciones y boletín.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_preferencia',
    )
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        db_column='id_usuario',
        related_name='preferencias',
    )
    notificar_novedades_casos = models.BooleanField(default=True)
    notificar_mensajes = models.BooleanField(default=True)
    suscrito_boletin = models.BooleanField(default=False)
    fecha_actualizacion = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'preferencias_usuarios'

    def save(self, *args, **kwargs):
        self.fecha_actualizacion = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Preferencias de {self.usuario.correo}'

