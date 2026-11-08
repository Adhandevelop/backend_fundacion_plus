-- ============================================================================
-- PLUS | Corporacion Pluralismo Social
-- Esquema integral v1.1 | 30 tablas | PostgreSQL 15+ y PostGIS 3+
-- Base: modelo de 22 tablas + iniciativas (6) + ediciones y vinculacion de casos (2)
-- Ejecutar dentro de una base de datos VACIA o previamente preparada.
-- No contiene CREATE DATABASE: conectarse primero a la BD deseada.
-- No inserta usuarios ni contrasenas de ejemplo.
-- ============================================================================

BEGIN;

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE SCHEMA IF NOT EXISTS plus;
SET LOCAL search_path TO plus, public;

-- 01. CATALOGOS DE SEGURIDAD Y TERRITORIO -----------------------------------
CREATE TABLE roles (
    id_rol UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT
);

CREATE TABLE departamentos (
    id_departamento UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    codigo_dane VARCHAR(2) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    CONSTRAINT ck_departamento_dane CHECK (codigo_dane ~ '^[0-9]{2}$')
);

CREATE TABLE municipios (
    id_municipio UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_departamento UUID NOT NULL REFERENCES departamentos(id_departamento) ON DELETE RESTRICT,
    codigo_dane VARCHAR(5) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    CONSTRAINT ck_municipio_dane CHECK (codigo_dane ~ '^[0-9]{5}$')
);

CREATE TABLE comunidades (
    id_comunidad UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_municipio UUID NOT NULL REFERENCES municipios(id_municipio) ON DELETE RESTRICT,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    tipo VARCHAR(50) NOT NULL,
    -- Opcional: perimetro de barrio, vereda, corregimiento, etc.
    ubicacion geometry(MultiPolygon,4326),
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT ck_comunidad_tipo CHECK (tipo IN ('barrio','vereda','corregimiento','comuna','sector','otro')),
    CONSTRAINT uq_comunidad_territorio UNIQUE (id_municipio, tipo, nombre)
);

CREATE TABLE usuarios (
    id_usuario UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_rol UUID NOT NULL REFERENCES roles(id_rol) ON DELETE RESTRICT,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    correo VARCHAR(150) NOT NULL,
    contrasena_hash TEXT NOT NULL,
    telefono VARCHAR(20),
    estado VARCHAR(20) NOT NULL DEFAULT 'activo',
    fecha_registro TIMESTAMPTZ NOT NULL DEFAULT now(),
    fecha_actualizacion TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT ck_usuario_estado CHECK (estado IN ('activo','suspendido','inactivo')),
    CONSTRAINT ck_usuario_correo CHECK (position('@' in correo) > 1)
);
-- Correos unicos sin distinguir mayusculas/minusculas.
CREATE UNIQUE INDEX ux_usuarios_correo_ci ON usuarios (lower(btrim(correo)));

CREATE TABLE tipos_caso (
    id_tipo_caso UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    categoria VARCHAR(50) NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT uq_tipo_caso UNIQUE (categoria, nombre)
);

CREATE TABLE estados_caso (
    id_estado UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT,
    orden INTEGER NOT NULL UNIQUE CHECK (orden > 0)
);

-- 02. CASOS Y PARTICIPACION --------------------------------------------------
CREATE TABLE casos (
    id_caso UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    codigo VARCHAR(30) NOT NULL UNIQUE,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL,
    id_usuario UUID NOT NULL REFERENCES usuarios(id_usuario) ON DELETE RESTRICT,
    id_tipo_caso UUID NOT NULL REFERENCES tipos_caso(id_tipo_caso) ON DELETE RESTRICT,
    id_comunidad UUID NOT NULL REFERENCES comunidades(id_comunidad) ON DELETE RESTRICT,
    id_estado UUID NOT NULL REFERENCES estados_caso(id_estado) ON DELETE RESTRICT,
    prioridad VARCHAR(20) NOT NULL DEFAULT 'media',
    estado_publicacion VARCHAR(20) NOT NULL DEFAULT 'pendiente',
    ubicacion geometry(Point,4326),
    direccion_referencia TEXT,
    fecha_creacion TIMESTAMPTZ NOT NULL DEFAULT now(),
    fecha_actualizacion TIMESTAMPTZ NOT NULL DEFAULT now(),
    fecha_aprobacion TIMESTAMPTZ,
    CONSTRAINT ck_caso_prioridad CHECK (prioridad IN ('baja','media','alta','critica')),
    CONSTRAINT ck_caso_publicacion CHECK (estado_publicacion IN ('pendiente','aprobado','rechazado')),
    CONSTRAINT ck_caso_aprobacion CHECK (estado_publicacion <> 'aprobado' OR fecha_aprobacion IS NOT NULL)
);

