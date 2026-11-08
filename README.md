# Backend — Plataforma Web PLUS (Corporación Pluralismo Social)

Backend institucional y operativo desarrollado con **Python, Django, Django REST Framework y PostgreSQL/PostGIS** para la **Corporación Pluralismo Social (PLUS)**.

## 1. Arquitectura Modular

El proyecto implementa una arquitectura monolítica modular en `backend_fundacion_plus/`:

- `core/`: Modelos abstractos (`TimeStampedUUIDModel`), utilidades geográficas WGS84/SRID 4326 (`gis.py`), validadores de dominio y archivos (`validators.py`), paginación (`pagination.py`) y manejador estándar de excepciones (`exceptions.py`).
- `apps/accounts/`: Usuarios (`User`), Roles (`Role`), Asignación de roles y alcances territoriales (`UserRole`), Perfiles con consentimiento de tratamiento de datos (`UserProfile`), autenticación JWT y permisos RBAC.
- `apps/territories/`: Departamentos (`Department`), Municipios (`Municipality`) y Comunidades/Veredas (`Community`) georreferenciados en SRID 4326.
- `apps/cases/`: Categorías (`CaseCategory`), Casos comunitarios (`Case`) con separación entre estado de moderación y estado de gestión y ofuscación de coordenadas sensibles, Asignaciones (`CaseAssignment`) y Evidencias (`CaseEvidence`) con protección de menores.
- `apps/tracking/`: Avances cronológicos (`CaseUpdate`) con niveles de visibilidad (`INTERNAL`, `CITIZEN_VISIBLE`, `PUBLIC`) e Historial de estados (`CaseStatusHistory`).
- `apps/communications/`: Comentarios públicos moderados (`CaseComment`), Mensajes privados (`CaseMessage`), Propuestas comunitarias (`EventProposal`), Redes sociales (`SocialLink`) y Parámetros institucionales (`SiteSetting`).
- `apps/initiatives/`: Iniciativas comunitarias (`Initiative`), Jornadas (`InitiativeActivity`), Galería multimedia (`InitiativeMedia`) e Indicadores de impacto (`InitiativeMetric`).
- `apps/news/`: Categorías (`NewsCategory`) y Artículos de noticias (`NewsArticle`), además de los agregadores del Home público (`/api/v1/public/home/`) y Dashboard administrativo (`/api/v1/admin/metrics/dashboard/`).
- `apps/notifications/`: Notificaciones internas (`Notification`).
- `apps/audit/`: Registro inmutable de auditoría administrativa (`AuditLog`) con sincronización de variable de sesión PostgreSQL (`plus.actor_id`).

---

## 2. Instalación y Ejecución

```bash
cd backend_fundacion_plus
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_plus_initial
python manage.py createsuperuser
python manage.py runserver
```

### Ejecución de Pruebas Automatizadas
```bash
python manage.py test apps.accounts apps.cases -v 2
```

---

## 3. Contratos Principales de API (`/api/v1/`) para Angular

- **Documentación Interactiva OpenAPI / Swagger:** `GET /api/v1/docs/` y `GET /api/v1/schema/`
- **Autenticación (`/api/v1/auth/`):**
  - `POST /api/v1/auth/register/` — Registro ciudadano (valida Ley 1581 de 2012).
  - `POST /api/v1/auth/login/` — Inicio de sesión JWT (`access`, `refresh`, perfil, roles y permisos).
  - `POST /api/v1/auth/refresh/` — Renovación de token JWT.
  - `GET / PATCH /api/v1/auth/me/` — Perfil, roles y permisos del usuario autenticado.
- **Portal Público (`/api/v1/public/`):**
  - `GET /api/v1/public/home/` — Datos del Hero (Luis Alberto Muñoz Granada, PLUS), indicadores reales, iniciativas destacadas y noticias recientes.
  - `GET /api/v1/public/cases/map/` — GeoJSON (`FeatureCollection`, SRID 4326) de casos aprobados para Leaflet (`?municipality=`, `?community=`, `?category=`, `?management_status=`, `?bbox=minLon,minLat,maxLon,maxLat`).
  - `GET /api/v1/public/cases/` y `GET /api/v1/public/cases/{radicado_code}/`
  - `GET /api/v1/public/initiatives/` y `GET /api/v1/public/initiatives/{slug}/`
  - `GET /api/v1/public/news/` y `GET /api/v1/public/news/{slug}/`
- **Portal Ciudadano (`/api/v1/citizen/`):**
  - `GET /api/v1/citizen/dashboard/`
  - `GET / POST / PATCH /api/v1/citizen/cases/`
  - `POST /api/v1/citizen/cases/{id}/evidence/` y `POST /api/v1/citizen/cases/{id}/updates/`
  - `GET / POST /api/v1/citizen/cases/{id}/messages/` y `POST /api/v1/citizen/cases/{id}/comments/`
  - `GET /api/v1/citizen/notifications/`
- **Panel Administrativo (`/api/v1/admin/`):**
  - `GET /api/v1/admin/metrics/dashboard/`
  - `/api/v1/admin/users/`, `/api/v1/admin/users/{id}/roles/`, `/api/v1/admin/roles/`
  - `/api/v1/admin/departments/`, `/api/v1/admin/municipalities/`, `/api/v1/admin/communities/`
  - `/api/v1/admin/cases/`, `POST /api/v1/admin/cases/{id}/moderate/`, `POST /api/v1/admin/cases/{id}/assign/`, `POST /api/v1/admin/cases/{id}/status/`, `POST /api/v1/admin/cases/{id}/updates/`
  - `POST /api/v1/admin/evidence/{id}/authorize/` y `POST /api/v1/admin/comments/{id}/moderate/`
  - `/api/v1/admin/initiatives/`, `/api/v1/admin/initiative-activities/`, `/api/v1/admin/initiative-media/`, `/api/v1/admin/initiative-metrics/`
  - `/api/v1/admin/news/`, `/api/v1/admin/news-categories/`, `/api/v1/admin/settings/`, `/api/v1/admin/social-links/`
  - `GET /api/v1/admin/audit-logs/`
