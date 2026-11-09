# Documentación Oficial de Endpoints — Backend PLUS (`v1.2.0`)

**Versión del Esquema OpenAPI:** `1.2.0` (`GET /api/v1/schema/` · archivo [`openapi-schema.yaml`](openapi-schema.yaml))  
**Estado:** Sincronizado con los modelos Django, migraciones, vistas y validadores reales del servidor (`01_init_plus_schema.sql` + `02_ampliaciones_v1_2.sql`).

---

## 1. Convenciones Generales, Almacenamiento y Decisiones de Integración

### 1.1. Base URL y Esquema OpenAPI `1.2.0`
- **Prefijo base:** `/api/v1/`
- **Esquema OpenAPI 3 (`v1.2.0`):** `GET /api/v1/schema/`
- **Interfaz Swagger UI:** `GET /api/v1/docs/`

### 1.2. Tipo de Identificadores: **100% UUID**
- **Todas las claves primarias y foráneas** del dominio (`id_usuario`, `id_rol`, `id_departamento`, `id_municipio`, `id_comunidad`, `id_cuenca`, `id_tipo_caso`, `id_estado`, `id_caso`, `id_asignacion_caso`, `id_solicitud`, `id_aporte`, `id_evidencia`, `id_seguimiento`, `id_historial`, `id_mensaje`, `id_comentario`, `id_notificacion`, `id_iniciativa`, `id_edicion`, `id_actividad`, `id_indicador`, `id_multimedia`, `id_noticia`, `id_categoria`, `id_propuesta`) son **UUID v4** tanto al leer como al enviar relaciones.
- En rutas de consulta de casos (`{lookup}`, `{case_id}`), el backend resuelve transparentemente tanto el **UUID** (`880e8400-e29b-41d4-a716-446655440000`) como el **código de radicado** (`PLUS-2026-00001`).
- En rutas de consulta de noticias e iniciativas (`{lookup}`), el backend resuelve tanto el **UUID** como el **`slug`**.

### 1.3. Autenticación JWT, Renovación y Revocación en Servidor
- **Cabecera requerida en endpoints autenticados:**
  ```http
  Authorization: Bearer <access_token>
  ```
  *(También soporta `Authorization: Token <drf_token>` por compatibilidad).*
- **Cómo funciona la revocación de JWT (`access` y `refresh`) y la suspensión de cuentas:**
  1. Al emitir los tokens JWT en `login`, `register` o `refresh`, el backend incluye en el payload del JWT una marca de sesión (`sid`) vinculada al registro del usuario en `authtoken_token`.
  2. La clase `RevocableJWTAuthentication` (para cada petición con `Bearer <access>`) y `RevocableTokenRefreshView` (`POST /api/v1/auth/refresh/`) verifican en servidor:
     - Que el usuario exista y su campo `usuarios.estado` sea `'activo'` (`is_active = True`). Si un administrador cambia el estado a `'suspendido'` o `'inactivo'` (`PATCH /api/v1/admin/users/{id}/status/`), **tanto el `access` como el `refresh` quedan rechazados de inmediato con `401 Unauthorized`**.
     - Que la marca `sid` del JWT coincida con la sesión activa en servidor. Al ejecutar `POST /api/v1/auth/logout/`, cambiar la contraseña o restablecerla, el servidor elimina el registro en `authtoken_token`, **invalidando inmediatamente tanto el `access` como el `refresh` token** sin esperar a su expiración natural.

### 1.4. Paginación y Formato Estándar de Errores
- **Paginación (`StandardResultsSetPagination`):**
  - Tamaño por defecto: `12` registros por página (`?page=1&page_size=12`, máximo `100`).
  - Estructura:
    ```json
    {
      "count": 42,
      "next": "http://localhost:8000/api/v1/public/cases/?page=2",
      "previous": null,
      "results": [ ... ]
    }
    ```
- **Sobre común de errores (`core.exceptions.custom_exception_handler`):**
  ```json
  {
    "code": "validation_error",
    "message": "No se pudo completar la solicitud.",
    "errors": {
      "correo": ["Este correo electrónico ya está registrado."]
    }
  }
  ```

### 1.5. Almacenamiento (`MEDIA_ROOT`) y Entrega Segura de Archivos (`/api/v1/public/media/...`)
- **Persistencia en contenedor:** `MEDIA_ROOT` apunta a `/app/media`, montado sobre el volumen persistente `plus_media:/app/media` en `docker-compose.yml`.
- **Límites configurados en Django:**
  - Tamaño máximo por archivo individual: **15 MB** (`15,728,640 bytes`).
  - Tamaño máximo total del cuerpo de la petición (`DATA_UPLOAD_MAX_MEMORY_SIZE`): **64 MB** (permite subir varios adjuntos en una sola petición multipart). *Nota para despliegue: asegurar `client_max_body_size 64M;` en Nginx.*
  - Extensiones permitidas: `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`, `.pdf`, `.doc`, `.docx`, `.xls`, `.xlsx`, `.txt`, `.csv`, `.mp4`, `.mp3`, `.wav`, `.ogg`.
- **Campos `multipart/form-data`:**
  - Evidencia individual: `file` o `archivo`.
  - Archivos iniciales al radicar caso o crear aporte: `files` o `archivos`.
  - Foto de perfil: `photo`, `foto` o `file`.
  - Portada/multimedia de noticias e iniciativas: `archivo`, `file` o `imagen_portada`.
- **Entrega pública autorizada sin exponer el volumen completo (`GET /api/v1/public/media/<path:file_path>`):**
  - Dado que `docker/nginx.conf` del frontend reenvía `/api/` al backend y no expone `/media/`, el backend provee el endpoint público **`GET /api/v1/public/media/<path:file_path>`**.
  - Este endpoint sirve **únicamente**:
    1. Archivos en carpetas públicas (`profiles/`, `news/`, `initiatives/`).
    2. Archivos en `cases/evidence/` **solo si** en base de datos la evidencia tiene `audiencia = 'publico'`, `estado_revision = 'aprobada'` y pertenece a un caso con `estado_publicacion = 'aprobado'`.
  - Cualquier intento de acceder a una evidencia privada o en revisión por esta ruta responde `403 Forbidden`. Las evidencias privadas del ciudadano o del equipo solo se descargan mediante los endpoints autenticados `GET /api/v1/me/cases/{id}/evidence/{evidence_id}/download/?download=1` o `GET /api/v1/admin/cases/{id}/evidence/{evidence_id}/download/?download=1`.

---

## 2. Autenticación y Recuperación de Sesión (`/api/v1/auth/`)

### `AUTH-01` · Registro Ciudadano
- **Ruta:** `POST /api/v1/auth/register/`
- **Acceso:** Público (`AllowAny`)
- **Descripción:** Crea el usuario en `plus.usuarios` con rol único `ciudadano` y `estado = 'activo'`, inicializa `perfiles_usuario` y `preferencias_usuario`, y registra el consentimiento en `aceptaciones_legales` (`AMP-04`).
- **Request JSON:**
  ```json
  {
    "nombres": "María Fernanda",
    "apellidos": "López Gómez",
    "correo": "maria.lopez@ejemplo.org",
    "telefono": "3001234567",
    "password": "PasswordSegura123!",
    "acepta_tratamiento_datos": true
  }
  ```
- **Response (`201 Created`):** Devuelve los tokens tanto en la raíz como dentro del objeto `tokens`, además de `user` (`UserMeSerializer`):
  ```json
  {
    "access": "<jwt_access_token>",
    "refresh": "<jwt_refresh_token>",
    "token": "<drf_authtoken>",
    "token_type": "Bearer",
    "expires_in": 3600,
    "refresh_expires_in": 604800,
    "tokens": {
      "access": "<jwt_access_token>",
      "refresh": "<jwt_refresh_token>",
      "token": "<drf_authtoken>",
      "token_type": "Bearer",
      "expires_in": 3600,
      "refresh_expires_in": 604800
    },
    "primary_role": "ciudadano",
    "roles": ["ciudadano"],
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "id_usuario": "550e8400-e29b-41d4-a716-446655440000",
      "id_rol": "110e8400-e29b-41d4-a716-446655440000",
      "rol_nombre": "ciudadano",
      "nombres": "María Fernanda",
      "apellidos": "López Gómez",
      "full_name": "María Fernanda López Gómez",
      "correo": "maria.lopez@ejemplo.org",
      "telefono": "3001234567",
      "estado": "activo",
      "primary_role": "ciudadano",
      "roles": ["ciudadano"],
      "permissions": {
        "can_create_cases": true,
        "can_manage_own_cases": true,
        "can_moderate_cases": false,
        "can_assign_cases": false,
        "can_resolve_cases": false,
        "can_manage_users": false,
        "can_view_audit": false,
        "can_export_reports": false
      },
      "perfil": {
        "id_perfil": "220e8400-e29b-41d4-a716-446655440000",
        "ruta_foto": null,
        "foto_url": null,
        "id_departamento": null,
        "departamento_nombre": null,
        "id_municipio": null,
        "municipio_nombre": null,
        "id_comunidad": null,
        "comunidad_nombre": null,
        "fecha_actualizacion": "2026-11-09T02:00:00Z"
      },
      "preferencias": {
        "id_preferencia": "330e8400-e29b-41d4-a716-446655440000",
        "notificar_novedades_casos": true,
        "notificar_avance_casos": true,
        "notificar_mensajes": true,
        "suscrito_boletin": false,
        "recibir_boletin": false,
        "fecha_actualizacion": "2026-11-09T02:00:00Z"
      },
      "ambitos_responsable": [],
      "fecha_registro": "2026-11-09T02:00:00Z",
      "fecha_actualizacion": "2026-11-09T02:00:00Z"
    }
  }
  ```

