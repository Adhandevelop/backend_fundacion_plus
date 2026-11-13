-- =============================================================================
-- PLUS — Ampliaciones Incrementales del Esquema (Sección 18 de endpoints.md)
-- Compatible con bases de datos ya desplegadas (idempotente con IF NOT EXISTS).
-- =============================================================================

BEGIN;

SET search_path TO plus, public;

-- -----------------------------------------------------------------------------
-- AMP-12: Naturaleza del tipo de caso en plus.tipos_caso
-- -----------------------------------------------------------------------------
ALTER TABLE plus.tipos_caso
    ADD COLUMN IF NOT EXISTS naturaleza VARCHAR(30) NOT NULL DEFAULT 'problematica';

-- -----------------------------------------------------------------------------
-- AMP-05 y AMP-11: Cantidades de afectación y resultado narrativo en plus.casos
-- -----------------------------------------------------------------------------
ALTER TABLE plus.casos
    ADD COLUMN IF NOT EXISTS familias_afectadas INTEGER NULL,
    ADD COLUMN IF NOT EXISTS meses_afectacion INTEGER NULL,
    ADD COLUMN IF NOT EXISTS resultado_resumen TEXT NULL,
    ADD COLUMN IF NOT EXISTS id_seguimiento_resolucion UUID NULL REFERENCES plus.seguimientos(id_seguimiento) ON DELETE SET NULL,
    ADD COLUMN IF NOT EXISTS id_usuario_resolucion UUID NULL REFERENCES plus.usuarios(id_usuario) ON DELETE SET NULL,
    ADD COLUMN IF NOT EXISTS fecha_resolucion TIMESTAMPTZ NULL;

-- -----------------------------------------------------------------------------
-- AMP-08: Título, audiencia explícita (3 niveles) y tipo de evento en plus.seguimientos
-- -----------------------------------------------------------------------------
ALTER TABLE plus.seguimientos
    ADD COLUMN IF NOT EXISTS titulo VARCHAR(200) NULL,
    ADD COLUMN IF NOT EXISTS audiencia VARCHAR(20) NOT NULL DEFAULT 'interno',
    ADD COLUMN IF NOT EXISTS tipo_evento VARCHAR(30) NOT NULL DEFAULT 'seguimiento';

-- Migración conservadora AMP-08: visible_publicamente=true -> 'publico', false -> 'interno'
UPDATE plus.seguimientos
SET audiencia = 'publico'
WHERE visible_publicamente = TRUE AND audiencia = 'interno';

-- -----------------------------------------------------------------------------
-- AMP-06: Solicitudes de corrección sobre casos (plus.solicitudes_correccion)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS plus.solicitudes_correccion (
    id_solicitud UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_caso UUID NOT NULL REFERENCES plus.casos(id_caso) ON DELETE CASCADE,
    id_solicitante UUID NOT NULL REFERENCES plus.usuarios(id_usuario) ON DELETE RESTRICT,
    motivo TEXT NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'abierta'
        CHECK (estado IN ('abierta', 'respondida', 'cerrada', 'cancelada')),
    respuesta TEXT NULL,
    id_revisor UUID NULL REFERENCES plus.usuarios(id_usuario) ON DELETE SET NULL,
    fecha_solicitud TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    fecha_respuesta TIMESTAMPTZ NULL,
    fecha_revision TIMESTAMPTZ NULL
);

CREATE INDEX IF NOT EXISTS ix_solicitudes_corr_caso
    ON plus.solicitudes_correccion (id_caso, estado);

