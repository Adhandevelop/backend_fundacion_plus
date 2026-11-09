openapi: 3.0.3
info:
  title: Plataforma Web PLUS — API REST
  version: 1.0.0
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
                $ref: '#/components/schemas/Login'
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
      operationId: v1_admin_audit_events_retrieve
      description: |-
        AUD-01: GET /api/v1/admin/audit-events/
        Proyección unificada de las 5 tablas de auditoría con referencia `event_ref` (`{source}:{uuid}`).
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          description: No response body
  /api/v1/admin/audit/events/{event_ref}/:
    get:
      operationId: v1_admin_audit_events_retrieve_2
      description: |-
        AUD-02: GET /api/v1/admin/audit/events/{event_ref}/
        Soporta referencia `{source}:{uuid}` o búsqueda directa por UUID.
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
          description: No response body
  /api/v1/admin/basins/:
    get:
      operationId: v1_admin_basins_retrieve
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
          description: No response body
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
  /api/v1/admin/cases/{id}/assignments/:
    post:
      operationId: v1_admin_cases_assignments_create
      description: 'ADM-08: POST /api/v1/admin/cases/{case_id}/assignments/'
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
  /api/v1/admin/cases/{id}/correction-requests/:
    post:
      operationId: v1_admin_cases_correction_requests_create
      description: 'ADM-07: POST /api/v1/admin/cases/{case_id}/correction-requests/'
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
  /api/v1/admin/cases/{id}/evidence/:
    get:
      operationId: v1_admin_cases_evidence_retrieve
      description: 'ADM-05: GET / POST /api/v1/admin/cases/{case_id}/evidence/'
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
    post:
      operationId: v1_admin_cases_evidence_create
      description: 'ADM-05: GET / POST /api/v1/admin/cases/{case_id}/evidence/'
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
  /api/v1/admin/cases/{id}/evidence/{evidence_id}/:
    patch:
      operationId: v1_admin_cases_evidence_partial_update
      description: 'ADM-11 (AMP-10): PATCH /api/v1/admin/cases/{case_id}/evidence/{evidence_id}/'
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
  /api/v1/admin/cases/{id}/evidence/{evidence_id}/download/:
    get:
      operationId: v1_admin_cases_evidence_download_retrieve
      description: 'ADM-06: GET /api/v1/admin/cases/{case_id}/evidence/{evidence_id}/download/'
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
  /api/v1/admin/cases/{id}/moderation/:
    post:
      operationId: v1_admin_cases_moderation_create
      description: 'ADM-07: POST /api/v1/admin/cases/{case_id}/moderation/'
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
  /api/v1/admin/cases/{id}/progress/:
    post:
      operationId: v1_admin_cases_progress_create
      description: 'ADM-09 (AMP-08): POST /api/v1/admin/cases/{case_id}/progress/'
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
  /api/v1/admin/cases/{id}/resolution/:
    post:
      operationId: v1_admin_cases_resolution_create
      description: 'ADM-10 (AMP-11): POST /api/v1/admin/cases/{case_id}/resolution/'
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
  /api/v1/admin/cases/{id}/resolve/:
    post:
      operationId: v1_admin_cases_resolve_create
      description: Alias compatible con POST /api/v1/admin/cases/{case_id}/resolve/
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
  /api/v1/admin/cases/{id}/status/:
    post:
      operationId: v1_admin_cases_status_create
      description: Alias compatible con POST /api/v1/admin/cases/{case_id}/status/
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
  /api/v1/admin/comments/{id}/moderation/:
    post:
      operationId: v1_admin_comments_moderation_create
      description: 'Sección 14: POST /api/v1/admin/comments/{id}/moderation/'
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
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          description: No response body
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
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          description: No response body
  /api/v1/admin/reports/cases/export/:
    get:
      operationId: v1_admin_reports_cases_export_retrieve
      description: |-
        REP-02: GET /api/v1/admin/reports/cases/export/
        Exporta en CSV toda la selección autorizada neutralizando fórmulas en celdas de texto.
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          description: No response body
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
    put:
      operationId: v1_admin_users_role_update
      description: 'USR-05: PUT /api/v1/admin/users/{id}/role/ — Asigna un único rol
        al usuario.'
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
  /api/v1/admin/users/{id}/roles/:
    get:
      operationId: v1_admin_users_roles_retrieve
      description: Compatibilidad con /api/v1/admin/users/{id}/roles/
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
    post:
      operationId: v1_admin_users_roles_create
      description: Compatibilidad con /api/v1/admin/users/{id}/roles/
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
    put:
      operationId: v1_admin_users_roles_update
      description: Compatibilidad con /api/v1/admin/users/{id}/roles/
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
  /api/v1/admin/users/{id}/status/:
    patch:
      operationId: v1_admin_users_status_partial_update
      description: 'USR-06: PATCH /api/v1/admin/users/{id}/status/ — Cambia el estado
        (activo, suspendido, inactivo).'
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
                $ref: '#/components/schemas/Login'
          description: ''
  /api/v1/auth/logout/:
    post:
      operationId: v1_auth_logout_create
      description: 'AUTH-04: POST /api/v1/auth/logout/ — Cierra sesión y revoca Token
        de API.'
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          description: No response body
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
                $ref: '#/components/schemas/PasswordResetConfirm'
          description: ''
  /api/v1/auth/password-reset/request/:
    post:
      operationId: v1_auth_password_reset_request_create
      description: 'AUTH-05: POST /api/v1/auth/password-reset/request/'
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
                $ref: '#/components/schemas/PasswordResetRequest'
          description: ''
  /api/v1/auth/password-reset/validate/:
    post:
      operationId: v1_auth_password_reset_validate_create
      description: 'AUTH-06: POST /api/v1/auth/password-reset/validate/'
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
                $ref: '#/components/schemas/PasswordResetValidate'
          description: ''
  /api/v1/auth/refresh/:
    post:
      operationId: v1_auth_refresh_create
      description: |-
        Takes a refresh type JSON web token and returns an access type JSON web
        token if the refresh token is valid.
      tags:
      - v1
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TokenRefresh'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/TokenRefresh'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/TokenRefresh'
        required: true
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TokenRefresh'
          description: ''
  /api/v1/auth/register/:
    post:
      operationId: v1_auth_register_create
      description: 'AUTH-01: POST /api/v1/auth/register/ — Registro ciudadano en plus.usuarios.'
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
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CitizenRegistration'
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
          format: uuid
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
  /api/v1/cases/{case_id}/messages/mark-read/:
    put:
      operationId: v1_cases_messages_mark_read_update
      description: |-
        MSG-04: PUT /api/v1/cases/{case_id}/messages/read/
        Marca como leídos únicamente los mensajes destinados al usuario autenticado.
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
          description: No response body
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
          description: No response body
  /api/v1/catalogs/case-categories/:
    get:
      operationId: v1_catalogs_case_categories_retrieve
      description: |-
        CAT-05: GET /api/v1/catalogs/case-categories/
        Retorna valores distintos de `tipos_caso.categoria` (textos de hasta 50 caracteres) y los tipos activos.
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          description: No response body
  /api/v1/catalogs/case-options/:
    get:
      operationId: v1_catalogs_case_options_retrieve
      description: |-
        CAT-06: GET /api/v1/catalogs/case-options/
        Retorna tipos_caso activos, estados_caso, prioridades, estados de publicación y naturalezas.
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          description: No response body
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
          format: uuid
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
      operationId: v1_citizen_cases_contributions_retrieve
      description: 'CIT-08 (AMP-07): GET / POST /api/v1/me/cases/{case_id}/contributions/'
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
    post:
      operationId: v1_citizen_cases_contributions_create
      description: 'CIT-08 (AMP-07): GET / POST /api/v1/me/cases/{case_id}/contributions/'
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
  /api/v1/citizen/cases/{id}/evidence/:
    get:
      operationId: v1_citizen_cases_evidence_retrieve
      description: 'CIT-06: GET / POST /api/v1/me/cases/{case_id}/evidence/'
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
    post:
      operationId: v1_citizen_cases_evidence_create
      description: 'CIT-06: GET / POST /api/v1/me/cases/{case_id}/evidence/'
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
  /api/v1/citizen/cases/{id}/evidence/{evidence_id}/download/:
    get:
      operationId: v1_citizen_cases_evidence_download_retrieve
      description: 'CIT-07: GET /api/v1/me/cases/{case_id}/evidence/{evidence_id}/download/'
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
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          description: No response body
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
      operationId: v1_me_cases_contributions_retrieve
      description: 'CIT-08 (AMP-07): GET / POST /api/v1/me/cases/{case_id}/contributions/'
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
    post:
      operationId: v1_me_cases_contributions_create
      description: 'CIT-08 (AMP-07): GET / POST /api/v1/me/cases/{case_id}/contributions/'
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
  /api/v1/me/cases/{id}/evidence/:
    get:
      operationId: v1_me_cases_evidence_retrieve
      description: 'CIT-06: GET / POST /api/v1/me/cases/{case_id}/evidence/'
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
    post:
      operationId: v1_me_cases_evidence_create
      description: 'CIT-06: GET / POST /api/v1/me/cases/{case_id}/evidence/'
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
  /api/v1/me/cases/{id}/evidence/{evidence_id}/download/:
    get:
      operationId: v1_me_cases_evidence_download_retrieve
      description: 'CIT-07: GET /api/v1/me/cases/{case_id}/evidence/{evidence_id}/download/'
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
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          description: No response body
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
          format: uuid
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
          format: uuid
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
          format: uuid
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
    put:
      operationId: v1_me_photo_update
      description: 'ME-03 y ME-04: PUT / DELETE /api/v1/me/photo/'
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      responses:
        '200':
          description: No response body
    delete:
      operationId: v1_me_photo_destroy
      description: 'ME-03 y ME-04: PUT / DELETE /api/v1/me/photo/'
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
          format: uuid
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
  /api/v1/public/cases/{case_id}/evidences/:
    get:
      operationId: v1_public_cases_evidences_retrieve
      description: |-
        MAP-05: GET /api/v1/public/cases/{case_id}/evidence/
        Solo entrega evidencias expresamente marcadas como `audiencia='publico'` y `estado_revision='aprobada'`.
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
      - {}
      responses:
        '200':
          description: No response body
  /api/v1/public/cases/{case_id}/history/:
    get:
      operationId: v1_public_cases_history_retrieve
      description: |-
        MAP-04: GET /api/v1/public/cases/{case_id}/history/
        Solo entrega seguimientos con `visible_publicamente=True` (audiencia='publico') y cambios de estado del caso aprobado.
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
      - {}
      responses:
        '200':
          description: No response body
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
        MAP-02: GET /api/v1/public/cases/map/
        Retorna un GeoJSON FeatureCollection (SRID 4326) de los casos con `estado_publicacion='aprobado'`.
        Generaliza las coordenadas (`public_location`) para proteger ubicaciones sensibles (base de datos.md línea 60).
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
                $ref: '#/components/schemas/PublicCaseList'
          description: ''
  /api/v1/public/cases/map/:
    get:
      operationId: v1_public_cases_map_retrieve
      description: |-
        MAP-02: GET /api/v1/public/cases/map/
        Retorna un GeoJSON FeatureCollection (SRID 4326) de los casos con `estado_publicacion='aprobado'`.
        Generaliza las coordenadas (`public_location`) para proteger ubicaciones sensibles (base de datos.md línea 60).
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
                $ref: '#/components/schemas/PublicCaseList'
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
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          description: No response body
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
  /api/v1/public/initiatives/categories/:
    get:
      operationId: v1_public_initiatives_categories_retrieve
      description: |-
        CAT-08: GET /api/v1/catalogs/initiative-categories/
        Retorna valores distintos de `iniciativas.categoria` para programas publicados.
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          description: No response body
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
  /api/v1/public/newsletter/confirm/:
    post:
      operationId: v1_public_newsletter_confirm_create
      description: 'PUB-10 (AMP-02): POST /api/v1/public/newsletter-subscriptions/confirm/'
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
  /api/v1/public/site-info/:
    get:
      operationId: v1_public_site_info_retrieve
      description: |-
        PUB-01: GET /api/v1/public/site/
        Proyección pública autorizada de `configuracion_plataforma` y documentos legales vigentes (AMP-09).
      tags:
      - v1
      security:
      - jwtAuth: []
      - tokenAuth: []
      - cookieAuth: []
      - {}
      responses:
        '200':
          description: No response body
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
          - $ref: '#/components/schemas/EstadoModeracionEnum'
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
          $ref: '#/components/schemas/CaseEvidenceAudienciaEnum'
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
      - ruta_archivo
      - usuario
      - usuario_nombre
    CaseEvidenceAudienciaEnum:
      enum:
      - publico
      - ciudadano
      - privado
      type: string
      description: |-
        * `publico` - Público
        * `ciudadano` - Ciudadano / Equipo
        * `privado` - Privado / Interno
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
          $ref: '#/components/schemas/CaseUpdateAudienciaEnum'
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
    CaseUpdateAudienciaEnum:
      enum:
      - publico
      - ciudadano
      - interno
      type: string
      description: |-
        * `publico` - Público
        * `ciudadano` - Ciudadano / Equipo
        * `interno` - Interno
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
    EstadoModeracionEnum:
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
        token:
          type: string
        new_password:
          type: string
          writeOnly: true
          minLength: 8
      required:
      - new_password
      - token
      - uid
    PasswordResetRequest:
      type: object
      properties:
        correo:
          type: string
          format: email
        email:
          type: string
          format: email
    PasswordResetValidate:
      type: object
      properties:
        uid:
          type: string
        token:
          type: string
      required:
      - token
      - uid
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
          $ref: '#/components/schemas/CaseEvidenceAudienciaEnum'
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
        notificar_mensajes:
          type: boolean
        suscrito_boletin:
          type: boolean
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
    TokenRefresh:
      type: object
      properties:
        access:
          type: string
          readOnly: true
        refresh:
          type: string
      required:
      - access
      - refresh
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
        notificar_mensajes:
          type: boolean
        suscrito_boletin:
          type: boolean
        fecha_actualizacion:
          type: string
          format: date-time
          readOnly: true
      required:
      - fecha_actualizacion
      - id_preferencia
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