### `AUTH-02` · Inicio de Sesión (Login)
- **Ruta:** `POST /api/v1/auth/login/` *(Alias legacy: `POST /api/login/`)*
- **Acceso:** Público (`AllowAny`)
- **Request JSON:**
  ```json
  {
    "correo": "admin@plus.org",
    "password": "AdminPlus2026!"
  }
  ```
- **Response (`200 OK`):** Misma estructura que `AUTH-01` (`access`, `refresh`, `token`, `token_type`, `expires_in`, `refresh_expires_in`, `tokens`, `primary_role`, `roles`, `user`). Registra cada intento exitoso o fallido en `auditoria_accesos`.

### `AUTH-03` · Renovación de Token JWT
- **Ruta:** `POST /api/v1/auth/refresh/`
- **Acceso:** Público con token `refresh` vigente y no revocado.
- **Request JSON:**
  ```json
  {
    "refresh": "<jwt_refresh_token>"
  }
  ```
- **Response (`200 OK`):**
  ```json
  {
    "access": "<nuevo_jwt_access_token>",
    "refresh": "<nuevo_jwt_refresh_token>",
    "token_type": "Bearer",
    "expires_in": 3600
  }
  ```

### `AUTH-04` · Cierre de Sesión (Logout)
- **Ruta:** `POST /api/v1/auth/logout/`
- **Acceso:** Usuario autenticado (`IsAuthenticated`)
- **Efecto en servidor:** Elimina el token de sesión del usuario en `authtoken_token`, lo que invalida de inmediato la marca `sid` de cualquier `access` y `refresh` JWT emitido previamente, y registra el evento `logout` en `auditoria_accesos`.
- **Response (`200 OK`):**
  ```json
  {
    "message": "Sesión cerrada exitosamente.",
    "detail": "Sesión cerrada exitosamente."
  }
  ```

### `AUTH-05`, `AUTH-06` y `AUTH-07` · Recuperación de Contraseña (vía Resend SMTP)
- **Solicitar recuperación (`AUTH-05`):** `POST /api/v1/auth/password-reset/request/`
  - **Request:** `{"correo": "usuario@ejemplo.org"}`
  - **Comportamiento en servidor:**
    - Para cuentas con `estado = 'activo'`, genera `uid` (base64 URL-safe del UUID del usuario) y `token` temporal con vigencia de **1 hora** (`PASSWORD_RESET_TIMEOUT = 3600` segundos).
    - Envía correo multipart (**texto plano + HTML**) mediante **Resend SMTP** (`DEFAULT_FROM_EMAIL = PLUS <notificaciones@fundacionplus.site>`) con el enlace:
      ```text
      https://fundacionplus.site/restablecer-contrasena?uid=<uid>&token=<token>
      ```
    - Incluye limitador de solicitudes repetidas (`PasswordResetRateThrottle` y ventana de enfriamiento por cuenta) y registra el resultado (`exitoso` o `fallido`) en `auditoria_accesos` sin exponer jamás el token en logs ni en respuestas.
  - **Response (`200 OK` — genérica sin revelar existencia de cuenta):**
    ```json
    {
      "message": "Si el correo está asociado a una cuenta activa, recibirás instrucciones para restablecer tu contraseña.",
      "detail": "Si el correo está asociado a una cuenta activa, recibirás instrucciones para restablecer tu contraseña."
    }
    ```
- **Validar enlace/token (`AUTH-06`):** `POST /api/v1/auth/password-reset/validate/`
  - **Request:** Acepta `{"uid": "<uid_base64>", "token": "<token>"}` o token compuesto `{"token": "<uid_base64>.<token>"}`.
  - **Response (`200 OK`):** `{"valid": true}` (o `400 Bad Request` con `{"code": "invalid_token", "message": "El enlace de recuperación es inválido o ha expirado."}`).
- **Confirmar nueva contraseña (`AUTH-07`):** `POST /api/v1/auth/password-reset/confirm/`
  - **Request:**
    ```json
    {
      "uid": "<uid_base64>",
      "token": "<token>",
      "new_password": "NuevaPassword123!",
      "new_password_confirm": "NuevaPassword123!"
    }
    ```
    *(Si no se envía `uid` por separado, puede enviarse `"token": "<uid_base64>.<token>"`).*
  - **Efecto en servidor:** Valida la nueva contraseña contra los validadores de seguridad de Django (incluyendo similitud con datos del usuario), actualiza el hash de contraseña (lo que invalida inmediatamente el enlace para que no pueda reutilizarse) y elimina el registro en `authtoken_token` revocando todas las sesiones anteriores (`access`, `refresh` y `Token`).
  - **Response (`200 OK`):** `{"message": "Contraseña restablecida exitosamente.", "detail": "Contraseña restablecida exitosamente."}`.

---

## 3. Perfil, Fotografía y Preferencias de Cuenta Propia (`/api/v1/me/`)

### `ME-01` y `ME-02` · Consultar y Actualizar Perfil Propio
- **Rutas:** `GET /api/v1/me/`, `PATCH /api/v1/me/`, `PUT /api/v1/me/` *(Alias: `/api/v1/auth/me/`)*
- **Acceso:** Usuario autenticado (`IsAuthenticated`)
- **Request JSON (`PATCH`):**
  ```json
  {
    "nombres": "María Fernanda",
    "apellidos": "López Gómez",
    "correo": "maria.lopez@ejemplo.org",
    "telefono": "3109876543",
    "id_departamento": "440e8400-e29b-41d4-a716-446655440000",
    "id_municipio": "550e8400-e29b-41d4-a716-446655440000",
    "id_comunidad": "660e8400-e29b-41d4-a716-446655440000"
  }
  ```
  > **Regla `ME-02`:** Cualquier intento de enviar `rol`, `id_rol` o `estado` en `PATCH /api/v1/me/` es rechazado con `400 Bad Request`.
- **Response (`200 OK`):** Objeto `UserMeSerializer` (ver estructura completa en `AUTH-01`).
  - **Roles y capacidades (`USR-05` / `ME-01`):** El modelo mantiene **rol único** en `usuarios.id_rol` (`administrador`, `representante`, `moderador`, `ciudadano`), expuesto en `id_rol` (UUID), `rol_nombre` y `primary_role`. El arreglo `roles` se incluye únicamente por compatibilidad con guards de lectura, y el objeto `permissions` entrega las capacidades booleanas calculadas por el servidor.

### `ME-03` y `ME-04` · Subir, Actualizar o Eliminar Fotografía de Perfil (`AMP-04`)
- **Subir/actualizar (`ME-03`):** `PUT /api/v1/me/photo/` o `POST /api/v1/me/photo/`
  - **Formato:** `multipart/form-data` con el archivo en `photo`, `foto` o `file` (formatos `.jpg`, `.jpeg`, `.png`, `.webp`, máx. 15 MB).
  - **Response (`200 OK` — `UserProfileSerializer`):**
    ```json
    {
      "id_perfil": "220e8400-e29b-41d4-a716-446655440000",
      "ruta_foto": "/api/v1/public/media/profiles/550e8400-e29b-41d4-a716-446655440000/avatar.jpg",
      "foto_url": "/api/v1/public/media/profiles/550e8400-e29b-41d4-a716-446655440000/avatar.jpg",
      "id_departamento": null,
      "departamento_nombre": null,
      "id_municipio": null,
      "municipio_nombre": null,
      "id_comunidad": null,
      "comunidad_nombre": null,
      "fecha_actualizacion": "2026-11-09T02:05:00Z"
    }
    ```
- **Eliminar fotografía (`ME-04`):** `DELETE /api/v1/me/photo/` -> Responde `204 No Content`.

