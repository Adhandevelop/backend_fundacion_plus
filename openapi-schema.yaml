openapi: 3.0.3
info:
  title: Plataforma Web PLUS — API REST
  version: 1.2.0
  description: API RESTful para la Corporación Pluralismo Social (PLUS). Incluye gestión
    de casos georreferenciados (PostGIS), iniciativas comunitarias, jornadas, noticias
    institucionales, participación ciudadana y auditoría.
paths:
  /api/administrativos/me/:
    get:
      operationId: administrativos_me_retrieve
      description: GET /api/administrativos/me/
      tags:
      - administrativos
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserMe'
          description: ''
  /api/clientes/me/:
    get:
      operationId: clientes_me_retrieve
      description: GET /api/clientes/me/
      tags:
      - clientes
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserMe'
          description: ''
  /api/login/:
    post:
      operationId: login_create
      description: |-
        AUTH-02: POST /api/v1/auth/login/ (y endpoint legacy /api/login/)
        Registra en plus.auditoria_accesos cada intento exitoso o fallido.
      summary: Inicio de sesión JWT + perfil de usuario (AUTH-02)
      tags:
      - login
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Login'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/Login'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/Login'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AuthSessionResponse'
          description: ''
  /api/v1/admin/audit-events/:
    get:
      operationId: v1_admin_audit_events_retrieve
      description: |-
        AUD-01: GET /api/v1/admin/audit-events/ (y /api/v1/admin/audit/events/)
        Proyección unificada de las 5 tablas de auditoría con referencia `event_ref` (`{source}:{uuid}`).
      summary: Listado unificado de las 5 fuentes de auditoría con KPIs y filtros
        (AUD-01)
      parameters:
      - in: query
        name: action
        schema:
          type: string
        description: Filtrar por tipo de acción
      - in: query
        name: actor
        schema:
          type: string
          format: uuid
        description: Filtrar por UUID de usuario actor
      - in: query
        name: source
        schema:
          type: string
        description: 'Fuente: eventos, accesos, casos, permisos, seguridad'
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminAuditEventListResponse'
          description: ''
  /api/v1/admin/audit-events/{event_ref}/:
    get:
      operationId: v1_admin_audit_events_retrieve_2
      description: |-
        AUD-02: GET /api/v1/admin/audit/events/{event_ref}/
        Soporta referencia `{source}:{uuid}` o búsqueda directa por UUID.
      summary: Detalle de evento de auditoría por referencia {source}:{uuid} o UUID
        (AUD-02)
      parameters:
      - in: path
        name: event_ref
        schema:
          type: string
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AuditLog'
          description: ''
  /api/v1/admin/audit-logs/:
    get:
      operationId: v1_admin_audit_logs_list
      description: |-
        Endpoint administrativo de solo lectura para consultar las 5 tablas de auditoría de `plus`:
        - GET /api/v1/admin/audit-logs/ (auditoria_eventos)
        - GET /api/v1/admin/audit-logs/accesos/ (auditoria_accesos)
        - GET /api/v1/admin/audit-logs/casos/ (auditoria_casos)
        - GET /api/v1/admin/audit-logs/permisos/ (auditoria_permisos)
        - GET /api/v1/admin/audit-logs/seguridad/ (auditoria_seguridad)
      parameters:
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedAuditLogList'
          description: ''
  /api/v1/admin/audit-logs/{id}/:
    get:
      operationId: v1_admin_audit_logs_retrieve
      description: |-
        Endpoint administrativo de solo lectura para consultar las 5 tablas de auditoría de `plus`:
        - GET /api/v1/admin/audit-logs/ (auditoria_eventos)
        - GET /api/v1/admin/audit-logs/accesos/ (auditoria_accesos)
        - GET /api/v1/admin/audit-logs/casos/ (auditoria_casos)
        - GET /api/v1/admin/audit-logs/permisos/ (auditoria_permisos)
        - GET /api/v1/admin/audit-logs/seguridad/ (auditoria_seguridad)
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this audit log.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AuditLog'
          description: ''
  /api/v1/admin/audit-logs/accesos/:
    get:
      operationId: v1_admin_audit_logs_accesos_retrieve
      description: |-
        Endpoint administrativo de solo lectura para consultar las 5 tablas de auditoría de `plus`:
        - GET /api/v1/admin/audit-logs/ (auditoria_eventos)
        - GET /api/v1/admin/audit-logs/accesos/ (auditoria_accesos)
        - GET /api/v1/admin/audit-logs/casos/ (auditoria_casos)
        - GET /api/v1/admin/audit-logs/permisos/ (auditoria_permisos)
        - GET /api/v1/admin/audit-logs/seguridad/ (auditoria_seguridad)
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AuditLog'
          description: ''
  /api/v1/admin/audit-logs/casos/:
    get:
      operationId: v1_admin_audit_logs_casos_retrieve
      description: |-
        Endpoint administrativo de solo lectura para consultar las 5 tablas de auditoría de `plus`:
        - GET /api/v1/admin/audit-logs/ (auditoria_eventos)
        - GET /api/v1/admin/audit-logs/accesos/ (auditoria_accesos)
        - GET /api/v1/admin/audit-logs/casos/ (auditoria_casos)
        - GET /api/v1/admin/audit-logs/permisos/ (auditoria_permisos)
        - GET /api/v1/admin/audit-logs/seguridad/ (auditoria_seguridad)
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AuditLog'
          description: ''
  /api/v1/admin/audit-logs/permisos/:
    get:
      operationId: v1_admin_audit_logs_permisos_retrieve
      description: |-
        Endpoint administrativo de solo lectura para consultar las 5 tablas de auditoría de `plus`:
        - GET /api/v1/admin/audit-logs/ (auditoria_eventos)
        - GET /api/v1/admin/audit-logs/accesos/ (auditoria_accesos)
        - GET /api/v1/admin/audit-logs/casos/ (auditoria_casos)
        - GET /api/v1/admin/audit-logs/permisos/ (auditoria_permisos)
        - GET /api/v1/admin/audit-logs/seguridad/ (auditoria_seguridad)
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AuditLog'
          description: ''
  /api/v1/admin/audit-logs/seguridad/:
    get:
      operationId: v1_admin_audit_logs_seguridad_retrieve
      description: |-
        Endpoint administrativo de solo lectura para consultar las 5 tablas de auditoría de `plus`:
        - GET /api/v1/admin/audit-logs/ (auditoria_eventos)
        - GET /api/v1/admin/audit-logs/accesos/ (auditoria_accesos)
        - GET /api/v1/admin/audit-logs/casos/ (auditoria_casos)
        - GET /api/v1/admin/audit-logs/permisos/ (auditoria_permisos)
        - GET /api/v1/admin/audit-logs/seguridad/ (auditoria_seguridad)
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AuditLog'
          description: ''
  /api/v1/admin/audit/events/:
    get:
      operationId: v1_admin_audit_events_retrieve_3
      description: |-
        AUD-01: GET /api/v1/admin/audit-events/ (y /api/v1/admin/audit/events/)
        Proyección unificada de las 5 tablas de auditoría con referencia `event_ref` (`{source}:{uuid}`).
      summary: Listado unificado de las 5 fuentes de auditoría con KPIs y filtros
        (AUD-01)
      parameters:
      - in: query
        name: action
        schema:
          type: string
        description: Filtrar por tipo de acción
      - in: query
        name: actor
        schema:
          type: string
          format: uuid
        description: Filtrar por UUID de usuario actor
      - in: query
        name: source
        schema:
          type: string
        description: 'Fuente: eventos, accesos, casos, permisos, seguridad'
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminAuditEventListResponse'
          description: ''
  /api/v1/admin/audit/events/{event_ref}/:
    get:
      operationId: v1_admin_audit_events_retrieve_4
      description: |-
        AUD-02: GET /api/v1/admin/audit/events/{event_ref}/
        Soporta referencia `{source}:{uuid}` o búsqueda directa por UUID.
      summary: Detalle de evento de auditoría por referencia {source}:{uuid} o UUID
        (AUD-02)
      parameters:
      - in: path
        name: event_ref
        schema:
          type: string
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AuditLog'
          description: ''
  /api/v1/admin/basins/:
    get:
      operationId: v1_admin_basins_list
      description: CRUD /api/v1/admin/basins/ — Pendiente de fuente oficial AMP-13;
        responde lista vacía controlada.
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Community'
          description: ''
  /api/v1/admin/case-categories/:
    get:
      operationId: v1_admin_case_categories_list
      parameters:
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedCaseCategoryList'
          description: ''
    post:
      operationId: v1_admin_case_categories_create
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CaseCategory'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/CaseCategory'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CaseCategory'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseCategory'
          description: ''
  /api/v1/admin/case-categories/{id}/:
    get:
      operationId: v1_admin_case_categories_retrieve
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this case category.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseCategory'
          description: ''
    put:
      operationId: v1_admin_case_categories_update
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this case category.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CaseCategory'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/CaseCategory'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CaseCategory'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseCategory'
          description: ''
    patch:
      operationId: v1_admin_case_categories_partial_update
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this case category.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedCaseCategory'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedCaseCategory'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedCaseCategory'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseCategory'
          description: ''
    delete:
      operationId: v1_admin_case_categories_destroy
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this case category.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '204':
          description: No response body
  /api/v1/admin/case-comments/:
    get:
      operationId: v1_admin_case_comments_list
      parameters:
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedCaseCommentList'
          description: ''
    post:
      operationId: v1_admin_case_comments_create
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CaseComment'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/CaseComment'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CaseComment'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseComment'
          description: ''
  /api/v1/admin/case-comments/{id}/:
    get:
      operationId: v1_admin_case_comments_retrieve
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this case comment.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseComment'
          description: ''
    delete:
      operationId: v1_admin_case_comments_destroy
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this case comment.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '204':
          description: No response body
  /api/v1/admin/case-comments/{id}/moderate/:
    post:
      operationId: v1_admin_case_comments_moderate_create
      description: Alias compatible con POST /api/v1/admin/comments/{id}/moderate/
      summary: Alias compatible para moderar un comentario
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this case comment.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CommentModerationAction'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/CommentModerationAction'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CommentModerationAction'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseComment'
          description: ''
  /api/v1/admin/case-comments/{id}/moderation/:
    post:
      operationId: v1_admin_case_comments_moderation_create
      description: 'Sección 14: POST /api/v1/admin/comments/{id}/moderation/'
      summary: Aprobar, rechazar u ocultar un comentario y guardar motivo en auditoría
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this case comment.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CommentModerationAction'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/CommentModerationAction'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CommentModerationAction'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseComment'
          description: ''
  /api/v1/admin/cases/:
    get:
      operationId: v1_admin_cases_list
      description: |-
        ADM-02 a ADM-11: Gestión administrativa de casos (`/api/v1/admin/cases/`).
        Soporta lectura tanto por UUID como por código de radicado (`{case_ref}`).
      parameters:
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedAdminCaseDetailList'
          description: ''
    post:
      operationId: v1_admin_cases_create
      description: |-
        ADM-02 a ADM-11: Gestión administrativa de casos (`/api/v1/admin/cases/`).
        Soporta lectura tanto por UUID como por código de radicado (`{case_ref}`).
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AdminCaseDetail'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/AdminCaseDetail'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/AdminCaseDetail'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminCaseDetail'
          description: ''
  /api/v1/admin/cases/{case_id}/messages/:
    get:
      operationId: v1_admin_cases_messages_retrieve
      description: |-
        MSG-02 y MSG-03:
        GET / POST /api/v1/cases/{case_id}/messages/, /api/v1/citizen/cases/{case_id}/messages/ y /api/v1/admin/cases/{case_id}/messages/
        Restringe el acceso estrictamente al ciudadano propietario, al responsable asignado o al administrador.
      parameters:
      - in: path
        name: case_id
        schema:
          type: string
          format: uuid
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseMessage'
          description: ''
    post:
      operationId: v1_admin_cases_messages_create
      description: |-
        MSG-02 y MSG-03:
        GET / POST /api/v1/cases/{case_id}/messages/, /api/v1/citizen/cases/{case_id}/messages/ y /api/v1/admin/cases/{case_id}/messages/
        Restringe el acceso estrictamente al ciudadano propietario, al responsable asignado o al administrador.
      parameters:
      - in: path
        name: case_id
        schema:
          type: string
          format: uuid
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CaseMessage'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/CaseMessage'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CaseMessage'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseMessage'
          description: ''
  /api/v1/admin/cases/{id}/:
    get:
      operationId: v1_admin_cases_retrieve
      description: |-
        ADM-02 a ADM-11: Gestión administrativa de casos (`/api/v1/admin/cases/`).
        Soporta lectura tanto por UUID como por código de radicado (`{case_ref}`).
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminCaseDetail'
          description: ''
    put:
      operationId: v1_admin_cases_update
      description: |-
        ADM-02 a ADM-11: Gestión administrativa de casos (`/api/v1/admin/cases/`).
        Soporta lectura tanto por UUID como por código de radicado (`{case_ref}`).
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AdminCaseDetail'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/AdminCaseDetail'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/AdminCaseDetail'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminCaseDetail'
          description: ''
    patch:
      operationId: v1_admin_cases_partial_update
      description: |-
        ADM-02 a ADM-11: Gestión administrativa de casos (`/api/v1/admin/cases/`).
        Soporta lectura tanto por UUID como por código de radicado (`{case_ref}`).
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedAdminCaseDetail'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedAdminCaseDetail'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedAdminCaseDetail'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminCaseDetail'
          description: ''
    delete:
      operationId: v1_admin_cases_destroy
      description: |-
        ADM-02 a ADM-11: Gestión administrativa de casos (`/api/v1/admin/cases/`).
        Soporta lectura tanto por UUID como por código de radicado (`{case_ref}`).
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '204':
          description: No response body
  /api/v1/admin/cases/{id}/assign/:
    post:
      operationId: v1_admin_cases_assign_create
      description: Alias compatible con POST /api/v1/admin/cases/{case_id}/assign/
      summary: Alias compatible para asignar responsable al caso (ADM-08)
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CaseAssignResponsible'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/CaseAssignResponsible'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CaseAssignResponsible'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminCaseDetail'
          description: ''
  /api/v1/admin/cases/{id}/assignments/:
    post:
      operationId: v1_admin_cases_assignments_create
      description: 'ADM-08: POST /api/v1/admin/cases/{case_id}/assignments/'
      summary: Asignar o reasignar responsable territorial al caso (ADM-08)
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CaseAssignResponsible'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/CaseAssignResponsible'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CaseAssignResponsible'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminCaseDetail'
          description: ''
  /api/v1/admin/cases/{id}/correction-requests/:
    post:
      operationId: v1_admin_cases_correction_requests_create
      description: 'ADM-07: POST /api/v1/admin/cases/{case_id}/correction-requests/'
      summary: Crear solicitud formal de corrección para el ciudadano (ADM-07)
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CaseCorrectionRequestCreate'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/CaseCorrectionRequestCreate'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CaseCorrectionRequestCreate'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseCorrectionRequest'
          description: ''
  /api/v1/admin/cases/{id}/evidence/:
    get:
      operationId: v1_admin_cases_evidence_list
      description: 'ADM-05: GET / POST /api/v1/admin/cases/{case_id}/evidence/'
      summary: Listar o subir evidencias desde el panel administrativo (ADM-05)
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedCaseEvidenceList'
          description: ''
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseEvidence'
          description: ''
    post:
      operationId: v1_admin_cases_evidence_create
      description: 'ADM-05: GET / POST /api/v1/admin/cases/{case_id}/evidence/'
      summary: Listar o subir evidencias desde el panel administrativo (ADM-05)
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CaseEvidence'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/CaseEvidence'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CaseEvidence'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedCaseEvidenceList'
          description: ''
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseEvidence'
          description: ''
  /api/v1/admin/cases/{id}/evidence/{evidence_id}/:
    patch:
      operationId: v1_admin_cases_evidence_partial_update
      description: 'ADM-11 (AMP-10): PATCH /api/v1/admin/cases/{case_id}/evidence/{evidence_id}/'
      summary: Actualizar audiencia, estado de revisión o descripción de evidencia
        (ADM-11)
      parameters:
      - in: path
        name: evidence_id
        schema:
          type: string
        required: true
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedCaseEvidenceUpdate'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedCaseEvidenceUpdate'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedCaseEvidenceUpdate'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseEvidence'
          description: ''
  /api/v1/admin/cases/{id}/evidence/{evidence_id}/download/:
    get:
      operationId: v1_admin_cases_evidence_download_retrieve
      description: 'ADM-06: GET /api/v1/admin/cases/{case_id}/evidence/{evidence_id}/download/'
      summary: Descargar o consultar metadatos protegidos de una evidencia (ADM-06)
      parameters:
      - in: query
        name: download
        schema:
          type: boolean
        description: Si es 1/true, descarga el binario directamente (FileResponse).
      - in: path
        name: evidence_id
        schema:
          type: string
        required: true
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseEvidence'
          description: ''
  /api/v1/admin/cases/{id}/history/:
    get:
      operationId: v1_admin_cases_history_retrieve
      description: 'ADM-04: GET /api/v1/admin/cases/{case_id}/history/'
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminCaseDetail'
          description: ''
  /api/v1/admin/cases/{id}/moderate/:
    post:
      operationId: v1_admin_cases_moderate_create
      description: Alias compatible con POST /api/v1/admin/cases/{case_id}/moderate/
      summary: Alias compatible para moderar publicación de caso (ADM-07)
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CaseModerationAction'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/CaseModerationAction'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CaseModerationAction'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminCaseDetail'
          description: ''
  /api/v1/admin/cases/{id}/moderation/:
    post:
      operationId: v1_admin_cases_moderation_create
      description: 'ADM-07: POST /api/v1/admin/cases/{case_id}/moderation/'
      summary: Aprobar, rechazar o solicitar corrección sobre la publicación de un
        caso (ADM-07)
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CaseModerationAction'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/CaseModerationAction'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CaseModerationAction'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminCaseDetail'
          description: ''
  /api/v1/admin/cases/{id}/progress/:
    post:
      operationId: v1_admin_cases_progress_create
      description: 'ADM-09 (AMP-08): POST /api/v1/admin/cases/{case_id}/progress/'
      summary: Registrar avance o seguimiento con nivel de audiencia (ADM-09)
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CaseUpdateCreate'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/CaseUpdateCreate'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CaseUpdateCreate'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseUpdate'
          description: ''
  /api/v1/admin/cases/{id}/resolution/:
    post:
      operationId: v1_admin_cases_resolution_create
      description: 'ADM-10 (AMP-11): POST /api/v1/admin/cases/{case_id}/resolution/'
      summary: Resolver o cerrar narrativamente un caso y cambiar estado operativo
        (ADM-10)
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CaseManagementStatus'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/CaseManagementStatus'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CaseManagementStatus'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminCaseDetail'
          description: ''
  /api/v1/admin/cases/{id}/resolve/:
    post:
      operationId: v1_admin_cases_resolve_create
      description: Alias compatible con POST /api/v1/admin/cases/{case_id}/resolve/
      summary: Alias compatible para resolver o cerrar un caso (ADM-10)
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CaseManagementStatus'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/CaseManagementStatus'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CaseManagementStatus'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminCaseDetail'
          description: ''
  /api/v1/admin/cases/{id}/status/:
    post:
      operationId: v1_admin_cases_status_create
      description: Alias compatible con POST /api/v1/admin/cases/{case_id}/status/
      summary: Cambiar estado operativo de un caso (ADM-10)
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CaseManagementStatus'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/CaseManagementStatus'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CaseManagementStatus'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminCaseDetail'
          description: ''
  /api/v1/admin/cases/{id}/timeline/:
    get:
      operationId: v1_admin_cases_timeline_retrieve
      description: Alias compatible con GET /api/v1/me/cases/{case_id}/timeline/
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminCaseDetail'
          description: ''
  /api/v1/admin/cases/{id}/updates/:
    post:
      operationId: v1_admin_cases_updates_create
      description: Alias compatible con POST /api/v1/admin/cases/{case_id}/updates/
      summary: Alias compatible para registrar avance o seguimiento (ADM-09)
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CaseUpdateCreate'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/CaseUpdateCreate'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CaseUpdateCreate'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseUpdate'
          description: ''
  /api/v1/admin/comments/:
    get:
      operationId: v1_admin_comments_list
      parameters:
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedCaseCommentList'
          description: ''
    post:
      operationId: v1_admin_comments_create
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CaseComment'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/CaseComment'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CaseComment'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseComment'
          description: ''
  /api/v1/admin/comments/{id}/:
    get:
      operationId: v1_admin_comments_retrieve
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this case comment.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseComment'
          description: ''
    delete:
      operationId: v1_admin_comments_destroy
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this case comment.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '204':
          description: No response body
  /api/v1/admin/comments/{id}/moderate/:
    post:
      operationId: v1_admin_comments_moderate_create
      description: Alias compatible con POST /api/v1/admin/comments/{id}/moderate/
      summary: Alias compatible para moderar un comentario
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this case comment.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CommentModerationAction'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/CommentModerationAction'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CommentModerationAction'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseComment'
          description: ''
  /api/v1/admin/comments/{id}/moderation/:
    post:
      operationId: v1_admin_comments_moderation_create
      description: 'Sección 14: POST /api/v1/admin/comments/{id}/moderation/'
      summary: Aprobar, rechazar u ocultar un comentario y guardar motivo en auditoría
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this case comment.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CommentModerationAction'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/CommentModerationAction'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CommentModerationAction'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseComment'
          description: ''
  /api/v1/admin/communities/:
    get:
      operationId: v1_admin_communities_list
      parameters:
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedCommunityList'
          description: ''
    post:
      operationId: v1_admin_communities_create
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Community'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/Community'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/Community'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Community'
          description: ''
  /api/v1/admin/communities/{id}/:
    get:
      operationId: v1_admin_communities_retrieve
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this community.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Community'
          description: ''
    put:
      operationId: v1_admin_communities_update
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this community.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Community'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/Community'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/Community'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Community'
          description: ''
    patch:
      operationId: v1_admin_communities_partial_update
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this community.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedCommunity'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedCommunity'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedCommunity'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Community'
          description: ''
    delete:
      operationId: v1_admin_communities_destroy
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this community.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '204':
          description: No response body
  /api/v1/admin/dashboard/:
    get:
      operationId: v1_admin_dashboard_retrieve
      description: |-
        ADM-01: GET /api/v1/admin/dashboard/ (y /api/v1/admin/metrics/dashboard/)
        Indicadores operativos del Panel Administrativo desde las tablas de `plus`.
      summary: Indicadores operativos del Dashboard Administrativo (ADM-01)
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminMetricsDashboardResponse'
          description: ''
  /api/v1/admin/departments/:
    get:
      operationId: v1_admin_departments_list
      parameters:
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedDepartmentList'
          description: ''
    post:
      operationId: v1_admin_departments_create
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Department'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/Department'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/Department'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Department'
          description: ''
  /api/v1/admin/departments/{id}/:
    get:
      operationId: v1_admin_departments_retrieve
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this department.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Department'
          description: ''
    put:
      operationId: v1_admin_departments_update
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this department.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Department'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/Department'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/Department'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Department'
          description: ''
    patch:
      operationId: v1_admin_departments_partial_update
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this department.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedDepartment'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedDepartment'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedDepartment'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Department'
          description: ''
    delete:
      operationId: v1_admin_departments_destroy
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this department.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '204':
          description: No response body
  /api/v1/admin/event-proposals/:
    get:
      operationId: v1_admin_event_proposals_list
      description: 'Sección 14: GET / PATCH /api/v1/admin/initiative-proposals/'
      parameters:
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedAdminEventProposalList'
          description: ''
    post:
      operationId: v1_admin_event_proposals_create
      description: 'Sección 14: GET / PATCH /api/v1/admin/initiative-proposals/'
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AdminEventProposal'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/AdminEventProposal'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/AdminEventProposal'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminEventProposal'
          description: ''
  /api/v1/admin/event-proposals/{id}/:
    get:
      operationId: v1_admin_event_proposals_retrieve
      description: 'Sección 14: GET / PATCH /api/v1/admin/initiative-proposals/'
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this event proposal.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminEventProposal'
          description: ''
    put:
      operationId: v1_admin_event_proposals_update
      description: 'Sección 14: GET / PATCH /api/v1/admin/initiative-proposals/'
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this event proposal.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AdminEventProposal'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/AdminEventProposal'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/AdminEventProposal'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminEventProposal'
          description: ''
    patch:
      operationId: v1_admin_event_proposals_partial_update
      description: 'Sección 14: GET / PATCH /api/v1/admin/initiative-proposals/'
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this event proposal.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedAdminEventProposal'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedAdminEventProposal'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedAdminEventProposal'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminEventProposal'
          description: ''
    delete:
      operationId: v1_admin_event_proposals_destroy
      description: 'Sección 14: GET / PATCH /api/v1/admin/initiative-proposals/'
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this event proposal.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '204':
          description: No response body
  /api/v1/admin/evidence/:
    get:
      operationId: v1_admin_evidence_list
      parameters:
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedCaseEvidenceList'
          description: ''
    post:
      operationId: v1_admin_evidence_create
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CaseEvidence'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/CaseEvidence'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CaseEvidence'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseEvidence'
          description: ''
  /api/v1/admin/evidence/{id}/:
    get:
      operationId: v1_admin_evidence_retrieve
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this case evidence.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseEvidence'
          description: ''
    put:
      operationId: v1_admin_evidence_update
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this case evidence.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CaseEvidence'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/CaseEvidence'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CaseEvidence'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseEvidence'
          description: ''
    patch:
      operationId: v1_admin_evidence_partial_update
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this case evidence.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedCaseEvidence'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedCaseEvidence'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedCaseEvidence'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseEvidence'
          description: ''
    delete:
      operationId: v1_admin_evidence_destroy
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this case evidence.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '204':
          description: No response body
  /api/v1/admin/initiative-activities/:
    get:
      operationId: v1_admin_initiative_activities_list
      parameters:
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedInitiativeActivityList'
          description: ''
    post:
      operationId: v1_admin_initiative_activities_create
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/InitiativeActivity'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/InitiativeActivity'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/InitiativeActivity'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InitiativeActivity'
          description: ''
  /api/v1/admin/initiative-activities/{id}/:
    get:
      operationId: v1_admin_initiative_activities_retrieve
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this initiative activity.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InitiativeActivity'
          description: ''
    put:
      operationId: v1_admin_initiative_activities_update
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this initiative activity.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/InitiativeActivity'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/InitiativeActivity'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/InitiativeActivity'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InitiativeActivity'
          description: ''
    patch:
      operationId: v1_admin_initiative_activities_partial_update
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this initiative activity.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedInitiativeActivity'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedInitiativeActivity'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedInitiativeActivity'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InitiativeActivity'
          description: ''
    delete:
      operationId: v1_admin_initiative_activities_destroy
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this initiative activity.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '204':
          description: No response body
  /api/v1/admin/initiative-case-links/:
    get:
      operationId: v1_admin_initiative_case_links_list
      parameters:
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedInitiativeCaseLinkList'
          description: ''
    post:
      operationId: v1_admin_initiative_case_links_create
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/InitiativeCaseLink'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/InitiativeCaseLink'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/InitiativeCaseLink'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InitiativeCaseLink'
          description: ''
  /api/v1/admin/initiative-case-links/{id}/:
    get:
      operationId: v1_admin_initiative_case_links_retrieve
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this initiative case link.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InitiativeCaseLink'
          description: ''
    put:
      operationId: v1_admin_initiative_case_links_update
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this initiative case link.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/InitiativeCaseLink'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/InitiativeCaseLink'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/InitiativeCaseLink'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InitiativeCaseLink'
          description: ''
    patch:
      operationId: v1_admin_initiative_case_links_partial_update
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this initiative case link.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedInitiativeCaseLink'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedInitiativeCaseLink'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedInitiativeCaseLink'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InitiativeCaseLink'
          description: ''
    delete:
      operationId: v1_admin_initiative_case_links_destroy
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this initiative case link.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '204':
          description: No response body
  /api/v1/admin/initiative-communities/:
    get:
      operationId: v1_admin_initiative_communities_list
      parameters:
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedInitiativeCommunityList'
          description: ''
    post:
      operationId: v1_admin_initiative_communities_create
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/InitiativeCommunity'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/InitiativeCommunity'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/InitiativeCommunity'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InitiativeCommunity'
          description: ''
  /api/v1/admin/initiative-communities/{id}/:
    get:
      operationId: v1_admin_initiative_communities_retrieve
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this initiative community.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InitiativeCommunity'
          description: ''
    put:
      operationId: v1_admin_initiative_communities_update
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this initiative community.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/InitiativeCommunity'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/InitiativeCommunity'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/InitiativeCommunity'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InitiativeCommunity'
          description: ''
    patch:
      operationId: v1_admin_initiative_communities_partial_update
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this initiative community.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedInitiativeCommunity'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedInitiativeCommunity'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedInitiativeCommunity'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InitiativeCommunity'
          description: ''
    delete:
      operationId: v1_admin_initiative_communities_destroy
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this initiative community.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '204':
          description: No response body
  /api/v1/admin/initiative-editions/:
    get:
      operationId: v1_admin_initiative_editions_list
      parameters:
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedInitiativeEditionList'
          description: ''
    post:
      operationId: v1_admin_initiative_editions_create
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/InitiativeEdition'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/InitiativeEdition'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/InitiativeEdition'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InitiativeEdition'
          description: ''
  /api/v1/admin/initiative-editions/{id}/:
    get:
      operationId: v1_admin_initiative_editions_retrieve
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this initiative edition.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InitiativeEdition'
          description: ''
    put:
      operationId: v1_admin_initiative_editions_update
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this initiative edition.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/InitiativeEdition'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/InitiativeEdition'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/InitiativeEdition'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InitiativeEdition'
          description: ''
    patch:
      operationId: v1_admin_initiative_editions_partial_update
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this initiative edition.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedInitiativeEdition'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedInitiativeEdition'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedInitiativeEdition'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InitiativeEdition'
          description: ''
    delete:
      operationId: v1_admin_initiative_editions_destroy
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this initiative edition.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '204':
          description: No response body
  /api/v1/admin/initiative-media/:
    get:
      operationId: v1_admin_initiative_media_list
      parameters:
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedInitiativeMediaList'
          description: ''
    post:
      operationId: v1_admin_initiative_media_create
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/InitiativeMedia'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/InitiativeMedia'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/InitiativeMedia'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InitiativeMedia'
          description: ''
  /api/v1/admin/initiative-media/{id}/:
    get:
      operationId: v1_admin_initiative_media_retrieve
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this initiative media.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InitiativeMedia'
          description: ''
    put:
      operationId: v1_admin_initiative_media_update
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this initiative media.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/InitiativeMedia'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/InitiativeMedia'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/InitiativeMedia'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InitiativeMedia'
          description: ''
    patch:
      operationId: v1_admin_initiative_media_partial_update
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this initiative media.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedInitiativeMedia'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedInitiativeMedia'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedInitiativeMedia'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InitiativeMedia'
          description: ''
    delete:
      operationId: v1_admin_initiative_media_destroy
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this initiative media.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '204':
          description: No response body
  /api/v1/admin/initiative-metrics/:
    get:
      operationId: v1_admin_initiative_metrics_list
      parameters:
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedInitiativeMetricList'
          description: ''
    post:
      operationId: v1_admin_initiative_metrics_create
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/InitiativeMetric'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/InitiativeMetric'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/InitiativeMetric'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InitiativeMetric'
          description: ''
  /api/v1/admin/initiative-metrics/{id}/:
    get:
      operationId: v1_admin_initiative_metrics_retrieve
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this initiative metric.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InitiativeMetric'
          description: ''
    put:
      operationId: v1_admin_initiative_metrics_update
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this initiative metric.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/InitiativeMetric'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/InitiativeMetric'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/InitiativeMetric'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InitiativeMetric'
          description: ''
    patch:
      operationId: v1_admin_initiative_metrics_partial_update
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this initiative metric.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedInitiativeMetric'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedInitiativeMetric'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedInitiativeMetric'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InitiativeMetric'
          description: ''
    delete:
      operationId: v1_admin_initiative_metrics_destroy
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this initiative metric.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '204':
          description: No response body
  /api/v1/admin/initiatives/:
    get:
      operationId: v1_admin_initiatives_list
      parameters:
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedAdminInitiativeList'
          description: ''
    post:
      operationId: v1_admin_initiatives_create
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AdminInitiative'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/AdminInitiative'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/AdminInitiative'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminInitiative'
          description: ''
  /api/v1/admin/initiatives/{id}/:
    get:
      operationId: v1_admin_initiatives_retrieve
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this initiative.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminInitiative'
          description: ''
    put:
      operationId: v1_admin_initiatives_update
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this initiative.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AdminInitiative'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/AdminInitiative'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/AdminInitiative'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminInitiative'
          description: ''
    patch:
      operationId: v1_admin_initiatives_partial_update
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this initiative.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedAdminInitiative'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedAdminInitiative'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedAdminInitiative'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminInitiative'
          description: ''
    delete:
      operationId: v1_admin_initiatives_destroy
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this initiative.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '204':
          description: No response body
  /api/v1/admin/metrics/dashboard/:
    get:
      operationId: v1_admin_metrics_dashboard_retrieve
      description: |-
        ADM-01: GET /api/v1/admin/dashboard/ (y /api/v1/admin/metrics/dashboard/)
        Indicadores operativos del Panel Administrativo desde las tablas de `plus`.
      summary: Indicadores operativos del Dashboard Administrativo (ADM-01)
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminMetricsDashboardResponse'
          description: ''
  /api/v1/admin/municipalities/:
    get:
      operationId: v1_admin_municipalities_list
      parameters:
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedMunicipalityList'
          description: ''
    post:
      operationId: v1_admin_municipalities_create
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Municipality'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/Municipality'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/Municipality'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Municipality'
          description: ''
  /api/v1/admin/municipalities/{id}/:
    get:
      operationId: v1_admin_municipalities_retrieve
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this municipality.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Municipality'
          description: ''
    put:
      operationId: v1_admin_municipalities_update
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this municipality.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Municipality'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/Municipality'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/Municipality'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Municipality'
          description: ''
    patch:
      operationId: v1_admin_municipalities_partial_update
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this municipality.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedMunicipality'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedMunicipality'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedMunicipality'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Municipality'
          description: ''
    delete:
      operationId: v1_admin_municipalities_destroy
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this municipality.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '204':
          description: No response body
  /api/v1/admin/news/:
    get:
      operationId: v1_admin_news_list
      parameters:
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedNewsArticleDetailList'
          description: ''
    post:
      operationId: v1_admin_news_create
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/NewsArticleDetail'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/NewsArticleDetail'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/NewsArticleDetail'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/NewsArticleDetail'
          description: ''
  /api/v1/admin/news-categories/:
    get:
      operationId: v1_admin_news_categories_list
      parameters:
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedNewsCategoryList'
          description: ''
    post:
      operationId: v1_admin_news_categories_create
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/NewsCategory'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/NewsCategory'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/NewsCategory'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/NewsCategory'
          description: ''
  /api/v1/admin/news-categories/{id}/:
    get:
      operationId: v1_admin_news_categories_retrieve
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this news category.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/NewsCategory'
          description: ''
    put:
      operationId: v1_admin_news_categories_update
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this news category.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/NewsCategory'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/NewsCategory'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/NewsCategory'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/NewsCategory'
          description: ''
    patch:
      operationId: v1_admin_news_categories_partial_update
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this news category.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedNewsCategory'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedNewsCategory'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedNewsCategory'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/NewsCategory'
          description: ''
    delete:
      operationId: v1_admin_news_categories_destroy
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this news category.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '204':
          description: No response body
  /api/v1/admin/news-media/:
    get:
      operationId: v1_admin_news_media_list
      parameters:
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedNewsMediaList'
          description: ''
    post:
      operationId: v1_admin_news_media_create
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/NewsMedia'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/NewsMedia'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/NewsMedia'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/NewsMedia'
          description: ''
  /api/v1/admin/news-media/{id}/:
    get:
      operationId: v1_admin_news_media_retrieve
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this news media.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/NewsMedia'
          description: ''
    put:
      operationId: v1_admin_news_media_update
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this news media.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/NewsMedia'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/NewsMedia'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/NewsMedia'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/NewsMedia'
          description: ''
    patch:
      operationId: v1_admin_news_media_partial_update
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this news media.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedNewsMedia'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedNewsMedia'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedNewsMedia'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/NewsMedia'
          description: ''
    delete:
      operationId: v1_admin_news_media_destroy
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this news media.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '204':
          description: No response body
  /api/v1/admin/news/{id}/:
    get:
      operationId: v1_admin_news_retrieve
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this news article.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/NewsArticleDetail'
          description: ''
    put:
      operationId: v1_admin_news_update
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this news article.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/NewsArticleDetail'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/NewsArticleDetail'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/NewsArticleDetail'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/NewsArticleDetail'
          description: ''
    patch:
      operationId: v1_admin_news_partial_update
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this news article.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedNewsArticleDetail'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedNewsArticleDetail'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedNewsArticleDetail'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/NewsArticleDetail'
          description: ''
    delete:
      operationId: v1_admin_news_destroy
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this news article.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '204':
          description: No response body
  /api/v1/admin/proposals/:
    get:
      operationId: v1_admin_proposals_list
      description: 'Sección 14: GET / PATCH /api/v1/admin/initiative-proposals/'
      parameters:
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedAdminEventProposalList'
          description: ''
    post:
      operationId: v1_admin_proposals_create
      description: 'Sección 14: GET / PATCH /api/v1/admin/initiative-proposals/'
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AdminEventProposal'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/AdminEventProposal'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/AdminEventProposal'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminEventProposal'
          description: ''
  /api/v1/admin/proposals/{id}/:
    get:
      operationId: v1_admin_proposals_retrieve
      description: 'Sección 14: GET / PATCH /api/v1/admin/initiative-proposals/'
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this event proposal.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminEventProposal'
          description: ''
    put:
      operationId: v1_admin_proposals_update
      description: 'Sección 14: GET / PATCH /api/v1/admin/initiative-proposals/'
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this event proposal.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AdminEventProposal'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/AdminEventProposal'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/AdminEventProposal'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminEventProposal'
          description: ''
    patch:
      operationId: v1_admin_proposals_partial_update
      description: 'Sección 14: GET / PATCH /api/v1/admin/initiative-proposals/'
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this event proposal.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedAdminEventProposal'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedAdminEventProposal'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedAdminEventProposal'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminEventProposal'
          description: ''
    delete:
      operationId: v1_admin_proposals_destroy
      description: 'Sección 14: GET / PATCH /api/v1/admin/initiative-proposals/'
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this event proposal.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '204':
          description: No response body
  /api/v1/admin/reports/cases/:
    get:
      operationId: v1_admin_reports_cases_retrieve
      description: |-
        REP-01: GET /api/v1/admin/reports/cases/
        Retorna agregados de toda la selección autorizada y filas paginadas.
      summary: Informe filtrado de casos con agregados globales y filas paginadas
        (REP-01)
      parameters:
      - in: query
        name: categoria
        schema:
          type: string
        description: Categoría temática textual
      - in: query
        name: estado
        schema:
          type: string
        description: Nombre de estado operativo
      - in: query
        name: estado_publicacion
        schema:
          type: string
        description: pendiente, aprobado, rechazado
      - in: query
        name: id_comunidad
        schema:
          type: string
          format: uuid
        description: UUID de comunidad
      - in: query
        name: id_departamento
        schema:
          type: string
          format: uuid
        description: UUID de departamento
      - in: query
        name: id_estado
        schema:
          type: string
          format: uuid
        description: UUID de estado operativo
      - in: query
        name: id_municipio
        schema:
          type: string
          format: uuid
        description: UUID de municipio
      - in: query
        name: id_responsable
        schema:
          type: string
          format: uuid
        description: UUID de responsable activo
      - in: query
        name: id_tipo_caso
        schema:
          type: string
          format: uuid
        description: UUID de tipo de caso
      - in: query
        name: naturaleza
        schema:
          type: string
        description: problematica, proyecto_iniciativa, otro
      - in: query
        name: page
        schema:
          type: integer
        description: Número de página (1..N)
      - in: query
        name: page_size
        schema:
          type: integer
        description: Tamaño de página (default 20)
      - in: query
        name: prioridad
        schema:
          type: string
        description: baja, media, alta, critica
      - in: query
        name: search
        schema:
          type: string
        description: Búsqueda por código, título o descripción
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminCaseReportResponse'
          description: ''
  /api/v1/admin/reports/cases/export/:
    get:
      operationId: v1_admin_reports_cases_export_retrieve
      description: |-
        REP-02: GET /api/v1/admin/reports/cases/export/
        Exporta en CSV toda la selección autorizada neutralizando fórmulas en celdas de texto.
      summary: Exportación CSV de toda la selección filtrada de casos (REP-02)
      parameters:
      - in: query
        name: categoria
        schema:
          type: string
      - in: query
        name: estado
        schema:
          type: string
      - in: query
        name: estado_publicacion
        schema:
          type: string
      - in: query
        name: id_comunidad
        schema:
          type: string
          format: uuid
      - in: query
        name: id_departamento
        schema:
          type: string
          format: uuid
      - in: query
        name: id_estado
        schema:
          type: string
          format: uuid
      - in: query
        name: id_municipio
        schema:
          type: string
          format: uuid
      - in: query
        name: id_responsable
        schema:
          type: string
          format: uuid
      - in: query
        name: id_tipo_caso
        schema:
          type: string
          format: uuid
      - in: query
        name: naturaleza
        schema:
          type: string
      - in: query
        name: prioridad
        schema:
          type: string
      - in: query
        name: search
        schema:
          type: string
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            text/csv:
              schema:
                type: string
                format: binary
          description: ''
  /api/v1/admin/roles/:
    get:
      operationId: v1_admin_roles_list
      description: 'USR-07: GET /api/v1/admin/roles/'
      parameters:
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedRoleList'
          description: ''
    post:
      operationId: v1_admin_roles_create
      description: 'USR-07: GET /api/v1/admin/roles/'
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Role'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/Role'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/Role'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Role'
          description: ''
  /api/v1/admin/roles/{id}/:
    get:
      operationId: v1_admin_roles_retrieve
      description: 'USR-07: GET /api/v1/admin/roles/'
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this role.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Role'
          description: ''
    put:
      operationId: v1_admin_roles_update
      description: 'USR-07: GET /api/v1/admin/roles/'
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this role.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Role'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/Role'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/Role'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Role'
          description: ''
    patch:
      operationId: v1_admin_roles_partial_update
      description: 'USR-07: GET /api/v1/admin/roles/'
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this role.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedRole'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedRole'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedRole'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Role'
          description: ''
    delete:
      operationId: v1_admin_roles_destroy
      description: 'USR-07: GET /api/v1/admin/roles/'
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this role.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '204':
          description: No response body
  /api/v1/admin/scope-assignments/:
    get:
      operationId: v1_admin_scope_assignments_list
      description: 'Sección 14: GET/POST /api/v1/admin/responsibility-scopes/ y PATCH
        /api/v1/admin/responsibility-scopes/{id}/'
      parameters:
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedResponsibleScopeAssignmentList'
          description: ''
    post:
      operationId: v1_admin_scope_assignments_create
      description: 'Sección 14: GET/POST /api/v1/admin/responsibility-scopes/ y PATCH
        /api/v1/admin/responsibility-scopes/{id}/'
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ResponsibleScopeAssignment'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/ResponsibleScopeAssignment'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/ResponsibleScopeAssignment'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ResponsibleScopeAssignment'
          description: ''
  /api/v1/admin/scope-assignments/{id}/:
    get:
      operationId: v1_admin_scope_assignments_retrieve
      description: 'Sección 14: GET/POST /api/v1/admin/responsibility-scopes/ y PATCH
        /api/v1/admin/responsibility-scopes/{id}/'
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this responsible scope assignment.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ResponsibleScopeAssignment'
          description: ''
    put:
      operationId: v1_admin_scope_assignments_update
      description: 'Sección 14: GET/POST /api/v1/admin/responsibility-scopes/ y PATCH
        /api/v1/admin/responsibility-scopes/{id}/'
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this responsible scope assignment.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ResponsibleScopeAssignment'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/ResponsibleScopeAssignment'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/ResponsibleScopeAssignment'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ResponsibleScopeAssignment'
          description: ''
    patch:
      operationId: v1_admin_scope_assignments_partial_update
      description: 'Sección 14: GET/POST /api/v1/admin/responsibility-scopes/ y PATCH
        /api/v1/admin/responsibility-scopes/{id}/'
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this responsible scope assignment.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedResponsibleScopeAssignment'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedResponsibleScopeAssignment'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedResponsibleScopeAssignment'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ResponsibleScopeAssignment'
          description: ''
    delete:
      operationId: v1_admin_scope_assignments_destroy
      description: 'Sección 14: GET/POST /api/v1/admin/responsibility-scopes/ y PATCH
        /api/v1/admin/responsibility-scopes/{id}/'
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this responsible scope assignment.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '204':
          description: No response body
  /api/v1/admin/settings/:
    get:
      operationId: v1_admin_settings_list
      parameters:
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedSiteSettingList'
          description: ''
    post:
      operationId: v1_admin_settings_create
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/SiteSetting'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/SiteSetting'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/SiteSetting'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SiteSetting'
          description: ''
  /api/v1/admin/settings/{id}/:
    get:
      operationId: v1_admin_settings_retrieve
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this site setting.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SiteSetting'
          description: ''
    put:
      operationId: v1_admin_settings_update
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this site setting.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/SiteSetting'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/SiteSetting'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/SiteSetting'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SiteSetting'
          description: ''
    patch:
      operationId: v1_admin_settings_partial_update
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this site setting.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedSiteSetting'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedSiteSetting'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedSiteSetting'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SiteSetting'
          description: ''
    delete:
      operationId: v1_admin_settings_destroy
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this site setting.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '204':
          description: No response body
  /api/v1/admin/users/:
    get:
      operationId: v1_admin_users_list
      description: 'USR-01 a USR-06: Administración de usuarios (`plus.usuarios`),
        rol único y estado.'
      parameters:
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedAdminUserCreateUpdateList'
          description: ''
    post:
      operationId: v1_admin_users_create
      description: 'USR-01 a USR-06: Administración de usuarios (`plus.usuarios`),
        rol único y estado.'
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AdminUserCreateUpdate'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/AdminUserCreateUpdate'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/AdminUserCreateUpdate'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminUserCreateUpdate'
          description: ''
  /api/v1/admin/users/{id}/:
    get:
      operationId: v1_admin_users_retrieve
      description: 'USR-01 a USR-06: Administración de usuarios (`plus.usuarios`),
        rol único y estado.'
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this user.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminUserCreateUpdate'
          description: ''
    put:
      operationId: v1_admin_users_update
      description: 'USR-01 a USR-06: Administración de usuarios (`plus.usuarios`),
        rol único y estado.'
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this user.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AdminUserCreateUpdate'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/AdminUserCreateUpdate'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/AdminUserCreateUpdate'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminUserCreateUpdate'
          description: ''
    patch:
      operationId: v1_admin_users_partial_update
      description: 'USR-01 a USR-06: Administración de usuarios (`plus.usuarios`),
        rol único y estado.'
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this user.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedAdminUserCreateUpdate'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedAdminUserCreateUpdate'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedAdminUserCreateUpdate'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AdminUserCreateUpdate'
          description: ''
    delete:
      operationId: v1_admin_users_destroy
      description: 'USR-01 a USR-06: Administración de usuarios (`plus.usuarios`),
        rol único y estado.'
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this user.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '204':
          description: No response body
  /api/v1/admin/users/{id}/role/:
    post:
      operationId: v1_admin_users_role_create
      description: 'USR-05: PUT /api/v1/admin/users/{id}/role/ — Asigna un único rol
        al usuario.'
      summary: Asignar rol único al usuario (USR-05)
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this user.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AssignUserRole'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/AssignUserRole'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/AssignUserRole'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserMe'
          description: ''
    put:
      operationId: v1_admin_users_role_update
      description: 'USR-05: PUT /api/v1/admin/users/{id}/role/ — Asigna un único rol
        al usuario.'
      summary: Asignar rol único al usuario (USR-05)
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this user.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AssignUserRole'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/AssignUserRole'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/AssignUserRole'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserMe'
          description: ''
  /api/v1/admin/users/{id}/roles/:
    get:
      operationId: v1_admin_users_roles_retrieve
      description: Compatibilidad con /api/v1/admin/users/{id}/roles/
      summary: Consultar o actualizar rol y ámbitos del usuario
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this user.
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserMe'
          description: ''
    post:
      operationId: v1_admin_users_roles_create
      description: Compatibilidad con /api/v1/admin/users/{id}/roles/
      summary: Consultar o actualizar rol y ámbitos del usuario
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this user.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AssignUserRole'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/AssignUserRole'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/AssignUserRole'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserMe'
          description: ''
    put:
      operationId: v1_admin_users_roles_update
      description: Compatibilidad con /api/v1/admin/users/{id}/roles/
      summary: Consultar o actualizar rol y ámbitos del usuario
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this user.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AssignUserRole'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/AssignUserRole'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/AssignUserRole'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserMe'
          description: ''
  /api/v1/admin/users/{id}/status/:
    patch:
      operationId: v1_admin_users_status_partial_update
      description: 'USR-06: PATCH /api/v1/admin/users/{id}/status/ — Cambia el estado
        (activo, suspendido, inactivo).'
      summary: 'Cambiar estado del usuario: activo, suspendido, inactivo (USR-06)'
      parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
        description: A UUID string identifying this user.
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedAdminUserStatus'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedAdminUserStatus'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedAdminUserStatus'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserMe'
          description: ''
  /api/v1/auth/change-password/:
    post:
      operationId: v1_auth_change_password_create
      description: POST /api/v1/auth/change-password/
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ChangePassword'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/ChangePassword'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/ChangePassword'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ChangePassword'
          description: ''
  /api/v1/auth/login/:
    post:
      operationId: v1_auth_login_create
      description: |-
        AUTH-02: POST /api/v1/auth/login/ (y endpoint legacy /api/login/)
        Registra en plus.auditoria_accesos cada intento exitoso o fallido.
      summary: Inicio de sesión JWT + perfil de usuario (AUTH-02)
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Login'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/Login'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/Login'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AuthSessionResponse'
          description: ''
  /api/v1/auth/logout/:
    post:
      operationId: v1_auth_logout_create
      description: 'AUTH-04: POST /api/v1/auth/logout/ — Cierra sesión, revoca Token
        en servidor e invalida refresh.'
      summary: Cierre de sesión e invalidación de token en servidor (AUTH-04)
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/LogoutRequest'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/LogoutRequest'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/LogoutRequest'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LogoutResponse'
          description: ''
  /api/v1/auth/me/:
    get:
      operationId: v1_auth_me_retrieve
      description: 'ME-01 y ME-02: GET / PATCH /api/v1/me/ (y /api/v1/auth/me/)'
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserMe'
          description: ''
    put:
      operationId: v1_auth_me_update
      description: 'ME-01 y ME-02: GET / PATCH /api/v1/me/ (y /api/v1/auth/me/)'
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserMe'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/UserMe'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/UserMe'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserMe'
          description: ''
    patch:
      operationId: v1_auth_me_partial_update
      description: 'ME-01 y ME-02: GET / PATCH /api/v1/me/ (y /api/v1/auth/me/)'
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedUserMe'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedUserMe'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedUserMe'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserMe'
          description: ''
  /api/v1/auth/password-reset/confirm/:
    post:
      operationId: v1_auth_password_reset_confirm_create
      description: 'AUTH-07: POST /api/v1/auth/password-reset/confirm/'
      summary: Confirmar nueva contraseña, invalidar enlace y revocar sesiones anteriores
        (AUTH-07)
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PasswordResetConfirm'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PasswordResetConfirm'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PasswordResetConfirm'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PasswordResetConfirmResponse'
          description: ''
  /api/v1/auth/password-reset/request/:
    post:
      operationId: v1_auth_password_reset_request_create
      description: 'AUTH-05: POST /api/v1/auth/password-reset/request/'
      summary: Solicitar enlace de recuperación de contraseña por correo (AUTH-05)
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PasswordResetRequest'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PasswordResetRequest'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PasswordResetRequest'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PasswordResetRequestResponse'
          description: ''
  /api/v1/auth/password-reset/validate/:
    post:
      operationId: v1_auth_password_reset_validate_create
      description: 'AUTH-06: POST /api/v1/auth/password-reset/validate/'
      summary: Validar enlace/token de recuperación sin cambiar la contraseña (AUTH-06)
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PasswordResetValidate'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PasswordResetValidate'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PasswordResetValidate'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PasswordResetValidateResponse'
          description: ''
  /api/v1/auth/refresh/:
    post:
      operationId: v1_auth_refresh_create
      description: |-
        AUTH-03: POST /api/v1/auth/refresh/
        Renueva el JWT validando que la cuenta siga en estado 'activo' y que la sesión ('sid')
        no haya sido cerrada mediante `/auth/logout/` ni revocada por cambio de contraseña/suspensión.
      summary: Renovar token JWT verificando estado de cuenta y sesión activa (AUTH-03)
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TokenRefreshRequest'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/TokenRefreshRequest'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/TokenRefreshRequest'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TokenRefreshResponse'
          description: ''
  /api/v1/auth/register/:
    post:
      operationId: v1_auth_register_create
      description: 'AUTH-01: POST /api/v1/auth/register/ — Registro ciudadano en plus.usuarios.'
      summary: Registro de cuenta ciudadana (AUTH-01)
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CitizenRegistration'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/CitizenRegistration'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CitizenRegistration'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AuthSessionResponse'
          description: ''
  /api/v1/cases/{case_id}/comments/:
    post:
      operationId: v1_cases_comments_create
      description: |-
        MAP-07: POST /api/v1/cases/{case_id}/comments/ (y /api/v1/citizen/cases/{case_id}/comments/)
        Permite comentar un caso publicado; ingresa siempre como `estado_moderacion='pendiente'`.
      parameters:
      - in: path
        name: case_id
        schema:
          type: string
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CaseComment'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/CaseComment'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CaseComment'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseComment'
          description: ''
  /api/v1/cases/{case_id}/messages/:
    get:
      operationId: v1_cases_messages_retrieve
      description: |-
        MSG-02 y MSG-03:
        GET / POST /api/v1/cases/{case_id}/messages/, /api/v1/citizen/cases/{case_id}/messages/ y /api/v1/admin/cases/{case_id}/messages/
        Restringe el acceso estrictamente al ciudadano propietario, al responsable asignado o al administrador.
      parameters:
      - in: path
        name: case_id
        schema:
          type: string
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseMessage'
          description: ''
    post:
      operationId: v1_cases_messages_create
      description: |-
        MSG-02 y MSG-03:
        GET / POST /api/v1/cases/{case_id}/messages/, /api/v1/citizen/cases/{case_id}/messages/ y /api/v1/admin/cases/{case_id}/messages/
        Restringe el acceso estrictamente al ciudadano propietario, al responsable asignado o al administrador.
      parameters:
      - in: path
        name: case_id
        schema:
          type: string
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CaseMessage'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/CaseMessage'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CaseMessage'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseMessage'
          description: ''
  /api/v1/cases/{case_id}/messages/mark-read/:
    post:
      operationId: v1_cases_messages_mark_read_create
      description: |-
        MSG-04: PUT / POST /api/v1/cases/{case_id}/messages/read/
        Marca como leídos únicamente los mensajes destinados al usuario autenticado,
        soportando selección por lista (`message_ids`), corte por mensaje (`up_to_message_id`)
        o corte temporal (`up_to_timestamp`) para no marcar mensajes recibidos después de abrir la conversación.
      summary: Marcar mensajes privados recibidos como leídos con corte opcional (MSG-04)
      parameters:
      - in: path
        name: case_id
        schema:
          type: string
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/MarkMessagesReadRequest'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/MarkMessagesReadRequest'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/MarkMessagesReadRequest'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MarkMessagesReadResponse'
          description: ''
    put:
      operationId: v1_cases_messages_mark_read_update
      description: |-
        MSG-04: PUT / POST /api/v1/cases/{case_id}/messages/read/
        Marca como leídos únicamente los mensajes destinados al usuario autenticado,
        soportando selección por lista (`message_ids`), corte por mensaje (`up_to_message_id`)
        o corte temporal (`up_to_timestamp`) para no marcar mensajes recibidos después de abrir la conversación.
      summary: Marcar mensajes privados recibidos como leídos con corte opcional (MSG-04)
      parameters:
      - in: path
        name: case_id
        schema:
          type: string
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/MarkMessagesReadPutRequest'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/MarkMessagesReadPutRequest'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/MarkMessagesReadPutRequest'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MarkMessagesReadPutResponse'
          description: ''
  /api/v1/cases/{case_id}/messages/read/:
    post:
      operationId: v1_cases_messages_read_create
      description: |-
        MSG-04: PUT / POST /api/v1/cases/{case_id}/messages/read/
        Marca como leídos únicamente los mensajes destinados al usuario autenticado,
        soportando selección por lista (`message_ids`), corte por mensaje (`up_to_message_id`)
        o corte temporal (`up_to_timestamp`) para no marcar mensajes recibidos después de abrir la conversación.
      summary: Marcar mensajes privados recibidos como leídos con corte opcional (MSG-04)
      parameters:
      - in: path
        name: case_id
        schema:
          type: string
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/MarkMessagesReadRequest'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/MarkMessagesReadRequest'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/MarkMessagesReadRequest'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MarkMessagesReadResponse'
          description: ''
    put:
      operationId: v1_cases_messages_read_update
      description: |-
        MSG-04: PUT / POST /api/v1/cases/{case_id}/messages/read/
        Marca como leídos únicamente los mensajes destinados al usuario autenticado,
        soportando selección por lista (`message_ids`), corte por mensaje (`up_to_message_id`)
        o corte temporal (`up_to_timestamp`) para no marcar mensajes recibidos después de abrir la conversación.
      summary: Marcar mensajes privados recibidos como leídos con corte opcional (MSG-04)
      parameters:
      - in: path
        name: case_id
        schema:
          type: string
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/MarkMessagesReadPutRequest'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/MarkMessagesReadPutRequest'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/MarkMessagesReadPutRequest'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MarkMessagesReadPutResponse'
          description: ''
  /api/v1/catalogs/basins/:
    get:
      operationId: v1_catalogs_basins_retrieve
      description: 'CAT-04: GET /api/v1/catalogs/basins/ — Pendiente de fuente oficial
        AMP-13; responde lista vacía controlada.'
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Community'
          description: ''
  /api/v1/catalogs/case-categories/:
    get:
      operationId: v1_catalogs_case_categories_retrieve
      description: |-
        CAT-05: GET /api/v1/catalogs/case-categories/
        Retorna valores distintos de `tipos_caso.categoria` (textos de hasta 50 caracteres) y los tipos activos.
      summary: Categorías temáticas y tipos de caso activos (CAT-05)
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PublicCaseCategoryNamesResponse'
          description: ''
  /api/v1/catalogs/case-options/:
    get:
      operationId: v1_catalogs_case_options_retrieve
      description: |-
        CAT-06: GET /api/v1/catalogs/case-options/
        Retorna tipos_caso activos, estados_caso, prioridades, estados de publicación y naturalezas.
      summary: 'Opciones maestras de casos: tipos, estados, prioridades y audiencias
        (CAT-06)'
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PublicCaseOptionsResponse'
          description: ''
  /api/v1/catalogs/case-statuses/:
    get:
      operationId: v1_catalogs_case_statuses_list
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/CaseStatus'
          description: ''
  /api/v1/catalogs/case-types/:
    get:
      operationId: v1_catalogs_case_types_list
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/CaseCategory'
          description: ''
  /api/v1/catalogs/communities/:
    get:
      operationId: v1_catalogs_communities_list
      description: 'CAT-03: GET /api/v1/catalogs/communities/'
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Community'
          description: ''
  /api/v1/catalogs/departments/:
    get:
      operationId: v1_catalogs_departments_list
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Department'
          description: ''
  /api/v1/catalogs/initiative-categories/:
    get:
      operationId: v1_catalogs_initiative_categories_retrieve
      description: |-
        CAT-08: GET /api/v1/catalogs/initiative-categories/
        Retorna valores distintos de `iniciativas.categoria` para programas publicados.
      summary: Categorías distintas de iniciativas publicadas (CAT-08)
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PublicInitiativeCategoriesResponse'
          description: ''
  /api/v1/catalogs/municipalities/:
    get:
      operationId: v1_catalogs_municipalities_list
      description: 'CAT-02: GET /api/v1/catalogs/municipalities/'
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Municipality'
          description: ''
  /api/v1/catalogs/news-categories/:
    get:
      operationId: v1_catalogs_news_categories_list
      description: 'CAT-07 (AMP-01): GET /api/v1/catalogs/news-categories/ (y /api/v1/public/news/categories/)'
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/NewsCategory'
          description: ''
  /api/v1/citizen/cases/:
    get:
      operationId: v1_citizen_cases_list
      description: |-
        CIT-02 a CIT-08: Gestión de casos propios del ciudadano (`/api/v1/me/cases/` y `/api/v1/citizen/cases/`).
        Soporta lectura tanto por UUID como por código de radicado (`{case_ref}`).
      parameters:
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedCitizenCaseCreateUpdateList'
          description: ''
    post:
      operationId: v1_citizen_cases_create
      description: |-
        CIT-02 a CIT-08: Gestión de casos propios del ciudadano (`/api/v1/me/cases/` y `/api/v1/citizen/cases/`).
        Soporta lectura tanto por UUID como por código de radicado (`{case_ref}`).
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CitizenCaseCreateUpdate'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/CitizenCaseCreateUpdate'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CitizenCaseCreateUpdate'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CitizenCaseCreateUpdate'
          description: ''
  /api/v1/citizen/cases/{case_id}/comments/:
    post:
      operationId: v1_citizen_cases_comments_create
      description: |-
        MAP-07: POST /api/v1/cases/{case_id}/comments/ (y /api/v1/citizen/cases/{case_id}/comments/)
        Permite comentar un caso publicado; ingresa siempre como `estado_moderacion='pendiente'`.
      parameters:
      - in: path
        name: case_id
        schema:
          type: string
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CaseComment'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/CaseComment'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CaseComment'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseComment'
          description: ''
  /api/v1/citizen/cases/{case_id}/messages/:
    get:
      operationId: v1_citizen_cases_messages_retrieve
      description: |-
        MSG-02 y MSG-03:
        GET / POST /api/v1/cases/{case_id}/messages/, /api/v1/citizen/cases/{case_id}/messages/ y /api/v1/admin/cases/{case_id}/messages/
        Restringe el acceso estrictamente al ciudadano propietario, al responsable asignado o al administrador.
      parameters:
      - in: path
        name: case_id
        schema:
          type: string
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseMessage'
          description: ''
    post:
      operationId: v1_citizen_cases_messages_create
      description: |-
        MSG-02 y MSG-03:
        GET / POST /api/v1/cases/{case_id}/messages/, /api/v1/citizen/cases/{case_id}/messages/ y /api/v1/admin/cases/{case_id}/messages/
        Restringe el acceso estrictamente al ciudadano propietario, al responsable asignado o al administrador.
      parameters:
      - in: path
        name: case_id
        schema:
          type: string
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CaseMessage'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/CaseMessage'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CaseMessage'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseMessage'
          description: ''
  /api/v1/citizen/cases/{id}/:
    get:
      operationId: v1_citizen_cases_retrieve
      description: |-
        CIT-02 a CIT-08: Gestión de casos propios del ciudadano (`/api/v1/me/cases/` y `/api/v1/citizen/cases/`).
        Soporta lectura tanto por UUID como por código de radicado (`{case_ref}`).
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CitizenCaseCreateUpdate'
          description: ''
    patch:
      operationId: v1_citizen_cases_partial_update
      description: |-
        CIT-02 a CIT-08: Gestión de casos propios del ciudadano (`/api/v1/me/cases/` y `/api/v1/citizen/cases/`).
        Soporta lectura tanto por UUID como por código de radicado (`{case_ref}`).
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedCitizenCaseCreateUpdate'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedCitizenCaseCreateUpdate'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedCitizenCaseCreateUpdate'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CitizenCaseCreateUpdate'
          description: ''
  /api/v1/citizen/cases/{id}/contributions/:
    get:
      operationId: v1_citizen_cases_contributions_list
      description: 'CIT-08 (AMP-07): GET / POST /api/v1/me/cases/{case_id}/contributions/'
      summary: Listar o registrar aportes ciudadanos y respuestas a corrección (CIT-08)
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedCaseContributionList'
          description: ''
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseContribution'
          description: ''
    post:
      operationId: v1_citizen_cases_contributions_create
      description: 'CIT-08 (AMP-07): GET / POST /api/v1/me/cases/{case_id}/contributions/'
      summary: Listar o registrar aportes ciudadanos y respuestas a corrección (CIT-08)
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CitizenContributionCreate'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/CitizenContributionCreate'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CitizenContributionCreate'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedCaseContributionList'
          description: ''
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseContribution'
          description: ''
  /api/v1/citizen/cases/{id}/evidence/:
    get:
      operationId: v1_citizen_cases_evidence_list
      description: 'CIT-06: GET / POST /api/v1/me/cases/{case_id}/evidence/'
      summary: Listar o subir evidencias del caso ciudadano (CIT-06)
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedCaseEvidenceList'
          description: ''
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseEvidence'
          description: ''
    post:
      operationId: v1_citizen_cases_evidence_create
      description: 'CIT-06: GET / POST /api/v1/me/cases/{case_id}/evidence/'
      summary: Listar o subir evidencias del caso ciudadano (CIT-06)
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CaseEvidence'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/CaseEvidence'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CaseEvidence'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedCaseEvidenceList'
          description: ''
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseEvidence'
          description: ''
  /api/v1/citizen/cases/{id}/evidence/{evidence_id}/download/:
    get:
      operationId: v1_citizen_cases_evidence_download_retrieve
      description: 'CIT-07: GET /api/v1/me/cases/{case_id}/evidence/{evidence_id}/download/'
      summary: Descargar o consultar metadatos protegidos de una evidencia (CIT-07)
      parameters:
      - in: query
        name: download
        schema:
          type: boolean
        description: Si es 1/true, descarga el binario directamente (FileResponse).
      - in: path
        name: evidence_id
        schema:
          type: string
        required: true
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseEvidence'
          description: ''
  /api/v1/citizen/cases/{id}/history/:
    get:
      operationId: v1_citizen_cases_history_retrieve
      description: |-
        CIT-05: GET /api/v1/me/cases/{case_id}/history/
        Compone seguimientos autorizados al ciudadano (`publico` o `ciudadano`, nunca `interno`),
        cambios de estado y aportes ciudadanos.
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CitizenCaseCreateUpdate'
          description: ''
  /api/v1/citizen/cases/{id}/timeline/:
    get:
      operationId: v1_citizen_cases_timeline_retrieve
      description: Alias compatible con GET /api/v1/me/cases/{case_id}/timeline/
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CitizenCaseCreateUpdate'
          description: ''
  /api/v1/citizen/cases/{id}/updates/:
    post:
      operationId: v1_citizen_cases_updates_create
      description: |-
        CIT-02 a CIT-08: Gestión de casos propios del ciudadano (`/api/v1/me/cases/` y `/api/v1/citizen/cases/`).
        Soporta lectura tanto por UUID como por código de radicado (`{case_ref}`).
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CitizenCaseCreateUpdate'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/CitizenCaseCreateUpdate'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CitizenCaseCreateUpdate'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CitizenCaseCreateUpdate'
          description: ''
  /api/v1/citizen/dashboard/:
    get:
      operationId: v1_citizen_dashboard_retrieve
      description: 'CIT-01: GET /api/v1/me/dashboard/ (y /api/v1/citizen/dashboard/)'
      summary: Resumen del panel ciudadano autenticado (CIT-01)
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CitizenDashboardResponse'
          description: ''
  /api/v1/citizen/notifications/:
    get:
      operationId: v1_citizen_notifications_list
      description: 'NOT-01, NOT-02, NOT-03: /api/v1/me/notifications/ y /api/v1/citizen/notifications/'
      parameters:
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedNotificationList'
          description: ''
  /api/v1/citizen/notifications/{id}/:
    get:
      operationId: v1_citizen_notifications_retrieve
      description: 'NOT-01, NOT-02, NOT-03: /api/v1/me/notifications/ y /api/v1/citizen/notifications/'
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Notification'
          description: ''
    patch:
      operationId: v1_citizen_notifications_partial_update
      description: 'NOT-02: PATCH /api/v1/me/notifications/{id}/ — Solo permite actualizar
        `leida`.'
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedNotification'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedNotification'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedNotification'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Notification'
          description: ''
  /api/v1/citizen/notifications/{id}/mark-read/:
    post:
      operationId: v1_citizen_notifications_mark_read_create_2
      description: 'NOT-01, NOT-02, NOT-03: /api/v1/me/notifications/ y /api/v1/citizen/notifications/'
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Notification'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/Notification'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/Notification'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Notification'
          description: ''
    patch:
      operationId: v1_citizen_notifications_mark_read_partial_update
      description: 'NOT-01, NOT-02, NOT-03: /api/v1/me/notifications/ y /api/v1/citizen/notifications/'
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedNotification'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedNotification'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedNotification'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Notification'
          description: ''
  /api/v1/citizen/notifications/mark-all-read/:
    post:
      operationId: v1_citizen_notifications_mark_all_read_create
      description: 'NOT-01, NOT-02, NOT-03: /api/v1/me/notifications/ y /api/v1/citizen/notifications/'
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Notification'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/Notification'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/Notification'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Notification'
          description: ''
  /api/v1/citizen/notifications/mark-read/:
    post:
      operationId: v1_citizen_notifications_mark_read_create
      description: 'NOT-03: POST /api/v1/me/notifications/mark-read/'
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Notification'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/Notification'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/Notification'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Notification'
          description: ''
  /api/v1/me/:
    get:
      operationId: v1_me_retrieve
      description: 'ME-01 y ME-02: GET / PATCH /api/v1/me/ (y /api/v1/auth/me/)'
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserMe'
          description: ''
    put:
      operationId: v1_me_update
      description: 'ME-01 y ME-02: GET / PATCH /api/v1/me/ (y /api/v1/auth/me/)'
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserMe'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/UserMe'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/UserMe'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserMe'
          description: ''
    patch:
      operationId: v1_me_partial_update
      description: 'ME-01 y ME-02: GET / PATCH /api/v1/me/ (y /api/v1/auth/me/)'
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedUserMe'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedUserMe'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedUserMe'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserMe'
          description: ''
  /api/v1/me/cases/:
    get:
      operationId: v1_me_cases_list
      description: |-
        CIT-02 a CIT-08: Gestión de casos propios del ciudadano (`/api/v1/me/cases/` y `/api/v1/citizen/cases/`).
        Soporta lectura tanto por UUID como por código de radicado (`{case_ref}`).
      parameters:
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedCitizenCaseCreateUpdateList'
          description: ''
    post:
      operationId: v1_me_cases_create
      description: |-
        CIT-02 a CIT-08: Gestión de casos propios del ciudadano (`/api/v1/me/cases/` y `/api/v1/citizen/cases/`).
        Soporta lectura tanto por UUID como por código de radicado (`{case_ref}`).
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CitizenCaseCreateUpdate'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/CitizenCaseCreateUpdate'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CitizenCaseCreateUpdate'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CitizenCaseCreateUpdate'
          description: ''
  /api/v1/me/cases/{id}/:
    get:
      operationId: v1_me_cases_retrieve
      description: |-
        CIT-02 a CIT-08: Gestión de casos propios del ciudadano (`/api/v1/me/cases/` y `/api/v1/citizen/cases/`).
        Soporta lectura tanto por UUID como por código de radicado (`{case_ref}`).
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CitizenCaseCreateUpdate'
          description: ''
    patch:
      operationId: v1_me_cases_partial_update
      description: |-
        CIT-02 a CIT-08: Gestión de casos propios del ciudadano (`/api/v1/me/cases/` y `/api/v1/citizen/cases/`).
        Soporta lectura tanto por UUID como por código de radicado (`{case_ref}`).
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedCitizenCaseCreateUpdate'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedCitizenCaseCreateUpdate'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedCitizenCaseCreateUpdate'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CitizenCaseCreateUpdate'
          description: ''
  /api/v1/me/cases/{id}/contributions/:
    get:
      operationId: v1_me_cases_contributions_list
      description: 'CIT-08 (AMP-07): GET / POST /api/v1/me/cases/{case_id}/contributions/'
      summary: Listar o registrar aportes ciudadanos y respuestas a corrección (CIT-08)
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedCaseContributionList'
          description: ''
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseContribution'
          description: ''
    post:
      operationId: v1_me_cases_contributions_create
      description: 'CIT-08 (AMP-07): GET / POST /api/v1/me/cases/{case_id}/contributions/'
      summary: Listar o registrar aportes ciudadanos y respuestas a corrección (CIT-08)
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CitizenContributionCreate'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/CitizenContributionCreate'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CitizenContributionCreate'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedCaseContributionList'
          description: ''
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseContribution'
          description: ''
  /api/v1/me/cases/{id}/evidence/:
    get:
      operationId: v1_me_cases_evidence_list
      description: 'CIT-06: GET / POST /api/v1/me/cases/{case_id}/evidence/'
      summary: Listar o subir evidencias del caso ciudadano (CIT-06)
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedCaseEvidenceList'
          description: ''
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseEvidence'
          description: ''
    post:
      operationId: v1_me_cases_evidence_create
      description: 'CIT-06: GET / POST /api/v1/me/cases/{case_id}/evidence/'
      summary: Listar o subir evidencias del caso ciudadano (CIT-06)
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CaseEvidence'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/CaseEvidence'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CaseEvidence'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedCaseEvidenceList'
          description: ''
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseEvidence'
          description: ''
  /api/v1/me/cases/{id}/evidence/{evidence_id}/download/:
    get:
      operationId: v1_me_cases_evidence_download_retrieve
      description: 'CIT-07: GET /api/v1/me/cases/{case_id}/evidence/{evidence_id}/download/'
      summary: Descargar o consultar metadatos protegidos de una evidencia (CIT-07)
      parameters:
      - in: query
        name: download
        schema:
          type: boolean
        description: Si es 1/true, descarga el binario directamente (FileResponse).
      - in: path
        name: evidence_id
        schema:
          type: string
        required: true
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseEvidence'
          description: ''
  /api/v1/me/cases/{id}/history/:
    get:
      operationId: v1_me_cases_history_retrieve
      description: |-
        CIT-05: GET /api/v1/me/cases/{case_id}/history/
        Compone seguimientos autorizados al ciudadano (`publico` o `ciudadano`, nunca `interno`),
        cambios de estado y aportes ciudadanos.
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CitizenCaseCreateUpdate'
          description: ''
  /api/v1/me/cases/{id}/timeline/:
    get:
      operationId: v1_me_cases_timeline_retrieve
      description: Alias compatible con GET /api/v1/me/cases/{case_id}/timeline/
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CitizenCaseCreateUpdate'
          description: ''
  /api/v1/me/cases/{id}/updates/:
    post:
      operationId: v1_me_cases_updates_create
      description: |-
        CIT-02 a CIT-08: Gestión de casos propios del ciudadano (`/api/v1/me/cases/` y `/api/v1/citizen/cases/`).
        Soporta lectura tanto por UUID como por código de radicado (`{case_ref}`).
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CitizenCaseCreateUpdate'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/CitizenCaseCreateUpdate'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CitizenCaseCreateUpdate'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CitizenCaseCreateUpdate'
          description: ''
  /api/v1/me/change-password/:
    post:
      operationId: v1_me_change_password_create
      description: POST /api/v1/auth/change-password/
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ChangePassword'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/ChangePassword'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/ChangePassword'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ChangePassword'
          description: ''
  /api/v1/me/conversations/:
    get:
      operationId: v1_me_conversations_retrieve
      description: |-
        MSG-01: GET /api/v1/me/conversations/
        Agrupa los mensajes privados permitidos al usuario autenticado por caso y contraparte.
      summary: Listar conversaciones privadas agrupadas por caso y contraparte (MSG-01)
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MeConversationListResponse'
          description: ''
  /api/v1/me/dashboard/:
    get:
      operationId: v1_me_dashboard_retrieve
      description: 'CIT-01: GET /api/v1/me/dashboard/ (y /api/v1/citizen/dashboard/)'
      summary: Resumen del panel ciudadano autenticado (CIT-01)
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CitizenDashboardResponse'
          description: ''
  /api/v1/me/followed-cases/:
    get:
      operationId: v1_me_followed_cases_retrieve
      description: |-
        MAP-08, MAP-09, MAP-10 (AMP-03):
        GET / PUT / DELETE /api/v1/me/followed-cases/{case_id}/
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/FollowedCase'
          description: ''
    post:
      operationId: v1_me_followed_cases_create
      description: |-
        MAP-08, MAP-09, MAP-10 (AMP-03):
        GET / PUT / DELETE /api/v1/me/followed-cases/{case_id}/
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/FollowedCase'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/FollowedCase'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/FollowedCase'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/FollowedCase'
          description: ''
    put:
      operationId: v1_me_followed_cases_update
      description: |-
        MAP-08, MAP-09, MAP-10 (AMP-03):
        GET / PUT / DELETE /api/v1/me/followed-cases/{case_id}/
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/FollowedCase'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/FollowedCase'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/FollowedCase'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/FollowedCase'
          description: ''
    delete:
      operationId: v1_me_followed_cases_destroy
      description: |-
        MAP-08, MAP-09, MAP-10 (AMP-03):
        GET / PUT / DELETE /api/v1/me/followed-cases/{case_id}/
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '204':
          description: No response body
  /api/v1/me/followed-cases/{case_id}/:
    get:
      operationId: v1_me_followed_cases_retrieve_2
      description: |-
        MAP-08, MAP-09, MAP-10 (AMP-03):
        GET / PUT / DELETE /api/v1/me/followed-cases/{case_id}/
      parameters:
      - in: path
        name: case_id
        schema:
          type: string
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/FollowedCase'
          description: ''
    post:
      operationId: v1_me_followed_cases_create_2
      description: |-
        MAP-08, MAP-09, MAP-10 (AMP-03):
        GET / PUT / DELETE /api/v1/me/followed-cases/{case_id}/
      parameters:
      - in: path
        name: case_id
        schema:
          type: string
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/FollowedCase'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/FollowedCase'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/FollowedCase'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/FollowedCase'
          description: ''
    put:
      operationId: v1_me_followed_cases_update_2
      description: |-
        MAP-08, MAP-09, MAP-10 (AMP-03):
        GET / PUT / DELETE /api/v1/me/followed-cases/{case_id}/
      parameters:
      - in: path
        name: case_id
        schema:
          type: string
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/FollowedCase'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/FollowedCase'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/FollowedCase'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/FollowedCase'
          description: ''
    delete:
      operationId: v1_me_followed_cases_destroy_2
      description: |-
        MAP-08, MAP-09, MAP-10 (AMP-03):
        GET / PUT / DELETE /api/v1/me/followed-cases/{case_id}/
      parameters:
      - in: path
        name: case_id
        schema:
          type: string
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '204':
          description: No response body
  /api/v1/me/notifications/:
    get:
      operationId: v1_me_notifications_list
      description: 'NOT-01, NOT-02, NOT-03: /api/v1/me/notifications/ y /api/v1/citizen/notifications/'
      parameters:
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedNotificationList'
          description: ''
  /api/v1/me/notifications/{id}/:
    get:
      operationId: v1_me_notifications_retrieve
      description: 'NOT-01, NOT-02, NOT-03: /api/v1/me/notifications/ y /api/v1/citizen/notifications/'
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Notification'
          description: ''
    patch:
      operationId: v1_me_notifications_partial_update
      description: 'NOT-02: PATCH /api/v1/me/notifications/{id}/ — Solo permite actualizar
        `leida`.'
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedNotification'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedNotification'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedNotification'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Notification'
          description: ''
  /api/v1/me/notifications/{id}/mark-read/:
    post:
      operationId: v1_me_notifications_mark_read_create_2
      description: 'NOT-01, NOT-02, NOT-03: /api/v1/me/notifications/ y /api/v1/citizen/notifications/'
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Notification'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/Notification'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/Notification'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Notification'
          description: ''
    patch:
      operationId: v1_me_notifications_mark_read_partial_update
      description: 'NOT-01, NOT-02, NOT-03: /api/v1/me/notifications/ y /api/v1/citizen/notifications/'
      parameters:
      - in: path
        name: id
        schema:
          type: string
        required: true
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedNotification'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedNotification'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedNotification'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Notification'
          description: ''
  /api/v1/me/notifications/mark-all-read/:
    post:
      operationId: v1_me_notifications_mark_all_read_create
      description: 'NOT-01, NOT-02, NOT-03: /api/v1/me/notifications/ y /api/v1/citizen/notifications/'
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Notification'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/Notification'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/Notification'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Notification'
          description: ''
  /api/v1/me/notifications/mark-read/:
    post:
      operationId: v1_me_notifications_mark_read_create
      description: 'NOT-03: POST /api/v1/me/notifications/mark-read/'
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Notification'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/Notification'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/Notification'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Notification'
          description: ''
  /api/v1/me/photo/:
    post:
      operationId: v1_me_photo_create
      description: 'ME-03 y ME-04: PUT / POST / DELETE /api/v1/me/photo/'
      summary: Subir o actualizar fotografía de perfil (ME-03)
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/MePhotoUploadRequest'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/MePhotoUploadRequest'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/MePhotoUploadRequest'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserProfile'
          description: ''
    put:
      operationId: v1_me_photo_update
      description: 'ME-03 y ME-04: PUT / POST / DELETE /api/v1/me/photo/'
      summary: Subir o actualizar fotografía de perfil (ME-03)
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/MePhotoPutRequest'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/MePhotoPutRequest'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/MePhotoPutRequest'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserProfile'
          description: ''
    delete:
      operationId: v1_me_photo_destroy
      description: 'ME-03 y ME-04: PUT / POST / DELETE /api/v1/me/photo/'
      summary: Eliminar fotografía de perfil (ME-04)
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '204':
          description: No response body
  /api/v1/me/preferences/:
    get:
      operationId: v1_me_preferences_retrieve
      description: 'ME-05: GET / PATCH /api/v1/me/preferences/'
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserPreference'
          description: ''
    put:
      operationId: v1_me_preferences_update
      description: 'ME-05: GET / PATCH /api/v1/me/preferences/'
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserPreference'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/UserPreference'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/UserPreference'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserPreference'
          description: ''
    patch:
      operationId: v1_me_preferences_partial_update
      description: 'ME-05: GET / PATCH /api/v1/me/preferences/'
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchedUserPreference'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PatchedUserPreference'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PatchedUserPreference'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserPreference'
          description: ''
  /api/v1/public/case-categories/:
    get:
      operationId: v1_public_case_categories_list
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/CaseCategory'
          description: ''
  /api/v1/public/case-statuses/:
    get:
      operationId: v1_public_case_statuses_list
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/CaseStatus'
          description: ''
  /api/v1/public/cases/:
    get:
      operationId: v1_public_cases_list
      description: 'MAP-01: GET /api/v1/public/cases/'
      parameters:
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedPublicCaseListList'
          description: ''
  /api/v1/public/cases/{case_id}/comments/:
    get:
      operationId: v1_public_cases_comments_list
      description: |-
        MAP-06: GET /api/v1/public/cases/{case_id}/comments/
        Retorna comentarios con `estado_moderacion='aprobado'` sobre un caso aprobado.
      parameters:
      - in: path
        name: case_id
        schema:
          type: string
        required: true
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedPublicCaseCommentList'
          description: ''
  /api/v1/public/cases/{case_id}/evidence/:
    get:
      operationId: v1_public_cases_evidence_list
      description: |-
        MAP-05: GET /api/v1/public/cases/{case_id}/evidence/
        Solo entrega evidencias expresamente marcadas como `audiencia='publico'` y `estado_revision='aprobada'`.
      summary: Listado de evidencias públicas aprobadas de un caso (MAP-05)
      parameters:
      - in: path
        name: case_id
        schema:
          type: string
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/CaseEvidence'
          description: ''
  /api/v1/public/cases/{case_id}/evidences/:
    get:
      operationId: v1_public_cases_evidences_list
      description: |-
        MAP-05: GET /api/v1/public/cases/{case_id}/evidence/
        Solo entrega evidencias expresamente marcadas como `audiencia='publico'` y `estado_revision='aprobada'`.
      summary: Listado de evidencias públicas aprobadas de un caso (MAP-05)
      parameters:
      - in: path
        name: case_id
        schema:
          type: string
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/CaseEvidence'
          description: ''
  /api/v1/public/cases/{case_id}/history/:
    get:
      operationId: v1_public_cases_history_retrieve
      description: |-
        MAP-04: GET /api/v1/public/cases/{case_id}/history/
        Solo entrega seguimientos con `visible_publicamente=True` (audiencia='publico') y cambios de estado del caso aprobado.
      summary: Historial público de seguimientos autorizados y cambios de estado (MAP-04)
      parameters:
      - in: path
        name: case_id
        schema:
          type: string
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PublicCaseHistoryResponse'
          description: ''
  /api/v1/public/cases/{lookup}/:
    get:
      operationId: v1_public_cases_retrieve
      description: 'MAP-03: GET /api/v1/public/cases/{case_ref}/'
      parameters:
      - in: path
        name: lookup
        schema:
          type: string
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PublicCaseDetail'
          description: ''
  /api/v1/public/cases/geojson/:
    get:
      operationId: v1_public_cases_geojson_retrieve
      description: |-
        MAP-02: GET /api/v1/public/cases/map/ (y /api/v1/public/cases/geojson/)
        Retorna un GeoJSON FeatureCollection (SRID 4326) de los casos con `estado_publicacion='aprobado'`.
        Generaliza las coordenadas (`public_location`) para proteger ubicaciones sensibles (base de datos.md línea 60).
      summary: Capa GeoJSON FeatureCollection de casos públicos aprobados (MAP-02)
      parameters:
      - in: query
        name: bbox
        schema:
          type: string
        description: 'Bounding box: minLon,minLat,maxLon,maxLat (SRID 4326)'
      - in: query
        name: categoria
        schema:
          type: string
        description: Filtrar por categoría temática textual
      - in: query
        name: estado
        schema:
          type: string
        description: Filtrar por nombre de estado operativo
      - in: query
        name: id_comunidad
        schema:
          type: string
          format: uuid
        description: Filtrar por comunidad
      - in: query
        name: id_departamento
        schema:
          type: string
          format: uuid
        description: Filtrar por departamento
      - in: query
        name: id_estado
        schema:
          type: string
          format: uuid
        description: Filtrar por UUID de estado operativo
      - in: query
        name: id_municipio
        schema:
          type: string
          format: uuid
        description: Filtrar por municipio
      - in: query
        name: id_tipo_caso
        schema:
          type: string
          format: uuid
        description: Filtrar por tipo de caso
      - in: query
        name: naturaleza
        schema:
          type: string
        description: Filtrar por naturaleza (problematica, proyecto_iniciativa, otro)
      - in: query
        name: prioridad
        schema:
          type: string
        description: Filtrar por prioridad (baja, media, alta, critica)
      - in: query
        name: search
        schema:
          type: string
        description: Búsqueda por código, título o descripción
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/GeoJSONCaseFeatureCollection'
          description: ''
  /api/v1/public/cases/map/:
    get:
      operationId: v1_public_cases_map_retrieve
      description: |-
        MAP-02: GET /api/v1/public/cases/map/ (y /api/v1/public/cases/geojson/)
        Retorna un GeoJSON FeatureCollection (SRID 4326) de los casos con `estado_publicacion='aprobado'`.
        Generaliza las coordenadas (`public_location`) para proteger ubicaciones sensibles (base de datos.md línea 60).
      summary: Capa GeoJSON FeatureCollection de casos públicos aprobados (MAP-02)
      parameters:
      - in: query
        name: bbox
        schema:
          type: string
        description: 'Bounding box: minLon,minLat,maxLon,maxLat (SRID 4326)'
      - in: query
        name: categoria
        schema:
          type: string
        description: Filtrar por categoría temática textual
      - in: query
        name: estado
        schema:
          type: string
        description: Filtrar por nombre de estado operativo
      - in: query
        name: id_comunidad
        schema:
          type: string
          format: uuid
        description: Filtrar por comunidad
      - in: query
        name: id_departamento
        schema:
          type: string
          format: uuid
        description: Filtrar por departamento
      - in: query
        name: id_estado
        schema:
          type: string
          format: uuid
        description: Filtrar por UUID de estado operativo
      - in: query
        name: id_municipio
        schema:
          type: string
          format: uuid
        description: Filtrar por municipio
      - in: query
        name: id_tipo_caso
        schema:
          type: string
          format: uuid
        description: Filtrar por tipo de caso
      - in: query
        name: naturaleza
        schema:
          type: string
        description: Filtrar por naturaleza (problematica, proyecto_iniciativa, otro)
      - in: query
        name: prioridad
        schema:
          type: string
        description: Filtrar por prioridad (baja, media, alta, critica)
      - in: query
        name: search
        schema:
          type: string
        description: Búsqueda por código, título o descripción
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/GeoJSONCaseFeatureCollection'
          description: ''
  /api/v1/public/event-proposals/:
    post:
      operationId: v1_public_event_proposals_create
      description: 'PUB-08: POST /api/v1/public/initiative-proposals/ (y /api/v1/citizen/proposals/)'
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/EventProposal'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/EventProposal'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/EventProposal'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/EventProposal'
          description: ''
  /api/v1/public/home/:
    get:
      operationId: v1_public_home_retrieve
      description: |-
        PUB-02: GET /api/v1/public/home/
        Agrega datos institucionales desde plus.configuracion_plataforma, indicadores reales validados,
        iniciativas destacadas (plus.iniciativas) y noticias recientes (plus.noticias) para el Home en Angular.
      summary: Resumen de portada institucional, indicadores verificados, iniciativas
        y noticias (PUB-02)
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PublicHomeSummaryResponse'
          description: ''
  /api/v1/public/initiative-proposals/:
    post:
      operationId: v1_public_initiative_proposals_create
      description: 'PUB-08: POST /api/v1/public/initiative-proposals/ (y /api/v1/citizen/proposals/)'
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/EventProposal'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/EventProposal'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/EventProposal'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/EventProposal'
          description: ''
  /api/v1/public/initiatives/:
    get:
      operationId: v1_public_initiatives_list
      description: 'PUB-05: GET /api/v1/public/initiatives/'
      parameters:
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedInitiativeListList'
          description: ''
  /api/v1/public/initiatives/{lookup}/:
    get:
      operationId: v1_public_initiatives_retrieve
      description: 'PUB-06: GET /api/v1/public/initiatives/{slug}/'
      parameters:
      - in: path
        name: lookup
        schema:
          type: string
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InitiativeDetail'
          description: ''
  /api/v1/public/initiatives/{lookup}/editions/:
    get:
      operationId: v1_public_initiatives_editions_list
      description: 'INI-01: GET /api/v1/public/initiatives/{id}/editions/'
      parameters:
      - in: path
        name: lookup
        schema:
          type: string
        required: true
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedInitiativeEditionList'
          description: ''
  /api/v1/public/initiatives/{lookup}/editions/{edition_id}/:
    get:
      operationId: v1_public_initiatives_editions_retrieve
      description: |-
        INI-02: GET /api/v1/public/initiatives/{id}/editions/{edition_id}/
        Comprueba estrictamente la pertenencia de la edición al programa indicado.
      parameters:
      - in: path
        name: edition_id
        schema:
          type: string
          format: uuid
        required: true
      - in: path
        name: lookup
        schema:
          type: string
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InitiativeEdition'
          description: ''
  /api/v1/public/initiatives/{lookup}/editions/{edition_id}/activities/:
    get:
      operationId: v1_public_initiatives_editions_activities_list
      description: 'INI-03: GET /api/v1/public/initiatives/{id}/editions/{edition_id}/activities/'
      parameters:
      - in: path
        name: edition_id
        schema:
          type: string
          format: uuid
        required: true
      - in: path
        name: lookup
        schema:
          type: string
        required: true
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedInitiativeActivityList'
          description: ''
  /api/v1/public/initiatives/{lookup}/gallery/:
    get:
      operationId: v1_public_initiatives_gallery_list_2
      description: 'PUB-07: GET /api/v1/public/initiatives/{id}/gallery/'
      parameters:
      - in: path
        name: lookup
        schema:
          type: string
        required: true
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedInitiativeMediaList'
          description: ''
  /api/v1/public/initiatives/categories/:
    get:
      operationId: v1_public_initiatives_categories_retrieve
      description: |-
        CAT-08: GET /api/v1/catalogs/initiative-categories/
        Retorna valores distintos de `iniciativas.categoria` para programas publicados.
      summary: Categorías distintas de iniciativas publicadas (CAT-08)
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PublicInitiativeCategoriesResponse'
          description: ''
  /api/v1/public/initiatives/gallery/:
    get:
      operationId: v1_public_initiatives_gallery_list
      description: 'PUB-07: GET /api/v1/public/initiatives/{id}/gallery/'
      parameters:
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedInitiativeMediaList'
          description: ''
  /api/v1/public/initiatives/proposals/:
    post:
      operationId: v1_public_initiatives_proposals_create
      description: 'PUB-08: POST /api/v1/public/initiative-proposals/ (y /api/v1/citizen/proposals/)'
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/EventProposal'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/EventProposal'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/EventProposal'
        required: true
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/EventProposal'
          description: ''
  /api/v1/public/media/{file_path}:
    get:
      operationId: v1_public_media_retrieve
      description: |-
        Entrega autorizada de archivos multimedia públicos a través de `/api/v1/public/media/<path:file_path>`.
        Compatible con configuraciones Nginx donde solo `/api/` se reenvía al contenedor backend.
        - Permite carpetas públicas: `profiles/`, `news/`, `initiatives/`.
        - Para `cases/evidence/`, verifica en base de datos que la evidencia pertenezca a un caso con
          `estado_publicacion='aprobado'` y que la evidencia tenga `audiencia='publico'` y `estado_revision='aprobada'`.
        - Cualquier evidencia privada o en revisión es bloqueada con 403/404.
      summary: Servir archivo multimedia público verificado (fotos de perfil, portadas
        y evidencias públicas aprobadas)
      parameters:
      - in: path
        name: file_path
        schema:
          type: string
        description: Ruta relativa del recurso multimedia público (ej. profiles/foto.jpg,
          news/portada.webp).
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                type: string
                format: binary
          description: ''
  /api/v1/public/news/:
    get:
      operationId: v1_public_news_list
      description: 'PUB-03 (AMP-01): GET /api/v1/public/news/'
      parameters:
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedNewsArticleListList'
          description: ''
  /api/v1/public/news-categories/:
    get:
      operationId: v1_public_news_categories_list
      description: 'CAT-07 (AMP-01): GET /api/v1/catalogs/news-categories/ (y /api/v1/public/news/categories/)'
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/NewsCategory'
          description: ''
  /api/v1/public/news/{lookup}/:
    get:
      operationId: v1_public_news_retrieve
      description: 'PUB-04 (AMP-01): GET /api/v1/public/news/{slug}/'
      parameters:
      - in: path
        name: lookup
        schema:
          type: string
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/NewsArticleDetail'
          description: ''
  /api/v1/public/news/categories/:
    get:
      operationId: v1_public_news_categories_list_2
      description: 'CAT-07 (AMP-01): GET /api/v1/catalogs/news-categories/ (y /api/v1/public/news/categories/)'
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/NewsCategory'
          description: ''
  /api/v1/public/newsletter-subscriptions/:
    post:
      operationId: v1_public_newsletter_subscriptions_create
      description: 'PUB-09 (AMP-02): POST /api/v1/public/newsletter-subscriptions/'
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/NewsletterSubscription'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/NewsletterSubscription'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/NewsletterSubscription'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/NewsletterSubscription'
          description: ''
  /api/v1/public/newsletter-subscriptions/confirm/:
    get:
      operationId: v1_public_newsletter_subscriptions_confirm_retrieve
      description: 'PUB-10 (AMP-02): POST / GET /api/v1/public/newsletter-subscriptions/confirm/'
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/NewsletterTokenAction'
          description: ''
    post:
      operationId: v1_public_newsletter_subscriptions_confirm_create
      description: 'PUB-10 (AMP-02): POST / GET /api/v1/public/newsletter-subscriptions/confirm/'
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/NewsletterTokenAction'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/NewsletterTokenAction'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/NewsletterTokenAction'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/NewsletterTokenAction'
          description: ''
  /api/v1/public/newsletter-subscriptions/unsubscribe/:
    post:
      operationId: v1_public_newsletter_subscriptions_unsubscribe_create
      description: 'PUB-11 (AMP-02): POST /api/v1/public/newsletter-subscriptions/unsubscribe/'
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/NewsletterTokenAction'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/NewsletterTokenAction'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/NewsletterTokenAction'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/NewsletterTokenAction'
          description: ''
  /api/v1/public/newsletter/confirm/:
    get:
      operationId: v1_public_newsletter_confirm_retrieve
      description: 'PUB-10 (AMP-02): POST / GET /api/v1/public/newsletter-subscriptions/confirm/'
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/NewsletterTokenAction'
          description: ''
    post:
      operationId: v1_public_newsletter_confirm_create
      description: 'PUB-10 (AMP-02): POST / GET /api/v1/public/newsletter-subscriptions/confirm/'
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/NewsletterTokenAction'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/NewsletterTokenAction'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/NewsletterTokenAction'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/NewsletterTokenAction'
          description: ''
  /api/v1/public/newsletter/subscribe/:
    post:
      operationId: v1_public_newsletter_subscribe_create
      description: 'PUB-09 (AMP-02): POST /api/v1/public/newsletter-subscriptions/'
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/NewsletterSubscription'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/NewsletterSubscription'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/NewsletterSubscription'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/NewsletterSubscription'
          description: ''
  /api/v1/public/newsletter/unsubscribe/:
    post:
      operationId: v1_public_newsletter_unsubscribe_create
      description: 'PUB-11 (AMP-02): POST /api/v1/public/newsletter-subscriptions/unsubscribe/'
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/NewsletterTokenAction'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/NewsletterTokenAction'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/NewsletterTokenAction'
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/NewsletterTokenAction'
          description: ''
  /api/v1/public/settings/:
    get:
      operationId: v1_public_settings_list
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/SiteSetting'
          description: ''
  /api/v1/public/site/:
    get:
      operationId: v1_public_site_retrieve
      description: |-
        PUB-01: GET /api/v1/public/site/
        Proyección pública autorizada de `configuracion_plataforma` y documentos legales vigentes (AMP-09).
      summary: Información institucional pública y políticas vigentes (PUB-01)
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PublicSiteInfoResponse'
          description: ''
  /api/v1/public/site-info/:
    get:
      operationId: v1_public_site_info_retrieve
      description: |-
        PUB-01: GET /api/v1/public/site/
        Proyección pública autorizada de `configuracion_plataforma` y documentos legales vigentes (AMP-09).
      summary: Información institucional pública y políticas vigentes (PUB-01)
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PublicSiteInfoResponse'
          description: ''
  /api/v1/public/territories/communities/:
    get:
      operationId: v1_public_territories_communities_list
      description: 'CAT-03: GET /api/v1/catalogs/communities/'
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Community'
          description: ''
  /api/v1/public/territories/departments/:
    get:
      operationId: v1_public_territories_departments_list
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Department'
          description: ''
  /api/v1/public/territories/municipalities/:
    get:
      operationId: v1_public_territories_municipalities_list
      description: 'CAT-02: GET /api/v1/catalogs/municipalities/'
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Municipality'
          description: ''
  /api/v1/public/territories/municipalities/{municipality_id}/communities/:
    get:
      operationId: v1_public_territories_municipalities_communities_list
      description: 'CAT-03: GET /api/v1/catalogs/communities/'
      parameters:
      - in: path
        name: municipality_id
        schema:
          type: string
          format: uuid
        required: true
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Community'
          description: ''