CREATE TABLE asignaciones_responsables (
    id_asignacion UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_usuario UUID NOT NULL REFERENCES usuarios(id_usuario) ON DELETE RESTRICT,
    id_comunidad UUID REFERENCES comunidades(id_comunidad) ON DELETE RESTRICT,
    id_tipo_caso UUID REFERENCES tipos_caso(id_tipo_caso) ON DELETE RESTRICT,
    fecha_asignacion TIMESTAMPTZ NOT NULL DEFAULT now(),
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT ck_ambito_responsable CHECK (id_comunidad IS NOT NULL OR id_tipo_caso IS NOT NULL)
);

CREATE TABLE evidencias (
    id_evidencia UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_caso UUID NOT NULL REFERENCES casos(id_caso) ON DELETE RESTRICT,
    id_usuario UUID NOT NULL REFERENCES usuarios(id_usuario) ON DELETE RESTRICT,
    tipo_archivo VARCHAR(30) NOT NULL,
    ruta_archivo TEXT NOT NULL,
    descripcion TEXT,
    fecha_subida TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT ck_evidencia_tipo CHECK (tipo_archivo IN ('imagen','video','audio','documento'))
);

CREATE TABLE seguimientos (
    id_seguimiento UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_caso UUID NOT NULL REFERENCES casos(id_caso) ON DELETE RESTRICT,
    id_usuario UUID NOT NULL REFERENCES usuarios(id_usuario) ON DELETE RESTRICT,
    descripcion TEXT NOT NULL,
    fecha_seguimiento TIMESTAMPTZ NOT NULL DEFAULT now(),
    visible_publicamente BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE historial_estados (
    id_historial UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_caso UUID NOT NULL REFERENCES casos(id_caso) ON DELETE RESTRICT,
    id_estado_anterior UUID REFERENCES estados_caso(id_estado) ON DELETE RESTRICT,
    id_estado_nuevo UUID NOT NULL REFERENCES estados_caso(id_estado) ON DELETE RESTRICT,
    id_usuario UUID REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    motivo TEXT,
    fecha_cambio TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT ck_historial_distinto CHECK (id_estado_anterior IS DISTINCT FROM id_estado_nuevo)
);

CREATE TABLE asignaciones_casos (
    id_asignacion_caso UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_caso UUID NOT NULL REFERENCES casos(id_caso) ON DELETE RESTRICT,
    id_responsable UUID NOT NULL REFERENCES usuarios(id_usuario) ON DELETE RESTRICT,
    id_asignador UUID NOT NULL REFERENCES usuarios(id_usuario) ON DELETE RESTRICT,
    fecha_asignacion TIMESTAMPTZ NOT NULL DEFAULT now(),
    fecha_finalizacion TIMESTAMPTZ,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT ck_fin_asignacion CHECK (fecha_finalizacion IS NULL OR fecha_finalizacion >= fecha_asignacion)
);

CREATE TABLE comentarios (
    id_comentario UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_caso UUID NOT NULL REFERENCES casos(id_caso) ON DELETE RESTRICT,
    id_usuario UUID NOT NULL REFERENCES usuarios(id_usuario) ON DELETE RESTRICT,
    contenido TEXT NOT NULL,
    estado_moderacion VARCHAR(20) NOT NULL DEFAULT 'pendiente',
    fecha_creacion TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT ck_comentario_moderacion CHECK (estado_moderacion IN ('pendiente','aprobado','rechazado','oculto'))
);

CREATE TABLE mensajes_privados (
    id_mensaje UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_caso UUID REFERENCES casos(id_caso) ON DELETE RESTRICT,
    id_remitente UUID NOT NULL REFERENCES usuarios(id_usuario) ON DELETE RESTRICT,
    id_destinatario UUID NOT NULL REFERENCES usuarios(id_usuario) ON DELETE RESTRICT,
    contenido TEXT NOT NULL,
    fecha_envio TIMESTAMPTZ NOT NULL DEFAULT now(),
    fecha_lectura TIMESTAMPTZ,
    CONSTRAINT ck_mensaje_destino CHECK (id_remitente <> id_destinatario),
    CONSTRAINT ck_fecha_lectura CHECK (fecha_lectura IS NULL OR fecha_lectura >= fecha_envio)
);

CREATE TABLE notificaciones (
    id_notificacion UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_usuario UUID NOT NULL REFERENCES usuarios(id_usuario) ON DELETE RESTRICT,
    id_caso UUID REFERENCES casos(id_caso) ON DELETE RESTRICT,
    titulo VARCHAR(150) NOT NULL,
    mensaje TEXT NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    leida BOOLEAN NOT NULL DEFAULT FALSE,
    fecha_creacion TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE configuracion_plataforma (
    id_configuracion UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    clave VARCHAR(100) NOT NULL UNIQUE,
    valor JSONB NOT NULL,
    fecha_actualizacion TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 03. INICIATIVAS Y EDICIONES ------------------------------------------------
-- Iniciativa = programa permanente; edicion = ejecucion en un ano determinado.
CREATE TABLE iniciativas (
    id_iniciativa UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_creador UUID NOT NULL REFERENCES usuarios(id_usuario) ON DELETE RESTRICT,
    titulo VARCHAR(200) NOT NULL,
    subtitulo VARCHAR(250),
    slug VARCHAR(220) NOT NULL UNIQUE,
    descripcion_corta TEXT,
    descripcion TEXT,
    categoria VARCHAR(80) NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'planificada',
    estado_publicacion VARCHAR(20) NOT NULL DEFAULT 'borrador',
    destacada BOOLEAN NOT NULL DEFAULT FALSE,
    orden_destacado INTEGER,
    fecha_creacion TIMESTAMPTZ NOT NULL DEFAULT now(),
    fecha_actualizacion TIMESTAMPTZ NOT NULL DEFAULT now(),
    fecha_publicacion TIMESTAMPTZ,
    CONSTRAINT ck_iniciativa_slug CHECK (slug ~ '^[a-z0-9]+(-[a-z0-9]+)*$'),
    CONSTRAINT ck_iniciativa_estado CHECK (estado IN ('planificada','en_curso','finalizada','cancelada')),
    CONSTRAINT ck_iniciativa_publicacion CHECK (estado_publicacion IN ('borrador','pendiente','publicada','rechazada')),
    CONSTRAINT ck_iniciativa_fecha_pub CHECK (estado_publicacion <> 'publicada' OR fecha_publicacion IS NOT NULL),
    CONSTRAINT ck_iniciativa_destacada CHECK (NOT destacada OR estado_publicacion = 'publicada'),
    CONSTRAINT ck_iniciativa_orden CHECK (orden_destacado IS NULL OR orden_destacado > 0)
);

CREATE TABLE iniciativa_ediciones (
    id_edicion UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_iniciativa UUID NOT NULL REFERENCES iniciativas(id_iniciativa) ON DELETE RESTRICT,
    anio SMALLINT NOT NULL CHECK (anio BETWEEN 2000 AND 2200),
    nombre_edicion VARCHAR(150),
    temporada VARCHAR(100),
    descripcion TEXT,
    fecha_inicio DATE,
    fecha_fin DATE,
    estado VARCHAR(20) NOT NULL DEFAULT 'planificada',
    fecha_creacion TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_edicion_anual UNIQUE (id_iniciativa, anio),
    CONSTRAINT uq_edicion_pertenencia UNIQUE (id_iniciativa, id_edicion),
    CONSTRAINT ck_edicion_fechas CHECK (fecha_fin IS NULL OR fecha_inicio IS NULL OR fecha_fin >= fecha_inicio),
    CONSTRAINT ck_edicion_estado CHECK (estado IN ('planificada','en_curso','finalizada','cancelada'))
);

CREATE TABLE iniciativa_multimedia (
    id_multimedia UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_iniciativa UUID NOT NULL REFERENCES iniciativas(id_iniciativa) ON DELETE RESTRICT,
    id_edicion UUID,
    tipo VARCHAR(20) NOT NULL,
    ruta_archivo TEXT NOT NULL,
    texto_alternativo TEXT,
    descripcion TEXT,
    es_portada BOOLEAN NOT NULL DEFAULT FALSE,
    orden INTEGER NOT NULL DEFAULT 0 CHECK (orden >= 0),
    fecha_subida TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT ck_multimedia_tipo CHECK (tipo IN ('imagen','video','documento')),
    CONSTRAINT ck_portada_imagen CHECK (NOT es_portada OR tipo = 'imagen'),
    CONSTRAINT fk_multimedia_edicion FOREIGN KEY (id_iniciativa, id_edicion)
        REFERENCES iniciativa_ediciones (id_iniciativa, id_edicion) ON DELETE RESTRICT
);
-- Una portada general por iniciativa y una portada por edicion.
CREATE UNIQUE INDEX ux_multimedia_portada_general ON iniciativa_multimedia(id_iniciativa)
    WHERE es_portada AND id_edicion IS NULL;
CREATE UNIQUE INDEX ux_multimedia_portada_edicion ON iniciativa_multimedia(id_edicion)
    WHERE es_portada AND id_edicion IS NOT NULL;

CREATE TABLE iniciativa_indicadores (
    id_indicador UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_edicion UUID NOT NULL REFERENCES iniciativa_ediciones(id_edicion) ON DELETE RESTRICT,
    nombre VARCHAR(100) NOT NULL,
    valor NUMERIC(14,2) NOT NULL DEFAULT 0,
    unidad VARCHAR(50),
    descripcion TEXT,
    icono VARCHAR(50),
    tipo_medicion VARCHAR(20) NOT NULL DEFAULT 'real',
    orden INTEGER NOT NULL DEFAULT 0 CHECK (orden >= 0),
    fecha_corte DATE,
    CONSTRAINT ck_indicador_valor CHECK (valor >= 0),
    CONSTRAINT ck_indicador_medicion CHECK (tipo_medicion IN ('estimado','real'))
);

CREATE TABLE iniciativa_comunidades (
    id_iniciativa_comunidad UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_edicion UUID NOT NULL REFERENCES iniciativa_ediciones(id_edicion) ON DELETE RESTRICT,
    id_comunidad UUID NOT NULL REFERENCES comunidades(id_comunidad) ON DELETE RESTRICT,
    observaciones TEXT,
    CONSTRAINT uq_edicion_comunidad UNIQUE (id_edicion, id_comunidad)
);

CREATE TABLE iniciativa_actividades (
    id_actividad UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_edicion UUID NOT NULL REFERENCES iniciativa_ediciones(id_edicion) ON DELETE RESTRICT,
    id_responsable UUID REFERENCES usuarios(id_usuario) ON DELETE RESTRICT,
    id_comunidad UUID REFERENCES comunidades(id_comunidad) ON DELETE RESTRICT,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT,
    fecha_inicio TIMESTAMPTZ NOT NULL,
    fecha_fin TIMESTAMPTZ,
    lugar VARCHAR(200),
    ubicacion geometry(Point,4326),
    estado VARCHAR(20) NOT NULL DEFAULT 'programada',
    fecha_creacion TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT ck_actividad_fechas CHECK (fecha_fin IS NULL OR fecha_fin >= fecha_inicio),
    CONSTRAINT ck_actividad_estado CHECK (estado IN ('programada','realizada','cancelada'))
);

CREATE TABLE propuestas_iniciativas (
    id_propuesta UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_usuario UUID REFERENCES usuarios(id_usuario) ON DELETE RESTRICT,
    id_comunidad UUID REFERENCES comunidades(id_comunidad) ON DELETE RESTRICT,
    nombre_contacto VARCHAR(150),
    telefono_contacto VARCHAR(25),
    comunidad_declarada VARCHAR(200),
    acepta_tratamiento_datos BOOLEAN NOT NULL DEFAULT FALSE,
    id_iniciativa_solicitada UUID REFERENCES iniciativas(id_iniciativa) ON DELETE RESTRICT,
    id_iniciativa_generada UUID REFERENCES iniciativas(id_iniciativa) ON DELETE RESTRICT,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL,
    tipo_actividad VARCHAR(80),
    fecha_sugerida DATE,
    estado VARCHAR(20) NOT NULL DEFAULT 'pendiente',
    respuesta TEXT,
    id_revisor UUID REFERENCES usuarios(id_usuario) ON DELETE RESTRICT,
    fecha_creacion TIMESTAMPTZ NOT NULL DEFAULT now(),
    fecha_revision TIMESTAMPTZ,
    CONSTRAINT ck_propuesta_estado CHECK (estado IN ('pendiente','en_revision','aprobada','rechazada')),
    CONSTRAINT ck_propuesta_contacto CHECK
        (id_usuario IS NOT NULL OR (nombre_contacto IS NOT NULL AND telefono_contacto IS NOT NULL)),
    CONSTRAINT ck_propuesta_territorio CHECK
        (id_comunidad IS NOT NULL OR comunidad_declarada IS NOT NULL),
    CONSTRAINT ck_propuesta_consentimiento CHECK (acepta_tratamiento_datos = TRUE),
    CONSTRAINT ck_propuesta_revision CHECK (
        (estado IN ('pendiente','en_revision')) OR (id_revisor IS NOT NULL AND fecha_revision IS NOT NULL)
    )
);
-- Admite postulaciones publicas: conservar los contactos con acceso restringido,
-- limitar retencion y validar consentimiento desde la interfaz y el backend.

CREATE TABLE iniciativa_casos (
    id_iniciativa_caso UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_edicion UUID NOT NULL REFERENCES iniciativa_ediciones(id_edicion) ON DELETE RESTRICT,
    id_caso UUID NOT NULL REFERENCES casos(id_caso) ON DELETE RESTRICT,
    tipo_vinculo VARCHAR(30) NOT NULL DEFAULT 'hallazgo',
    observaciones TEXT,
    fecha_vinculacion TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_edicion_caso UNIQUE (id_edicion,id_caso),
    CONSTRAINT ck_vinculo_tipo CHECK (tipo_vinculo IN ('hallazgo','seguimiento','resultado','otro'))
);

-- 04. AUDITORIA ESPECIALIZADA (5 TABLAS) -------------------------------------
-- Estas tablas no deben ser editables por los usuarios de la aplicacion.
CREATE TABLE auditoria_eventos (
    id_auditoria UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_usuario UUID REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    accion VARCHAR(100) NOT NULL,
    modulo VARCHAR(100) NOT NULL,
    tabla_afectada VARCHAR(100),
    id_registro UUID,
    datos_anteriores JSONB,
    datos_nuevos JSONB,
    direccion_ip INET,
    user_agent TEXT,
    fecha_evento TIMESTAMPTZ NOT NULL DEFAULT now(),
    resultado VARCHAR(20) NOT NULL DEFAULT 'exitoso',
    CONSTRAINT ck_auditoria_resultado CHECK (resultado IN ('exitoso','fallido'))
);

CREATE TABLE auditoria_accesos (
    id_acceso UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_usuario UUID REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    correo_intentado VARCHAR(150),
    tipo_evento VARCHAR(50) NOT NULL,
    resultado VARCHAR(20) NOT NULL,
    direccion_ip INET,
    user_agent TEXT,
    fecha_evento TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT ck_acceso_resultado CHECK (resultado IN ('exitoso','fallido'))
);

CREATE TABLE auditoria_casos (
    id_auditoria_caso UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_caso UUID NOT NULL REFERENCES casos(id_caso) ON DELETE RESTRICT,
    id_usuario UUID REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    tipo_accion VARCHAR(100) NOT NULL,
    estado_anterior VARCHAR(50),
    estado_nuevo VARCHAR(50),
    motivo TEXT,
    fecha_accion TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE auditoria_permisos (
    id_auditoria_permiso UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_usuario_afectado UUID NOT NULL REFERENCES usuarios(id_usuario) ON DELETE RESTRICT,
    id_usuario_responsable UUID REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    tipo_cambio VARCHAR(100) NOT NULL,
    valor_anterior JSONB,
    valor_nuevo JSONB,
    motivo TEXT,
    fecha_cambio TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE auditoria_seguridad (
    id_evento_seguridad UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_usuario UUID REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    tipo_evento VARCHAR(100) NOT NULL,
    nivel_severidad VARCHAR(20) NOT NULL DEFAULT 'medio',
    descripcion TEXT,
    direccion_ip INET,
    fecha_evento TIMESTAMPTZ NOT NULL DEFAULT now(),
    atendido BOOLEAN NOT NULL DEFAULT FALSE,
    fecha_atencion TIMESTAMPTZ,
    CONSTRAINT ck_seguridad_severidad CHECK (nivel_severidad IN ('bajo','medio','alto','critico')),
    CONSTRAINT ck_seguridad_atencion CHECK (fecha_atencion IS NULL OR atendido)
);

-- 05. INDICES DE BUSQUEDA Y ESPACIALES --------------------------------------
CREATE INDEX ix_municipios_departamento ON municipios(id_departamento);
CREATE INDEX ix_comunidades_municipio ON comunidades(id_municipio);
CREATE INDEX ix_comunidades_gist ON comunidades USING GIST(ubicacion);
CREATE INDEX ix_usuarios_rol ON usuarios(id_rol);
CREATE INDEX ix_casos_comunidad_estado ON casos(id_comunidad,id_estado);
CREATE INDEX ix_casos_tipo ON casos(id_tipo_caso);
CREATE INDEX ix_casos_usuario_fecha ON casos(id_usuario,fecha_creacion DESC);
CREATE INDEX ix_casos_estado_publicacion ON casos(estado_publicacion,fecha_creacion DESC);
CREATE INDEX ix_casos_gist ON casos USING GIST(ubicacion);
CREATE INDEX ix_asignacion_ambito_usuario ON asignaciones_responsables(id_usuario,activo);
CREATE INDEX ix_asignacion_responsables_comunidad ON asignaciones_responsables(id_comunidad);
CREATE INDEX ix_asignacion_responsables_tipo ON asignaciones_responsables(id_tipo_caso);
CREATE INDEX ix_evidencias_caso ON evidencias(id_caso);
CREATE INDEX ix_seguimientos_caso_fecha ON seguimientos(id_caso,fecha_seguimiento DESC);
CREATE INDEX ix_historial_caso_fecha ON historial_estados(id_caso,fecha_cambio DESC);
CREATE INDEX ix_historial_estado_anterior ON historial_estados(id_estado_anterior);
CREATE INDEX ix_historial_estado_nuevo ON historial_estados(id_estado_nuevo);
CREATE INDEX ix_historial_usuario ON historial_estados(id_usuario);
CREATE INDEX ix_asignacion_caso_responsable ON asignaciones_casos(id_responsable);
CREATE INDEX ix_asignacion_caso_asignador ON asignaciones_casos(id_asignador);
CREATE UNIQUE INDEX ux_asignacion_caso_activa ON asignaciones_casos(id_caso)
    WHERE activo = TRUE; -- Solo un responsable activo por caso (politica MVP).
CREATE INDEX ix_comentarios_caso ON comentarios(id_caso,estado_moderacion,fecha_creacion DESC);
CREATE INDEX ix_comentarios_usuario ON comentarios(id_usuario);
CREATE INDEX ix_mensajes_destinatario ON mensajes_privados(id_destinatario,fecha_envio DESC);
CREATE INDEX ix_mensajes_remitente ON mensajes_privados(id_remitente,fecha_envio DESC);
CREATE INDEX ix_mensajes_caso ON mensajes_privados(id_caso);
CREATE INDEX ix_notificaciones_usuario ON notificaciones(id_usuario,leida,fecha_creacion DESC);
CREATE INDEX ix_notificaciones_caso ON notificaciones(id_caso);
CREATE INDEX ix_iniciativas_destacadas ON iniciativas(orden_destacado,fecha_publicacion DESC)
    WHERE destacada AND estado_publicacion = 'publicada';
CREATE INDEX ix_iniciativas_categoria ON iniciativas(categoria,estado_publicacion);
CREATE INDEX ix_ediciones_iniciativa_anio ON iniciativa_ediciones(id_iniciativa,anio DESC);
CREATE INDEX ix_multimedia_iniciativa ON iniciativa_multimedia(id_iniciativa,orden);
CREATE INDEX ix_multimedia_edicion ON iniciativa_multimedia(id_edicion,orden);
CREATE INDEX ix_indicadores_edicion ON iniciativa_indicadores(id_edicion,orden);
CREATE INDEX ix_iniciativa_comunidades_comunidad ON iniciativa_comunidades(id_comunidad);
CREATE INDEX ix_actividades_edicion_fecha ON iniciativa_actividades(id_edicion,fecha_inicio);
CREATE INDEX ix_actividades_comunidad ON iniciativa_actividades(id_comunidad);
CREATE INDEX ix_actividades_responsable ON iniciativa_actividades(id_responsable);
CREATE INDEX ix_actividades_gist ON iniciativa_actividades USING GIST(ubicacion);
CREATE INDEX ix_propuestas_usuario ON propuestas_iniciativas(id_usuario,fecha_creacion DESC);
CREATE INDEX ix_propuestas_comunidad_estado ON propuestas_iniciativas(id_comunidad,estado);
CREATE INDEX ix_propuestas_revisor ON propuestas_iniciativas(id_revisor);
CREATE INDEX ix_propuestas_iniciativa_solicitada ON propuestas_iniciativas(id_iniciativa_solicitada);
CREATE INDEX ix_propuestas_iniciativa_generada ON propuestas_iniciativas(id_iniciativa_generada);
CREATE INDEX ix_iniciativa_casos_caso ON iniciativa_casos(id_caso);
CREATE INDEX ix_auditoria_eventos_usuario_fecha ON auditoria_eventos(id_usuario,fecha_evento DESC);
CREATE INDEX ix_auditoria_eventos_tabla_fecha ON auditoria_eventos(tabla_afectada,fecha_evento DESC);
CREATE INDEX ix_auditoria_accesos_fecha ON auditoria_accesos(fecha_evento DESC);
CREATE INDEX ix_auditoria_casos_caso_fecha ON auditoria_casos(id_caso,fecha_accion DESC);
CREATE INDEX ix_auditoria_permisos_usuario_fecha ON auditoria_permisos(id_usuario_afectado,fecha_cambio DESC);
CREATE INDEX ix_auditoria_seguridad_fecha ON auditoria_seguridad(nivel_severidad,fecha_evento DESC);

-- 06. TRIGGERS DE TIMESTAMPS Y TRAZABILIDAD ---------------------------------
CREATE OR REPLACE FUNCTION actualizar_fecha_modificacion()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
    NEW.fecha_actualizacion := now();
    RETURN NEW;
END;
$$;

CREATE TRIGGER tg_usuarios_actualizacion BEFORE UPDATE ON usuarios
    FOR EACH ROW EXECUTE FUNCTION actualizar_fecha_modificacion();
CREATE TRIGGER tg_casos_actualizacion BEFORE UPDATE ON casos
    FOR EACH ROW EXECUTE FUNCTION actualizar_fecha_modificacion();
CREATE TRIGGER tg_iniciativas_actualizacion BEFORE UPDATE ON iniciativas
    FOR EACH ROW EXECUTE FUNCTION actualizar_fecha_modificacion();
CREATE TRIGGER tg_configuracion_actualizacion BEFORE UPDATE ON configuracion_plataforma
    FOR EACH ROW EXECUTE FUNCTION actualizar_fecha_modificacion();

-- Los cambios del estado operativo generan su historial en la misma transaccion.
-- El actor se obtiene de SET LOCAL plus.actor_id='UUID' configurado por el backend.
CREATE OR REPLACE FUNCTION registrar_historial_estado()
RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE
    actor UUID;
BEGIN
    IF TG_OP = 'INSERT' THEN
        actor := NULLIF(current_setting('plus.actor_id',true),'')::UUID;
        INSERT INTO historial_estados(id_caso,id_estado_anterior,id_estado_nuevo,id_usuario,motivo)
        VALUES (NEW.id_caso,NULL,NEW.id_estado,actor,'Creacion del caso');
    ELSIF OLD.id_estado IS DISTINCT FROM NEW.id_estado THEN
        actor := NULLIF(current_setting('plus.actor_id',true),'')::UUID;
        INSERT INTO historial_estados(id_caso,id_estado_anterior,id_estado_nuevo,id_usuario,motivo)
        VALUES (NEW.id_caso,OLD.id_estado,NEW.id_estado,actor,'Cambio de estado');
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER tg_casos_historial AFTER INSERT OR UPDATE OF id_estado ON casos
    FOR EACH ROW EXECUTE FUNCTION registrar_historial_estado();

-- Auditoria general: guarda solo nombres de columnas modificadas, no PII,
-- contrasenas, mensajes o contenido sensible. La auditoria detallada de casos,
-- permisos, accesos y seguridad se completa desde el backend autorizado.
CREATE OR REPLACE FUNCTION registrar_auditoria_basica()
RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE
    actor UUID := NULLIF(current_setting('plus.actor_id',true),'')::UUID;
    pk_col TEXT := TG_ARGV[0];
    objeto_id UUID;
    cambio TEXT[];
BEGIN
    IF TG_OP = 'DELETE' THEN
        objeto_id := (to_jsonb(OLD)->>pk_col)::UUID;
    ELSE
        objeto_id := (to_jsonb(NEW)->>pk_col)::UUID;
    END IF;
    IF TG_OP = 'UPDATE' THEN
        SELECT array_agg(k ORDER BY k) INTO cambio
        FROM jsonb_object_keys(to_jsonb(NEW)) AS k
        WHERE (to_jsonb(OLD)->k) IS DISTINCT FROM (to_jsonb(NEW)->k);
    END IF;
    INSERT INTO auditoria_eventos(id_usuario,accion,modulo,tabla_afectada,id_registro,datos_nuevos)
    VALUES (actor,lower(TG_OP),'gestion',TG_TABLE_NAME,objeto_id,
        CASE WHEN TG_OP = 'UPDATE' THEN jsonb_build_object('columnas_modificadas',to_jsonb(cambio))
             ELSE NULL END);
    IF TG_OP = 'DELETE' THEN
        RETURN OLD;
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER tg_audit_usuarios AFTER INSERT OR UPDATE OR DELETE ON usuarios
    FOR EACH ROW EXECUTE FUNCTION registrar_auditoria_basica('id_usuario');
CREATE TRIGGER tg_audit_casos AFTER INSERT OR UPDATE OR DELETE ON casos
    FOR EACH ROW EXECUTE FUNCTION registrar_auditoria_basica('id_caso');
CREATE TRIGGER tg_audit_iniciativas AFTER INSERT OR UPDATE OR DELETE ON iniciativas
    FOR EACH ROW EXECUTE FUNCTION registrar_auditoria_basica('id_iniciativa');
CREATE TRIGGER tg_audit_ediciones AFTER INSERT OR UPDATE OR DELETE ON iniciativa_ediciones
    FOR EACH ROW EXECUTE FUNCTION registrar_auditoria_basica('id_edicion');
CREATE TRIGGER tg_audit_propuestas AFTER INSERT OR UPDATE OR DELETE ON propuestas_iniciativas
    FOR EACH ROW EXECUTE FUNCTION registrar_auditoria_basica('id_propuesta');
CREATE TRIGGER tg_audit_asignaciones AFTER INSERT OR UPDATE OR DELETE ON asignaciones_casos
    FOR EACH ROW EXECUTE FUNCTION registrar_auditoria_basica('id_asignacion_caso');

-- Eventos especificos: publica/rechaza casos, modifica prioridades y roles.
CREATE OR REPLACE FUNCTION registrar_auditoria_caso_clave()
RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE actor UUID := NULLIF(current_setting('plus.actor_id',true),'')::UUID;
BEGIN
    IF OLD.estado_publicacion IS DISTINCT FROM NEW.estado_publicacion THEN
        INSERT INTO auditoria_casos(id_caso,id_usuario,tipo_accion,estado_anterior,estado_nuevo,motivo)
        VALUES (NEW.id_caso,actor,'publicacion',OLD.estado_publicacion,NEW.estado_publicacion,
                'Cambio de estado de publicacion');
    END IF;
    IF OLD.prioridad IS DISTINCT FROM NEW.prioridad THEN
        INSERT INTO auditoria_casos(id_caso,id_usuario,tipo_accion,estado_anterior,estado_nuevo,motivo)
        VALUES (NEW.id_caso,actor,'prioridad',OLD.prioridad,NEW.prioridad,
                'Cambio de prioridad');
    END IF;
    RETURN NEW;
END;
$$;
CREATE TRIGGER tg_auditoria_caso_clave AFTER UPDATE OF estado_publicacion,prioridad ON casos
    FOR EACH ROW EXECUTE FUNCTION registrar_auditoria_caso_clave();

CREATE OR REPLACE FUNCTION registrar_auditoria_cambio_rol()
RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE actor UUID := NULLIF(current_setting('plus.actor_id',true),'')::UUID;
BEGIN
    IF OLD.id_rol IS DISTINCT FROM NEW.id_rol THEN
        INSERT INTO auditoria_permisos
            (id_usuario_afectado,id_usuario_responsable,tipo_cambio,valor_anterior,valor_nuevo)
        VALUES (NEW.id_usuario,actor,'cambio_rol',
                jsonb_build_object('id_rol',OLD.id_rol),
                jsonb_build_object('id_rol',NEW.id_rol));
    END IF;
    RETURN NEW;
END;
$$;
CREATE TRIGGER tg_auditoria_cambio_rol AFTER UPDATE OF id_rol ON usuarios
    FOR EACH ROW EXECUTE FUNCTION registrar_auditoria_cambio_rol();

-- 07. VISTAS PUBLICAS (NO EXPONER DATOS PERSONALES) --------------------------
CREATE VIEW vw_casos_mapa AS
SELECT c.id_caso, c.codigo, c.titulo, c.prioridad,
       ec.nombre AS estado, tc.nombre AS tipo,
       co.nombre AS comunidad,
       ST_X(c.ubicacion) AS longitud, ST_Y(c.ubicacion) AS latitud,
       c.fecha_creacion
FROM casos c
JOIN estados_caso ec ON ec.id_estado = c.id_estado
JOIN tipos_caso tc ON tc.id_tipo_caso = c.id_tipo_caso
JOIN comunidades co ON co.id_comunidad = c.id_comunidad
WHERE c.estado_publicacion = 'aprobado' AND c.ubicacion IS NOT NULL;
-- IMPORTANTE: esta vista contiene coordenadas exactas. NO conceder acceso publico
-- sin revisar ubicaciones sensibles; preferir API que generalice coordenadas.

CREATE VIEW vw_iniciativas_destacadas AS
SELECT i.id_iniciativa,i.titulo,i.subtitulo,i.slug,i.descripcion_corta,
       i.categoria,i.orden_destacado,i.fecha_publicacion,
       m.ruta_archivo AS portada
FROM iniciativas i
LEFT JOIN LATERAL (
    SELECT ruta_archivo FROM iniciativa_multimedia im
    WHERE im.id_iniciativa=i.id_iniciativa AND im.es_portada
      AND im.id_edicion IS NULL
    LIMIT 1
) m ON TRUE
WHERE i.estado_publicacion='publicada' AND i.destacada=TRUE;

-- 08. DATOS DE CATALOGO (NO SON ESTADISTICAS NI CASOS REALES) ----------------
INSERT INTO roles(nombre,descripcion) VALUES
    ('administrador','Administracion general de PLUS'),
    ('representante','Representacion y gestion territorial'),
    ('moderador','Revision de publicaciones y comentarios'),
    ('ciudadano','Usuario que reporta casos y propone iniciativas');

INSERT INTO estados_caso(nombre,descripcion,orden) VALUES
    ('pendiente','Caso recibido pendiente de gestion',1),
    ('en_revision','Caso en verificacion',2),
    ('en_proceso','Caso en seguimiento',3),
    ('resuelto','Caso solucionado',4),
    ('cerrado','Caso archivado o cerrado',5);

INSERT INTO configuracion_plataforma(clave,valor) VALUES
    ('institucion.nombre',to_jsonb('Corporacion Pluralismo Social'::text)),
    ('mapa.srid',to_jsonb(4326)),
    ('iniciativas.max_destacadas',to_jsonb(4));

COMMIT;

-- ============================================================================
-- FIN. Comprobacion sugerida (una vez conectado a la BD):
-- SELECT count(*) FROM information_schema.tables
-- WHERE table_schema='plus' AND table_type='BASE TABLE'; -- 30
-- SELECT postgis_full_version();
-- SELECT * FROM plus.vw_iniciativas_destacadas;
--
-- Ejemplo seguro desde backend dentro de una transaccion:
-- BEGIN;
-- SET LOCAL plus.actor_id = 'UUID-VALIDO-DEL-USUARIO-AUTENTICADO';
-- UPDATE plus.casos SET id_estado = 'UUID-ESTADO' WHERE id_caso = 'UUID-CASO';
-- COMMIT;
--
-- PENDIENTE PARA PRODUCCION:
-- * Crear roles PostgreSQL de minimo privilegio y GRANT explicitos;
-- * Validar autorizacion de negocio en backend (incluidos archivos y datos GIS);
-- * No exponer la vista de coordenadas precisas directamente al publico;
-- * Implementar almacenamiento de archivos, consentimiento, retencion de datos;
-- * Gestionar migraciones y copias de seguridad;
-- * Evitar acceso INSERT/UPDATE/DELETE directo a tablas de auditoria;
-- * Registrar accesos, cambios de permisos y decisiones de moderacion desde backend.
-- ============================================================================