### `ME-05` · Consultar y Actualizar Preferencias (`AMP-04`)
- **Rutas:** `GET /api/v1/me/preferences/`, `PATCH /api/v1/me/preferences/`, `PUT /api/v1/me/preferences/`
- **Acceso:** Usuario autenticado (`IsAuthenticated`)
- **Campos reales en `preferencias_usuario` (y sus alias soportados):**
  ```json
  {
    "id_preferencia": "330e8400-e29b-41d4-a716-446655440000",
    "notificar_novedades_casos": true,
    "notificar_avance_casos": true,
    "notificar_mensajes": true,
    "suscrito_boletin": true,
    "recibir_boletin": true,
    "fecha_actualizacion": "2026-11-09T02:05:00Z"
  }
  ```
  > **Regla `18.4.6`:** Cambiar `suscrito_boletin` (o su alias `recibir_boletin`) sincroniza en transacción la fila del usuario en `suscripciones_boletin` y registra la aceptación en `aceptaciones_legales`.

### Cambio de Contraseña en Sesión Activa
- **Rutas:** `POST /api/v1/me/change-password/` *(Alias: `POST /api/v1/auth/change-password/`)*
- **Request JSON:** `{"current_password": "...", "new_password": "..."}`
- **Response (`200 OK`):** `{"message": "Contraseña actualizada exitosamente."}`

---

## 4. Catálogos Territoriales y Maestros (`/api/v1/catalogs/`)

Todos los catálogos son de acceso público (`AllowAny`) y devuelven **UUID reales**:

### `CAT-01` · Departamentos
- **Ruta:** `GET /api/v1/catalogs/departments/` *(Alias: `/api/v1/public/territories/departments/`)*
- **Filtros:** `?search=`
- **Response (`200 OK`):**
  ```json
  [
    {
      "id": "d10e8400-e29b-41d4-a716-446655440000",
      "id_departamento": "d10e8400-e29b-41d4-a716-446655440000",
      "codigo_dane": "05",
      "nombre": "Antioquia",
      "municipios_count": 125
    }
  ]
  ```

### `CAT-02` · Municipios
- **Ruta:** `GET /api/v1/catalogs/municipalities/` *(Alias: `/api/v1/public/territories/municipalities/`)*
- **Filtros:** `?id_departamento=<uuid>` (alias `?departamento=<uuid>` o código DANE), `?search=`
- **Response (`200 OK`):**
  ```json
  [
    {
      "id": "a20e8400-e29b-41d4-a716-446655440000",
      "id_municipio": "a20e8400-e29b-41d4-a716-446655440000",
      "departamento": "d10e8400-e29b-41d4-a716-446655440000",
      "id_departamento": "d10e8400-e29b-41d4-a716-446655440000",
      "departamento_nombre": "Antioquia",
      "departamento_codigo": "05",
      "codigo_dane": "05001",
      "nombre": "Medellín",
      "comunidades_count": 12
    }
  ]
  ```

### `CAT-03` · Comunidades
- **Rutas:** `GET /api/v1/catalogs/communities/` *(Aliases: `/api/v1/public/territories/communities/` y `/api/v1/public/territories/municipalities/{municipality_id}/communities/`)*
- **Filtros:** `?id_municipio=<uuid>` (alias `?municipio=`), `?id_departamento=<uuid>`, `?tipo=` (`barrio`, `vereda`, `corregimiento`, `comuna`, `sector`, `otro`), `?activo=true`, `?search=`
- **Response (`200 OK`):**
  ```json
  [
    {
      "id": "660e8400-e29b-41d4-a716-446655440000",
      "id_comunidad": "660e8400-e29b-41d4-a716-446655440000",
      "municipio": "a20e8400-e29b-41d4-a716-446655440000",
      "id_municipio": "a20e8400-e29b-41d4-a716-446655440000",
      "municipio_nombre": "Medellín",
      "municipio_codigo": "05001",
      "id_departamento": "d10e8400-e29b-41d4-a716-446655440000",
      "departamento_nombre": "Antioquia",
      "nombre": "Vereda La Loma",
      "descripcion": "Sector rural occidental",
      "tipo": "vereda",
      "ubicacion": null,
      "activo": true
    }
  ]
  ```
  > **Nota sobre `tipo`:** Los valores del catálogo SQL `comunidades.tipo` son exactamente `barrio`, `vereda`, `corregimiento`, `comuna`, `sector`, `otro`.

### `CAT-04` · Cuencas Hidrográficas
- **Ruta:** `GET /api/v1/catalogs/basins/`
- **Descripción:** Punto de extensión para cuencas (`AMP-13`). Devuelve arreglo `[]` mientras no se cargue una fuente oficial de cuencas, permitiendo filtrar por municipio y comunidad.

### `CAT-05` y `CAT-06` · Categorías, Tipos, Estados y Opciones de Caso
- **Categorías temáticas distintas (`CAT-05`):** `GET /api/v1/catalogs/case-categories/`
  - **Response (`200 OK`):**
    ```json
    {
      "count": 4,
      "results": ["ambiental", "derechos_humanos", "infraestructura", "social"]
    }
    ```
- **Tipos de caso (`CAT-06a`):** `GET /api/v1/catalogs/case-types/` *(Alias: `/api/v1/public/case-categories/`)*
  - **Filtros:** `?categoria=`, `?naturaleza=` (`problematica`, `proyecto_iniciativa`, `otro`)
  - **Response (`200 OK`):**
    ```json
    [
      {
        "id": "b10e8400-e29b-41d4-a716-446655440000",
        "id_tipo_caso": "b10e8400-e29b-41d4-a716-446655440000",
        "nombre": "Contaminación de fuente hídrica",
        "descripcion": "Afectación sobre quebradas o acueductos comunitarios",
        "categoria": "ambiental",
        "naturaleza": "problematica",
        "activo": true,
        "casos_count": 3
      }
    ]
    ```
- **Estados operativos de caso (`CAT-06b`):** `GET /api/v1/catalogs/case-statuses/` *(Alias: `/api/v1/public/case-statuses/`)*
  - **Valores oficiales SQL (`estados_caso`):** `pendiente` (orden 1), `en_revision` (orden 2), `en_proceso` (orden 3), `resuelto` (orden 4), `cerrado` (orden 5).
  - **Response (`200 OK`):**
    ```json
    [
      {
        "id": "e10e8400-e29b-41d4-a716-446655440000",
        "id_estado": "e10e8400-e29b-41d4-a716-446655440000",
        "nombre": "pendiente",
        "descripcion": "Caso recibido pendiente de gestión",
        "orden": 1
      }
    ]
    ```
- **Opciones consolidadas para formularios (`CAT-06c`):** `GET /api/v1/catalogs/case-options/`
  - **Response (`200 OK`):**
    ```json
    {
      "tipos_caso": [ ... ],
      "categorias": ["ambiental", "derechos_humanos", "infraestructura", "social"],
      "naturalezas": [
        {"value": "problematica", "label": "Problemática"},
        {"value": "proyecto_iniciativa", "label": "Proyecto / Iniciativa"},
        {"value": "otro", "label": "Otro"}
      ],
      "estados_caso": [ ... ],
      "prioridades": [
        {"value": "baja", "label": "Baja"},
        {"value": "media", "label": "Media"},
        {"value": "alta", "label": "Alta"},
        {"value": "critica", "label": "Crítica"}
      ],
      "estados_publicacion": [
        {"value": "pendiente", "label": "Pendiente"},
        {"value": "aprobado", "label": "Aprobado"},
        {"value": "rechazado", "label": "Rechazado"}
      ]
    }
    ```

### `CAT-07` y `CAT-08` · Categorías de Noticias e Iniciativas
- **Categorías de noticias (`CAT-07`):** `GET /api/v1/catalogs/news-categories/` *(Aliases: `/api/v1/public/news/categories/`, `/api/v1/public/news-categories/`)*
  - **Response (`200 OK`):** Lista de `NewsCategorySerializer` (`id`, `id_categoria` UUID, `nombre`, `slug`, `descripcion`, `activa`).
- **Categorías de iniciativas (`CAT-08`):** `GET /api/v1/catalogs/initiative-categories/` *(Alias: `/api/v1/public/initiatives/categories/`)*
  - **Response (`200 OK`):** `{"count": 2, "results": ["Ambiental", "Derechos Humanos"]}`.

---

## 5. Portal Público, Sitio, Noticias, Iniciativas y Boletín (`/api/v1/public/`)

### `PUB-01` · Configuración e Identidad Institucional Pública
- **Rutas:** `GET /api/v1/public/site/` *(Alias: `/api/v1/public/site-info/`)*
- **Response (`200 OK`):**
  ```json
  {
    "configuracion": {
      "institucion.nombre": {"nombre": "Corporación Pluralismo Social", "sigla": "PLUS"},
      "mapa.srid_defecto": {"srid": 4326},
      "iniciativas.max_destacadas": {"maximo": 3}
    },
    "documentos_legales": [
      {
        "id": "900e8400-e29b-41d4-a716-446655440000",
        "id_documento": "900e8400-e29b-41d4-a716-446655440000",
        "tipo": "tratamiento_datos",
        "version": "1.0",
        "titulo": "Política de Tratamiento de Datos Personales",
        "contenido": "...",
        "vigente": true,
        "fecha_vigencia": "2026-01-01T00:00:00Z"
      }
    ]
  }
  ```