-- -----------------------------------------------------------------------------
-- AMP-07: Aportes ciudadanos al expediente (plus.aportes_caso)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS plus.aportes_caso (
    id_aporte UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_caso UUID NOT NULL REFERENCES plus.casos(id_caso) ON DELETE CASCADE,
    id_usuario UUID NOT NULL REFERENCES plus.usuarios(id_usuario) ON DELETE RESTRICT,
    id_solicitud_correccion UUID NULL REFERENCES plus.solicitudes_correccion(id_solicitud) ON DELETE SET NULL,
    contenido TEXT NOT NULL,
    fecha_creacion TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_aportes_caso_fecha
    ON plus.aportes_caso (id_caso, fecha_creacion DESC);

-- -----------------------------------------------------------------------------
-- AMP-07, AMP-10 y P24: Asociación a aporte/seguimiento, audiencia, revisión y metadatos en plus.evidencias
-- -----------------------------------------------------------------------------
ALTER TABLE plus.evidencias
    ADD COLUMN IF NOT EXISTS id_aporte UUID NULL REFERENCES plus.aportes_caso(id_aporte) ON DELETE SET NULL,
    ADD COLUMN IF NOT EXISTS id_seguimiento UUID NULL REFERENCES plus.seguimientos(id_seguimiento) ON DELETE SET NULL,
    ADD COLUMN IF NOT EXISTS audiencia VARCHAR(20) NOT NULL DEFAULT 'ciudadano',
    ADD COLUMN IF NOT EXISTS estado_revision VARCHAR(20) NOT NULL DEFAULT 'pendiente',
    ADD COLUMN IF NOT EXISTS nombre_original VARCHAR(255) NULL,
    ADD COLUMN IF NOT EXISTS mime_type VARCHAR(100) NULL,
    ADD COLUMN IF NOT EXISTS tamano_bytes BIGINT NULL;

CREATE INDEX IF NOT EXISTS ix_evidencias_seguimiento
    ON plus.evidencias (id_seguimiento);

-- -----------------------------------------------------------------------------
-- AMP-03: Casos seguidos por ciudadanos (plus.casos_seguidos)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS plus.casos_seguidos (
    id_seguimiento_usuario UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_usuario UUID NOT NULL REFERENCES plus.usuarios(id_usuario) ON DELETE CASCADE,
    id_caso UUID NOT NULL REFERENCES plus.casos(id_caso) ON DELETE CASCADE,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_creacion TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    fecha_baja TIMESTAMPTZ NULL,
    CONSTRAINT uq_usuario_caso_seguido UNIQUE (id_usuario, id_caso)
);

-- -----------------------------------------------------------------------------
-- AMP-04: Perfiles y preferencias de usuarios (plus.perfiles_usuarios, plus.preferencias_usuarios)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS plus.perfiles_usuarios (
    id_perfil UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_usuario UUID NOT NULL UNIQUE REFERENCES plus.usuarios(id_usuario) ON DELETE CASCADE,
    ruta_foto TEXT NULL,
    id_departamento UUID NULL REFERENCES plus.departamentos(id_departamento) ON DELETE SET NULL,
    id_municipio UUID NULL REFERENCES plus.municipios(id_municipio) ON DELETE SET NULL,
    id_comunidad UUID NULL REFERENCES plus.comunidades(id_comunidad) ON DELETE SET NULL,
    fecha_actualizacion TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS plus.preferencias_usuarios (
    id_preferencia UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_usuario UUID NOT NULL UNIQUE REFERENCES plus.usuarios(id_usuario) ON DELETE CASCADE,
    notificar_novedades_casos BOOLEAN NOT NULL DEFAULT TRUE,
    notificar_mensajes BOOLEAN NOT NULL DEFAULT TRUE,
    suscrito_boletin BOOLEAN NOT NULL DEFAULT FALSE,
    fecha_actualizacion TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- -----------------------------------------------------------------------------
-- AMP-09: Documentos legales y aceptaciones auditables (plus.documentos_legales, plus.aceptaciones_legales)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS plus.documentos_legales (
    id_documento UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tipo VARCHAR(50) NOT NULL,
    version VARCHAR(30) NOT NULL DEFAULT '1.0',
    titulo VARCHAR(200) NOT NULL,
    contenido TEXT NOT NULL,
    vigente BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_vigencia TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    fecha_creacion TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_documento_legal_version UNIQUE (tipo, version)
);

CREATE TABLE IF NOT EXISTS plus.aceptaciones_legales (
    id_aceptacion UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_documento UUID NOT NULL REFERENCES plus.documentos_legales(id_documento) ON DELETE RESTRICT,
    version_aceptada VARCHAR(30) NOT NULL,
    finalidad VARCHAR(50) NOT NULL,
    id_usuario UUID NULL REFERENCES plus.usuarios(id_usuario) ON DELETE SET NULL,
    id_caso UUID NULL REFERENCES plus.casos(id_caso) ON DELETE SET NULL,
    id_propuesta UUID NULL REFERENCES plus.propuestas_iniciativas(id_propuesta) ON DELETE SET NULL,
    correo_declarado VARCHAR(150) NULL,
    fecha_aceptacion TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- -----------------------------------------------------------------------------
-- AMP-02: Suscripciones al boletín institucional (plus.suscripciones_boletin)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS plus.suscripciones_boletin (
    id_suscripcion UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre VARCHAR(150) NULL,
    correo VARCHAR(150) NOT NULL UNIQUE,
    id_usuario UUID NULL REFERENCES plus.usuarios(id_usuario) ON DELETE SET NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'pendiente'
        CHECK (estado IN ('pendiente', 'confirmada', 'baja')),
    token_hash VARCHAR(128) NULL,
    expira_en TIMESTAMPTZ NULL,
    id_aceptacion_legal UUID NULL REFERENCES plus.aceptaciones_legales(id_aceptacion) ON DELETE SET NULL,
    fecha_solicitud TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    fecha_confirmacion TIMESTAMPTZ NULL,
    fecha_baja TIMESTAMPTZ NULL
);

-- -----------------------------------------------------------------------------
-- AMP-01: Noticias institucionales en español (plus.categorias_noticias, plus.noticias, plus.noticia_multimedia)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS plus.categorias_noticias (
    id_categoria_noticia UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre VARCHAR(120) NOT NULL UNIQUE,
    slug VARCHAR(140) NOT NULL UNIQUE,
    descripcion TEXT NULL,
    activa BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_creacion TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    fecha_actualizacion TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS plus.noticias (
    id_noticia UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_autor UUID NOT NULL REFERENCES plus.usuarios(id_usuario) ON DELETE RESTRICT,
    id_categoria UUID NOT NULL REFERENCES plus.categorias_noticias(id_categoria_noticia) ON DELETE RESTRICT,
    id_iniciativa UUID NULL REFERENCES plus.iniciativas(id_iniciativa) ON DELETE SET NULL,
    titulo VARCHAR(220) NOT NULL,
    slug VARCHAR(240) NOT NULL UNIQUE,
    extracto TEXT NOT NULL,
    contenido TEXT NOT NULL,
    estado_publicacion VARCHAR(20) NOT NULL DEFAULT 'borrador'
        CHECK (estado_publicacion IN ('borrador', 'en_revision', 'publicada', 'archivada')),
    destacada BOOLEAN NOT NULL DEFAULT FALSE,
    fecha_publicacion TIMESTAMPTZ NULL,
    fecha_creacion TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    fecha_actualizacion TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_noticias_pub_fecha
    ON plus.noticias (estado_publicacion, fecha_publicacion DESC);

CREATE TABLE IF NOT EXISTS plus.noticia_multimedia (
    id_multimedia UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_noticia UUID NOT NULL REFERENCES plus.noticias(id_noticia) ON DELETE CASCADE,
    tipo_archivo VARCHAR(20) NOT NULL DEFAULT 'imagen'
        CHECK (tipo_archivo IN ('imagen', 'video', 'documento')),
    ruta_archivo TEXT NOT NULL,
    texto_alternativo VARCHAR(250) NULL,
    descripcion TEXT NULL,
    orden INTEGER NOT NULL DEFAULT 0,
    es_portada BOOLEAN NOT NULL DEFAULT FALSE,
    fecha_carga TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX IF NOT EXISTS ux_noticia_portada_unica
    ON plus.noticia_multimedia (id_noticia)
    WHERE es_portada = TRUE;

COMMIT;