components:
  schemas:
    AdminAuditEventListResponse:
      type: object
      properties:
        kpis:
          type: object
          additionalProperties: {}
        count:
          type: integer
        results:
          type: array
          items:
            $ref: '#/components/schemas/UnifiedAuditEventItem'
      required:
      - count
      - kpis
      - results
    AdminCaseDetail:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_caso:
          type: string
          format: uuid
          readOnly: true
        codigo:
          type: string
          readOnly: true
        radicado_code:
          type: string
          readOnly: true
        titulo:
          type: string
          maxLength: 200
        descripcion:
          type: string
        usuario:
          type: string
          format: uuid
          readOnly: true
        usuario_nombre:
          type: string
          readOnly: true
        usuario_correo:
          type: string
          readOnly: true
        usuario_telefono:
          type: string
          readOnly: true
        tipo_caso:
          type: string
          format: uuid
        tipo_nombre:
          type: string
          readOnly: true
        tipo_categoria:
          type: string
          readOnly: true
        tipo_naturaleza:
          type: string
          readOnly: true
        comunidad:
          type: string
          format: uuid
        comunidad_nombre:
          type: string
          readOnly: true
        id_municipio:
          type: string
          format: uuid
          readOnly: true
        municipio_nombre:
          type: string
          readOnly: true
        id_departamento:
          type: string
          format: uuid
          readOnly: true
        departamento_nombre:
          type: string
          readOnly: true
        estado:
          type: string
          format: uuid
        estado_nombre:
          type: string
          readOnly: true
        management_status:
          type: string
          readOnly: true
        prioridad:
          $ref: '#/components/schemas/PrioridadEnum'
        estado_publicacion:
          $ref: '#/components/schemas/EstadoPublicacionE6cEnum'
        moderation_status:
          type: string
          readOnly: true
        ubicacion:
          type: string
          nullable: true
          description: Coordenada geográfica PostGIS geometry(Point, 4326)
        direccion_referencia:
          type: string
          nullable: true
        familias_afectadas:
          type: integer
          maximum: 9223372036854775807
          minimum: 0
          format: int64
          nullable: true
        meses_afectacion:
          type: integer
          maximum: 9223372036854775807
          minimum: 0
          format: int64
          nullable: true
        resultado_resumen:
          type: string
          nullable: true
        seguimiento_resolucion:
          type: string
          format: uuid
          nullable: true
        usuario_resolucion:
          type: string
          format: uuid
          nullable: true
        fecha_resolucion:
          type: string
          format: date-time
          nullable: true
        active_assignment:
          allOf:
          - $ref: '#/components/schemas/CaseAssignment'
          readOnly: true
        active_correction_request:
          allOf:
          - $ref: '#/components/schemas/CaseCorrectionRequest'
          readOnly: true
        solicitudes_correccion:
          type: array
          items:
            $ref: '#/components/schemas/CaseCorrectionRequest'
          readOnly: true
        aportes:
          type: array
          items:
            $ref: '#/components/schemas/CaseContribution'
          readOnly: true
        asignaciones:
          type: array
          items:
            $ref: '#/components/schemas/CaseAssignment'
          readOnly: true
        seguimientos:
          type: array
          items:
            $ref: '#/components/schemas/CaseUpdate'
          readOnly: true
        historial_estados:
          type: array
          items:
            $ref: '#/components/schemas/CaseStatusHistory'
          readOnly: true
        evidencias:
          type: array
          items:
            $ref: '#/components/schemas/CaseEvidence'
          readOnly: true
        allowed_actions:
          type: array
          items:
            type: string
          readOnly: true
        fecha_creacion:
          type: string
          format: date-time
          readOnly: true
        fecha_actualizacion:
          type: string
          format: date-time
          readOnly: true
        fecha_aprobacion:
          type: string
          format: date-time
          nullable: true
      required:
      - active_assignment
      - active_correction_request
      - allowed_actions
      - aportes
      - asignaciones
      - codigo
      - comunidad
      - comunidad_nombre
      - departamento_nombre
      - descripcion
      - estado
      - estado_nombre
      - evidencias
      - fecha_actualizacion
      - fecha_creacion
      - historial_estados
      - id
      - id_caso
      - id_departamento
      - id_municipio
      - management_status
      - moderation_status
      - municipio_nombre
      - radicado_code
      - seguimientos
      - solicitudes_correccion
      - tipo_caso
      - tipo_categoria
      - tipo_naturaleza
      - tipo_nombre
      - titulo
      - usuario
      - usuario_correo
      - usuario_nombre
      - usuario_telefono
    AdminCaseReportResponse:
      type: object
      properties:
        kpis:
          type: object
          additionalProperties: {}
        totals:
          type: object
          additionalProperties: {}
        count:
          type: integer
        page:
          type: integer
        page_size:
          type: integer
        results:
          type: array
          items:
            $ref: '#/components/schemas/AdminCaseDetail'
      required:
      - count
      - kpis
      - page
      - page_size
      - results
      - totals
    AdminEventProposal:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_propuesta:
          type: string
          format: uuid
          readOnly: true
        usuario:
          type: string
          format: uuid
          readOnly: true
          nullable: true
        comunidad:
          type: string
          format: uuid
          nullable: true
        id_comunidad:
          type: string
          format: uuid
          nullable: true
        comunidad_nombre:
          type: string
          readOnly: true
        nombre_contacto:
          type: string
          nullable: true
          maxLength: 150
        telefono_contacto:
          type: string
          nullable: true
          maxLength: 25
        comunidad_declarada:
          type: string
          nullable: true
          maxLength: 200
        acepta_tratamiento_datos:
          type: boolean
        iniciativa_solicitada:
          type: string
          format: uuid
          nullable: true
        iniciativa_generada:
          type: string
          format: uuid
          nullable: true
        titulo:
          type: string
          maxLength: 200
        descripcion:
          type: string
        tipo_actividad:
          type: string
          nullable: true
          maxLength: 80
        fecha_sugerida:
          type: string
          format: date
          nullable: true
        estado:
          $ref: '#/components/schemas/Estado5feEnum'
        respuesta:
          type: string
          nullable: true
        revisor:
          type: string
          format: uuid
          readOnly: true
          nullable: true
        fecha_creacion:
          type: string
          format: date-time
          readOnly: true
        fecha_revision:
          type: string
          format: date-time
          nullable: true
      required:
      - comunidad_nombre
      - descripcion
      - fecha_creacion
      - id
      - id_propuesta
      - revisor
      - titulo
      - usuario
    AdminInitiative:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_iniciativa:
          type: string
          format: uuid
          readOnly: true
        creador:
          type: string
          format: uuid
          readOnly: true
        titulo:
          type: string
          maxLength: 200
        name:
          type: string
        subtitulo:
          type: string
          nullable: true
          maxLength: 250
        featured_title:
          type: string
        slug:
          type: string
          readOnly: true
          pattern: ^[-a-zA-Z0-9_]+$
        descripcion_corta:
          type: string
          nullable: true
        short_description:
          type: string
        descripcion:
          type: string
          nullable: true
        full_content:
          type: string
        categoria:
          type: string
          maxLength: 80
        category:
          type: string
        estado:
          $ref: '#/components/schemas/EstadoC21Enum'
        estado_publicacion:
          $ref: '#/components/schemas/EstadoPublicacion653Enum'
        publication_status:
          type: string
          writeOnly: true
        destacada:
          type: boolean
        is_featured:
          type: boolean
        orden_destacado:
          type: integer
          maximum: 9223372036854775807
          minimum: -9223372036854775808
          format: int64
          nullable: true
        ediciones:
          type: array
          items:
            $ref: '#/components/schemas/InitiativeEdition'
          readOnly: true
        multimedia:
          type: array
          items:
            $ref: '#/components/schemas/InitiativeMedia'
          readOnly: true
        fecha_creacion:
          type: string
          format: date-time
          readOnly: true
        fecha_actualizacion:
          type: string
          format: date-time
          readOnly: true
        fecha_publicacion:
          type: string
          format: date-time
          readOnly: true
          nullable: true
      required:
      - creador
      - ediciones
      - fecha_actualizacion
      - fecha_creacion
      - fecha_publicacion
      - id
      - id_iniciativa
      - multimedia
      - slug
    AdminMetricsDashboardResponse:
      type: object
      properties:
        cases:
          type: object
          additionalProperties: {}
        moderation_queues:
          type: object
          additionalProperties: {}
        territories:
          type: object
          additionalProperties: {}
        content:
          type: object
          additionalProperties: {}
        users:
          type: object
          additionalProperties: {}
      required:
      - cases
      - content
      - moderation_queues
      - territories
      - users
    AdminUserCreateUpdate:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_usuario:
          type: string
          format: uuid
          readOnly: true
        rol:
          type: string
          format: uuid
        id_rol:
          type: string
          format: uuid
        rol_nombre:
          type: string
          writeOnly: true
        nombres:
          type: string
          maxLength: 100
        apellidos:
          type: string
          maxLength: 100
        correo:
          type: string
          format: email
          maxLength: 150
        password:
          type: string
          writeOnly: true
          minLength: 8
        telefono:
          type: string
          nullable: true
          maxLength: 20
        estado:
          $ref: '#/components/schemas/Estado6c7Enum'
        primary_role:
          type: string
          readOnly: true
        roles:
          type: array
          items:
            type: string
          readOnly: true
        fecha_registro:
          type: string
          format: date-time
          readOnly: true
        fecha_actualizacion:
          type: string
          format: date-time
          readOnly: true
      required:
      - apellidos
      - correo
      - fecha_actualizacion
      - fecha_registro
      - id
      - id_usuario
      - nombres
      - primary_role
      - roles
    AssignUserRole:
      type: object
      description: 'USR-05: Soporta PUT /admin/users/{id}/role/ con un único rol (id_rol
        UUID o role_code).'
      properties:
        id_rol:
          type: string
          format: uuid
        role_code:
          type: string
        rol:
          type: string
        motivo:
          type: string
          default: ''
        id_comunidad:
          type: string
          format: uuid
          nullable: true
        id_tipo_caso:
          type: string
          format: uuid
          nullable: true
    Audiencia01dEnum:
      enum:
      - publico
      - ciudadano
      - interno
      type: string
      description: |-
        * `publico` - Público
        * `ciudadano` - Ciudadano / Equipo
        * `interno` - Interno
    AudienciaFebEnum:
      enum:
      - publico
      - ciudadano
      - privado
      type: string
      description: |-
        * `publico` - Público
        * `ciudadano` - Ciudadano / Equipo
        * `privado` - Privado / Interno
    AuditLog:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_auditoria:
          type: string
          format: uuid
          readOnly: true
        usuario:
          type: string
          format: uuid
          readOnly: true
          nullable: true
        usuario_correo:
          type: string
          readOnly: true
        accion:
          type: string
          readOnly: true
        modulo:
          type: string
          readOnly: true
        tabla_afectada:
          type: string
          readOnly: true
          nullable: true
        id_registro:
          type: string
          format: uuid
          readOnly: true
          nullable: true
        datos_anteriores:
          readOnly: true
          nullable: true
        datos_nuevos:
          readOnly: true
          nullable: true
        direccion_ip:
          type: string
          readOnly: true
          nullable: true
        user_agent:
          type: string
          readOnly: true
          nullable: true
        fecha_evento:
          type: string
          format: date-time
          readOnly: true
        resultado:
          allOf:
          - $ref: '#/components/schemas/ResultadoEnum'
          readOnly: true
      required:
      - accion
      - datos_anteriores
      - datos_nuevos
      - direccion_ip
      - fecha_evento
      - id
      - id_auditoria
      - id_registro
      - modulo
      - resultado
      - tabla_afectada
      - user_agent
      - usuario
      - usuario_correo
    AuthSessionResponse:
      type: object
      properties:
        tokens:
          $ref: '#/components/schemas/TokenBundle'
        access:
          type: string
          description: Token JWT de acceso (Bearer).
        refresh:
          type: string
          description: Token JWT de renovación.
        token:
          type: string
          description: Token de sesión revocable en servidor.
        token_type:
          type: string
          default: Bearer
        expires_in:
          type: integer
          description: Segundos de vigencia del access token.
        refresh_expires_in:
          type: integer
          description: Segundos de vigencia del refresh token.
        primary_role:
          type: string
        roles:
          type: array
          items:
            type: string
        user:
          $ref: '#/components/schemas/UserMe'
      required:
      - access
      - expires_in
      - refresh
      - refresh_expires_in
      - token
      - tokens
      - user
    CaseAssignResponsible:
      type: object
      properties:
        id_responsable:
          type: string
          format: uuid
        assigned_to:
          type: string
          format: uuid
        motivo:
          type: string
          default: ''
    CaseAssignment:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_asignacion_caso:
          type: string
          format: uuid
          readOnly: true
        caso:
          type: string
          format: uuid
          readOnly: true
        responsable:
          type: string
          format: uuid
          readOnly: true
        responsable_nombre:
          type: string
          readOnly: true
        responsable_correo:
          type: string
          readOnly: true
        asignador:
          type: string
          format: uuid
          readOnly: true
        asignador_nombre:
          type: string
          readOnly: true
        fecha_asignacion:
          type: string
          format: date-time
          readOnly: true
        fecha_finalizacion:
          type: string
          format: date-time
          readOnly: true
          nullable: true
        activo:
          type: boolean
          readOnly: true
      required:
      - activo
      - asignador
      - asignador_nombre
      - caso
      - fecha_asignacion
      - fecha_finalizacion
      - id
      - id_asignacion_caso
      - responsable
      - responsable_correo
      - responsable_nombre
    CaseCategory:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_tipo_caso:
          type: string
          format: uuid
          readOnly: true
        nombre:
          type: string
          maxLength: 100
        descripcion:
          type: string
          nullable: true
        categoria:
          type: string
          default: general
          maxLength: 50
        naturaleza:
          $ref: '#/components/schemas/NaturalezaEnum'
        activo:
          type: boolean
        casos_count:
          type: integer
          readOnly: true
      required:
      - casos_count
      - id
      - id_tipo_caso
      - nombre
    CaseComment:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_comentario:
          type: string
          format: uuid
          readOnly: true
        caso:
          type: string
          format: uuid
          readOnly: true
        caso_codigo:
          type: string
          readOnly: true
        usuario:
          type: string
          format: uuid
          readOnly: true
        autor_nombre:
          type: string
          readOnly: true
        contenido:
          type: string
        content:
          type: string
        estado_moderacion:
          allOf:
          - $ref: '#/components/schemas/CaseCommentEstadoModeracionEnum'
          readOnly: true
        fecha_creacion:
          type: string
          format: date-time
          readOnly: true
      required:
      - autor_nombre
      - caso
      - caso_codigo
      - estado_moderacion
      - fecha_creacion
      - id
      - id_comentario
      - usuario
    CaseCommentEstadoModeracionEnum:
      enum:
      - pendiente
      - aprobado
      - rechazado
      - oculto
      type: string
      description: |-
        * `pendiente` - Pendiente
        * `aprobado` - Aprobado
        * `rechazado` - Rechazado
        * `oculto` - Oculto
    CaseContribution:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_aporte:
          type: string
          format: uuid
          readOnly: true
        caso:
          type: string
          format: uuid
          readOnly: true
        usuario:
          type: string
          format: uuid
          readOnly: true
        autor_nombre:
          type: string
          readOnly: true
        id_solicitud_correccion:
          type: string
          format: uuid
          nullable: true
        contenido:
          type: string
        evidencias:
          type: array
          items:
            $ref: '#/components/schemas/CaseEvidence'
          readOnly: true
        fecha_creacion:
          type: string
          format: date-time
          readOnly: true
      required:
      - autor_nombre
      - caso
      - contenido
      - evidencias
      - fecha_creacion
      - id
      - id_aporte
      - usuario
    CaseCorrectionRequest:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_solicitud:
          type: string
          format: uuid
          readOnly: true
        caso:
          type: string
          format: uuid
          readOnly: true
        solicitante:
          type: string
          format: uuid
          readOnly: true
        solicitante_nombre:
          type: string
          readOnly: true
        motivo:
          type: string
          readOnly: true
        estado:
          allOf:
          - $ref: '#/components/schemas/CaseCorrectionRequestEstadoEnum'
          readOnly: true
        respuesta:
          type: string
          readOnly: true
          nullable: true
        revisor:
          type: string
          format: uuid
          readOnly: true
          nullable: true
        revisor_nombre:
          type: string
          readOnly: true
        fecha_solicitud:
          type: string
          format: date-time
          readOnly: true
        fecha_respuesta:
          type: string
          format: date-time
          readOnly: true
          nullable: true
        fecha_revision:
          type: string
          format: date-time
          readOnly: true
          nullable: true
      required:
      - caso
      - estado
      - fecha_respuesta
      - fecha_revision
      - fecha_solicitud
      - id
      - id_solicitud
      - motivo
      - respuesta
      - revisor
      - revisor_nombre
      - solicitante
      - solicitante_nombre
    CaseCorrectionRequestCreate:
      type: object
      description: 'ADM-07: Solicitud formal de corrección sobre un caso.'
      properties:
        motivo:
          type: string
          description: Explicación clara de los datos o soportes requeridos al ciudadano.
        campos_solicitados:
          type: array
          items:
            type: string
          description: Lista opcional de campos sugeridos para subsanar.
      required:
      - motivo
    CaseCorrectionRequestEstadoEnum:
      enum:
      - abierta
      - respondida
      - cerrada
      - cancelada
      type: string
      description: |-
        * `abierta` - Abierta
        * `respondida` - Respondida
        * `cerrada` - Cerrada
        * `cancelada` - Cancelada
    CaseEvidence:
      type: object
      description: |-
        Serializador de evidencias de caso (CIT-06, ADM-05).
        Soporta subida multipart mediante el campo `file` o `archivo` (máximo 15 MB; JPG, PNG, WEBP, PDF, MP4, MP3, DOC/X, XLS/X),
        o referencia interna `ruta_archivo`.
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_evidencia:
          type: string
          format: uuid
          readOnly: true
        caso:
          type: string
          format: uuid
          readOnly: true
        usuario:
          type: string
          format: uuid
          readOnly: true
        usuario_nombre:
          type: string
          readOnly: true
        id_aporte:
          type: string
          format: uuid
          readOnly: true
        file:
          type: string
          format: uri
          nullable: true
          writeOnly: true
        archivo:
          type: string
          format: uri
          nullable: true
          writeOnly: true
        tipo_archivo:
          $ref: '#/components/schemas/CaseEvidenceTipoArchivoEnum'
        ruta_archivo:
          type: string
        download_url:
          type: string
          readOnly: true
        descripcion:
          type: string
          nullable: true
        audiencia:
          $ref: '#/components/schemas/AudienciaFebEnum'
        estado_revision:
          $ref: '#/components/schemas/EstadoRevisionEnum'
        nombre_original:
          type: string
          nullable: true
          maxLength: 255
        mime_type:
          type: string
          nullable: true
          maxLength: 100
        tamano_bytes:
          type: integer
          maximum: 9223372036854775807
          minimum: -9223372036854775808
          format: int64
          nullable: true
        fecha_subida:
          type: string
          format: date-time
          readOnly: true
      required:
      - caso
      - download_url
      - fecha_subida
      - id
      - id_aporte
      - id_evidencia
      - usuario
      - usuario_nombre
    CaseEvidenceTipoArchivoEnum:
      enum:
      - imagen
      - video
      - audio
      - documento
      type: string
      description: |-
        * `imagen` - Imagen
        * `video` - Video
        * `audio` - Audio
        * `documento` - Documento
    CaseManagementStatus:
      type: object
      properties:
        id_estado:
          type: string
        estado:
          type: string
        management_status:
          type: string
        titulo:
          type: string
          default: ''
        descripcion:
          type: string
          default: ''
        motivo:
          type: string
          default: ''
        observations:
          type: string
          default: ''
        final_result:
          type: string
          default: ''
        resultado_resumen:
          type: string
          default: ''
    CaseMessage:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_mensaje:
          type: string
          format: uuid
          readOnly: true
        caso:
          type: string
          format: uuid
          readOnly: true
          nullable: true
        remitente:
          type: string
          format: uuid
          readOnly: true
        remitente_nombre:
          type: string
          readOnly: true
        destinatario:
          type: string
          format: uuid
        destinatario_nombre:
          type: string
          readOnly: true
        contenido:
          type: string
        content:
          type: string
        fecha_envio:
          type: string
          format: date-time
          readOnly: true
        fecha_lectura:
          type: string
          format: date-time
          readOnly: true
          nullable: true
      required:
      - caso
      - destinatario_nombre
      - fecha_envio
      - fecha_lectura
      - id
      - id_mensaje
      - remitente
      - remitente_nombre
    CaseModerationAction:
      type: object
      properties:
        estado_publicacion:
          type: string
        moderation_status:
          type: string
        accion:
          type: string
        solicitar_correccion:
          type: boolean
          default: false
        motivo:
          type: string
          default: ''
        moderation_reason:
          type: string
          default: ''
        prioridad:
          type: string
        priority:
          type: string
    CaseStatus:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_estado:
          type: string
          format: uuid
          readOnly: true
        nombre:
          type: string
          maxLength: 50
        descripcion:
          type: string
          nullable: true
        orden:
          type: integer
          maximum: 9223372036854775807
          minimum: -9223372036854775808
          format: int64
      required:
      - id
      - id_estado
      - nombre
      - orden
    CaseStatusHistory:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_historial:
          type: string
          format: uuid
          readOnly: true
        estado_anterior:
          type: string
          format: uuid
          readOnly: true
          nullable: true
        estado_anterior_nombre:
          type: string
          readOnly: true
        estado_nuevo:
          type: string
          format: uuid
          readOnly: true
        estado_nuevo_nombre:
          type: string
          readOnly: true
        motivo:
          type: string
          readOnly: true
          nullable: true
        fecha_cambio:
          type: string
          format: date-time
          readOnly: true
        caso:
          type: string
          format: uuid
          readOnly: true
        usuario:
          type: string
          format: uuid
          readOnly: true
          nullable: true
        usuario_nombre:
          type: string
          readOnly: true
      required:
      - caso
      - estado_anterior
      - estado_anterior_nombre
      - estado_nuevo
      - estado_nuevo_nombre
      - fecha_cambio
      - id
      - id_historial
      - motivo
      - usuario
      - usuario_nombre
    CaseUpdate:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_seguimiento:
          type: string
          format: uuid
          readOnly: true
        caso:
          type: string
          format: uuid
          readOnly: true
        usuario:
          type: string
          format: uuid
          readOnly: true
        autor_nombre:
          type: string
          readOnly: true
        titulo:
          type: string
          nullable: true
          maxLength: 200
        descripcion:
          type: string
        audiencia:
          $ref: '#/components/schemas/Audiencia01dEnum'
        tipo_evento:
          $ref: '#/components/schemas/TipoEventoEnum'
        fecha_seguimiento:
          type: string
          format: date-time
          readOnly: true
        visible_publicamente:
          type: boolean
      required:
      - autor_nombre
      - caso
      - descripcion
      - fecha_seguimiento
      - id
      - id_seguimiento
      - usuario
    CaseUpdateCreate:
      type: object
      properties:
        titulo:
          type: string
          maxLength: 200
        title:
          type: string
          maxLength: 200
        descripcion:
          type: string
        content:
          type: string
        audiencia:
          type: string
        visibility:
          type: string
        visible_publicamente:
          type: boolean
        tipo_evento:
          type: string
          default: seguimiento
        id_estado:
          type: string
        estado:
          type: string
    ChangePassword:
      type: object
      properties:
        current_password:
          type: string
          writeOnly: true
        new_password:
          type: string
          writeOnly: true
          minLength: 8
      required:
      - current_password
      - new_password
    CitizenCaseCreateUpdate:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_caso:
          type: string
          format: uuid
          readOnly: true
        codigo:
          type: string
          readOnly: true
        radicado_code:
          type: string
          readOnly: true
        titulo:
          type: string
          maxLength: 200
        title:
          type: string
        descripcion:
          type: string
        description:
          type: string
        tipo_caso:
          type: string
          format: uuid
        id_tipo_caso:
          type: string
          format: uuid
        tipo_nombre:
          type: string
          readOnly: true
        category:
          type: string
          format: uuid
        comunidad:
          type: string
          format: uuid
        id_comunidad:
          type: string
          format: uuid
        comunidad_nombre:
          type: string
          readOnly: true
        municipio_nombre:
          type: string
          readOnly: true
        departamento_nombre:
          type: string
          readOnly: true
        community:
          type: string
          format: uuid
        estado:
          type: string
          format: uuid
          readOnly: true
        estado_nombre:
          type: string
          readOnly: true
        management_status:
          type: string
          readOnly: true
        prioridad:
          $ref: '#/components/schemas/PrioridadEnum'
        estado_publicacion:
          allOf:
          - $ref: '#/components/schemas/EstadoPublicacionE6cEnum'
          readOnly: true
        moderation_status:
          type: string
          readOnly: true
        ubicacion:
          type: string
          nullable: true
          description: Coordenada geográfica PostGIS geometry(Point, 4326)
        exact_latitude:
          type: string
          format: decimal
          pattern: ^-?\d{0,3}(?:\.\d{0,6})?$
          writeOnly: true
        exact_longitude:
          type: string
          format: decimal
          pattern: ^-?\d{0,3}(?:\.\d{0,6})?$
          writeOnly: true
        latitud:
          type: string
          format: decimal
          pattern: ^-?\d{0,3}(?:\.\d{0,6})?$
          writeOnly: true
        longitud:
          type: string
          format: decimal
          pattern: ^-?\d{0,3}(?:\.\d{0,6})?$
          writeOnly: true
        direccion_referencia:
          type: string
          nullable: true
        familias_afectadas:
          type: integer
          maximum: 9223372036854775807
          minimum: 0
          format: int64
          nullable: true
        meses_afectacion:
          type: integer
          maximum: 9223372036854775807
          minimum: 0
          format: int64
          nullable: true
        resultado_resumen:
          type: string
          readOnly: true
          nullable: true
        fecha_resolucion:
          type: string
          format: date-time
          readOnly: true
          nullable: true
        acepta_tratamiento_datos:
          type: boolean
          writeOnly: true
          default: true
        accepts_data_policy:
          type: boolean
          writeOnly: true
          default: true
        active_assignment:
          allOf:
          - $ref: '#/components/schemas/CaseAssignment'
          readOnly: true
        active_correction_request:
          allOf:
          - $ref: '#/components/schemas/CaseCorrectionRequest'
          readOnly: true
        solicitudes_correccion:
          type: array
          items:
            $ref: '#/components/schemas/CaseCorrectionRequest'
          readOnly: true
        aportes:
          type: array
          items:
            $ref: '#/components/schemas/CaseContribution'
          readOnly: true
        seguimientos:
          type: string
          readOnly: true
        evidencias:
          type: string
          readOnly: true
        allowed_actions:
          type: array
          items:
            type: string
          readOnly: true
        fecha_creacion:
          type: string
          format: date-time
          readOnly: true
        fecha_actualizacion:
          type: string
          format: date-time
          readOnly: true
        fecha_aprobacion:
          type: string
          format: date-time
          readOnly: true
          nullable: true
      required:
      - active_assignment
      - active_correction_request
      - allowed_actions
      - aportes
      - codigo
      - comunidad_nombre
      - departamento_nombre
      - estado
      - estado_nombre
      - estado_publicacion
      - evidencias
      - fecha_actualizacion
      - fecha_aprobacion
      - fecha_creacion
      - fecha_resolucion
      - id
      - id_caso
      - management_status
      - moderation_status
      - municipio_nombre
      - radicado_code
      - resultado_resumen
      - seguimientos
      - solicitudes_correccion
      - tipo_nombre
    CitizenContributionCreate:
      type: object
      description: 'CIT-08: Envío de aporte ciudadano o respuesta a solicitud de corrección.'
      properties:
        contenido:
          type: string
          description: Texto del aporte o subsanación del ciudadano.
        mensaje:
          type: string
          description: Alias de contenido.
        id_solicitud_correccion:
          type: string
          format: uuid
          nullable: true
          description: UUID de la solicitud de corrección que se responde (opcional).
        files:
          type: array
          items:
            type: string
            format: uri
          description: Archivos adjuntos opcionales (multipart/form-data, máx. 15
            MB por archivo).
    CitizenDashboardResponse:
      type: object
      properties:
        total_cases:
          type: integer
        pendientes_publicacion:
          type: integer
        aprobados_publicacion:
          type: integer
        en_gestion:
          type: integer
        resueltos_o_cerrados:
          type: integer
        open_correction_requests:
          type: integer
        unread_notifications:
          type: integer
        unread_messages:
          type: integer
        followed_cases_count:
          type: integer
      required:
      - aprobados_publicacion
      - en_gestion
      - followed_cases_count
      - open_correction_requests
      - pendientes_publicacion
      - resueltos_o_cerrados
      - total_cases
      - unread_messages
      - unread_notifications
    CitizenRegistration:
      type: object
      properties:
        correo:
          type: string
          format: email
          maxLength: 150
        email:
          type: string
          format: email
          maxLength: 150
        username:
          type: string
          maxLength: 150
        password:
          type: string
          writeOnly: true
          minLength: 8
        nombres:
          type: string
          maxLength: 100
        apellidos:
          type: string
          maxLength: 100
        first_name:
          type: string
          maxLength: 100
        last_name:
          type: string
          maxLength: 100
        telefono:
          type: string
          maxLength: 20
        accepts_data_policy:
          type: boolean
          default: true
        acepta_tratamiento_datos:
          type: boolean
      required:
      - password
    CommentModerationAction:
      type: object
      properties:
        estado_moderacion:
          allOf:
          - $ref: '#/components/schemas/CommentModerationActionEstadoModeracionEnum'
          description: |-
            Acción de moderación sobre el comentario: 'pendiente', 'aprobado', 'rechazado' u 'oculto'.

            * `pendiente` - pendiente
            * `aprobado` - aprobado
            * `rechazado` - rechazado
            * `oculto` - oculto
            * `pending` - pending
            * `approved` - approved
            * `rejected` - rejected
            * `hidden` - hidden
        moderation_status:
          type: string
        motivo:
          type: string
          default: ''
          description: Nota o motivo interno de moderación (se guarda en auditoria_eventos;
            no se expone al autor salvo que notificar_motivo=true).
        nota_interna:
          type: string
          default: ''
        moderation_reason:
          type: string
          default: ''
        notificar_motivo:
          type: boolean
          default: false
          description: Si es true, incluye el motivo en la notificación enviada al
            autor del comentario.
    CommentModerationActionEstadoModeracionEnum:
      enum:
      - pendiente
      - aprobado
      - rechazado
      - oculto
      - pending
      - approved
      - rejected
      - hidden
      type: string
      description: |-
        * `pendiente` - pendiente
        * `aprobado` - aprobado
        * `rechazado` - rechazado
        * `oculto` - oculto
        * `pending` - pending
        * `approved` - approved
        * `rejected` - rejected
        * `hidden` - hidden
    Community:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_comunidad:
          type: string
          format: uuid
          readOnly: true
        municipio:
          type: string
          format: uuid
        id_municipio:
          type: string
          format: uuid
        municipio_nombre:
          type: string
          readOnly: true
        nombre:
          type: string
          maxLength: 150
        descripcion:
          type: string
          nullable: true
        tipo:
          allOf:
          - $ref: '#/components/schemas/CommunityTipoEnum'
          default: vereda
        tipo_display:
          type: string
          readOnly: true
        ubicacion:
          type: string
          nullable: true
          description: Perímetro opcional geometry(MultiPolygon, 4326)
        activo:
          type: boolean
      required:
      - id
      - id_comunidad
      - municipio_nombre
      - nombre
      - tipo_display
    CommunityTipoEnum:
      enum:
      - barrio
      - vereda
      - corregimiento
      - comuna
      - sector
      - otro
      type: string
      description: |-
        * `barrio` - Barrio
        * `vereda` - Vereda
        * `corregimiento` - Corregimiento
        * `comuna` - Comuna
        * `sector` - Sector
        * `otro` - Otro
    ConversationSummaryItem:
      type: object
      properties:
        id_caso:
          type: string
          format: uuid
          nullable: true
        caso_codigo:
          type: string
          nullable: true
        caso_titulo:
          type: string
          nullable: true
        contraparte_id:
          type: string
          format: uuid
        contraparte_nombre:
          type: string
        ultimo_mensaje:
          type: string
        fecha_ultimo_mensaje:
          type: string
          format: date-time
        unread_count:
          type: integer
      required:
      - caso_codigo
      - caso_titulo
      - contraparte_id
      - contraparte_nombre
      - fecha_ultimo_mensaje
      - id_caso
      - ultimo_mensaje
      - unread_count
    Department:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_departamento:
          type: string
          format: uuid
          readOnly: true
        codigo_dane:
          type: string
          pattern: ^[0-9]{2}$
          maxLength: 2
        nombre:
          type: string
          maxLength: 100
        municipios:
          type: array
          items:
            $ref: '#/components/schemas/Municipality'
          readOnly: true
      required:
      - codigo_dane
      - id
      - id_departamento
      - municipios
      - nombre
    Estado5feEnum:
      enum:
      - pendiente
      - en_revision
      - aprobada
      - rechazada
      type: string
      description: |-
        * `pendiente` - Pendiente
        * `en_revision` - En Revisión
        * `aprobada` - Aprobada
        * `rechazada` - Rechazada
    Estado6c7Enum:
      enum:
      - activo
      - suspendido
      - inactivo
      type: string
      description: |-
        * `activo` - Activo
        * `suspendido` - Suspendido
        * `inactivo` - Inactivo
    EstadoC21Enum:
      enum:
      - planificada
      - en_curso
      - finalizada
      - cancelada
      type: string
      description: |-
        * `planificada` - Planificada
        * `en_curso` - En Curso
        * `finalizada` - Finalizada
        * `cancelada` - Cancelada
    EstadoPublicacion0baEnum:
      enum:
      - borrador
      - en_revision
      - publicada
      - archivada
      type: string
      description: |-
        * `borrador` - Borrador
        * `en_revision` - En revisión
        * `publicada` - Publicada
        * `archivada` - Archivada
    EstadoPublicacion653Enum:
      enum:
      - borrador
      - pendiente
      - publicada
      - rechazada
      type: string
      description: |-
        * `borrador` - Borrador
        * `pendiente` - Pendiente
        * `publicada` - Publicada
        * `rechazada` - Rechazada
    EstadoPublicacionE6cEnum:
      enum:
      - pendiente
      - aprobado
      - rechazado
      type: string
      description: |-
        * `pendiente` - Pendiente
        * `aprobado` - Aprobado
        * `rechazado` - Rechazado
    EstadoRevisionEnum:
      enum:
      - pendiente
      - aprobada
      - rechazada
      type: string
      description: |-
        * `pendiente` - Pendiente
        * `aprobada` - Aprobada
        * `rechazada` - Rechazada
    EventProposal:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_propuesta:
          type: string
          format: uuid
          readOnly: true
        usuario:
          type: string
          format: uuid
          readOnly: true
          nullable: true
        comunidad:
          type: string
          format: uuid
          nullable: true
        id_comunidad:
          type: string
          format: uuid
          nullable: true
        comunidad_nombre:
          type: string
          readOnly: true
        nombre_contacto:
          type: string
          nullable: true
          maxLength: 150
        telefono_contacto:
          type: string
          nullable: true
          maxLength: 25
        comunidad_declarada:
          type: string
          nullable: true
          maxLength: 200
        acepta_tratamiento_datos:
          type: boolean
        iniciativa_solicitada:
          type: string
          format: uuid
          nullable: true
        iniciativa_generada:
          type: string
          format: uuid
          readOnly: true
          nullable: true
        titulo:
          type: string
          maxLength: 200
        descripcion:
          type: string
        tipo_actividad:
          type: string
          nullable: true
          maxLength: 80
        fecha_sugerida:
          type: string
          format: date
          nullable: true
        estado:
          allOf:
          - $ref: '#/components/schemas/Estado5feEnum'
          readOnly: true
        respuesta:
          type: string
          readOnly: true
          nullable: true
        revisor:
          type: string
          format: uuid
          readOnly: true
          nullable: true
        fecha_creacion:
          type: string
          format: date-time
          readOnly: true
        fecha_revision:
          type: string
          format: date-time
          readOnly: true
          nullable: true
      required:
      - comunidad_nombre
      - descripcion
      - estado
      - fecha_creacion
      - fecha_revision
      - id
      - id_propuesta
      - iniciativa_generada
      - respuesta
      - revisor
      - titulo
      - usuario
    FollowedCase:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_seguimiento_usuario:
          type: string
          format: uuid
          readOnly: true
        id_caso:
          type: string
          format: uuid
          readOnly: true
        codigo:
          type: string
          readOnly: true
        titulo:
          type: string
          readOnly: true
        activo:
          type: boolean
          readOnly: true
        fecha_creacion:
          type: string
          format: date-time
          readOnly: true
        fecha_baja:
          type: string
          format: date-time
          readOnly: true
          nullable: true
      required:
      - activo
      - codigo
      - fecha_baja
      - fecha_creacion
      - id
      - id_caso
      - id_seguimiento_usuario
      - titulo
    GeoJSONCaseFeature:
      type: object
      properties:
        type:
          type: string
          default: Feature
        id:
          type: string
          format: uuid
        geometry:
          $ref: '#/components/schemas/GeoJSONPointGeometry'
        properties:
          $ref: '#/components/schemas/GeoJSONCaseProperties'
      required:
      - geometry
      - id
      - properties
    GeoJSONCaseFeatureCollection:
      type: object
      description: 'MAP-02: Respuesta GeoJSON FeatureCollection RFC 7946 (SRID 4326).'
      properties:
        type:
          type: string
          default: FeatureCollection
        srid:
          type: integer
          default: 4326
        count:
          type: integer
        features:
          type: array
          items:
            $ref: '#/components/schemas/GeoJSONCaseFeature'
      required:
      - count
      - features
    GeoJSONCaseProperties:
      type: object
      properties:
        id_caso:
          type: string
          format: uuid
        codigo:
          type: string
        radicado_code:
          type: string
        titulo:
          type: string
        prioridad:
          $ref: '#/components/schemas/PrioridadEnum'
        id_estado:
          type: string
          format: uuid
        estado:
          type: string
        id_tipo_caso:
          type: string
          format: uuid
        tipo:
          type: string
        categoria:
          type: string
        naturaleza:
          type: string
        id_comunidad:
          type: string
          format: uuid
        comunidad:
          type: string
        id_municipio:
          type: string
          format: uuid
        municipio:
          type: string
        id_departamento:
          type: string
          format: uuid
        departamento:
          type: string
        longitud:
          type: number
          format: double
        latitud:
          type: number
          format: double
        fecha_creacion:
          type: string
          format: date-time
      required:
      - categoria
      - codigo
      - comunidad
      - departamento
      - estado
      - fecha_creacion
      - id_caso
      - id_comunidad
      - id_departamento
      - id_estado
      - id_municipio
      - id_tipo_caso
      - latitud
      - longitud
      - municipio
      - naturaleza
      - prioridad
      - radicado_code
      - tipo
      - titulo
    GeoJSONPointGeometry:
      type: object
      properties:
        type:
          type: string
          default: Point
        srid:
          type: integer
          default: 4326
        coordinates:
          type: array
          items:
            type: number
            format: double
          description: '[longitud, latitud] generalizadas a 2 decimales en SRID 4326.'
          maxItems: 2
          minItems: 2
      required:
      - coordinates
    InitiativeActivity:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_actividad:
          type: string
          format: uuid
          readOnly: true
        edicion:
          type: string
          format: uuid
        responsable:
          type: string
          format: uuid
          nullable: true
        responsable_nombre:
          type: string
          readOnly: true
        comunidad:
          type: string
          format: uuid
          nullable: true
        comunidad_nombre:
          type: string
          readOnly: true
        titulo:
          type: string
          maxLength: 200
        descripcion:
          type: string
          nullable: true
        fecha_inicio:
          type: string
          format: date-time
        fecha_fin:
          type: string
          format: date-time
          nullable: true
        lugar:
          type: string
          nullable: true
          maxLength: 200
        ubicacion:
          type: string
          nullable: true
          description: Coordenada geográfica PostGIS geometry(Point, 4326)
        estado:
          $ref: '#/components/schemas/InitiativeActivityEstadoEnum'
        fecha_creacion:
          type: string
          format: date-time
          readOnly: true
      required:
      - comunidad_nombre
      - edicion
      - fecha_creacion
      - id
      - id_actividad
      - responsable_nombre
      - titulo
    InitiativeActivityEstadoEnum:
      enum:
      - programada
      - realizada
      - cancelada
      type: string
      description: |-
        * `programada` - Programada
        * `realizada` - Realizada
        * `cancelada` - Cancelada
    InitiativeCaseLink:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        edicion:
          type: string
          format: uuid
        caso:
          type: string
          format: uuid
        caso_codigo:
          type: string
          readOnly: true
        tipo_vinculo:
          $ref: '#/components/schemas/TipoVinculoEnum'
        observaciones:
          type: string
          nullable: true
        fecha_vinculacion:
          type: string
          format: date-time
      required:
      - caso
      - caso_codigo
      - edicion
      - id
    InitiativeCommunity:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        edicion:
          type: string
          format: uuid
        comunidad:
          type: string
          format: uuid
        comunidad_nombre:
          type: string
          readOnly: true
        observaciones:
          type: string
          nullable: true
      required:
      - comunidad
      - comunidad_nombre
      - edicion
      - id
    InitiativeDetail:
      type: object
      description: Contrato alineado con vw_iniciativas_destacadas y el catálogo público
        de Angular.
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_iniciativa:
          type: string
          format: uuid
          readOnly: true
        titulo:
          type: string
          readOnly: true
        name:
          type: string
          readOnly: true
        subtitulo:
          type: string
          readOnly: true
          nullable: true
        featured_title:
          type: string
          readOnly: true
        slug:
          type: string
          readOnly: true
          pattern: ^[-a-zA-Z0-9_]+$
        descripcion_corta:
          type: string
          readOnly: true
          nullable: true
        short_description:
          type: string
          readOnly: true
        categoria:
          type: string
          readOnly: true
        estado:
          allOf:
          - $ref: '#/components/schemas/EstadoC21Enum'
          readOnly: true
        estado_publicacion:
          allOf:
          - $ref: '#/components/schemas/EstadoPublicacion653Enum'
          readOnly: true
        destacada:
          type: boolean
          readOnly: true
        orden_destacado:
          type: integer
          readOnly: true
          nullable: true
        fecha_publicacion:
          type: string
          format: date-time
          readOnly: true
          nullable: true
        portada:
          type: string
          readOnly: true
        metrics:
          type: string
          readOnly: true
        descripcion:
          type: string
          nullable: true
        ediciones:
          type: array
          items:
            $ref: '#/components/schemas/InitiativeEdition'
          readOnly: true
        multimedia:
          type: array
          items:
            $ref: '#/components/schemas/InitiativeMedia'
          readOnly: true
        fecha_creacion:
          type: string
          format: date-time
        fecha_actualizacion:
          type: string
          format: date-time
      required:
      - categoria
      - descripcion_corta
      - destacada
      - ediciones
      - estado
      - estado_publicacion
      - featured_title
      - fecha_publicacion
      - id
      - id_iniciativa
      - metrics
      - multimedia
      - name
      - orden_destacado
      - portada
      - short_description
      - slug
      - subtitulo
      - titulo
    InitiativeEdition:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_edicion:
          type: string
          format: uuid
          readOnly: true
        iniciativa:
          type: string
          format: uuid
        anio:
          type: integer
          maximum: 9223372036854775807
          minimum: -9223372036854775808
          format: int64
        nombre_edicion:
          type: string
          nullable: true
          maxLength: 150
        temporada:
          type: string
          nullable: true
          maxLength: 100
        descripcion:
          type: string
          nullable: true
        fecha_inicio:
          type: string
          format: date
          nullable: true
        fecha_fin:
          type: string
          format: date
          nullable: true
        estado:
          $ref: '#/components/schemas/EstadoC21Enum'
        indicadores:
          type: array
          items:
            $ref: '#/components/schemas/InitiativeMetric'
          readOnly: true
        actividades:
          type: array
          items:
            $ref: '#/components/schemas/InitiativeActivity'
          readOnly: true
        comunidades_vinculadas:
          type: array
          items:
            $ref: '#/components/schemas/InitiativeCommunity'
          readOnly: true
        casos_vinculados:
          type: array
          items:
            $ref: '#/components/schemas/InitiativeCaseLink'
          readOnly: true
        fecha_creacion:
          type: string
          format: date-time
          readOnly: true
      required:
      - actividades
      - anio
      - casos_vinculados
      - comunidades_vinculadas
      - fecha_creacion
      - id
      - id_edicion
      - indicadores
      - iniciativa
    InitiativeList:
      type: object
      description: Contrato alineado con vw_iniciativas_destacadas y el catálogo público
        de Angular.
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_iniciativa:
          type: string
          format: uuid
          readOnly: true
        titulo:
          type: string
          readOnly: true
        name:
          type: string
          readOnly: true
        subtitulo:
          type: string
          readOnly: true
          nullable: true
        featured_title:
          type: string
          readOnly: true
        slug:
          type: string
          readOnly: true
          pattern: ^[-a-zA-Z0-9_]+$
        descripcion_corta:
          type: string
          readOnly: true
          nullable: true
        short_description:
          type: string
          readOnly: true
        categoria:
          type: string
          readOnly: true
        estado:
          allOf:
          - $ref: '#/components/schemas/EstadoC21Enum'
          readOnly: true
        estado_publicacion:
          allOf:
          - $ref: '#/components/schemas/EstadoPublicacion653Enum'
          readOnly: true
        destacada:
          type: boolean
          readOnly: true
        orden_destacado:
          type: integer
          readOnly: true
          nullable: true
        fecha_publicacion:
          type: string
          format: date-time
          readOnly: true
          nullable: true
        portada:
          type: string
          readOnly: true
        metrics:
          type: string
          readOnly: true
      required:
      - categoria
      - descripcion_corta
      - destacada
      - estado
      - estado_publicacion
      - featured_title
      - fecha_publicacion
      - id
      - id_iniciativa
      - metrics
      - name
      - orden_destacado
      - portada
      - short_description
      - slug
      - subtitulo
      - titulo
    InitiativeMedia:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_multimedia:
          type: string
          format: uuid
          readOnly: true
        iniciativa:
          type: string
          format: uuid
        edicion:
          type: string
          format: uuid
          nullable: true
        tipo:
          $ref: '#/components/schemas/Tipo669Enum'
        ruta_archivo:
          type: string
        texto_alternativo:
          type: string
          nullable: true
        descripcion:
          type: string
          nullable: true
        es_portada:
          type: boolean
        orden:
          type: integer
          maximum: 9223372036854775807
          minimum: -9223372036854775808
          format: int64
        fecha_subida:
          type: string
          format: date-time
          readOnly: true
      required:
      - fecha_subida
      - id
      - id_multimedia
      - iniciativa
      - ruta_archivo
    InitiativeMetric:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_indicador:
          type: string
          format: uuid
          readOnly: true
        edicion:
          type: string
          format: uuid
        nombre:
          type: string
          maxLength: 100
        label:
          type: string
        valor:
          type: string
          format: decimal
          pattern: ^-?\d{0,12}(?:\.\d{0,2})?$
        value:
          type: string
          format: decimal
          pattern: ^-?\d{0,12}(?:\.\d{0,2})?$
        unidad:
          type: string
          nullable: true
          maxLength: 50
        descripcion:
          type: string
          nullable: true
        icono:
          type: string
          nullable: true
          maxLength: 50
        tipo_medicion:
          $ref: '#/components/schemas/TipoMedicionEnum'
        orden:
          type: integer
          maximum: 9223372036854775807
          minimum: -9223372036854775808
          format: int64
        fecha_corte:
          type: string
          format: date
          nullable: true
      required:
      - edicion
      - id
      - id_indicador
    LegalDocument:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_documento:
          type: string
          format: uuid
          readOnly: true
        tipo:
          allOf:
          - $ref: '#/components/schemas/LegalDocumentTipoEnum'
          readOnly: true
          default: tratamiento_datos
        version:
          type: string
          readOnly: true
          default: '1.0'
        titulo:
          type: string
          readOnly: true
        contenido:
          type: string
          readOnly: true
        vigente:
          type: boolean
          readOnly: true
        fecha_vigencia:
          type: string
          format: date-time
          readOnly: true
      required:
      - contenido
      - fecha_vigencia
      - id
      - id_documento
      - tipo
      - titulo
      - version
      - vigente
    LegalDocumentTipoEnum:
      enum:
      - tratamiento_datos
      - terminos_uso
      - radicacion_caso
      - boletin
      type: string
      description: |-
        * `tratamiento_datos` - Política de tratamiento de datos personales
        * `terminos_uso` - Términos y condiciones de uso
        * `radicacion_caso` - Declaración de veracidad y radicación
        * `boletin` - Consentimiento de suscripción a boletín
    Login:
      type: object
      description: Soporta inicio de sesión por correo o username.
      properties:
        correo:
          type: string
        email:
          type: string
        username:
          type: string
        password:
          type: string
          writeOnly: true
      required:
      - password
    LogoutRequest:
      type: object
      properties:
        refresh:
          type: string
          description: Token JWT refresh opcional para invalidar.
    LogoutResponse:
      type: object
      properties:
        message:
          type: string
        detail:
          type: string
      required:
      - detail
      - message
    MarkMessagesReadPutRequest:
      type: object
      properties:
        message_ids:
          type: array
          items:
            type: string
            format: uuid
          description: Lista opcional de UUIDs de mensajes recibidos a marcar como
            leídos.
        up_to_message_id:
          type: string
          format: uuid
          description: UUID del último mensaje visible en pantalla; marca como leídos
            hasta ese mensaje inclusive.
        up_to_timestamp:
          type: string
          format: date-time
          description: Fecha/hora ISO de corte; excluye mensajes recibidos con fecha
            posterior.
    MarkMessagesReadPutResponse:
      type: object
      properties:
        marked_read:
          type: integer
        unread_remaining:
          type: integer
      required:
      - marked_read
      - unread_remaining
    MarkMessagesReadRequest:
      type: object
      properties:
        message_ids:
          type: array
          items:
            type: string
            format: uuid
          description: Lista opcional de UUIDs de mensajes recibidos a marcar como
            leídos.
        up_to_message_id:
          type: string
          format: uuid
          description: UUID del último mensaje visible en pantalla; marca como leídos
            hasta ese mensaje inclusive.
        up_to_timestamp:
          type: string
          format: date-time
          description: Fecha/hora ISO de corte; excluye mensajes recibidos con fecha
            posterior.
    MarkMessagesReadResponse:
      type: object
      properties:
        marked_read:
          type: integer
        unread_remaining:
          type: integer
      required:
      - marked_read
      - unread_remaining
    MeConversationListResponse:
      type: object
      properties:
        count:
          type: integer
        results:
          type: array
          items:
            $ref: '#/components/schemas/ConversationSummaryItem'
      required:
      - count
      - results
    MePhotoPutRequest:
      type: object
      properties:
        photo:
          type: string
          format: uri
          nullable: true
          description: Archivo de imagen (JPG, PNG o WEBP, máx. 15 MB). También acepta
            el nombre de campo `foto` o `file`.
        foto:
          type: string
          format: uri
          nullable: true
    MePhotoUploadRequest:
      type: object
      properties:
        photo:
          type: string
          format: uri
          nullable: true
          description: Archivo de imagen (JPG, PNG o WEBP, máx. 15 MB). También acepta
            el nombre de campo `foto` o `file`.
        foto:
          type: string
          format: uri
          nullable: true
    Municipality:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_municipio:
          type: string
          format: uuid
          readOnly: true
        departamento:
          type: string
          format: uuid
        id_departamento:
          type: string
          format: uuid
        departamento_nombre:
          type: string
          readOnly: true
        codigo_dane:
          type: string
          pattern: ^[0-9]{5}$
          maxLength: 5
        nombre:
          type: string
          maxLength: 100
        comunidades_count:
          type: integer
          readOnly: true
      required:
      - codigo_dane
      - comunidades_count
      - departamento_nombre
      - id
      - id_municipio
      - nombre
    NaturalezaEnum:
      enum:
      - problematica
      - proyecto_iniciativa
      - otro
      type: string
      description: |-
        * `problematica` - Problemática
        * `proyecto_iniciativa` - Proyecto / Iniciativa
        * `otro` - Otro
    NewsArticleDetail:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_noticia:
          type: string
          format: uuid
          readOnly: true
        titulo:
          type: string
          maxLength: 220
        title:
          type: string
        slug:
          type: string
          readOnly: true
          pattern: ^[-a-zA-Z0-9_]+$
        extracto:
          type: string
        summary:
          type: string
        contenido:
          type: string
        content:
          type: string
        portada:
          type: string
          readOnly: true
        multimedia:
          type: array
          items:
            $ref: '#/components/schemas/NewsMedia'
          readOnly: true
        categoria:
          type: string
          format: uuid
        category:
          type: string
          format: uuid
        categoria_nombre:
          type: string
          readOnly: true
        category_name:
          type: string
          readOnly: true
        iniciativa_relacionada:
          type: string
          format: uuid
          nullable: true
        related_initiative:
          type: string
          format: uuid
          nullable: true
        autor:
          type: string
          format: uuid
          readOnly: true
        autor_nombre:
          type: string
          readOnly: true
        author_name:
          type: string
          readOnly: true
        estado_publicacion:
          $ref: '#/components/schemas/EstadoPublicacion0baEnum'
        publication_status:
          type: string
          writeOnly: true
        destacada:
          type: boolean
        is_featured:
          type: boolean
        fecha_publicacion:
          type: string
          format: date-time
          readOnly: true
          nullable: true
        fecha_creacion:
          type: string
          format: date-time
          readOnly: true
        fecha_actualizacion:
          type: string
          format: date-time
          readOnly: true
      required:
      - author_name
      - autor
      - autor_nombre
      - categoria_nombre
      - category_name
      - fecha_actualizacion
      - fecha_creacion
      - fecha_publicacion
      - id
      - id_noticia
      - multimedia
      - portada
      - slug
    NewsArticleList:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_noticia:
          type: string
          format: uuid
          readOnly: true
        titulo:
          type: string
          readOnly: true
        title:
          type: string
          readOnly: true
        slug:
          type: string
          readOnly: true
          pattern: ^[-a-zA-Z0-9_]+$
        extracto:
          type: string
          readOnly: true
        summary:
          type: string
          readOnly: true
        portada:
          type: string
          readOnly: true
        categoria:
          type: string
          format: uuid
          readOnly: true
        category:
          type: string
          format: uuid
          readOnly: true
        categoria_nombre:
          type: string
          readOnly: true
        category_name:
          type: string
          readOnly: true
        iniciativa_relacionada:
          type: string
          format: uuid
          readOnly: true
          nullable: true
        related_initiative:
          type: string
          format: uuid
          readOnly: true
        related_initiative_name:
          type: string
          readOnly: true
        related_initiative_slug:
          type: string
          readOnly: true
        autor:
          type: string
          format: uuid
          readOnly: true
        author:
          type: string
          format: uuid
          readOnly: true
        autor_nombre:
          type: string
          readOnly: true
        author_name:
          type: string
          readOnly: true
        estado_publicacion:
          allOf:
          - $ref: '#/components/schemas/EstadoPublicacion0baEnum'
          readOnly: true
        publication_status:
          type: string
          readOnly: true
        destacada:
          type: boolean
          readOnly: true
        is_featured:
          type: boolean
          readOnly: true
        fecha_publicacion:
          type: string
          format: date-time
          readOnly: true
          nullable: true
        published_at:
          type: string
          format: date-time
          readOnly: true
        fecha_creacion:
          type: string
          format: date-time
          readOnly: true
        created_at:
          type: string
          format: date-time
          readOnly: true
      required:
      - author
      - author_name
      - autor
      - autor_nombre
      - categoria
      - categoria_nombre
      - category
      - category_name
      - created_at
      - destacada
      - estado_publicacion
      - extracto
      - fecha_creacion
      - fecha_publicacion
      - id
      - id_noticia
      - iniciativa_relacionada
      - is_featured
      - portada
      - publication_status
      - published_at
      - related_initiative
      - related_initiative_name
      - related_initiative_slug
      - slug
      - summary
      - title
      - titulo
    NewsCategory:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_categoria_noticia:
          type: string
          format: uuid
          readOnly: true
        nombre:
          type: string
          maxLength: 120
        name:
          type: string
        slug:
          type: string
          readOnly: true
          pattern: ^[-a-zA-Z0-9_]+$
        descripcion:
          type: string
          nullable: true
        description:
          type: string
        activa:
          type: boolean
        is_active:
          type: boolean
        articles_count:
          type: integer
          readOnly: true
        fecha_creacion:
          type: string
          format: date-time
          readOnly: true
        fecha_actualizacion:
          type: string
          format: date-time
          readOnly: true
      required:
      - articles_count
      - fecha_actualizacion
      - fecha_creacion
      - id
      - id_categoria_noticia
      - slug
    NewsMedia:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_multimedia:
          type: string
          format: uuid
          readOnly: true
        noticia:
          type: string
          format: uuid
        tipo_archivo:
          $ref: '#/components/schemas/TipoArchivo669Enum'
        ruta_archivo:
          type: string
        texto_alternativo:
          type: string
          nullable: true
          maxLength: 250
        descripcion:
          type: string
          nullable: true
        orden:
          type: integer
          maximum: 9223372036854775807
          minimum: -9223372036854775808
          format: int64
        es_portada:
          type: boolean
        fecha_carga:
          type: string
          format: date-time
          readOnly: true
      required:
      - fecha_carga
      - id
      - id_multimedia
      - noticia
      - ruta_archivo
    NewsletterSubscription:
      type: object
      description: 'PUB-09 (AMP-02): POST /api/v1/public/newsletter-subscriptions/'
      properties:
        nombre:
          type: string
          maxLength: 150
        correo:
          type: string
          format: email
          maxLength: 150
        email:
          type: string
          format: email
          maxLength: 150
        acepta_tratamiento_datos:
          type: boolean
          default: true
    NewsletterTokenAction:
      type: object
      description: 'PUB-10 y PUB-11: Confirmación o baja de boletín.'
      properties:
        token:
          type: string
        correo:
          type: string
          format: email
        email:
          type: string
          format: email
    Notification:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_notificacion:
          type: string
          format: uuid
          readOnly: true
        usuario:
          type: string
          format: uuid
          readOnly: true
        caso:
          type: string
          format: uuid
          readOnly: true
          nullable: true
        caso_codigo:
          type: string
          readOnly: true
        titulo:
          type: string
          readOnly: true
        mensaje:
          type: string
          readOnly: true
        tipo:
          type: string
          readOnly: true
        leida:
          type: boolean
          readOnly: true
        fecha_creacion:
          type: string
          format: date-time
          readOnly: true
      required:
      - caso
      - caso_codigo
      - fecha_creacion
      - id
      - id_notificacion
      - leida
      - mensaje
      - tipo
      - titulo
      - usuario
    PaginatedAdminCaseDetailList:
      type: object
      required:
      - count
      - results
      properties:
        count:
          type: integer
          example: 123
        next:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=4
        previous:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=2
        results:
          type: array
          items:
            $ref: '#/components/schemas/AdminCaseDetail'
    PaginatedAdminEventProposalList:
      type: object
      required:
      - count
      - results
      properties:
        count:
          type: integer
          example: 123
        next:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=4
        previous:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=2
        results:
          type: array
          items:
            $ref: '#/components/schemas/AdminEventProposal'
    PaginatedAdminInitiativeList:
      type: object
      required:
      - count
      - results
      properties:
        count:
          type: integer
          example: 123
        next:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=4
        previous:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=2
        results:
          type: array
          items:
            $ref: '#/components/schemas/AdminInitiative'
    PaginatedAdminUserCreateUpdateList:
      type: object
      required:
      - count
      - results
      properties:
        count:
          type: integer
          example: 123
        next:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=4
        previous:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=2
        results:
          type: array
          items:
            $ref: '#/components/schemas/AdminUserCreateUpdate'
    PaginatedAuditLogList:
      type: object
      required:
      - count
      - results
      properties:
        count:
          type: integer
          example: 123
        next:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=4
        previous:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=2
        results:
          type: array
          items:
            $ref: '#/components/schemas/AuditLog'
    PaginatedCaseCategoryList:
      type: object
      required:
      - count
      - results
      properties:
        count:
          type: integer
          example: 123
        next:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=4
        previous:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=2
        results:
          type: array
          items:
            $ref: '#/components/schemas/CaseCategory'
    PaginatedCaseCommentList:
      type: object
      required:
      - count
      - results
      properties:
        count:
          type: integer
          example: 123
        next:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=4
        previous:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=2
        results:
          type: array
          items:
            $ref: '#/components/schemas/CaseComment'
    PaginatedCaseContributionList:
      type: object
      required:
      - count
      - results
      properties:
        count:
          type: integer
          example: 123
        next:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=4
        previous:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=2
        results:
          type: array
          items:
            $ref: '#/components/schemas/CaseContribution'
    PaginatedCaseEvidenceList:
      type: object
      required:
      - count
      - results
      properties:
        count:
          type: integer
          example: 123
        next:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=4
        previous:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=2
        results:
          type: array
          items:
            $ref: '#/components/schemas/CaseEvidence'
    PaginatedCitizenCaseCreateUpdateList:
      type: object
      required:
      - count
      - results
      properties:
        count:
          type: integer
          example: 123
        next:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=4
        previous:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=2
        results:
          type: array
          items:
            $ref: '#/components/schemas/CitizenCaseCreateUpdate'
    PaginatedCommunityList:
      type: object
      required:
      - count
      - results
      properties:
        count:
          type: integer
          example: 123
        next:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=4
        previous:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=2
        results:
          type: array
          items:
            $ref: '#/components/schemas/Community'
    PaginatedDepartmentList:
      type: object
      required:
      - count
      - results
      properties:
        count:
          type: integer
          example: 123
        next:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=4
        previous:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=2
        results:
          type: array
          items:
            $ref: '#/components/schemas/Department'
    PaginatedInitiativeActivityList:
      type: object
      required:
      - count
      - results
      properties:
        count:
          type: integer
          example: 123
        next:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=4
        previous:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=2
        results:
          type: array
          items:
            $ref: '#/components/schemas/InitiativeActivity'
    PaginatedInitiativeCaseLinkList:
      type: object
      required:
      - count
      - results
      properties:
        count:
          type: integer
          example: 123
        next:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=4
        previous:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=2
        results:
          type: array
          items:
            $ref: '#/components/schemas/InitiativeCaseLink'
    PaginatedInitiativeCommunityList:
      type: object
      required:
      - count
      - results
      properties:
        count:
          type: integer
          example: 123
        next:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=4
        previous:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=2
        results:
          type: array
          items:
            $ref: '#/components/schemas/InitiativeCommunity'
    PaginatedInitiativeEditionList:
      type: object
      required:
      - count
      - results
      properties:
        count:
          type: integer
          example: 123
        next:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=4
        previous:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=2
        results:
          type: array
          items:
            $ref: '#/components/schemas/InitiativeEdition'
    PaginatedInitiativeListList:
      type: object
      required:
      - count
      - results
      properties:
        count:
          type: integer
          example: 123
        next:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=4
        previous:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=2
        results:
          type: array
          items:
            $ref: '#/components/schemas/InitiativeList'
    PaginatedInitiativeMediaList:
      type: object
      required:
      - count
      - results
      properties:
        count:
          type: integer
          example: 123
        next:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=4
        previous:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=2
        results:
          type: array
          items:
            $ref: '#/components/schemas/InitiativeMedia'
    PaginatedInitiativeMetricList:
      type: object
      required:
      - count
      - results
      properties:
        count:
          type: integer
          example: 123
        next:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=4
        previous:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=2
        results:
          type: array
          items:
            $ref: '#/components/schemas/InitiativeMetric'
    PaginatedMunicipalityList:
      type: object
      required:
      - count
      - results
      properties:
        count:
          type: integer
          example: 123
        next:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=4
        previous:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=2
        results:
          type: array
          items:
            $ref: '#/components/schemas/Municipality'
    PaginatedNewsArticleDetailList:
      type: object
      required:
      - count
      - results
      properties:
        count:
          type: integer
          example: 123
        next:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=4
        previous:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=2
        results:
          type: array
          items:
            $ref: '#/components/schemas/NewsArticleDetail'
    PaginatedNewsArticleListList:
      type: object
      required:
      - count
      - results
      properties:
        count:
          type: integer
          example: 123
        next:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=4
        previous:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=2
        results:
          type: array
          items:
            $ref: '#/components/schemas/NewsArticleList'
    PaginatedNewsCategoryList:
      type: object
      required:
      - count
      - results
      properties:
        count:
          type: integer
          example: 123
        next:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=4
        previous:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=2
        results:
          type: array
          items:
            $ref: '#/components/schemas/NewsCategory'
    PaginatedNewsMediaList:
      type: object
      required:
      - count
      - results
      properties:
        count:
          type: integer
          example: 123
        next:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=4
        previous:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=2
        results:
          type: array
          items:
            $ref: '#/components/schemas/NewsMedia'
    PaginatedNotificationList:
      type: object
      required:
      - count
      - results
      properties:
        count:
          type: integer
          example: 123
        next:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=4
        previous:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=2
        results:
          type: array
          items:
            $ref: '#/components/schemas/Notification'
    PaginatedPublicCaseCommentList:
      type: object
      required:
      - count
      - results
      properties:
        count:
          type: integer
          example: 123
        next:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=4
        previous:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=2
        results:
          type: array
          items:
            $ref: '#/components/schemas/PublicCaseComment'
    PaginatedPublicCaseListList:
      type: object
      required:
      - count
      - results
      properties:
        count:
          type: integer
          example: 123
        next:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=4
        previous:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=2
        results:
          type: array
          items:
            $ref: '#/components/schemas/PublicCaseList'
    PaginatedResponsibleScopeAssignmentList:
      type: object
      required:
      - count
      - results
      properties:
        count:
          type: integer
          example: 123
        next:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=4
        previous:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=2
        results:
          type: array
          items:
            $ref: '#/components/schemas/ResponsibleScopeAssignment'
    PaginatedRoleList:
      type: object
      required:
      - count
      - results
      properties:
        count:
          type: integer
          example: 123
        next:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=4
        previous:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=2
        results:
          type: array
          items:
            $ref: '#/components/schemas/Role'
    PaginatedSiteSettingList:
      type: object
      required:
      - count
      - results
      properties:
        count:
          type: integer
          example: 123
        next:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=4
        previous:
          type: string
          nullable: true
          format: uri
          example: http://api.example.org/accounts/?page=2
        results:
          type: array
          items:
            $ref: '#/components/schemas/SiteSetting'
    PasswordResetConfirm:
      type: object
      properties:
        uid:
          type: string
          description: Identificador base64 del usuario (opcional si token viene en
            formato <uid>.<token>).
        token:
          type: string
          description: Token de recuperación o cadena compuesta <uid>.<token>.
        new_password:
          type: string
          writeOnly: true
          minLength: 8
        new_password_confirm:
          type: string
          writeOnly: true
          minLength: 8
      required:
      - new_password
      - token
    PasswordResetConfirmResponse:
      type: object
      properties:
        message:
          type: string
        detail:
          type: string
      required:
      - detail
      - message
    PasswordResetRequest:
      type: object
      properties:
        correo:
          type: string
          format: email
        email:
          type: string
          format: email
    PasswordResetRequestResponse:
      type: object
      properties:
        message:
          type: string
        detail:
          type: string
      required:
      - detail
      - message
    PasswordResetValidate:
      type: object
      properties:
        uid:
          type: string
          description: Identificador base64 del usuario (opcional si token viene en
            formato <uid>.<token>).
        token:
          type: string
          description: Token de recuperación o cadena compuesta <uid>.<token>.
      required:
      - token
    PasswordResetValidateResponse:
      type: object
      properties:
        valid:
          type: boolean
      required:
      - valid
    PatchedAdminCaseDetail:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_caso:
          type: string
          format: uuid
          readOnly: true
        codigo:
          type: string
          readOnly: true
        radicado_code:
          type: string
          readOnly: true
        titulo:
          type: string
          maxLength: 200
        descripcion:
          type: string
        usuario:
          type: string
          format: uuid
          readOnly: true
        usuario_nombre:
          type: string
          readOnly: true
        usuario_correo:
          type: string
          readOnly: true
        usuario_telefono:
          type: string
          readOnly: true
        tipo_caso:
          type: string
          format: uuid
        tipo_nombre:
          type: string
          readOnly: true
        tipo_categoria:
          type: string
          readOnly: true
        tipo_naturaleza:
          type: string
          readOnly: true
        comunidad:
          type: string
          format: uuid
        comunidad_nombre:
          type: string
          readOnly: true
        id_municipio:
          type: string
          format: uuid
          readOnly: true
        municipio_nombre:
          type: string
          readOnly: true
        id_departamento:
          type: string
          format: uuid
          readOnly: true
        departamento_nombre:
          type: string
          readOnly: true
        estado:
          type: string
          format: uuid
        estado_nombre:
          type: string
          readOnly: true
        management_status:
          type: string
          readOnly: true
        prioridad:
          $ref: '#/components/schemas/PrioridadEnum'
        estado_publicacion:
          $ref: '#/components/schemas/EstadoPublicacionE6cEnum'
        moderation_status:
          type: string
          readOnly: true
        ubicacion:
          type: string
          nullable: true
          description: Coordenada geográfica PostGIS geometry(Point, 4326)
        direccion_referencia:
          type: string
          nullable: true
        familias_afectadas:
          type: integer
          maximum: 9223372036854775807
          minimum: 0
          format: int64
          nullable: true
        meses_afectacion:
          type: integer
          maximum: 9223372036854775807
          minimum: 0
          format: int64
          nullable: true
        resultado_resumen:
          type: string
          nullable: true
        seguimiento_resolucion:
          type: string
          format: uuid
          nullable: true
        usuario_resolucion:
          type: string
          format: uuid
          nullable: true
        fecha_resolucion:
          type: string
          format: date-time
          nullable: true
        active_assignment:
          allOf:
          - $ref: '#/components/schemas/CaseAssignment'
          readOnly: true
        active_correction_request:
          allOf:
          - $ref: '#/components/schemas/CaseCorrectionRequest'
          readOnly: true
        solicitudes_correccion:
          type: array
          items:
            $ref: '#/components/schemas/CaseCorrectionRequest'
          readOnly: true
        aportes:
          type: array
          items:
            $ref: '#/components/schemas/CaseContribution'
          readOnly: true
        asignaciones:
          type: array
          items:
            $ref: '#/components/schemas/CaseAssignment'
          readOnly: true
        seguimientos:
          type: array
          items:
            $ref: '#/components/schemas/CaseUpdate'
          readOnly: true
        historial_estados:
          type: array
          items:
            $ref: '#/components/schemas/CaseStatusHistory'
          readOnly: true
        evidencias:
          type: array
          items:
            $ref: '#/components/schemas/CaseEvidence'
          readOnly: true
        allowed_actions:
          type: array
          items:
            type: string
          readOnly: true
        fecha_creacion:
          type: string
          format: date-time
          readOnly: true
        fecha_actualizacion:
          type: string
          format: date-time
          readOnly: true
        fecha_aprobacion:
          type: string
          format: date-time
          nullable: true
    PatchedAdminEventProposal:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_propuesta:
          type: string
          format: uuid
          readOnly: true
        usuario:
          type: string
          format: uuid
          readOnly: true
          nullable: true
        comunidad:
          type: string
          format: uuid
          nullable: true
        id_comunidad:
          type: string
          format: uuid
          nullable: true
        comunidad_nombre:
          type: string
          readOnly: true
        nombre_contacto:
          type: string
          nullable: true
          maxLength: 150
        telefono_contacto:
          type: string
          nullable: true
          maxLength: 25
        comunidad_declarada:
          type: string
          nullable: true
          maxLength: 200
        acepta_tratamiento_datos:
          type: boolean
        iniciativa_solicitada:
          type: string
          format: uuid
          nullable: true
        iniciativa_generada:
          type: string
          format: uuid
          nullable: true
        titulo:
          type: string
          maxLength: 200
        descripcion:
          type: string
        tipo_actividad:
          type: string
          nullable: true
          maxLength: 80
        fecha_sugerida:
          type: string
          format: date
          nullable: true
        estado:
          $ref: '#/components/schemas/Estado5feEnum'
        respuesta:
          type: string
          nullable: true
        revisor:
          type: string
          format: uuid
          readOnly: true
          nullable: true
        fecha_creacion:
          type: string
          format: date-time
          readOnly: true
        fecha_revision:
          type: string
          format: date-time
          nullable: true
    PatchedAdminInitiative:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_iniciativa:
          type: string
          format: uuid
          readOnly: true
        creador:
          type: string
          format: uuid
          readOnly: true
        titulo:
          type: string
          maxLength: 200
        name:
          type: string
        subtitulo:
          type: string
          nullable: true
          maxLength: 250
        featured_title:
          type: string
        slug:
          type: string
          readOnly: true
          pattern: ^[-a-zA-Z0-9_]+$
        descripcion_corta:
          type: string
          nullable: true
        short_description:
          type: string
        descripcion:
          type: string
          nullable: true
        full_content:
          type: string
        categoria:
          type: string
          maxLength: 80
        category:
          type: string
        estado:
          $ref: '#/components/schemas/EstadoC21Enum'
        estado_publicacion:
          $ref: '#/components/schemas/EstadoPublicacion653Enum'
        publication_status:
          type: string
          writeOnly: true
        destacada:
          type: boolean
        is_featured:
          type: boolean
        orden_destacado:
          type: integer
          maximum: 9223372036854775807
          minimum: -9223372036854775808
          format: int64
          nullable: true
        ediciones:
          type: array
          items:
            $ref: '#/components/schemas/InitiativeEdition'
          readOnly: true
        multimedia:
          type: array
          items:
            $ref: '#/components/schemas/InitiativeMedia'
          readOnly: true
        fecha_creacion:
          type: string
          format: date-time
          readOnly: true
        fecha_actualizacion:
          type: string
          format: date-time
          readOnly: true
        fecha_publicacion:
          type: string
          format: date-time
          readOnly: true
          nullable: true
    PatchedAdminUserCreateUpdate:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_usuario:
          type: string
          format: uuid
          readOnly: true
        rol:
          type: string
          format: uuid
        id_rol:
          type: string
          format: uuid
        rol_nombre:
          type: string
          writeOnly: true
        nombres:
          type: string
          maxLength: 100
        apellidos:
          type: string
          maxLength: 100
        correo:
          type: string
          format: email
          maxLength: 150
        password:
          type: string
          writeOnly: true
          minLength: 8
        telefono:
          type: string
          nullable: true
          maxLength: 20
        estado:
          $ref: '#/components/schemas/Estado6c7Enum'
        primary_role:
          type: string
          readOnly: true
        roles:
          type: array
          items:
            type: string
          readOnly: true
        fecha_registro:
          type: string
          format: date-time
          readOnly: true
        fecha_actualizacion:
          type: string
          format: date-time
          readOnly: true
    PatchedAdminUserStatus:
      type: object
      description: 'USR-06: PATCH /admin/users/{id}/status/ con estado de tres valores.'
      properties:
        estado:
          $ref: '#/components/schemas/Estado6c7Enum'
        motivo:
          type: string
          default: ''
    PatchedCaseCategory:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_tipo_caso:
          type: string
          format: uuid
          readOnly: true
        nombre:
          type: string
          maxLength: 100
        descripcion:
          type: string
          nullable: true
        categoria:
          type: string
          default: general
          maxLength: 50
        naturaleza:
          $ref: '#/components/schemas/NaturalezaEnum'
        activo:
          type: boolean
        casos_count:
          type: integer
          readOnly: true
    PatchedCaseEvidence:
      type: object
      description: |-
        Serializador de evidencias de caso (CIT-06, ADM-05).
        Soporta subida multipart mediante el campo `file` o `archivo` (máximo 15 MB; JPG, PNG, WEBP, PDF, MP4, MP3, DOC/X, XLS/X),
        o referencia interna `ruta_archivo`.
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_evidencia:
          type: string
          format: uuid
          readOnly: true
        caso:
          type: string
          format: uuid
          readOnly: true
        usuario:
          type: string
          format: uuid
          readOnly: true
        usuario_nombre:
          type: string
          readOnly: true
        id_aporte:
          type: string
          format: uuid
          readOnly: true
        file:
          type: string
          format: uri
          nullable: true
          writeOnly: true
        archivo:
          type: string
          format: uri
          nullable: true
          writeOnly: true
        tipo_archivo:
          $ref: '#/components/schemas/CaseEvidenceTipoArchivoEnum'
        ruta_archivo:
          type: string
        download_url:
          type: string
          readOnly: true
        descripcion:
          type: string
          nullable: true
        audiencia:
          $ref: '#/components/schemas/AudienciaFebEnum'
        estado_revision:
          $ref: '#/components/schemas/EstadoRevisionEnum'
        nombre_original:
          type: string
          nullable: true
          maxLength: 255
        mime_type:
          type: string
          nullable: true
          maxLength: 100
        tamano_bytes:
          type: integer
          maximum: 9223372036854775807
          minimum: -9223372036854775808
          format: int64
          nullable: true
        fecha_subida:
          type: string
          format: date-time
          readOnly: true
    PatchedCaseEvidenceUpdate:
      type: object
      description: 'ADM-11 (AMP-10): PATCH /api/v1/admin/cases/{case_id}/evidence/{evidence_id}/'
      properties:
        descripcion:
          type: string
          nullable: true
        audiencia:
          $ref: '#/components/schemas/AudienciaFebEnum'
        estado_revision:
          $ref: '#/components/schemas/EstadoRevisionEnum'
    PatchedCitizenCaseCreateUpdate:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_caso:
          type: string
          format: uuid
          readOnly: true
        codigo:
          type: string
          readOnly: true
        radicado_code:
          type: string
          readOnly: true
        titulo:
          type: string
          maxLength: 200
        title:
          type: string
        descripcion:
          type: string
        description:
          type: string
        tipo_caso:
          type: string
          format: uuid
        id_tipo_caso:
          type: string
          format: uuid
        tipo_nombre:
          type: string
          readOnly: true
        category:
          type: string
          format: uuid
        comunidad:
          type: string
          format: uuid
        id_comunidad:
          type: string
          format: uuid
        comunidad_nombre:
          type: string
          readOnly: true
        municipio_nombre:
          type: string
          readOnly: true
        departamento_nombre:
          type: string
          readOnly: true
        community:
          type: string
          format: uuid
        estado:
          type: string
          format: uuid
          readOnly: true
        estado_nombre:
          type: string
          readOnly: true
        management_status:
          type: string
          readOnly: true
        prioridad:
          $ref: '#/components/schemas/PrioridadEnum'
        estado_publicacion:
          allOf:
          - $ref: '#/components/schemas/EstadoPublicacionE6cEnum'
          readOnly: true
        moderation_status:
          type: string
          readOnly: true
        ubicacion:
          type: string
          nullable: true
          description: Coordenada geográfica PostGIS geometry(Point, 4326)
        exact_latitude:
          type: string
          format: decimal
          pattern: ^-?\d{0,3}(?:\.\d{0,6})?$
          writeOnly: true
        exact_longitude:
          type: string
          format: decimal
          pattern: ^-?\d{0,3}(?:\.\d{0,6})?$
          writeOnly: true
        latitud:
          type: string
          format: decimal
          pattern: ^-?\d{0,3}(?:\.\d{0,6})?$
          writeOnly: true
        longitud:
          type: string
          format: decimal
          pattern: ^-?\d{0,3}(?:\.\d{0,6})?$
          writeOnly: true
        direccion_referencia:
          type: string
          nullable: true
        familias_afectadas:
          type: integer
          maximum: 9223372036854775807
          minimum: 0
          format: int64
          nullable: true
        meses_afectacion:
          type: integer
          maximum: 9223372036854775807
          minimum: 0
          format: int64
          nullable: true
        resultado_resumen:
          type: string
          readOnly: true
          nullable: true
        fecha_resolucion:
          type: string
          format: date-time
          readOnly: true
          nullable: true
        acepta_tratamiento_datos:
          type: boolean
          writeOnly: true
          default: true
        accepts_data_policy:
          type: boolean
          writeOnly: true
          default: true
        active_assignment:
          allOf:
          - $ref: '#/components/schemas/CaseAssignment'
          readOnly: true
        active_correction_request:
          allOf:
          - $ref: '#/components/schemas/CaseCorrectionRequest'
          readOnly: true
        solicitudes_correccion:
          type: array
          items:
            $ref: '#/components/schemas/CaseCorrectionRequest'
          readOnly: true
        aportes:
          type: array
          items:
            $ref: '#/components/schemas/CaseContribution'
          readOnly: true
        seguimientos:
          type: string
          readOnly: true
        evidencias:
          type: string
          readOnly: true
        allowed_actions:
          type: array
          items:
            type: string
          readOnly: true
        fecha_creacion:
          type: string
          format: date-time
          readOnly: true
        fecha_actualizacion:
          type: string
          format: date-time
          readOnly: true
        fecha_aprobacion:
          type: string
          format: date-time
          readOnly: true
          nullable: true
    PatchedCommunity:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_comunidad:
          type: string
          format: uuid
          readOnly: true
        municipio:
          type: string
          format: uuid
        id_municipio:
          type: string
          format: uuid
        municipio_nombre:
          type: string
          readOnly: true
        nombre:
          type: string
          maxLength: 150
        descripcion:
          type: string
          nullable: true
        tipo:
          allOf:
          - $ref: '#/components/schemas/CommunityTipoEnum'
          default: vereda
        tipo_display:
          type: string
          readOnly: true
        ubicacion:
          type: string
          nullable: true
          description: Perímetro opcional geometry(MultiPolygon, 4326)
        activo:
          type: boolean
    PatchedDepartment:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_departamento:
          type: string
          format: uuid
          readOnly: true
        codigo_dane:
          type: string
          pattern: ^[0-9]{2}$
          maxLength: 2
        nombre:
          type: string
          maxLength: 100
        municipios:
          type: array
          items:
            $ref: '#/components/schemas/Municipality'
          readOnly: true
    PatchedInitiativeActivity:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_actividad:
          type: string
          format: uuid
          readOnly: true
        edicion:
          type: string
          format: uuid
        responsable:
          type: string
          format: uuid
          nullable: true
        responsable_nombre:
          type: string
          readOnly: true
        comunidad:
          type: string
          format: uuid
          nullable: true
        comunidad_nombre:
          type: string
          readOnly: true
        titulo:
          type: string
          maxLength: 200
        descripcion:
          type: string
          nullable: true
        fecha_inicio:
          type: string
          format: date-time
        fecha_fin:
          type: string
          format: date-time
          nullable: true
        lugar:
          type: string
          nullable: true
          maxLength: 200
        ubicacion:
          type: string
          nullable: true
          description: Coordenada geográfica PostGIS geometry(Point, 4326)
        estado:
          $ref: '#/components/schemas/InitiativeActivityEstadoEnum'
        fecha_creacion:
          type: string
          format: date-time
          readOnly: true
    PatchedInitiativeCaseLink:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        edicion:
          type: string
          format: uuid
        caso:
          type: string
          format: uuid
        caso_codigo:
          type: string
          readOnly: true
        tipo_vinculo:
          $ref: '#/components/schemas/TipoVinculoEnum'
        observaciones:
          type: string
          nullable: true
        fecha_vinculacion:
          type: string
          format: date-time
    PatchedInitiativeCommunity:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        edicion:
          type: string
          format: uuid
        comunidad:
          type: string
          format: uuid
        comunidad_nombre:
          type: string
          readOnly: true
        observaciones:
          type: string
          nullable: true
    PatchedInitiativeEdition:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_edicion:
          type: string
          format: uuid
          readOnly: true
        iniciativa:
          type: string
          format: uuid
        anio:
          type: integer
          maximum: 9223372036854775807
          minimum: -9223372036854775808
          format: int64
        nombre_edicion:
          type: string
          nullable: true
          maxLength: 150
        temporada:
          type: string
          nullable: true
          maxLength: 100
        descripcion:
          type: string
          nullable: true
        fecha_inicio:
          type: string
          format: date
          nullable: true
        fecha_fin:
          type: string
          format: date
          nullable: true
        estado:
          $ref: '#/components/schemas/EstadoC21Enum'
        indicadores:
          type: array
          items:
            $ref: '#/components/schemas/InitiativeMetric'
          readOnly: true
        actividades:
          type: array
          items:
            $ref: '#/components/schemas/InitiativeActivity'
          readOnly: true
        comunidades_vinculadas:
          type: array
          items:
            $ref: '#/components/schemas/InitiativeCommunity'
          readOnly: true
        casos_vinculados:
          type: array
          items:
            $ref: '#/components/schemas/InitiativeCaseLink'
          readOnly: true
        fecha_creacion:
          type: string
          format: date-time
          readOnly: true
    PatchedInitiativeMedia:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_multimedia:
          type: string
          format: uuid
          readOnly: true
        iniciativa:
          type: string
          format: uuid
        edicion:
          type: string
          format: uuid
          nullable: true
        tipo:
          $ref: '#/components/schemas/Tipo669Enum'
        ruta_archivo:
          type: string
        texto_alternativo:
          type: string
          nullable: true
        descripcion:
          type: string
          nullable: true
        es_portada:
          type: boolean
        orden:
          type: integer
          maximum: 9223372036854775807
          minimum: -9223372036854775808
          format: int64
        fecha_subida:
          type: string
          format: date-time
          readOnly: true
    PatchedInitiativeMetric:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_indicador:
          type: string
          format: uuid
          readOnly: true
        edicion:
          type: string
          format: uuid
        nombre:
          type: string
          maxLength: 100
        label:
          type: string
        valor:
          type: string
          format: decimal
          pattern: ^-?\d{0,12}(?:\.\d{0,2})?$
        value:
          type: string
          format: decimal
          pattern: ^-?\d{0,12}(?:\.\d{0,2})?$
        unidad:
          type: string
          nullable: true
          maxLength: 50
        descripcion:
          type: string
          nullable: true
        icono:
          type: string
          nullable: true
          maxLength: 50
        tipo_medicion:
          $ref: '#/components/schemas/TipoMedicionEnum'
        orden:
          type: integer
          maximum: 9223372036854775807
          minimum: -9223372036854775808
          format: int64
        fecha_corte:
          type: string
          format: date
          nullable: true
    PatchedMunicipality:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_municipio:
          type: string
          format: uuid
          readOnly: true
        departamento:
          type: string
          format: uuid
        id_departamento:
          type: string
          format: uuid
        departamento_nombre:
          type: string
          readOnly: true
        codigo_dane:
          type: string
          pattern: ^[0-9]{5}$
          maxLength: 5
        nombre:
          type: string
          maxLength: 100
        comunidades_count:
          type: integer
          readOnly: true
    PatchedNewsArticleDetail:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_noticia:
          type: string
          format: uuid
          readOnly: true
        titulo:
          type: string
          maxLength: 220
        title:
          type: string
        slug:
          type: string
          readOnly: true
          pattern: ^[-a-zA-Z0-9_]+$
        extracto:
          type: string
        summary:
          type: string
        contenido:
          type: string
        content:
          type: string
        portada:
          type: string
          readOnly: true
        multimedia:
          type: array
          items:
            $ref: '#/components/schemas/NewsMedia'
          readOnly: true
        categoria:
          type: string
          format: uuid
        category:
          type: string
          format: uuid
        categoria_nombre:
          type: string
          readOnly: true
        category_name:
          type: string
          readOnly: true
        iniciativa_relacionada:
          type: string
          format: uuid
          nullable: true
        related_initiative:
          type: string
          format: uuid
          nullable: true
        autor:
          type: string
          format: uuid
          readOnly: true
        autor_nombre:
          type: string
          readOnly: true
        author_name:
          type: string
          readOnly: true
        estado_publicacion:
          $ref: '#/components/schemas/EstadoPublicacion0baEnum'
        publication_status:
          type: string
          writeOnly: true
        destacada:
          type: boolean
        is_featured:
          type: boolean
        fecha_publicacion:
          type: string
          format: date-time
          readOnly: true
          nullable: true
        fecha_creacion:
          type: string
          format: date-time
          readOnly: true
        fecha_actualizacion:
          type: string
          format: date-time
          readOnly: true
    PatchedNewsCategory:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_categoria_noticia:
          type: string
          format: uuid
          readOnly: true
        nombre:
          type: string
          maxLength: 120
        name:
          type: string
        slug:
          type: string
          readOnly: true
          pattern: ^[-a-zA-Z0-9_]+$
        descripcion:
          type: string
          nullable: true
        description:
          type: string
        activa:
          type: boolean
        is_active:
          type: boolean
        articles_count:
          type: integer
          readOnly: true
        fecha_creacion:
          type: string
          format: date-time
          readOnly: true
        fecha_actualizacion:
          type: string
          format: date-time
          readOnly: true
    PatchedNewsMedia:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_multimedia:
          type: string
          format: uuid
          readOnly: true
        noticia:
          type: string
          format: uuid
        tipo_archivo:
          $ref: '#/components/schemas/TipoArchivo669Enum'
        ruta_archivo:
          type: string
        texto_alternativo:
          type: string
          nullable: true
          maxLength: 250
        descripcion:
          type: string
          nullable: true
        orden:
          type: integer
          maximum: 9223372036854775807
          minimum: -9223372036854775808
          format: int64
        es_portada:
          type: boolean
        fecha_carga:
          type: string
          format: date-time
          readOnly: true
    PatchedNotification:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_notificacion:
          type: string
          format: uuid
          readOnly: true
        usuario:
          type: string
          format: uuid
          readOnly: true
        caso:
          type: string
          format: uuid
          readOnly: true
          nullable: true
        caso_codigo:
          type: string
          readOnly: true
        titulo:
          type: string
          readOnly: true
        mensaje:
          type: string
          readOnly: true
        tipo:
          type: string
          readOnly: true
        leida:
          type: boolean
          readOnly: true
        fecha_creacion:
          type: string
          format: date-time
          readOnly: true
    PatchedResponsibleScopeAssignment:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_asignacion:
          type: string
          format: uuid
          readOnly: true
        usuario:
          type: string
          format: uuid
        comunidad:
          type: string
          format: uuid
          nullable: true
        comunidad_nombre:
          type: string
          readOnly: true
        tipo_caso:
          type: string
          format: uuid
          nullable: true
        tipo_caso_nombre:
          type: string
          readOnly: true
        fecha_asignacion:
          type: string
          format: date-time
          readOnly: true
        activo:
          type: boolean
    PatchedRole:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_rol:
          type: string
          format: uuid
          readOnly: true
        nombre:
          type: string
          maxLength: 50
        descripcion:
          type: string
          nullable: true
        assignable:
          type: boolean
          readOnly: true
    PatchedSiteSetting:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_configuracion:
          type: string
          format: uuid
          readOnly: true
        clave:
          type: string
          maxLength: 100
        key:
          type: string
        valor: {}
        value: {}
        fecha_actualizacion:
          type: string
          format: date-time
          readOnly: true
    PatchedUserMe:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_usuario:
          type: string
          format: uuid
          readOnly: true
        id_rol:
          type: string
          format: uuid
          readOnly: true
        rol_nombre:
          type: string
          readOnly: true
        nombres:
          type: string
          maxLength: 100
        apellidos:
          type: string
          maxLength: 100
        full_name:
          type: string
          readOnly: true
        correo:
          type: string
          format: email
          maxLength: 150
        telefono:
          type: string
          nullable: true
          maxLength: 20
        estado:
          allOf:
          - $ref: '#/components/schemas/Estado6c7Enum'
          readOnly: true
        primary_role:
          type: string
          readOnly: true
        roles:
          type: array
          items:
            type: string
          readOnly: true
        permissions:
          type: object
          additionalProperties: {}
          readOnly: true
        perfil:
          type: object
          additionalProperties: {}
          readOnly: true
        preferencias:
          type: object
          additionalProperties: {}
          readOnly: true
        ambitos_responsable:
          type: array
          items:
            $ref: '#/components/schemas/ResponsibleScopeAssignment'
          readOnly: true
        id_departamento:
          type: string
          format: uuid
          writeOnly: true
          nullable: true
        id_municipio:
          type: string
          format: uuid
          writeOnly: true
          nullable: true
        id_comunidad:
          type: string
          format: uuid
          writeOnly: true
          nullable: true
        fecha_registro:
          type: string
          format: date-time
          readOnly: true
        fecha_actualizacion:
          type: string
          format: date-time
          readOnly: true
    PatchedUserPreference:
      type: object
      properties:
        id_preferencia:
          type: string
          format: uuid
          readOnly: true
        notificar_novedades_casos:
          type: boolean
        notificar_avance_casos:
          type: boolean
          description: Alias de notificar_novedades_casos.
        notificar_mensajes:
          type: boolean
        suscrito_boletin:
          type: boolean
        recibir_boletin:
          type: boolean
          description: Alias de suscrito_boletin.
        fecha_actualizacion:
          type: string
          format: date-time
          readOnly: true
    PrioridadEnum:
      enum:
      - baja
      - media
      - alta
      - critica
      type: string
      description: |-
        * `baja` - Baja
        * `media` - Media
        * `alta` - Alta
        * `critica` - Crítica
    PublicCaseCategoryNamesResponse:
      type: object
      properties:
        categories:
          type: array
          items:
            type: string
        tipos_caso:
          type: array
          items:
            $ref: '#/components/schemas/CaseCategory'
      required:
      - categories
      - tipos_caso
    PublicCaseComment:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_comentario:
          type: string
          format: uuid
          readOnly: true
        autor_nombre:
          type: string
          readOnly: true
        contenido:
          type: string
          readOnly: true
        fecha_creacion:
          type: string
          format: date-time
          readOnly: true
      required:
      - autor_nombre
      - contenido
      - fecha_creacion
      - id
      - id_comentario
    PublicCaseDetail:
      type: object
      description: |-
        Serializador público para casos aprobados (`estado_publicacion='aprobado'`).
        No expone datos personales del ciudadano (`id_usuario`) y devuelve coordenadas generalizadas.
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_caso:
          type: string
          format: uuid
          readOnly: true
        codigo:
          type: string
          readOnly: true
        radicado_code:
          type: string
          readOnly: true
        titulo:
          type: string
          readOnly: true
        tipo_caso:
          type: string
          format: uuid
          readOnly: true
        tipo_nombre:
          type: string
          readOnly: true
        tipo_categoria:
          type: string
          readOnly: true
        tipo_naturaleza:
          type: string
          readOnly: true
        comunidad:
          type: string
          format: uuid
          readOnly: true
        comunidad_nombre:
          type: string
          readOnly: true
        id_municipio:
          type: string
          format: uuid
          readOnly: true
        municipio_nombre:
          type: string
          readOnly: true
        id_departamento:
          type: string
          format: uuid
          readOnly: true
        departamento_nombre:
          type: string
          readOnly: true
        estado:
          type: string
          format: uuid
          readOnly: true
        estado_nombre:
          type: string
          readOnly: true
        prioridad:
          allOf:
          - $ref: '#/components/schemas/PrioridadEnum'
          readOnly: true
        estado_publicacion:
          allOf:
          - $ref: '#/components/schemas/EstadoPublicacionE6cEnum'
          readOnly: true
        familias_afectadas:
          type: integer
          readOnly: true
          nullable: true
        meses_afectacion:
          type: integer
          readOnly: true
          nullable: true
        public_location:
          type: string
          readOnly: true
        fecha_creacion:
          type: string
          format: date-time
          readOnly: true
        fecha_aprobacion:
          type: string
          format: date-time
          readOnly: true
          nullable: true
        descripcion:
          type: string
        resultado_resumen:
          type: string
          nullable: true
        fecha_resolucion:
          type: string
          format: date-time
          nullable: true
        public_updates:
          type: string
          readOnly: true
        public_status_history:
          type: string
          readOnly: true
        public_evidence:
          type: string
          readOnly: true
        approved_comments:
          type: string
          readOnly: true
      required:
      - approved_comments
      - codigo
      - comunidad
      - comunidad_nombre
      - departamento_nombre
      - descripcion
      - estado
      - estado_nombre
      - estado_publicacion
      - familias_afectadas
      - fecha_aprobacion
      - fecha_creacion
      - id
      - id_caso
      - id_departamento
      - id_municipio
      - meses_afectacion
      - municipio_nombre
      - prioridad
      - public_evidence
      - public_location
      - public_status_history
      - public_updates
      - radicado_code
      - tipo_caso
      - tipo_categoria
      - tipo_naturaleza
      - tipo_nombre
      - titulo
    PublicCaseHistoryResponse:
      type: object
      properties:
        id_caso:
          type: string
          format: uuid
        codigo:
          type: string
        seguimientos:
          type: array
          items:
            $ref: '#/components/schemas/PublicCaseUpdate'
        historial_estados:
          type: array
          items:
            $ref: '#/components/schemas/PublicCaseStatusHistory'
      required:
      - codigo
      - historial_estados
      - id_caso
      - seguimientos
    PublicCaseList:
      type: object
      description: |-
        Serializador público para casos aprobados (`estado_publicacion='aprobado'`).
        No expone datos personales del ciudadano (`id_usuario`) y devuelve coordenadas generalizadas.
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_caso:
          type: string
          format: uuid
          readOnly: true
        codigo:
          type: string
          readOnly: true
        radicado_code:
          type: string
          readOnly: true
        titulo:
          type: string
          readOnly: true
        tipo_caso:
          type: string
          format: uuid
          readOnly: true
        tipo_nombre:
          type: string
          readOnly: true
        tipo_categoria:
          type: string
          readOnly: true
        tipo_naturaleza:
          type: string
          readOnly: true
        comunidad:
          type: string
          format: uuid
          readOnly: true
        comunidad_nombre:
          type: string
          readOnly: true
        id_municipio:
          type: string
          format: uuid
          readOnly: true
        municipio_nombre:
          type: string
          readOnly: true
        id_departamento:
          type: string
          format: uuid
          readOnly: true
        departamento_nombre:
          type: string
          readOnly: true
        estado:
          type: string
          format: uuid
          readOnly: true
        estado_nombre:
          type: string
          readOnly: true
        prioridad:
          allOf:
          - $ref: '#/components/schemas/PrioridadEnum'
          readOnly: true
        estado_publicacion:
          allOf:
          - $ref: '#/components/schemas/EstadoPublicacionE6cEnum'
          readOnly: true
        familias_afectadas:
          type: integer
          readOnly: true
          nullable: true
        meses_afectacion:
          type: integer
          readOnly: true
          nullable: true
        public_location:
          type: string
          readOnly: true
        fecha_creacion:
          type: string
          format: date-time
          readOnly: true
        fecha_aprobacion:
          type: string
          format: date-time
          readOnly: true
          nullable: true
      required:
      - codigo
      - comunidad
      - comunidad_nombre
      - departamento_nombre
      - estado
      - estado_nombre
      - estado_publicacion
      - familias_afectadas
      - fecha_aprobacion
      - fecha_creacion
      - id
      - id_caso
      - id_departamento
      - id_municipio
      - meses_afectacion
      - municipio_nombre
      - prioridad
      - public_location
      - radicado_code
      - tipo_caso
      - tipo_categoria
      - tipo_naturaleza
      - tipo_nombre
      - titulo
    PublicCaseOptionsResponse:
      type: object
      properties:
        tipos_caso:
          type: array
          items:
            $ref: '#/components/schemas/CaseCategory'
        categorias:
          type: array
          items:
            type: string
        estados_caso:
          type: array
          items:
            $ref: '#/components/schemas/CaseStatus'
        prioridades:
          type: array
          items:
            type: object
            additionalProperties: {}
        estados_publicacion:
          type: array
          items:
            type: object
            additionalProperties: {}
        naturalezas:
          type: array
          items:
            type: object
            additionalProperties: {}
        audiencias_seguimiento:
          type: array
          items:
            type: object
            additionalProperties: {}
        tipos_evento_seguimiento:
          type: array
          items:
            type: object
            additionalProperties: {}
      required:
      - audiencias_seguimiento
      - categorias
      - estados_caso
      - estados_publicacion
      - naturalezas
      - prioridades
      - tipos_caso
      - tipos_evento_seguimiento
    PublicCaseStatusHistory:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_historial:
          type: string
          format: uuid
          readOnly: true
        estado_anterior:
          type: string
          format: uuid
          readOnly: true
          nullable: true
        estado_anterior_nombre:
          type: string
          readOnly: true
        estado_nuevo:
          type: string
          format: uuid
          readOnly: true
        estado_nuevo_nombre:
          type: string
          readOnly: true
        motivo:
          type: string
          readOnly: true
          nullable: true
        fecha_cambio:
          type: string
          format: date-time
          readOnly: true
      required:
      - estado_anterior
      - estado_anterior_nombre
      - estado_nuevo
      - estado_nuevo_nombre
      - fecha_cambio
      - id
      - id_historial
      - motivo
    PublicCaseUpdate:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_seguimiento:
          type: string
          format: uuid
          readOnly: true
        titulo:
          type: string
          readOnly: true
          nullable: true
        descripcion:
          type: string
          readOnly: true
        audiencia:
          allOf:
          - $ref: '#/components/schemas/Audiencia01dEnum'
          readOnly: true
        tipo_evento:
          allOf:
          - $ref: '#/components/schemas/TipoEventoEnum'
          readOnly: true
        fecha_seguimiento:
          type: string
          format: date-time
          readOnly: true
        visible_publicamente:
          type: boolean
          readOnly: true
      required:
      - audiencia
      - descripcion
      - fecha_seguimiento
      - id
      - id_seguimiento
      - tipo_evento
      - titulo
      - visible_publicamente
    PublicHomeSummaryResponse:
      type: object
      properties:
        institution:
          type: object
          additionalProperties: {}
        verified_indicators:
          type: object
          additionalProperties: {}
        featured_initiatives:
          type: array
          items:
            $ref: '#/components/schemas/InitiativeList'
        recent_news:
          type: array
          items:
            $ref: '#/components/schemas/NewsArticleList'
        site_settings:
          type: object
          additionalProperties: {}
      required:
      - featured_initiatives
      - institution
      - recent_news
      - site_settings
      - verified_indicators
    PublicInitiativeCategoriesResponse:
      type: object
      properties:
        categories:
          type: array
          items:
            type: string
      required:
      - categories
    PublicSiteInfoResponse:
      type: object
      properties:
        institucion: {}
        configuracion:
          type: object
          additionalProperties: {}
        documentos_legales:
          type: array
          items:
            $ref: '#/components/schemas/LegalDocument'
      required:
      - configuracion
      - documentos_legales
      - institucion
    ResponsibleScopeAssignment:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_asignacion:
          type: string
          format: uuid
          readOnly: true
        usuario:
          type: string
          format: uuid
        comunidad:
          type: string
          format: uuid
          nullable: true
        comunidad_nombre:
          type: string
          readOnly: true
        tipo_caso:
          type: string
          format: uuid
          nullable: true
        tipo_caso_nombre:
          type: string
          readOnly: true
        fecha_asignacion:
          type: string
          format: date-time
          readOnly: true
        activo:
          type: boolean
      required:
      - comunidad_nombre
      - fecha_asignacion
      - id
      - id_asignacion
      - tipo_caso_nombre
      - usuario
    ResultadoEnum:
      enum:
      - exitoso
      - fallido
      type: string
      description: |-
        * `exitoso` - Exitoso
        * `fallido` - Fallido
    Role:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_rol:
          type: string
          format: uuid
          readOnly: true
        nombre:
          type: string
          maxLength: 50
        descripcion:
          type: string
          nullable: true
        assignable:
          type: boolean
          readOnly: true
      required:
      - assignable
      - id
      - id_rol
      - nombre
    SiteSetting:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_configuracion:
          type: string
          format: uuid
          readOnly: true
        clave:
          type: string
          maxLength: 100
        key:
          type: string
        valor: {}
        value: {}
        fecha_actualizacion:
          type: string
          format: date-time
          readOnly: true
      required:
      - fecha_actualizacion
      - id
      - id_configuracion
    Tipo669Enum:
      enum:
      - imagen
      - video
      - documento
      type: string
      description: |-
        * `imagen` - Imagen
        * `video` - Video
        * `documento` - Documento
    TipoArchivo669Enum:
      enum:
      - imagen
      - video
      - documento
      type: string
      description: |-
        * `imagen` - Imagen
        * `video` - Video
        * `documento` - Documento
    TipoEventoEnum:
      enum:
      - seguimiento
      - resolucion
      - cierre
      - nota_interna
      - aporte_ciudadano
      type: string
      description: |-
        * `seguimiento` - Seguimiento
        * `resolucion` - Resolución
        * `cierre` - Cierre
        * `nota_interna` - Nota interna
        * `aporte_ciudadano` - Aporte ciudadano
    TipoMedicionEnum:
      enum:
      - estimado
      - real
      type: string
      description: |-
        * `estimado` - Estimado
        * `real` - Real
    TipoVinculoEnum:
      enum:
      - hallazgo
      - seguimiento
      - resultado
      - otro
      type: string
      description: |-
        * `hallazgo` - Hallazgo
        * `seguimiento` - Seguimiento
        * `resultado` - Resultado
        * `otro` - Otro
    TokenBundle:
      type: object
      properties:
        access:
          type: string
        refresh:
          type: string
        token:
          type: string
        token_type:
          type: string
          default: Bearer
        expires_in:
          type: integer
        refresh_expires_in:
          type: integer
      required:
      - access
      - expires_in
      - refresh
      - refresh_expires_in
      - token
    TokenRefreshRequest:
      type: object
      properties:
        refresh:
          type: string
          description: Token JWT refresh vigente.
      required:
      - refresh
    TokenRefreshResponse:
      type: object
      properties:
        access:
          type: string
        refresh:
          type: string
        token_type:
          type: string
          default: Bearer
        expires_in:
          type: integer
      required:
      - access
      - expires_in
      - refresh
    UnifiedAuditEventItem:
      type: object
      properties:
        event_ref:
          type: string
        id:
          type: string
          format: uuid
        source:
          type: string
        action:
          type: string
        module:
          type: string
        entity:
          type: string
          nullable: true
        entity_id:
          type: string
          nullable: true
        actor:
          type: string
          format: uuid
          nullable: true
        actor_nombre:
          type: string
          nullable: true
        result:
          type: string
        description:
          type: string
          nullable: true
        changed_columns:
          type: array
          items:
            type: string
          nullable: true
        timestamp:
          type: string
          format: date-time
      required:
      - action
      - actor
      - actor_nombre
      - changed_columns
      - description
      - entity
      - entity_id
      - event_ref
      - id
      - module
      - result
      - source
      - timestamp
    UserMe:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        id_usuario:
          type: string
          format: uuid
          readOnly: true
        id_rol:
          type: string
          format: uuid
          readOnly: true
        rol_nombre:
          type: string
          readOnly: true
        nombres:
          type: string
          maxLength: 100
        apellidos:
          type: string
          maxLength: 100
        full_name:
          type: string
          readOnly: true
        correo:
          type: string
          format: email
          maxLength: 150
        telefono:
          type: string
          nullable: true
          maxLength: 20
        estado:
          allOf:
          - $ref: '#/components/schemas/Estado6c7Enum'
          readOnly: true
        primary_role:
          type: string
          readOnly: true
        roles:
          type: array
          items:
            type: string
          readOnly: true
        permissions:
          type: object
          additionalProperties: {}
          readOnly: true
        perfil:
          type: object
          additionalProperties: {}
          readOnly: true
        preferencias:
          type: object
          additionalProperties: {}
          readOnly: true
        ambitos_responsable:
          type: array
          items:
            $ref: '#/components/schemas/ResponsibleScopeAssignment'
          readOnly: true
        id_departamento:
          type: string
          format: uuid
          writeOnly: true
          nullable: true
        id_municipio:
          type: string
          format: uuid
          writeOnly: true
          nullable: true
        id_comunidad:
          type: string
          format: uuid
          writeOnly: true
          nullable: true
        fecha_registro:
          type: string
          format: date-time
          readOnly: true
        fecha_actualizacion:
          type: string
          format: date-time
          readOnly: true
      required:
      - ambitos_responsable
      - apellidos
      - correo
      - estado
      - fecha_actualizacion
      - fecha_registro
      - full_name
      - id
      - id_rol
      - id_usuario
      - nombres
      - perfil
      - permissions
      - preferencias
      - primary_role
      - rol_nombre
      - roles
    UserPreference:
      type: object
      properties:
        id_preferencia:
          type: string
          format: uuid
          readOnly: true
        notificar_novedades_casos:
          type: boolean
        notificar_avance_casos:
          type: boolean
          description: Alias de notificar_novedades_casos.
        notificar_mensajes:
          type: boolean
        suscrito_boletin:
          type: boolean
        recibir_boletin:
          type: boolean
          description: Alias de suscrito_boletin.
        fecha_actualizacion:
          type: string
          format: date-time
          readOnly: true
      required:
      - fecha_actualizacion
      - id_preferencia
    UserProfile:
      type: object
      properties:
        id_perfil:
          type: string
          format: uuid
          readOnly: true
        ruta_foto:
          type: string
          readOnly: true
          nullable: true
        foto_url:
          type: string
          nullable: true
          readOnly: true
        id_departamento:
          type: string
          format: uuid
          readOnly: true
        departamento_nombre:
          type: string
          readOnly: true
        id_municipio:
          type: string
          format: uuid
          readOnly: true
        municipio_nombre:
          type: string
          readOnly: true
        id_comunidad:
          type: string
          format: uuid
          readOnly: true
        comunidad_nombre:
          type: string
          readOnly: true
        fecha_actualizacion:
          type: string
          format: date-time
          readOnly: true
      required:
      - comunidad_nombre
      - departamento_nombre
      - fecha_actualizacion
      - foto_url
      - id_comunidad
      - id_departamento
      - id_municipio
      - id_perfil
      - municipio_nombre
      - ruta_foto
  securitySchemes:
    cookieAuth:
      type: apiKey
      in: cookie
      name: sessionid
    jwtAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
    tokenAuth:
      type: apiKey
      in: header
      name: Authorization
      description: Token-based authentication with required prefix "Token"