### `PUB-02` · Resumen de la Página de Inicio (Home)
- **Ruta:** `GET /api/v1/public/home/`
- **Response (`200 OK`):**
  ```json
  {
    "site": {
      "institucion.nombre": {"nombre": "Corporación Pluralismo Social", "sigla": "PLUS"}
    },
    "metrics": {
      "casos_publicados_total": 12,
      "casos_resueltos_publicos": 5,
      "comunidades_con_casos_publicos": 8,
      "iniciativas_publicadas_total": 4
    },
    "featured_initiatives": [ ... ],
    "latest_news": [ ... ]
  }
  ```

### `PUB-03` y `PUB-04` · Noticias Institucionales (`AMP-01`)
- **Listado (`PUB-03`):** `GET /api/v1/public/news/`
  - **Filtros:** `?categoria=` (slug o UUID), `?destacada=true`, `?search=`, `?page=`, `?page_size=`.
- **Detalle (`PUB-04`):** `GET /api/v1/public/news/{lookup}/` (`{lookup}` acepta `slug` o UUID).
- **Campos del DTO (`NewsArticleDetailSerializer`):**
  ```json
  {
    "id": "710e8400-e29b-41d4-a716-446655440000",
    "id_noticia": "710e8400-e29b-41d4-a716-446655440000",
    "categoria": "700e8400-e29b-41d4-a716-446655440000",
    "id_categoria": "700e8400-e29b-41d4-a716-446655440000",
    "categoria_nombre": "Comunicados",
    "categoria_slug": "comunicados",
    "slug": "jornada-defensa-territorio-2026",
    "titulo": "Jornada por la defensa del territorio",
    "subtitulo": "Encuentro regional con líderes comunitarios",
    "extracto": "Resumen corto de la noticia...",
    "contenido": "Cuerpo completo de la noticia...",
    "estado": "publicada",
    "destacada": true,
    "autor": "c1a9f2d0-1234-4bcd-8ef0-112233445566",
    "autor_nombre": "Administrador PLUS",
    "portada": {
      "id_multimedia": "720e8400-e29b-41d4-a716-446655440000",
      "tipo": "imagen",
      "ruta_archivo": "/api/v1/public/media/news/portada.webp",
      "texto_alternativo": "Fotografía del encuentro"
    },
    "medios": [ ... ],
    "fecha_publicacion": "2026-11-08T12:00:00Z",
    "fecha_creacion": "2026-11-08T10:00:00Z",
    "fecha_actualizacion": "2026-11-08T12:00:00Z"
  }
  ```

### `PUB-05`, `PUB-06`, `PUB-07` e `INI-01` a `INI-03` · Iniciativas, Ediciones, Actividades y Galería
- **Listado de programas (`PUB-05`):** `GET /api/v1/public/initiatives/`
  - **Filtros:** `?categoria=`, `?destacada=true`, `?anio=2026` (filtra por año en `ediciones`), `?search=`.
- **Detalle de programa (`PUB-06`):** `GET /api/v1/public/initiatives/{lookup}/` (`slug` o UUID).
  - Devuelve `id_iniciativa` (UUID), `slug`, `titulo`, `subtitulo`, `descripcion_corta`, `descripcion`, `categoria`, `estado` (`publicada`), `destacada`, `portada_general`, `medios_generales` (`id_edicion = null`) y `ediciones`.
- **Galería multimedia (`PUB-07`):** `GET /api/v1/public/initiatives/{lookup}/gallery/` y `GET /api/v1/public/initiatives/gallery/`
  - **Filtros:** `?id_edicion=<uuid>`, `?general_only=true`, `?tipo=` (`imagen`, `video`, `documento`).
- **Ediciones anuales de una iniciativa (`INI-01`):** `GET /api/v1/public/initiatives/{lookup}/editions/`
  - **Filtros:** `?anio=2026`, `?estado=` (`planificada`, `en_curso`, `finalizada`, `cancelada`).
- **Detalle de edición anual (`INI-02`):** `GET /api/v1/public/initiatives/{lookup}/editions/{edition_id}/`
  - Verifica que `{edition_id}` pertenezca al programa `{lookup}`. Devuelve los `indicadores` (`valor` decimal, `unidad`, `tipo_medicion`: `estimado` o `real`), `comunidades` de cobertura, `actividades`, `multimedia` de la edición y `casos_vinculados` aprobados.
- **Actividades de una edición (`INI-03`):** `GET /api/v1/public/initiatives/{lookup}/editions/{edition_id}/activities/`
  - Devuelve `id_actividad` (UUID), `titulo`, `descripcion`, `tipo_actividad`, `comunidad_nombre`, `lugar`, `fecha_inicio`, `fecha_fin`, `estado` (sin exponer datos sensibles de contacto interno).

### `PUB-08` · Postulación Pública de Propuestas de Iniciativas (`propuestas_iniciativas`)
- **Rutas:** `POST /api/v1/public/initiative-proposals/` *(Aliases: `/api/v1/public/initiatives/proposals/`, `/api/v1/public/event-proposals/`)*
- **Acceso:** Público o usuario autenticado (`AllowAny`)
- **Campos reales del DTO (`EventProposalSerializer`):**
  ```json
  {
    "titulo": "Jornada de reforestación comunitaria",
    "descripcion": "Propuesta para articular a 40 jóvenes de la vereda...",
    "tipo_actividad": "ambiental",
    "fecha_sugerida": "2026-12-05",
    "iniciativa_solicitada": "770e8400-e29b-41d4-a716-446655440000",
    "id_comunidad": "660e8400-e29b-41d4-a716-446655440000",
    "comunidad_declarada": "Vereda La Loma",
    "nombre_contacto": "Carlos Ruiz",
    "telefono_contacto": "3151234567",
    "acepta_tratamiento_datos": true
  }
  ```
- **Response (`201 Created`):** Devuelve la propuesta con `id_propuesta` (UUID) y `estado: "pendiente"`.

### `PUB-09`, `PUB-10` y `PUB-11` · Suscripción al Boletín (`AMP-02`)
- **Suscribirse (`PUB-09`):** `POST /api/v1/public/newsletter-subscriptions/` *(Alias: `/api/v1/public/newsletter/subscribe/`)*
  - **Request:** `{"nombre": "Juan Pérez", "correo": "lector@ejemplo.org", "acepta_tratamiento_datos": true}`
  - **Response (`201 Created`):** `{"id_suscripcion": "<uuid>", "correo": "lector@ejemplo.org", "estado": "pendiente", "token_confirmacion": "<token>", "message": "..."}`
- **Confirmar (`PUB-10`):** `POST /api/v1/public/newsletter-subscriptions/confirm/` *(o `GET ...?token=<token>`)*
  - **Request:** `{"token": "<token_confirmacion>"}` -> **Response (`200 OK`):** `{"estado": "confirmada", "message": "Suscripción al boletín confirmada exitosamente."}`
- **Darse de baja (`PUB-11`):** `POST /api/v1/public/newsletter-subscriptions/unsubscribe/`
  - **Request:** `{"token": "<token_baja>", "correo": "lector@ejemplo.org"}` -> **Response (`200 OK`):** `{"estado": "baja", "message": "La suscripción al boletín ha sido dada de baja."}`

---

## 6. Mapa Interactivo (GeoJSON) y Expediente Público de Casos

### `MAP-01` · Listado Público de Casos Aprobados
- **Ruta:** `GET /api/v1/public/cases/`
- **Filtros Query:**
  - `?q=` o `?search=` (búsqueda en código, título, descripción, dirección)
  - `?naturaleza=` (`problematica`, `proyecto_iniciativa`, `otro`)
  - `?categoria=` (categoría textual de `tipos_caso`)
  - `?id_tipo_caso=<uuid>` (alias `?tipo_caso=`)
  - `?id_estado=<uuid>` o `?estado=` (`pendiente`, `en_revision`, `en_proceso`, `resuelto`, `cerrado`)
  - `?prioridad=` (`baja`, `media`, `alta`, `critica`)
  - `?id_departamento=<uuid>`, `?id_municipio=<uuid>`, `?id_comunidad=<uuid>`
  - `?fecha_desde=YYYY-MM-DD`, `?fecha_hasta=YYYY-MM-DD`
  - `?bbox=oeste,sur,este,norte` (`minLon,minLat,maxLon,maxLat`)
- **Response (`200 OK`):** Paginado con `PublicCaseListSerializer` (todos los IDs son UUID; coordenadas generalizadas en `public_location`).

### `MAP-02` · Mapa GeoJSON de Casos Aprobados
- **Rutas:** `GET /api/v1/public/cases/map/` *(Alias: `GET /api/v1/public/cases/geojson/`)*
- **Filtros Query:** Acepta todos los filtros de `MAP-01` más `?bbox=oeste,sur,este,norte`.
- **Response (`200 OK` — `GeoJSONCaseFeatureCollectionSerializer`):**
  ```json
  {
    "type": "FeatureCollection",
    "srid": 4326,
    "count": 1,
    "features": [
      {
        "type": "Feature",
        "id": "880e8400-e29b-41d4-a716-446655440000",
        "geometry": {
          "type": "Point",
          "srid": 4326,
          "coordinates": [-75.56, 6.25]
        },
        "properties": {
          "id_caso": "880e8400-e29b-41d4-a716-446655440000",
          "codigo": "PLUS-2026-00001",
          "radicado_code": "PLUS-2026-00001",
          "titulo": "Contaminación de quebrada en sector rural",
          "prioridad": "alta",
          "id_estado": "e10e8400-e29b-41d4-a716-446655440000",
          "estado": "en_proceso",
          "id_tipo_caso": "b10e8400-e29b-41d4-a716-446655440000",
          "tipo": "Contaminación de fuente hídrica",
          "categoria": "ambiental",
          "naturaleza": "problematica",
          "id_comunidad": "660e8400-e29b-41d4-a716-446655440000",
          "comunidad": "Vereda La Loma",
          "id_municipio": "a20e8400-e29b-41d4-a716-446655440000",
          "municipio": "Medellín",
          "id_departamento": "d10e8400-e29b-41d4-a716-446655440000",
          "departamento": "Antioquia",
          "longitud": -75.56,
          "latitud": 6.25,
          "fecha_creacion": "2026-11-08T14:20:00Z"
        }
      }
    ]
  }
  ```

### `MAP-03`, `MAP-04`, `MAP-05`, `MAP-06` y `MAP-07` · Expediente Público de Caso
- **Detalle público (`MAP-03`):** `GET /api/v1/public/cases/{lookup}/` (UUID o código `PLUS-2026-00001`).
  - Incluye `descripcion`, `resultado_resumen`, `fecha_resolucion`, `public_updates`, `public_status_history`, `public_evidence` y `approved_comments`.
- **Historial público (`MAP-04`):** `GET /api/v1/public/cases/{case_id}/history/`
  - Devuelve `{case_id, codigo, timeline, seguimientos, historial_estados}` filtrando únicamente `visible_publicamente = true`.
- **Evidencias públicas (`MAP-05` — `AMP-10`):** `GET /api/v1/public/cases/{case_id}/evidence/`
  - Devuelve solo las evidencias del caso aprobado que tengan `audiencia = 'publico'` y `estado_revision = 'aprobada'`.
- **Listar comentarios aprobados (`MAP-06`):** `GET /api/v1/public/cases/{case_id}/comments/`
  - Devuelve lista de `PublicCaseCommentSerializer` (`id`, `id_comentario` UUID, `autor_nombre`, `contenido`, `fecha_creacion`).
- **Crear comentario (`MAP-07`):** `POST /api/v1/cases/{case_id}/comments/` *(Alias: `/api/v1/citizen/cases/{case_id}/comments/`)*
  - **Acceso:** Usuario autenticado (`IsAuthenticated`).
  - **Request JSON:** `{"contenido": "Agradecemos el seguimiento en nuestra vereda."}`
  - **Response (`201 Created`):** Se guarda con `estado_moderacion = 'pendiente'`.

### `MAP-08`, `MAP-09` y `MAP-10` · Casos Seguidos (`casos_seguidos` — `AMP-03`)
- `GET /api/v1/me/followed-cases/` — Lista todos los casos seguidos activos del usuario.
- `GET /api/v1/me/followed-cases/{case_id}/` (`MAP-08`) — Devuelve `{"id_caso": "<uuid>", "following": true, "fecha_creacion": "..."}`.
- `PUT /api/v1/me/followed-cases/{case_id}/` o `POST /api/v1/me/followed-cases/{case_id}/` (`MAP-09`) — Activa el seguimiento.
- `DELETE /api/v1/me/followed-cases/{case_id}/` (`MAP-10`) — Desactiva el seguimiento (`activo = false`, registra `fecha_baja`).

---

## 7. Radicación y Portal Ciudadano (`/api/v1/me/` y `/api/v1/citizen/`)

### `CIT-01` · Dashboard Ciudadano
- **Rutas:** `GET /api/v1/me/dashboard/` y `GET /api/v1/citizen/dashboard/`
- **Response (`200 OK`):**
  ```json
  {
    "mis_casos_total": 3,
    "casos_seguidos_total": 2,
    "correcciones_pendientes": 1,
    "notificaciones_no_leidas": 4,
    "mensajes_no_leidos": 1,
    "casos_por_estado": [
      {"estado__nombre": "pendiente", "total": 1},
      {"estado__nombre": "en_proceso", "total": 1},
      {"estado__nombre": "resuelto", "total": 1}
    ],
    "casos_recientes": [ ... ]
  }
  ```

### `CIT-02`, `CIT-03` y `CIT-04` · Listar, Radicar y Consultar Mis Casos
- **Listar mis casos (`CIT-02`):** `GET /api/v1/me/cases/` (alias `/api/v1/citizen/cases/`).
- **Radicar caso (`CIT-03`):** `POST /api/v1/me/cases/` (alias `/api/v1/citizen/cases/`).
  - **Formatos:** `application/json` o `multipart/form-data` (adjuntando archivos iniciales en `files` o `archivos`).
  - **Request Payload (con UUIDs de catálogos):**
    ```json
    {
      "titulo": "Deterioro de puente peatonal veredal",
      "descripcion": "El puente presenta daños estructurales desde la temporada de lluvias...",
      "id_tipo_caso": "b10e8400-e29b-41d4-a716-446655440000",
      "id_comunidad": "660e8400-e29b-41d4-a716-446655440000",
      "prioridad": "alta",
      "direccion_referencia": "Km 4 vía a la escuela rural",
      "latitud": 6.3421,
      "longitud": -75.6912,
      "familias_afectadas": 35,
      "meses_afectacion": 4,
      "acepta_tratamiento_datos": true
    }
    ```
  - **Response (`201 Created` — `CitizenCaseCreateUpdateSerializer`):** Devuelve el caso con `id_caso` (UUID), `codigo` (`PLUS-2026-00002`), `estado_nombre: "pendiente"`, `estado_publicacion: "pendiente"`, `active_assignment`, `active_correction_request`, `solicitudes_correccion`, `aportes`, `seguimientos`, `evidencias` y `allowed_actions`.
- **Detalle de mi caso (`CIT-04`):** `GET /api/v1/me/cases/{id}/` (acepta UUID o código `PLUS-2026-XXXXX`).

### `CIT-05`, `CIT-06` y `CIT-07` · Historial, Evidencias y Descarga Privada
- **Historial ciudadano (`CIT-05`):** `GET /api/v1/me/cases/{id}/history/` *(Alias: `/timeline/`)*
  - Devuelve `{case_id, codigo, timeline, seguimientos, historial_estados, solicitudes_correccion, aportes}`. Excluye cualquier seguimiento con `audiencia = 'interno'`.
- **Listar y subir evidencias (`CIT-06`):** `GET / POST /api/v1/me/cases/{id}/evidence/`
  - Subida `multipart/form-data` con archivo en `file` o `archivo` y `descripcion` opcional.
  - **Response (`201 Created` — `CaseEvidenceSerializer`):**
    ```json
    {
      "id": "e90e8400-e29b-41d4-a716-446655440000",
      "id_evidencia": "e90e8400-e29b-41d4-a716-446655440000",
      "caso": "880e8400-e29b-41d4-a716-446655440000",
      "usuario": "550e8400-e29b-41d4-a716-446655440000",
      "usuario_nombre": "María Fernanda López Gómez",
      "id_aporte": null,
      "tipo_archivo": "documento",
      "ruta_archivo": "cases/evidence/4f8a9c_acta_comunidad.pdf",
      "download_url": "/api/v1/me/cases/880e8400-e29b-41d4-a716-446655440000/evidence/e90e8400-e29b-41d4-a716-446655440000/download/",
      "descripcion": "Acta firmada por la junta",
      "audiencia": "ciudadano",
      "estado_revision": "pendiente",
      "nombre_original": "acta_comunidad.pdf",
      "mime_type": "application/pdf",
      "tamano_bytes": 245120,
      "fecha_subida": "2026-11-09T02:10:00Z"
    }
    ```
- **Descarga protegida (`CIT-07`):** `GET /api/v1/me/cases/{id}/evidence/{evidence_id}/download/?download=1`
  - Verifica que el usuario sea propietario del caso (o equipo autorizado) y transmite el archivo binario con `Content-Disposition: attachment`.

### `CIT-08` · Aportes Ciudadanos y Respuesta a Solicitudes de Corrección (`aportes_caso` — `AMP-07`)
- **Ruta:** `POST /api/v1/me/cases/{id}/contributions/` *(También `GET` para listar los aportes del caso)*
- **Persistencia real (`AMP-07`):** Crea un registro en la tabla `plus.aportes_caso` con su propio **`id_aporte` (UUID)**, vincula los archivos adjuntos (`files`/`archivos`) a `evidencias.id_aporte`, registra el evento en `seguimientos` con `audiencia = 'ciudadano'` y, si se envía `id_solicitud_correccion` (UUID), actualiza la solicitud a `estado = 'respondida'` (sin cerrarla automáticamente hasta revisión del equipo, conforme a la regla `18.2` de `endpoints.md`).
- **Request (`application/json` o `multipart/form-data`):**
  ```json
  {
    "contenido": "Adjunto coordenadas precisas y copia legible del oficio radicado.",
    "id_solicitud_correccion": "c40e8400-e29b-41d4-a716-446655440000"
  }
  ```
- **Response (`201 Created` — `CaseContributionSerializer`):**
  ```json
  {
    "id": "a70e8400-e29b-41d4-a716-446655440000",
    "id_aporte": "a70e8400-e29b-41d4-a716-446655440000",
    "caso": "880e8400-e29b-41d4-a716-446655440000",
    "usuario": "550e8400-e29b-41d4-a716-446655440000",
    "autor_nombre": "María Fernanda López Gómez",
    "id_solicitud_correccion": "c40e8400-e29b-41d4-a716-446655440000",
    "contenido": "Adjunto coordenadas precisas y copia legible del oficio radicado.",
    "evidencias": [ ... ],
    "fecha_creacion": "2026-11-09T02:15:00Z"
  }
  ```

---

## 8. Mensajería Privada y Notificaciones

### `MSG-01` · Bandeja de Conversaciones
- **Ruta:** `GET /api/v1/me/conversations/`
- **Response (`200 OK`):** Arreglo de conversaciones agrupadas por caso y contraparte (`id_caso`, `caso_codigo`, `caso_titulo`, `counterpart: {id_usuario, nombre, rol}`, `last_message: {id_mensaje, contenido, fecha_envio, remitente}`, `unread_count`).

### `MSG-02` y `MSG-03` · Listar y Enviar Mensajes Privados de un Caso
- **Rutas:** `GET / POST /api/v1/cases/{case_id}/messages/` *(Aliases: `/api/v1/citizen/cases/{case_id}/messages/` y `/api/v1/admin/cases/{case_id}/messages/`)*
- **Filtros en `GET` (`MSG-02`):** `?counterpart=<uuid>` (filtra por participante cuando un miembro del equipo consulta hilos).
- **Estructura de respuesta en `GET` (`CaseMessageSerializer`):** Devuelve lista ordenada cronológicamente (`fecha_envio ASC`):
  ```json
  [
    {
      "id": "990e8400-e29b-41d4-a716-446655440000",
      "id_mensaje": "990e8400-e29b-41d4-a716-446655440000",
      "caso": "880e8400-e29b-41d4-a716-446655440000",
      "remitente": "c1a9f2d0-1234-4bcd-8ef0-112233445566",
      "remitente_nombre": "Coordinador Territorial",
      "destinatario": "550e8400-e29b-41d4-a716-446655440000",
      "destinatario_nombre": "María Fernanda López Gómez",
      "contenido": "Hemos programado visita para el jueves.",
      "content": "Hemos programado visita para el jueves.",
      "fecha_envio": "2026-11-08T18:10:00Z",
      "fecha_lectura": null
    }
  ]
  ```
- **Enviar mensaje (`MSG-03` — `POST`):**
  - **Request JSON:** `{"contenido": "Muchas gracias, estaremos atentos."}` (el servidor resuelve automáticamente el destinatario: si escribe el ciudadano, va al responsable activo del caso o al moderador/administrador de guardia; si escribe el equipo, va al ciudadano propietario o al `destinatario` UUID indicado).

### `MSG-04` · Marcar Mensajes como Leídos (con soporte de corte)
- **Rutas:** `PUT /api/v1/cases/{case_id}/messages/read/` o `POST /api/v1/cases/{case_id}/messages/read/` *(Alias: `/mark-read/`)*
- **Request JSON (todos los campos son opcionales; permiten evitar marcar mensajes que llegaron después de abrir la conversación):**
  ```json
  {
    "message_ids": ["990e8400-e29b-41d4-a716-446655440000"],
    "up_to_message_id": "990e8400-e29b-41d4-a716-446655440000",
    "up_to_timestamp": "2026-11-08T18:15:00Z"
  }
  ```
  - Si se envía `message_ids` (o `ids`), solo marca esos UUID.
  - Si se envía `up_to_message_id` (o `hasta_id_mensaje`), marca los no leídos hasta la `fecha_envio` de ese mensaje inclusive.
  - Si se envía `up_to_timestamp` (o `hasta_fecha`), marca los no leídos con `fecha_envio <= up_to_timestamp`.
- **Response (`200 OK`):** `{"marked_read": 1, "unread_remaining": 0}`.

### `NOT-01`, `NOT-02` y `NOT-03` · Notificaciones (`/api/v1/me/notifications/`)
- `GET /api/v1/me/notifications/` (`NOT-01`) — Filtros: `?unread=true`.
- `PATCH /api/v1/me/notifications/{id}/` (`NOT-02`) — Request: `{"leida": true}`.
- `POST /api/v1/me/notifications/mark-read/` (`NOT-03`) — Request opcional: `{"ids": ["<uuid>", ...]}` (si no se envían `ids`, marca todas las actuales como leídas). Responde `{"marked_read": 3, "unread_remaining": 0}`.

---

## 9. Gestión Administrativa de Casos (`/api/v1/admin/`)

### `ADM-01` · Dashboard Administrativo
- **Rutas:** `GET /api/v1/admin/dashboard/` y `GET /api/v1/admin/metrics/dashboard/`
- **Response (`200 OK`):**
  ```json
  {
    "casos": {
      "total": 25,
      "pendientes_moderacion": 3,
      "aprobados": 18,
      "rechazados": 4,
      "por_estado": [{"estado__nombre": "pendiente", "total": 5}, ...],
      "por_prioridad": [{"prioridad": "alta", "total": 8}, ...]
    },
    "iniciativas": {
      "total": 4,
      "publicadas": 3,
      "destacadas": 2
    },
    "participacion": {
      "propuestas_pendientes": 2,
      "comentarios_pendientes": 1
    }
  }
  ```

### `ADM-02`, `ADM-03`, `ADM-04`, `ADM-05`, `ADM-06` y `ADM-11` · Bandeja, Detalle, Historial y Evidencias
- **Bandeja administrativa (`ADM-02`):** `GET /api/v1/admin/cases/`
  - **Filtros Query:** `?q=` / `?search=`, `?id_estado=` / `?estado=` (`pendiente`, `en_revision`, `en_proceso`, `resuelto`, `cerrado`), `?estado_publicacion=` (`pendiente`, `aprobado`, `rechazado`), `?prioridad=` (`baja`, `media`, `alta`, `critica`), `?id_tipo_caso=`, `?categoria=`, `?naturaleza=`, `?id_comunidad=`, `?id_municipio=`, `?id_departamento=`, `?id_responsable=`, `?fecha_desde=`, `?fecha_hasta=`.
- **Detalle administrativo (`ADM-03`):** `GET /api/v1/admin/cases/{id}/` (UUID o código `PLUS-2026-XXXXX`).
  - Devuelve `AdminCaseDetailSerializer` con todos los datos del solicitante (`usuario_nombre`, `usuario_correo`, `usuario_telefono`), `ubicacion` exacta, `active_assignment`, `active_correction_request`, `solicitudes_correccion`, `aportes`, `asignaciones`, `seguimientos` (incluyendo `audiencia = 'interno'`), `historial_estados`, `evidencias` y `allowed_actions`.
- **Historial administrativo (`ADM-04`):** `GET /api/v1/admin/cases/{id}/history/` (alias `/timeline/`).
- **Evidencias del caso (`ADM-05` y `ADM-06`):**
  - `GET / POST /api/v1/admin/cases/{id}/evidence/`
  - `GET /api/v1/admin/cases/{id}/evidence/{evidence_id}/download/?download=1`
- **Actualizar audiencia y revisión de una evidencia (`ADM-11` — `AMP-10`):**
  - **Ruta:** `PATCH /api/v1/admin/cases/{id}/evidence/{evidence_id}/`
  - **Request JSON (`CaseEvidenceUpdateSerializer`):**
    ```json
    {
      "descripcion": "Fotografía verificada en campo",
      "audiencia": "publico",
      "estado_revision": "aprobada"
    }
    ```
    - `audiencia`: `publico`, `ciudadano`, `privado`.
    - `estado_revision`: `pendiente`, `aprobada`, `rechazada`.

### `ADM-07` · Moderación de Publicación y Solicitud de Correcciones (`AMP-06`)
- **Moderar publicación (`POST /api/v1/admin/cases/{id}/moderation/`, alias `/moderate/`):**
  - **Request JSON (`CaseModerationActionSerializer`):**
    ```json
    {
      "estado_publicacion": "aprobado",
      "prioridad": "alta",
      "solicitar_correccion": false,
      "motivo": "Información corroborada con la junta comunal."
    }
    ```
    - `estado_publicacion`: `pendiente`, `aprobado`, `rechazado`. (Al pasar a `aprobado`, el servidor fija automáticamente `fecha_aprobacion`).
    - Si `solicitar_correccion: true`, crea además un registro formal en `solicitudes_correccion` (`AMP-06`) con `estado = 'abierta'`.
- **Solicitar correcciones directamente (`POST /api/v1/admin/cases/{id}/correction-requests/`):**
  - **Request JSON (`CaseCorrectionRequestCreateSerializer`):**
    ```json
    {
      "motivo": "Por favor adjunte fotografía legible del acta y confirme la vereda.",
      "campos_solicitados": ["evidencias", "id_comunidad"]
    }
    ```

### `ADM-08` · Asignar Responsable al Caso (`asignaciones_casos`)
- **Rutas:** `POST /api/v1/admin/cases/{id}/assignments/` *(Alias: `POST /api/v1/admin/cases/{id}/assign/`)*
- **Request JSON (`CaseAssignResponsibleSerializer`):**
  ```json
  {
    "id_responsable": "c1a9f2d0-1234-4bcd-8ef0-112233445566",
    "motivo": "Asignado al representante territorial del municipio."
  }
  ```
- **Efecto:** Valida elegibilidad del responsable (`asignaciones_responsables` y estado `activo`), desactiva en transacción la asignación activa anterior (`ux_asignacion_caso_activa`) e inserta la nueva.

### `ADM-09` · Registrar Avance / Seguimiento (`seguimientos` — `AMP-08`)
- **Rutas:** `POST /api/v1/admin/cases/{id}/progress/` *(Alias: `POST /api/v1/admin/cases/{id}/updates/`)*
- **Request JSON (`CaseUpdateCreateSerializer`):**
  ```json
  {
    "titulo": "Mesa técnica realizada con acueducto veredal",
    "descripcion": "Se concertó plan de obra para la primera semana del mes.",
    "audiencia": "ciudadano",
    "visible_publicamente": false,
    "tipo_evento": "seguimiento",
    "estado": "en_proceso"
  }
  ```
  - `audiencia`: `publico` (fuerza `visible_publicamente = true`), `ciudadano` (visible para denunciante y equipo, `visible_publicamente = false`), `interno` (nota privada exclusiva del equipo, nunca expuesta al ciudadano ni al público).
  - `tipo_evento`: `seguimiento`, `solicitud_correccion`, `aporte_ciudadano`, `resolucion`, `nota_interna`.
  - `estado` / `id_estado` (opcional): Si se envía (`pendiente`, `en_revision`, `en_proceso`, `resuelto`, `cerrado` o su UUID), actualiza el estado operativo del caso en la misma transacción.

### `ADM-10` · Resolver o Cerrar Caso (`AMP-11`)
- **Rutas:** `POST /api/v1/admin/cases/{id}/resolution/` *(Aliases: `/resolve/`, `/status/`)*
- **Request JSON (`CaseManagementStatusSerializer`):**
  ```json
  {
    "estado": "resuelto",
    "titulo": "Resolución favorable del caso",
    "descripcion": "Se completó la rehabilitación del paso peatonal.",
    "resultado_resumen": "Obra entregada y acta de cierre firmada con la comunidad.",
    "motivo": "Cumplimiento total de los compromisos técnicos."
  }
  ```
  - `estado` / `id_estado`: `resuelto` o `cerrado` (o su UUID en `estados_caso`).
  - **Efecto (`AMP-11`):** Crea el seguimiento con `tipo_evento = 'resolucion'`, persiste `resultado_resumen`, `id_seguimiento_resolucion`, `id_usuario_resolucion` y `fecha_resolucion` en `plus.casos`, y actualiza el estado operativo.

### Moderación de Comentarios Públicos
- **Rutas:**
  - `GET /api/v1/admin/comments/` *(Alias: `/api/v1/admin/case-comments/`)* — Filtros: `?estado_moderacion=pendiente`, `?caso=<uuid>`.
  - `POST /api/v1/admin/comments/{id}/moderation/` *(Aliases: `/api/v1/admin/comments/{id}/moderate/`, `/api/v1/admin/case-comments/{id}/moderation/`)*
- **Request JSON (`CommentModerationActionSerializer`):**
  ```json
  {
    "estado_moderacion": "rechazado",
    "motivo": "Nota interna de moderación: contiene datos de terceros.",
    "notificar_motivo": false
  }
  ```
  - `estado_moderacion`: Acepta **`pendiente`**, **`aprobado`**, **`rechazado`** u **`oculto`**.
  - **Comportamiento de `motivo` (aclaración para el frontend):** El campo `motivo` (o `nota_interna`) se guarda **siempre como nota interna en `auditoria_eventos` (`datos_nuevos.motivo`)** y **NO se incluye en la notificación enviada al ciudadano** a menos que el moderador envíe explícitamente `"notificar_motivo": true`.

---

## 10. Informes, Auditoría y Usuarios (`/api/v1/admin/`)

### `REP-01` y `REP-02` · Informes de Casos y Exportación CSV
- **Informe JSON con agregados y filas paginadas (`REP-01`):** `GET /api/v1/admin/reports/cases/`
  - **Filtros Query:** Acepta exactamente los mismos filtros de `ADM-02` (`?estado=`, `?estado_publicacion=`, `?prioridad=`, `?id_tipo_caso=`, `?categoria=`, `?naturaleza=`, `?id_comunidad=`, `?id_municipio=`, `?id_departamento=`, `?id_responsable=`, `?fecha_desde=`, `?fecha_hasta=`, `?q=`, `?page=`, `?page_size=`).
  - **Response (`200 OK`):**
    ```json
    {
      "summary": {
        "total_seleccion": 15,
        "por_estado": [{"estado__nombre": "en_proceso", "total": 8}, ...],
        "por_publicacion": [{"estado_publicacion": "aprobado", "total": 10}, ...],
        "por_prioridad": [{"prioridad": "alta", "total": 6}, ...],
        "por_categoria": [{"tipo_caso__categoria": "ambiental", "total": 9}, ...],
        "por_naturaleza": [{"tipo_caso__naturaleza": "problematica", "total": 12}, ...],
        "por_departamento": [{"comunidad__municipio__departamento__nombre": "Antioquia", "total": 15}]
      },
      "count": 15,
      "page": 1,
      "page_size": 20,
      "results": [ ... ]
    }
    ```
- **Exportar selección completa en CSV (`REP-02`):** `GET /api/v1/admin/reports/cases/export/`
  - Aplica los mismos filtros sobre toda la selección autorizada y sanitiza celdas que comiencen con `=`, `+`, `-`, `@`.

### `AUD-01` y `AUD-02` · Auditoría Unificada (`5 tablas inmutables`)
- **Listado unificado (`AUD-01`):** `GET /api/v1/admin/audit-events/` *(Alias: `/api/v1/admin/audit/events/`)*
  - **Filtros Query:**
    - `?source=` (`eventos`, `accesos`, `casos`, `permisos`, `seguridad`)
    - `?action=` / `?accion=` (`insert`, `update`, `delete`, `login`, `logout`, `cambio_rol`, etc.)
    - `?actor=<uuid>` (UUID del usuario actor)
    - `?module=` / `?entidad=` (`casos`, `usuarios`, `comentarios`, etc.)
    - `?case_id=<uuid>` (filtra eventos de un caso específico)
    - `?resultado=` (`exitoso`, `fallido`)
    - `?fecha_desde=YYYY-MM-DD`, `?fecha_hasta=YYYY-MM-DD`
    - `?page=`, `?page_size=`
  - **Response (`200 OK`):**
    ```json
    {
      "count": 48,
      "page": 1,
      "page_size": 25,
      "results": [
        {
          "event_ref": "casos:f10e8400-e29b-41d4-a716-446655440000",
          "source": "casos",
          "id": "f10e8400-e29b-41d4-a716-446655440000",
          "accion": "moderacion_aprobado",
          "entidad": "casos",
          "id_registro": "880e8400-e29b-41d4-a716-446655440000",
          "caso_codigo": "PLUS-2026-00001",
          "actor_id": "c1a9f2d0-1234-4bcd-8ef0-112233445566",
          "actor_nombre": "Administrador PLUS",
          "resultado": "exitoso",
          "resumen": "Caso PLUS-2026-00001: moderacion_aprobado (pendiente -> aprobado)",
          "fecha_evento": "2026-11-08T15:30:00Z"
        }
      ]
    }
    ```
- **Detalle de evento (`AUD-02`):** `GET /api/v1/admin/audit-events/{event_ref}/`
  - `{event_ref}` usa el formato `<source>:<uuid>` devuelto en el listado (ej. `casos:f10e8400-...`, `eventos:a10e8400-...`, `accesos:...`, `permisos:...`, `seguridad:...`) o directamente el `<uuid>`.

### `USR-01` a `USR-07` · Usuarios, Rol Único, Estado y Ámbitos
- **Listar usuarios (`USR-01`):** `GET /api/v1/admin/users/`
  - **Filtros Query:**
    - `?search=` (nombres, apellidos, correo, teléfono)
    - `?id_rol=<uuid>` o `?rol=` (`administrador`, `representante`, `moderador`, `ciudadano`)
    - `?estado=` (`activo`, `suspendido`, `inactivo`)
    - `?eligible_for_case=<uuid_caso>` (filtra usuarios activos elegibles para ser asignados a ese caso según su rol o sus ámbitos en `asignaciones_responsables`).
- **Crear usuario (`USR-02`):** `POST /api/v1/admin/users/`
  - **Request JSON:**
    ```json
    {
      "nombres": "Laura",
      "apellidos": "Martínez",
      "correo": "laura.martinez@plus.org",
      "telefono": "3015556677",
      "password": "PasswordInicial123!",
      "id_rol": "120e8400-e29b-41d4-a716-446655440000",
      "rol_nombre": "moderador",
      "estado": "activo"
    }
    ```
    *(Acepta `id_rol` UUID o `rol_nombre` con uno de los 4 roles oficiales).*
- **Detalle y edición (`USR-03`, `USR-04`):** `GET / PATCH / PUT /api/v1/admin/users/{id}/`
- **Cambio de rol único (`USR-05`):** `PUT /api/v1/admin/users/{id}/role/` *(Alias: `POST /api/v1/admin/users/{id}/role/`)*
  - **Request JSON (`AssignUserRoleSerializer`):**
    ```json
    {
      "id_rol": "130e8400-e29b-41d4-a716-446655440000",
      "role_code": "representante",
      "motivo": "Designación como representante territorial",
      "id_comunidad": "660e8400-e29b-41d4-a716-446655440000",
      "id_tipo_caso": null
    }
    ```
    *(Puede enviarse `id_rol` UUID o `role_code`/`rol` textual. Actualiza `usuarios.id_rol` y registra el cambio en `auditoria_permisos`).*
- **Cambio de estado (`USR-06`):** `PATCH /api/v1/admin/users/{id}/status/`
  - **Request JSON (`AdminUserStatusSerializer`):**
    ```json
    {
      "estado": "suspendido",
      "motivo": "Suspensión preventiva de cuenta"
    }
    ```
    - `estado`: `activo`, `suspendido`, `inactivo`. (Si pasa a `suspendido` o `inactivo`, revoca las sesiones activas del usuario inmediatamente).
- **Catálogo de roles (`USR-07`):** `GET /api/v1/admin/roles/`
  - Devuelve las filas reales de `plus.roles`: `id` (UUID), `id_rol` (UUID), `nombre` (`administrador`, `representante`, `moderador`, `ciudadano`), `descripcion` y `assignable` (`bool`).
- **Ámbitos de responsables (`asignaciones_responsables`):** CRUD en `/api/v1/admin/scope-assignments/` (`id_asignacion` UUID, `usuario` UUID, `comunidad` UUID opcional, `tipo_caso` UUID opcional, `activo`).

---

## 11. CRUDs Administrativos Complementarios (`/api/v1/admin/`)

Todos los recursos siguientes soportan `GET`, `POST`, `GET /{id}/`, `PUT /{id}/`, `PATCH /{id}/` y `DELETE /{id}/` con clave primaria **UUID**:

| Recurso | Ruta Base | Serializador / Campos principales |
|---|---|---|
| **Departamentos** | `/api/v1/admin/departments/` | `DepartmentSerializer` (`id_departamento` UUID, `codigo_dane` 2 dígitos, `nombre`). |
| **Municipios** | `/api/v1/admin/municipalities/` | `MunicipalitySerializer` (`id_municipio` UUID, `departamento` UUID, `codigo_dane` 5 dígitos, `nombre`). |
| **Comunidades** | `/api/v1/admin/communities/` | `CommunitySerializer` (`id_comunidad` UUID, `municipio` UUID, `nombre`, `tipo`: `barrio`/`vereda`/`corregimiento`/`comuna`/`sector`/`otro`, `ubicacion`, `activo`). |
| **Tipos de Caso** | `/api/v1/admin/case-categories/` | `CaseCategorySerializer` (`id_tipo_caso` UUID, `nombre`, `descripcion`, `categoria`, `naturaleza`: `problematica`/`proyecto_iniciativa`/`otro`, `activo`). |
| **Propuestas de Iniciativas** | `/api/v1/admin/event-proposals/` *(Alias: `/api/v1/admin/proposals/`)* | `AdminEventProposalSerializer` (`id_propuesta` UUID, `titulo`, `descripcion`, `estado`: `pendiente`/`en_revision`/`aprobada`/`rechazada`, `respuesta`, `iniciativa_generada` UUID). |
| **Iniciativas (Programas)** | `/api/v1/admin/initiatives/` | `AdminInitiativeSerializer` (`id_iniciativa` UUID, `slug`, `titulo`, `subtitulo`, `descripcion_corta`, `descripcion`, `categoria`, `estado`: `borrador`/`publicada`/`archivada`, `destacada`). |
| **Ediciones de Iniciativas** | `/api/v1/admin/initiative-editions/` | `InitiativeEditionSerializer` (`id_edicion` UUID, `iniciativa` UUID, `anio` 2000..2200, `nombre_edicion`, `temporada`, `resumen`, `resultados`, `fecha_inicio`, `fecha_fin`, `estado`). |
| **Actividades de Edición** | `/api/v1/admin/initiative-activities/` | `InitiativeActivitySerializer` (`id_actividad` UUID, `edicion` UUID, `comunidad` UUID, `titulo`, `descripcion`, `tipo_actividad`, `lugar`, `fecha_inicio`, `fecha_fin`, `estado`). |
| **Comunidades por Edición** | `/api/v1/admin/initiative-communities/` | `InitiativeCommunitySerializer` (`id_iniciativa_comunidad` UUID, `edicion` UUID, `comunidad` UUID, `rol_participacion`, `notas`). |
| **Casos por Edición** | `/api/v1/admin/initiative-case-links/` | `InitiativeCaseLinkSerializer` (`id_iniciativa_caso` UUID, `edicion` UUID, `caso` UUID, `tipo_relacion`: `hallazgo`/`seguimiento`/`resultado`/`otro`, `notas`). |
| **Multimedia de Iniciativas** | `/api/v1/admin/initiative-media/` | `InitiativeMediaSerializer` (`id_multimedia` UUID, `iniciativa` UUID, `edicion` UUID nullable, `tipo`, `ruta_archivo`, `es_portada`, `orden`). |
| **Indicadores de Edición** | `/api/v1/admin/initiative-metrics/` | `InitiativeMetricSerializer` (`id_indicador` UUID, `edicion` UUID, `codigo_indicador`, `nombre_indicador`, `valor`, `unidad`, `tipo_medicion`: `estimado`/`real`, `fecha_corte`). |
| **Categorías de Noticias** | `/api/v1/admin/news-categories/` | `NewsCategorySerializer` (`id_categoria` UUID, `nombre`, `slug`, `descripcion`, `activa`). |
| **Noticias Institucionales** | `/api/v1/admin/news/` | `AdminNewsArticleSerializer` (`id_noticia` UUID, `categoria` UUID, `slug`, `titulo`, `subtitulo`, `extracto`, `contenido`, `estado`: `borrador`/`publicada`/`archivada`, `destacada`). |
| **Multimedia de Noticias** | `/api/v1/admin/news-media/` | `NewsMediaSerializer` (`id_multimedia` UUID, `noticia` UUID, `tipo`: `imagen`/`documento`, `ruta_archivo`, `es_portada`, `orden`). |
| **Configuración Plataforma** | `/api/v1/admin/settings/` | `SiteSettingSerializer` (`id_configuracion` UUID, `clave`, `valor` JSONB, `fecha_actualizacion`). |
