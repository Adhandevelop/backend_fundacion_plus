# Endpoints para integrar PLUS — revisión contra el esquema v1.1

**Estado:** solicitud revisada para el backend. Las rutas y los DTO siguen siendo propuestas; el SQL no demuestra que existan vistas Django, serializers ni endpoints implementados.

**Fuente principal:** [`base de datos.md`](../base%20de%20datos.md), esquema SQL integral v1.1 con **30 tablas** en `plus`, vistas, restricciones, índices, triggers y catálogos iniciales. Se contrastó con el frontend y con la propuesta anterior de este documento.

**Alcance de esta revisión:** ajustar la petición de API a lo que el modelo puede representar, señalar adaptaciones del frontend y separar ampliaciones pendientes. No se ejecutó el SQL, no se revisó una base desplegada y no se modificaron Angular, Django ni el esquema.

**Criterio acordado:** se pueden solicitar tablas y campos nuevos para cubrir las funciones previstas. La ausencia de persistencia no es motivo para retirar esas funciones del alcance. La sección 18 concreta las ampliaciones solicitadas al backend; siguen siendo propuestas de diseño que debe traducir a migraciones y contratos. Mientras no estén implementadas, los endpoints afectados no se presentan como disponibles.

## 1. Cambios principales frente a la petición anterior

| Tema | Lo que define el SQL | Corrección de la petición |
|---|---|---|
| Identificadores | Claves primarias UUID. | La API debe entregar UUID reales; los identificadores `demo-*` y `local-*` se eliminan al integrar. |
| Roles | `usuarios.id_rol` obligatorio: **un rol por usuario**. Catálogo inicial: `administrador`, `representante`, `moderador`, `ciudadano`. | Mantener rol único y `PUT .../role/` hasta decidir la ampliación multirrol AMP-14. No asumir editor/superadministrador/responsable como roles existentes. «Responsable» también es una relación de asignación, no necesariamente un rol. |
| Identidad | `nombres` y `apellidos` separados, ambos obligatorios; correo 150 y teléfono 20 caracteres. | Dividir el campo nombre en los formularios pertinentes y ajustar límites. No deducir apellidos automáticamente separando el último espacio. |
| Estado del usuario | `activo`, `suspendido`, `inactivo`. | Reemplazar el booleano del prototipo por un estado de tres valores; acordar transiciones y efectos sobre sesiones. |
| Estados de caso | Filas iniciales: `pendiente`, `en_revision`, `en_proceso`, `resuelto`, `cerrado`. La asignación se almacena aparte. | No enviar «Recibido», «Asignado» o «En gestión» como códigos de estado. Consumir `estados_caso`; mostrar asignación como dimensión independiente. |
| Prioridad y publicación | Prioridad: `baja`, `media`, `alta`, `critica`. Publicación: `pendiente`, `aprobado`, `rechazado`. | Incluir crítica y conservar la separación entre estado operativo y publicación. Una solicitud de corrección no tiene estado/entidad propios en este SQL. |
| Tipificación | `tipos_caso` contiene `nombre`, `descripcion`, `categoria` de texto. | No exigir una tabla independiente de categorías. Filtrar por categoría textual y seleccionar `id_tipo_caso`; acordar dónde representar «problemática» frente a «proyecto/iniciativa». |
| Territorio | Caso → comunidad → municipio → departamento. No hay cuencas. | Enviar `id_comunidad` al caso; derivar municipio/departamento para lectura. Cuencas queda condicionado a ampliar/adaptar el filtro. |
| Asignación | Ámbitos en `asignaciones_responsables`; asignación efectiva en `asignaciones_casos`, con un responsable activo por caso. | No asignar por coincidencia de nombre o rol. Resolver candidatos y autorización considerando ambas relaciones. |
| Evidencias | Hay archivo, tipo, descripción, autor y caso. **No hay visibilidad pública/privada por evidencia**. | No activar publicación ni el cambio de visibilidad hasta acordar persistencia. Aprobar un caso no publica sus archivos automáticamente. |
| Seguimiento | Solo `visible_publicamente` booleano; no hay título ni tres niveles de visibilidad. | No equiparar `false` con «visible para el ciudadano». Resolver la distinción interno/ciudadano antes de entregar notas privadas. |
| Iniciativas | Programa permanente → edición anual → indicadores/comunidades/actividades. | El filtro de año consulta ediciones; indicadores y cobertura no se atribuyen directamente al programa. Añadir lecturas de ediciones. |
| Postulaciones | `propuestas_iniciativas` exige título, descripción, contacto/usuario, territorio y consentimiento verdadero. | El formulario actual debe añadir título y consentimiento antes del envío real. No crear una iniciativa al recibir una propuesta. |
| Mensajes | Cada fila exige remitente y destinatario; `id_caso` puede ser nulo. | Una conversación no es un chat global del caso. Acordar destinatario, agrupación y lectura por participante. |
| Auditoría | Cinco tablas especializadas; auditoría general guarda nombres de columnas, no valores completos. | No prometer antes/después en todos los eventos. Definir fuente del evento y devolver diferencias solo si existen y son autorizadas. |
| Funciones ausentes | No hay tablas de noticias, boletín, casos seguidos, preferencias o foto de usuario. | Mantener esos endpoints como condicionados, sin afirmar que el SQL ya los soporta. |

## 2. Convenciones de la API y lectura del inventario

- Base propuesta `/api/v1/`, según `contexto.md`. Las rutas siguientes son relativas a esa base. No confundir rutas Angular en español con rutas de API todavía por acordar.
- Angular consume URLs relativas del mismo sitio. `docker/nginx.conf` conserva `/api/` al enviar al backend; `backend:8000` es una dirección interna, no una URL de navegador.
- El documento usa los **nombres SQL en español** para identificar datos persistidos. El backend puede publicar DTO en español o inglés, pero debe entregar un mapeo explícito; no mezclar ambos accidentalmente.
- `{id}`, `{case_id}`, `{edition_id}` y similares representan UUID. `{case_ref}` en lecturas de detalle propone UUID o `casos.codigo`, ya que la URL Angular usa radicado. Si el backend no admite ambos, proporcionar búsqueda exacta por `codigo` para resolver el UUID.
- JSON para operaciones ordinarias; multipart para binarios; CSV para exportar. El formato final se acuerda en OpenAPI.
- Paginación, búsqueda, autorización y agregados en servidor. Campos de autor, destinatario autorizado, rol inicial y estado inicial no se aceptan libremente por decisión del cliente.

### Etiquetas

| Marca | Significado |
|---|---|
| D | Los datos principales existen en el DDL. Sigue siendo necesario implementar serializers, validaciones, almacenamiento y autorización. No significa «endpoint disponible». |
| L | Requiere composición, cálculo, servicio o decisión de negocio del backend; no implica necesariamente nuevas tablas. |
| A | Requiere ampliación de persistencia solicitada en la sección 18 o una solución equivalente acordada con backend. No significa retirar la función del alcance. |
| P0 | Primera integración: sesión, catálogos y circuito de casos. Un punto marcado A no deja de estar bloqueado por llevar prioridad P0. |
| P1 | Completar las demás vistas existentes después del circuito principal. |
| C | Pendiente de soporte o decisión: no activar antes de sus dependencias. Las funciones ya previstas se solicitan para una entrega posterior; esta marca no las descarta. |

«Propio» exige pertenencia al usuario autenticado. «Equipo» exige permiso y ámbito. Los roles iniciales no definen por sí solos una matriz de capacidades: el backend debe especificar quién puede consultar, asignar, moderar, cerrar, exportar y administrar usuarios.

Se mantienen los identificadores del inventario anterior para facilitar la revisión y se añaden **INI-01 a INI-03** para ediciones y actividades: **81 operaciones propuestas**, incluidas condicionales y alternativas agrupables. No es una exigencia de 81 rutas nuevas ni de un CRUD por cada tabla.

## 3. Autenticación y sesión

| ID | Método y ruta propuesta | Acceso / prioridad | Soporte | Datos y resultado necesarios |
|---|---|---|---|---|
| AUTH-01 | `POST /auth/register/` | Público · P0 | L/A | `nombres`, `apellidos`, `correo`, contraseña y `telefono` opcional. Backend fija rol ciudadano y estado inicial. Aceptaciones requieren persistencia por acordar: `usuarios` no tiene campos de consentimiento. Retornar ID y resultado real de alta. |
| AUTH-02 | `POST /auth/login/` | Público · P0 | L | `correo` y contraseña. Validar hash y estado, devolver sesión JWT/expiración según contrato y perfil autorizado. Registrar acceso desde backend en `auditoria_accesos`; jamás devolver `contrasena_hash`. |
| AUTH-03 | `POST /auth/refresh/` | Sesión renovable · P0 | L | Renovación JWT mediante cookie o credencial por acordar; devolver acceso y expiración. Rotación/revocación no están resueltas por las 30 tablas. |
| AUTH-04 | `POST /auth/logout/` | Sesión · P0 | L | Cerrar/inutilizar renovación según estrategia acordada y limpiar sesión Angular. No asumir que borrar el token del navegador lo revoca en servidor. |
| AUTH-05 | `POST /auth/password-reset/request/` | Público · P1 | L | `correo`; respuesta genérica, sin revelar cuentas. Token, correo saliente, reintentos y auditoría son servicios pendientes. |
| AUTH-06 | `POST /auth/password-reset/validate/` | Token del enlace · P1 | L | Validar identificador/token sin cambiar contraseña; distinguir enlace vencido/inválido. Puede agruparse con AUTH-07 si se adapta el recorrido. |
| AUTH-07 | `POST /auth/password-reset/confirm/` | Token válido · P1 | L | Identificador/token y nueva contraseña. Actualizar hash, invalidar token y definir efecto sobre sesiones; errores estables de validación. |

El SQL no demuestra una integración con el modelo de usuarios de Django ni con su sistema de permisos. Acordar modelo de autenticación, algoritmo de hash y transporte de JWT, cookies/CSRF si aplica, renovación y revocación. Las tablas de infraestructura que requiera Django pueden añadirse mediante sus migraciones: no concluir que JWT sea imposible por no aparecer en este DDL.

«Recordar sesión» no cambia la duración de tokens desde el cliente. La afiliación del registro no debe convertirse en un rol privilegiado. Verificación de correo y consentimientos versionados necesitan una decisión y un circuito explícitos.

## 4. Perfil y preferencias

| ID | Método y ruta propuesta | Acceso / prioridad | Soporte | Datos y resultado necesarios |
|---|---|---|---|---|
| ME-01 | `GET /me/` | Propio · P0 | D/L | UUID, `nombres`, `apellidos`, `correo`, `telefono`, `estado`, rol único y capacidades calculadas por backend. No prometer foto, domicilio o preferencias inexistentes. |
| ME-02 | `PATCH /me/` | Propio · P1 | D/L | Campos de identidad editables; nombres/apellidos hasta 100 cada uno, correo hasta 150, teléfono hasta 20. Retornar datos efectivos; definir si cambiar correo exige verificación. Rechazar cambios de rol/estado por este endpoint. |
| ME-03 | `PUT /me/photo/` | Propio · C | A | No hay campo ni entidad de foto de usuario. Definir almacenamiento y referencia antes de aceptar multipart. |
| ME-04 | `DELETE /me/photo/` | Propio · C | A | Depende de ME-03 y de reglas de retirada del archivo. |
| ME-05 | `PATCH /me/preferences/` | Propio · C | A | No hay preferencias de novedades, mensajes o boletín. Crear persistencia definida o mantener controles inactivos. |

`usuarios` tampoco tiene comunidad/municipio/departamento de residencia. No sustituirlos por comunidades de casos o por ámbitos de asignación: representan conceptos distintos. Se solicita perfil y preferencias persistentes en AMP-04. `configuracion_plataforma` no se asume como almacén de perfiles privados sin contrato.

## 5. Catálogos

| ID | Método y ruta propuesta | Acceso / prioridad | Soporte | Filtros y datos necesarios |
|---|---|---|---|---|
| CAT-01 | `GET /catalogs/departments/` | Público · P0 | D | `departamentos`: UUID, `codigo_dane` de dos caracteres y nombre. Preservar ceros iniciales. |
| CAT-02 | `GET /catalogs/municipalities/` | Público · P0 | D | Filtrar por `id_departamento`; retornar UUID, DANE de cinco caracteres, nombre y departamento. |
| CAT-03 | `GET /catalogs/communities/` | Público · P0 | D | Filtrar por `id_municipio`, tipo y activas. UUID, nombre, tipo, municipio. `ubicacion` es MultiPolygon, no coordenada de un marcador. |
| CAT-04 | `GET /catalogs/basins/` | Según futuro uso · C | A | No hay tabla ni relación de cuencas/subcuencas. Adaptar el filtro a comunidad/municipio o definir ampliación; no extraer cuencas del nombre como en los ejemplos. |
| CAT-05 | `GET /catalogs/case-categories/` | Público · P0 | L | Proyección de valores distintos de `tipos_caso.categoria`, preferentemente de tipos activos. Son textos de hasta 50 caracteres, no UUID de una tabla de categorías. |
| CAT-06 | `GET /catalogs/case-options/` | Público/usuario según campos · P0 | D/L | `tipos_caso` activos con UUID, nombre, descripción y categoría; `estados_caso` con UUID, nombre y orden; prioridades/publicación desde enumeraciones. Puede separarse en varios catálogos. |
| CAT-07 | `GET /catalogs/news-categories/` | Público · C | A | No hay noticias ni categorías de noticias en el DDL. |
| CAT-08 | `GET /catalogs/initiative-categories/` | Público · P1 | L | Valores distintos de `iniciativas.categoria` (texto hasta 80), restringidos a programas publicados para consulta pública. No inventar IDs de categoría. |

El SQL no inserta tipos de caso, territorios ni iniciativas: sus endpoints pueden responder vacíos hasta cargar datos reales. Sí inserta cuatro roles y cinco estados, cuyos UUID deben consultarse; no pueden codificarse en Angular. La clasificación visual «problemática/proyecto» no está modelada aparte de `tipos_caso`: acordar su mapeo, sin exigir un campo inexistente.

## 6. Contenido institucional e iniciativas

| ID | Método y ruta propuesta | Acceso / prioridad | Soporte | Filtros, entrada y salida necesarios |
|---|---|---|---|---|
| PUB-01 | `GET /public/site/` | Público · P1 | L | Proyección pública de claves autorizadas de `configuracion_plataforma`: identidad, representante, contacto, redes y documentos. Hoy solo se insertan nombre institucional, SRID y máximo de destacadas; los demás contenidos deben cargarse/definirse. No devolver toda la tabla. |
| PUB-02 | `GET /public/home/` | Público · P1 | L/A | Agregados de casos aprobados e iniciativas publicadas; composición con PUB-01/PUB-05 y mapa. Noticias y métricas no respaldadas quedan fuera hasta ampliación. Periodo/fuente de indicadores, sin copiar cifras del diseño. |
| PUB-03 | `GET /public/news/` | Público · C | A | No existe tabla de noticias. Requiere modelo, publicación, categorías y medios antes de entregar listado filtrable. |
| PUB-04 | `GET /public/news/{slug}/` | Público · C | A | Depende de PUB-03; contenido completo y documentos publicados, no un resumen inventado. |
| PUB-05 | `GET /public/initiatives/` | Público · P1 | D/L | Programas `publicada`, búsqueda/categoría/destacada y año por edición. UUID, slug, título/subtítulo, descripción corta y portada general; edición seleccionada explícita si se muestran métricas anuales. |
| PUB-06 | `GET /public/initiatives/{slug}/` | Público · P1 | D/L | Programa publicado, descripción, estado, medios generales y ediciones disponibles. No colocar indicadores de una edición como si fueran permanentes. |
| PUB-07 | `GET /public/initiatives/{id}/gallery/` | Público · P1 | D/L | `iniciativa_multimedia`; filtro por `id_edicion` y paginación. Diferenciar medios generales (`id_edicion` nulo) de medios de edición; texto alternativo, descripción, tipo y orden. Política de exposición pendiente. |
| PUB-08 | `POST /public/initiative-proposals/` | Público o propio · P1 | D/L | Crear `propuestas_iniciativas` con contacto/usuario, comunidad o territorio declarado, **título**, descripción, iniciativa solicitada y **consentimiento verdadero**. Retornar UUID y estado `pendiente`; no publicar contactos ni crear programa automáticamente. |
| PUB-09 | `POST /public/newsletter-subscriptions/` | Público · C | A | No existe persistencia de suscripciones ni consentimiento de boletín. No activar envío real. |
| PUB-10 | `POST /public/newsletter-subscriptions/confirm/` | Token · C | A | Depende del circuito de boletín y tokens de confirmación. |
| PUB-11 | `POST /public/newsletter-subscriptions/unsubscribe/` | Token/propio · C | A | Depende del circuito de boletín y política de baja. |
| INI-01 | `GET /public/initiatives/{id}/editions/` | Público · P1 | D/L | `iniciativa_ediciones`: UUID, año, nombre, temporada, fechas y estado; filtro de año y orden. Solo bajo programa publicado y política de visibilidad acordada. |
| INI-02 | `GET /public/initiatives/{id}/editions/{edition_id}/` | Público · P1 | D/L | Edición del programa indicado, indicadores de `iniciativa_indicadores`, cobertura de `iniciativa_comunidades`, portada y resultados autorizados. Puede incluirse como expansión de PUB-06. |
| INI-03 | `GET /public/initiatives/{id}/editions/{edition_id}/activities/` | Público · P1 | D/L | Actividades de la edición, fechas, lugar, comunidad y estado; paginación. No exponer responsable/contacto o coordenada sensible automáticamente. Puede incluirse en INI-02 si el volumen lo permite. |

### Decisiones específicas de iniciativas

- Programa (`iniciativas`) y ejecución anual (`iniciativa_ediciones`) tienen IDs distintos. Hay una edición por programa y año; cualquier URL de edición debe comprobar su pertenencia al programa.
- Indicadores: `valor NUMERIC(14,2)`, unidad, descripción, icono, orden, fecha de corte y `tipo_medicion` (`estimado`/`real`). Acordar serialización decimal; no perder la distinción entre estimado y real ni mezclar unidades.
- La cobertura procede de comunidades por edición; el número de comunidades no equivale automáticamente a beneficiarios. No sumar indicadores de distintas ediciones sin una definición de agregación.
- Multimedia puede pertenecer al programa general o a una edición, con portada única por ámbito. No hay relación de multimedia con actividad ni un campo de publicación individual: definir qué medios se consideran autorizados. No anunciar una galería «por jornada» sin relación o adaptación adicionales.
- Ediciones/actividades no tienen un estado de publicación independiente. Backend debe acordar cuáles son visibles bajo un programa publicado; publicación del programa no equivale por sí sola a publicar datos personales o ubicaciones de cada actividad.
- `iniciativa_casos` vincula casos a **ediciones**, con tipos `hallazgo`, `seguimiento`, `resultado`, `otro`. Si se incluye en INI-02, filtrar casos aprobados y producir una representación pública; no crear acceso público a casos privados por estar vinculados.
- `vw_iniciativas_destacadas` sirve para programa/portada general, no sustituye las lecturas de indicadores anuales. `iniciativas.max_destacadas` es configuración, no una garantía de límite aplicada por una restricción SQL.

### Postulación: mapeo del formulario

| Dato del formulario | Campo SQL / decisión |
|---|---|
| Nombre de contacto | `nombre_contacto`, hasta 150. Si no hay usuario, nombre y teléfono son obligatorios. |
| Teléfono | `telefono_contacto`, hasta 25; validar contenido en backend, no solo no nulo. |
| Territorio escrito | `comunidad_declarada`, hasta 200, o `id_comunidad` del catálogo. |
| Iniciativa elegida | `id_iniciativa_solicitada`; no el título visible. |
| Descripción | `descripcion` obligatorio; límite de negocio por acordar. |
| Título | `titulo` obligatorio hasta 200: **falta en la interfaz actual**. |
| Aceptación de datos | `acepta_tratamiento_datos=true`: **falta en la interfaz actual y el CHECK la exige**. Versionado/fecha del consentimiento no están persistidos en esta tabla. |

El servidor fija revisión, revisor, fecha, respuesta e iniciativa generada. No admitirlos como campos editables de una postulación pública.

## 7. Mapa y expediente público

| ID | Método y ruta propuesta | Acceso / prioridad | Soporte | Datos y controles necesarios |
|---|---|---|---|---|
| MAP-01 | `GET /public/cases/` | Público · P0 | D/L | Casos `aprobado`, filtros por búsqueda, territorio, tipo/categoría, estado, prioridad y fechas; paginación. UUID, código, título, resumen autorizado y territorio derivado. |
| MAP-02 | `GET /public/cases/map/` | Público · P0 | D/L | Solo aprobados con punto, mismos filtros y `bbox`/zoom si se admiten. Coordenadas publicables y total; elegir GeoJSON o JSON y mecanismo de clusters/truncamiento. |
| MAP-03 | `GET /public/cases/{case_ref}/` | Público · P0 | D/L | Caso aprobado con campos expresamente públicos; comunidad/municipio/departamento por relación. Sin contacto del solicitante, mensajes o notas privadas. |
| MAP-04 | `GET /public/cases/{case_id}/history/` | Público · P0 | D/L | Solo `seguimientos.visible_publicamente=true` y caso aprobado. Decidir si se exponen eventos seleccionados de `historial_estados`; el historial completo no es automáticamente público. |
| MAP-05 | `GET /public/cases/{case_id}/evidence/` | Público · C | A | Evidencias carecen de visibilidad. Hasta resolverla, no publicar adjuntos por el solo hecho de estar aprobado el caso. Ampliar persistencia o mantener galería pública inactiva. |
| MAP-06 | `GET /public/cases/{case_id}/comments/` | Público · P1 | D/L | `comentarios.estado_moderacion=aprobado` y caso aprobado; paginación y autoría pública mínima autorizada. |
| MAP-07 | `POST /cases/{case_id}/comments/` | Usuario autorizado · P1 | D/L | `contenido`; servidor fija `id_usuario`, fecha y `pendiente`. Acordar límites y moderación; no publicar al recibir. |
| MAP-08 | `GET /me/followed-cases/{case_id}/` | Propio · C | A | No hay tabla/relación de casos seguidos. No deducir seguimiento de comentarios, mensajes o notificaciones. |
| MAP-09 | `PUT /me/followed-cases/{case_id}/` | Propio · C | A | Depende de persistencia y reglas de seguimiento. |
| MAP-10 | `DELETE /me/followed-cases/{case_id}/` | Propio · C | A | Depende del mismo circuito de seguimiento. |

`casos.ubicacion` es `Point,4326`: `ST_X` corresponde a longitud y `ST_Y` a latitud. `comunidades.ubicacion` es `MultiPolygon,4326`, no la ubicación puntual de un caso. `vw_casos_mapa` ya excluye no aprobados y puntos nulos, pero **contiene coordenadas exactas**; el propio documento exige revisar ubicaciones sensibles. Consumir una API autorizada que pueda generalizar/omitir precisión, no exponer la vista directamente.

Acordar `bbox` (propuesta: oeste,sur,este,norte), precisión pública, paginación/cluster y límites. Casos aprobados sin punto pueden aparecer en el listado si así se define, pero no en marcadores. Búsqueda, contadores y detalle deben aplicar la misma política de publicación.

## 8. Radicación y portal ciudadano

| ID | Método y ruta propuesta | Acceso / prioridad | Soporte | Datos y resultado necesarios |
|---|---|---|---|---|
| CIT-01 | `GET /me/dashboard/` | Propio · P1 | L | Agregados de casos propios, actividad autorizada y no leídos de mensajes/notificaciones; no hay tabla de dashboard ni hace falta crearla. |
| CIT-02 | `GET /me/cases/` | Propio · P0 | D/L | Filtrar `casos.id_usuario` por sesión. UUID/código, título, estado, publicación, territorio, fechas y responsable activo visible; filtros/paginación/total. |
| CIT-03 | `POST /me/cases/` | Propio · P0 | D/L/A | Título, descripción, `id_tipo_caso`, `id_comunidad`, prioridad solicitada, punto opcional/dirección y archivos. Servidor fija propietario, código único y estado inicial. Cantidades y declaraciones del formulario requieren decisión: ver sección 12. |
| CIT-04 | `GET /me/cases/{case_ref}/` | Propio · P0 | D/L/A | Ficha y asignación del propietario. Corrección activa y resultado narrativo estructurado no existen en `casos`: acordar fuente o adaptar la vista. |
| CIT-05 | `GET /me/cases/{case_id}/history/` | Propio · P0 | L/A | Componer seguimiento y cambios de estado, con tipo/ID de origen y orden. **Resolver visibilidad privada** antes de entregar `seguimientos` no públicos al ciudadano. |
| CIT-06 | `GET /me/cases/{case_id}/evidence/` | Propio · P0 | D/L | Evidencias autorizadas al propietario. UUID, tipo, descripción, fecha; nombre/tamaño/MIME/estado se derivan de almacenamiento o requieren metadatos adicionales. |
| CIT-07 | `GET /me/cases/{case_id}/evidence/{evidence_id}/download/` | Propio · P0 | D/L | Validar evidencia → caso → propietario; archivo o URL temporal protegida. `ruta_archivo` no es una URL que deba hacerse pública. |
| CIT-08 | `POST /me/cases/{case_id}/contributions/` | Propio · P0 | L/A | Texto y archivos opcionales. No existe entidad aporte privado: acordar si crea un seguimiento con política segura o una entidad nueva. No usar comentarios públicos como sustituto. |

La radicación genera UUID por defecto, pero **el código de radicado no tiene generador/default en el SQL**. El backend debe generarlo con unicidad y controlar reintentos. La confirmación Angular se alimentará de la respuesta real y, al recargar, de una lectura autorizada del expediente.

`historial_estados` registra creación y cambios operativos mediante trigger; no crear otra fila idéntica desde la API. El cambio de responsable no es por sí mismo un nuevo `id_estado` «asignado».

## 9. Mensajes privados y notificaciones

| ID | Método y ruta propuesta | Acceso / prioridad | Soporte | Datos y controles necesarios |
|---|---|---|---|---|
| MSG-01 | `GET /me/conversations/` | Propio · P1 | L | Agrupar mensajes permitidos por caso y participantes según contrato. No hay tabla conversaciones. Resumen, contraparte visible, último mensaje permitido y no leídos destinados al usuario. |
| MSG-02 | `GET /cases/{case_id}/messages/` | Participante autorizado · P0 | D/L | `mensajes_privados` del caso y participantes permitidos; filtro de contraparte si es necesario, paginación/cursor y orden. No entregar todo el chat por tener acceso operativo al caso. |
| MSG-03 | `POST /cases/{case_id}/messages/` | Participante autorizado · P0 | D/L | `contenido` y destinatario autorizado si no lo resuelve el servidor. `id_remitente` sale de la sesión; el destinatario es obligatorio en SQL y debe ser distinto. Retornar UUID, fecha y contraparte. |
| MSG-04 | `PUT /cases/{case_id}/messages/read/` | Destinatario · P1 | D/L | IDs o límite estable de mensajes recibidos. Actualizar `fecha_lectura` solo del destinatario autenticado; excluir mensajes posteriores y devolver no leídos actualizados. |
| NOT-01 | `GET /me/notifications/` | Propio · P1 | D | `notificaciones` del usuario: UUID, título, mensaje, tipo, caso opcional, `leida`, fecha; filtros/paginación y total de no leídas. |
| NOT-02 | `PATCH /me/notifications/{id}/` | Propio · P1 | D/L | Solo lectura (`leida`) según reglas acordadas; no modificar usuario, caso o contenido. |
| NOT-03 | `POST /me/notifications/mark-read/` | Propio · P1 | D/L | IDs o corte temporal para lectura masiva; confirmar cantidad y total restante. No marcar nuevas notificaciones fuera del conjunto enviado. |

Decisiones necesarias:

- El modelo es **mensaje entre dos usuarios**, no canal de caso. Resolver qué destinatario recibe un mensaje ciudadano cuando no hay responsable activo; no puede quedar vacío ni enviarse a una identidad de ejemplo.
- Una reasignación no convierte automáticamente al nuevo responsable en destinatario de mensajes antiguos. Acordar acceso histórico, contraparte y facultades de supervisión sin convertir mensajes privados en lectura general por rol.
- Existen mensajes con `id_caso` nulo: decidir si el portal actual los excluye o incorpora conversaciones generales. No asignarles un caso ficticio.
- `fecha_lectura` no puede ser anterior a `fecha_envio`; no hay tabla de puntos de lectura. El endpoint puede actualizar filas recibidas hasta un límite sin crearla si se acuerda esa semántica.
- `notificaciones` no tiene `fecha_lectura`, solo booleano. No prometer esa fecha sin ampliación. Puede devolver un destino basado en `id_caso`; enlaces a otras entidades necesitan contrato adicional.
- Notificaciones y mensajes reales se consultan en servidor; no se derivan en Angular recorriendo todos los historiales como en la demostración.

## 10. Gestión administrativa de casos

| ID | Método y ruta propuesta | Acceso / prioridad | Soporte | Datos y reglas necesarios |
|---|---|---|---|---|
| ADM-01 | `GET /admin/dashboard/` | Equipo autorizado · P1 | L/A | Agregados reales sobre casos, asignaciones y territorio dentro del ámbito. Tareas, plazos hábiles y alertas del diseño no tienen persistencia/reglas propias: omitir o definir su cálculo, nunca copiar cifras ficticias. |
| ADM-02 | `GET /admin/cases/` | Equipo autorizado · P0 | D/L | Filtros de código/texto, comunidad/municipio/departamento, tipo/categoría, estado, publicación, prioridad, responsable y fechas. Resolver asignación activa, paginación y totales; cuencas bloqueadas. |
| ADM-03 | `GET /admin/cases/{case_ref}/` | Equipo autorizado · P0 | D/L | Ficha, solicitante si puede verse, estado, publicación, responsable activo, ubicación y acciones permitidas. Correcciones/resultados exigen la fuente acordada. |
| ADM-04 | `GET /admin/cases/{case_id}/history/` | Equipo autorizado · P0 | L | Componer `seguimientos`, `historial_estados` y eventos de asignación/moderación que el contrato incluya. ID compuesto por fuente/UUID o estructura equivalente; respetar permisos de notas. |
| ADM-05 | `GET /admin/cases/{case_id}/evidence/` | Equipo autorizado · P0 | D/L | Evidencias autorizadas del caso y metadatos de almacenamiento. No devolver visibilidad individual inexistente. |
| ADM-06 | `GET /admin/cases/{case_id}/evidence/{evidence_id}/download/` | Equipo autorizado · P0 | D/L | Descarga con permiso por caso/evidencia; puede compartir lógica con CIT-07 bajo autorización apropiada. |
| ADM-07 | `POST /admin/cases/{case_id}/moderation/` | Permiso de moderación · P0 | D/L/A | Aprobar/rechazar actualiza `estado_publicacion`; al aprobar, completar `fecha_aprobacion` (CHECK obligatorio). Persistir motivo real según contrato. Solicitud de corrección requiere flujo adicional, no un cuarto estado inventado. |
| ADM-08 | `POST /admin/cases/{case_id}/assignments/` | Permiso de asignación · P0 | D/L | `id_responsable`, motivo si se exige. Actor real como asignador. Finalizar/desactivar asignación previa e insertar nueva en transacción; respetar índice de un responsable activo. No cambiar estado operativo por inferencia del cliente. |
| ADM-09 | `POST /admin/cases/{case_id}/progress/` | Permiso de seguimiento · P0 | D/L/A | Crear `seguimientos` con título, descripción y audiencia (`interno`, `ciudadano`, `publico`). Soporta `multipart/form-data` con `files`/`archivos` y `application/json` con `evidence_ids: UUID[]` vinculando evidencias directamente al seguimiento. Retorna `evidencias: CaseEvidenceSerializer[]` (P24). Alias: `POST /admin/cases/{case_id}/updates/`. |
| ADM-10 | `POST /admin/cases/{case_id}/resolution/` | Permiso de resolución/cierre · P0 | L/A | Cambiar a UUID de estado válido y persistir resultado mediante mecanismo acordado (p. ej. seguimiento autorizado o ampliación). No existe columna `resultado` en `casos`; trigger registra cambio de estado, no toda la narración. |
| ADM-11 | `PATCH /admin/cases/{case_id}/evidence/{evidence_id}/` | Permiso de evidencias · C | A | Permite actualizar `descripcion`, `audiencia` (`publico`, `ciudadano`, `privado`), `estado_revision` (`pendiente`, `aprobada`, `rechazada`) e `id_seguimiento` para asociar o desvincular un documento a una respuesta/avance administrativo (P24). |

### Responsables, ámbitos y transacciones

`asignaciones_responsables` habilita ámbitos por comunidad, tipo de caso o ambos; al menos uno es obligatorio. `asignaciones_casos` identifica el responsable efectivo del caso. El SQL no define si dos criterios en un ámbito significan intersección o unión ni cómo se combinan varias filas: backend debe fijarlo y aplicar reglas de elegibilidad, estado del usuario y permiso del asignador.

Para candidatos, USR-01 puede aceptar un filtro de elegibilidad por caso. Si el backend prefiere un endpoint específico, acordarlo como alternativa, sin limitarse a «usuarios con rol responsable» (ese rol no está entre los cuatro insertados).

El índice parcial `ux_asignacion_caso_activa` garantiza como máximo una fila activa por caso. La API debe operar en transacción y gestionar concurrencia; el frontend no desactiva la anterior con una petición independiente antes de asignar la nueva.

No hay versión numérica de expediente. `fecha_actualizacion` puede servir como precondición de una modificación de la fila `casos` si el backend lo implementa, pero **no cambia automáticamente por insertar seguimientos, evidencias o asignaciones**. Para versionar el expediente completo, acordar una estrategia real; no prometer un ETag global derivado de esa fecha sin cubrir las relaciones.

## 11. Informes, auditoría y usuarios

### 11.1. Informes

| ID | Método y ruta propuesta | Acceso / prioridad | Soporte | Datos y reglas necesarios |
|---|---|---|---|---|
| REP-01 | `GET /admin/reports/cases/` | Permiso de informes · P1 | L | Casos filtrados y agregados de toda la selección: estado, publicación, tipo/categoría, responsable vigente y territorio. Filas paginadas separadas de totales. No necesita tabla de informes. |
| REP-02 | `GET /admin/reports/cases/export/` | Permiso de exportación · P1 | L | CSV de toda la selección autorizada con los mismos filtros, no solo la página. Neutralizar fórmulas en celdas de texto; no incluir datos privados por defecto. |

No exportar `originalStatus`, `modified`, `fixture` o `local`: son marcas del prototipo, no columnas reales. Si se desea mostrar cambios recientes, usar información real definida y fecha de corte; no inventar métricas de tiempos de atención sin reglas.

### 11.2. Auditoría

| ID | Método y ruta propuesta | Acceso / prioridad | Soporte | Datos y reglas necesarios |
|---|---|---|---|---|
| AUD-01 | `GET /admin/audit-events/` | Permiso de auditoría · P1 | D/L | Proyección de las fuentes acordadas: `auditoria_eventos`, accesos, casos, permisos y seguridad. Filtros por fuente, acción, actor, módulo/entidad/caso, resultado, fechas; paginación y orden. No toda fuente tiene todos los campos. |
| AUD-02 | `GET /admin/audit-events/{event_ref}/` | Permiso de auditoría · P1 | D/L | Referencia con fuente y UUID o equivalente inequívoco. Datos autorizados, nombres de campos cambiados y antes/después solo cuando estén disponibles; no exponer JSONB crudo ni IP/user-agent/correos por defecto. |

`registrar_auditoria_basica` guarda en actualizaciones `datos_nuevos.columnas_modificadas`, **no un snapshot antes/después**. En inserciones/borrados sus valores de datos pueden ser nulos. La interfaz debe admitir «campos modificados sin valores disponibles»; no reconstruir valores históricos leyendo la fila actual.

Las tablas especializadas sí incluyen ciertos valores previos/nuevos, estados, motivos o severidad. El endpoint puede unificarlas como DTO de lectura con `source` y referencia de entidad; eso no exige fusionar tablas ni otorga acceso general a todos los eventos. Para las acciones fallidas, definir registro desde el backend: los triggers de operaciones revertidas no conservan automáticamente un evento de fallo.

El esquema obtiene actor mediante `SET LOCAL plus.actor_id` dentro de la transacción autenticada. Debe fijarlo el backend, nunca aceptar un actor arbitrario del navegador. Los triggers existentes generan historial operativo, auditoría general, cambios de publicación/prioridad y rol: coordinar los registros complementarios para no duplicarlos y conservar motivos reales, no sustituirlos por los textos genéricos del trigger.

No se pide `POST`, `PATCH` ni `DELETE` públicos de auditoría. Consulta no significa facultad de edición/borrado; permisos y privilegios de base deben proteger esas tablas.

### 11.3. Usuarios y rol único

| ID | Método y ruta propuesta | Acceso / prioridad | Soporte | Datos y reglas necesarios |
|---|---|---|---|---|
| USR-01 | `GET /admin/users/` | Permiso de usuarios/selección · P0 para asignar, P1 para directorio | D/L | Búsqueda, `id_rol`, estado y paginación; candidatos por caso si se implementa elegibilidad. UUID, nombres, apellidos, correo autorizado, rol único y estado. |
| USR-02 | `POST /admin/users/` | Permiso de alta · P1 | D/L | `nombres`, `apellidos`, `correo`, `telefono` opcional y **un `id_rol`** permitido. Definir provisión de contraseña: `contrasena_hash` es NOT NULL. El formulario sin contraseña no constituye por sí solo un flujo de invitación implementado. |
| USR-03 | `GET /admin/users/{id}/` | Permiso de consulta · P1 | D | Perfil autorizado, rol único, estado y fechas; nunca hash. |
| USR-04 | `PATCH /admin/users/{id}/` | Permiso de edición · P1 | D/L | Nombres/apellidos, correo y teléfono dentro de límites SQL y reglas de negocio. Mantener el estado si no se solicita cambiarlo. |
| USR-05 | `PUT /admin/users/{id}/role/` | Permiso de cambio de rol · P1 | D/L | **Un `id_rol`**, no una lista. Cambia FK `usuarios.id_rol`; auditar mediante trigger existente y políticas de actor autorizado. Ruta corregida respecto al anterior `/roles/`. |
| USR-06 | `PATCH /admin/users/{id}/status/` | Permiso de estado · P1 | D/L | Estado `activo`, `suspendido` o `inactivo`; motivo si se exige. Definir efecto sobre sesión y asignaciones existentes. |
| USR-07 | `GET /admin/roles/` | Permiso de roles · P1 | D/L | Filas reales de `roles` (UUID, nombre, descripción) y asignabilidad calculada para el actor, si se ofrece. No devolver roles ficticios ni una matriz granular inexistente. |

La unicidad de correo usa `lower(btrim(correo))`: la API debe normalizar y devolver error de campo en duplicados, manteniendo la restricción de base como defensa frente a concurrencia. El CHECK de correo solo comprueba `@`; el backend necesita validación de formato más completa.

Separar edición de perfil y cambio de rol puede producir guardado parcial en el formulario actual. Acordar una operación transaccional o dos resultados explícitos. La elección de un solo rol reduce datos, pero no elimina la necesidad de autorización por operación, ámbito y relación con el caso.

No asumir que `representante` equivale a todos los permisos administrativos, ni que `moderador` asigna o cierra casos. Definir capacidades, protección de cuentas privilegiadas, autoedición, última cuenta administradora y creación/invitaciones. No crear roles nuevos para hacer coincidir el prototipo sin aprobación de producto/backend.

## 12. Contratos críticos y carencias que bloquean funciones

### 12.1. Ficha de radicación y archivos

| Necesidad visual | Persistencia disponible | Decisión de integración |
|---|---|---|
| Título | `casos.titulo VARCHAR(200)` | Límite 200. |
| Descripción | `casos.descripcion TEXT` | El SQL no fija 5000; confirmar el límite de negocio del prototipo. |
| Tipo/categoría | FK `id_tipo_caso`; categoría textual en el tipo | Enviar UUID del tipo; derivar categoría. No guardar dos selecciones incoherentes. |
| Comunidad | FK obligatoria `id_comunidad` | No admitir texto libre como única comunidad al radicar sin resolver un ID válido; es distinto del formulario de propuestas, que sí admite territorio declarado. |
| Prioridad | Enum de cuatro valores | Mapear etiquetas a `baja/media/alta/critica`; definir quién puede fijar prioridad efectiva. |
| Punto/dirección | `ubicacion Point,4326` nullable; `direccion_referencia TEXT` | Coordenadas opcionales según DDL; el formulario hoy las exige. Acordar obligatoriedad real antes de cambiarlo. |
| Familias afectadas y meses | Sin columnas | Solicitar campos persistentes según AMP-05; no esconderlos en `descripcion` como persistencia equivalente. |
| Declaraciones y políticas | Sin campos/tabla de aceptación del caso | Acordar almacenamiento/versionado/fecha y texto vigente. No afirmar que se registraron aceptaciones que no se conservaron. |
| Archivos | `evidencias` con caso, usuario, tipo, ruta, descripción y fecha | Subida/almacenamiento desde backend; metadatos adicionales y política de publicación pendientes. |
| Corrección solicitada | Sin entidad/columnas específicas | Decidir persistencia y ciclo de respuesta; no usar solo `estado_publicacion=pendiente` para afirmar una solicitud activa. |
| Resolución narrativa | Sin columna `resultado` | Acordar seguimiento de resolución identificado o ampliación; `historial_estados.motivo` del trigger es genérico. |

Propuesta de multipart a concretar: campo JSON de ficha y campos repetidos de archivos; alternativa: carga temporal con IDs y asociación final. Elegir una y fijar atomicidad, limpieza de huérfanos y reintentos. Ante timeout después de guardar, no crear otro caso por falta de respuesta: acordar idempotencia/deduplicación.

El servidor genera UUID, radicado, actor, fechas y estado inicial. La FK de estado debe apuntar a una fila real (`pendiente` inicial si ese es el flujo confirmado); la publicación inicial es `pendiente`. No recibir `id_usuario` de otro remitente como dato libre del formulario ciudadano.

### 12.2. Privacidad y seguimiento: decisiones imprescindibles

1. **Evidencia pública:** falta un indicador/política persistida por evidencia. Hasta decidirlo, solo descargas privadas autorizadas; la galería pública y ADM-11 de visibilidad permanecen condicionadas.
2. **Notas internas frente al ciudadano:** `visible_publicamente=false` solo dice «no pública». No dice si el propietario puede verla. Para conservar los tres niveles del frontend, ampliar a una audiencia explícita o establecer una representación equivalente verificable. No devolver todas las filas `false` al ciudadano.
3. **Aportes privados:** no hay tabla de contribuciones ni vínculo de evidencia con un aporte/seguimiento. Definir representación y agrupación si la UI debe mostrar un aporte con sus archivos; el hecho de que compartan caso no prueba que pertenezcan al mismo aporte.
4. **Consentimiento de propuestas:** sí es obligatorio por CHECK y el formulario debe recogerlo. Para registro/casos/boletín no existe ese mismo soporte; no generalizar esa columna a todos los módulos.
5. **Medios privados:** `ruta_archivo` es una referencia interna. El nginx actual no define un circuito `/media/`; acordar descarga protegida, URL temporal o recursos públicos específicamente autorizados. Nunca publicar el volumen completo para resolver el problema.

### 12.3. Límites confirmados frente a límites de interfaz

| Dato | Límite SQL confirmado | Diferencia actual a corregir/acordar |
|---|---|---|
| Nombres y apellidos | 100 cada uno, no nulos | Formularios actuales usan nombre único de hasta 150. |
| Correo | 150, único sin mayúsculas/espacios exteriores | El directorio/perfil permite hasta 254. |
| Teléfono de usuario | 20 | El perfil admite hasta 30 en su patrón. |
| Contacto de propuesta | Nombre 150, teléfono 25, territorio declarado 200, título 200 | El formulario actual no tiene título/consentimiento y su patrón telefónico permite hasta 30. |
| Título de caso | 200 | Coincide con el límite visual. |
| Descripción de caso, comentarios, mensajes, seguimientos | TEXT | Los mínimos/máximos visuales no son restricciones SQL; deben acordarse y validarse en serializer. |
| Título/subtítulo de iniciativa | 200 / 250 | Usar campos reales, no reemplazar programa por edición. |
| Slug de iniciativa | 220 y patrón minúsculas/números/guiones | Resolver unicidad y reglas desde backend. |
| Año de edición | 2000 a 2200; único por iniciativa | Validar `anio` como número, no texto decorativo del periodo. |
| Imágenes de perfil y anexos | El DDL no fija MIME, bytes o cantidad | 2 MB para perfil y 15 MB por anexo son límites del prototipo, no límites confirmados del servidor. |

`tipo_archivo` de evidencia es `imagen/video/audio/documento`, no extensión ni MIME. El formulario actual acepta JPG/PNG/PDF: el soporte SQL de audio/video no obliga a habilitarlos en el navegador. Validar contenido y límites en backend antes de ampliar formatos.

## 13. Formato de respuestas, filtros y errores por acordar

- Listados propuestos: `count`, `next`, `previous`, `results`, o el formato de paginación real publicado por Django. Mensajes/historiales pueden usar cursor; Angular debe usar el mecanismo acordado.
- Agregados, no leídos y distribuciones pertenecen a toda la selección autorizada, no al tamaño de la página. Si se calculan en endpoints separados, mantener filtros y fecha de corte coherentes.
- Fechas de API ISO 8601 con zona; fechas sin hora para ediciones/indicadores cuando el campo SQL es DATE. Auditoría muestra UTC en el prototipo; definir filtros inclusivos y cuál fecha se consulta en cada recurso.
- Parámetros candidatos alineados con SQL: `search`, `id_departamento`, `id_municipio`, `id_comunidad`, `id_tipo_caso`, `categoria`, `id_estado`, `estado_publicacion`, `prioridad`, `id_responsable`, `id_rol`, `estado`, `anio`, `id_edicion`, fechas, orden y paginación. Son propuestas de API, no implementación demostrada. No pedir `category_id` si categoría sigue siendo texto.
- Respuestas deben distinguir null, campo no autorizado, campo no soportado y agregado no disponible. No devolver cadenas vacías o cifras de ejemplo para ocultar carencias de persistencia.
- Para errores, acordar código estable, mensaje, campos afectados y referencia de solicitud sin datos sensibles. 400/422 para validación según convención; 401 sesión, 403 permiso, 404 no disponible; 409/412 para conflictos si se adopta precondición; 413/415 archivos; 429 reintento; 5xx/red sin asumir resultado de una escritura.
- Éxito debe distinguir recibido, pendiente de revisión y publicado. 202 solo si existe procesamiento asíncrono y modo de consultar resultado; 204 puede no tener JSON.

### Ejemplo de datos mínimos que acordar para un caso

Esto es un mapeo de requerimientos, no un serializer aprobado:

| Concepto DTO | Origen |
|---|---|
| ID y radicado | `casos.id_caso`, `casos.codigo`. |
| Tipo y categoría | `tipos_caso.id_tipo_caso/nombre/categoria`. |
| Estado operativo | `estados_caso.id_estado/nombre/orden`. |
| Publicación/prioridad | Valores de `casos.estado_publicacion/prioridad`. |
| Ubicación | Conversión de `casos.ubicacion` a coordenadas/GeoJSON acordados; representación pública distinta si corresponde. |
| Territorio | Join comunidad → municipio → departamento, sin duplicar esos IDs en escrituras inconsistentes. |
| Propietario | `casos.id_usuario`; datos de usuario solo según permiso. |
| Responsable | Fila activa de `asignaciones_casos`, no un campo inventado en `casos`. |
| Acciones posibles | Cálculo del backend por rol único, estado del usuario, ámbito, relación y transición. No hay tabla `permissions` en el DDL. |

## 14. Ampliaciones y operaciones fuera del circuito actual

Estas operaciones no se consideran ya implementadas. Se solicitan para las funciones previstas conforme a la sección 18; las interfaces administrativas aún pendientes pueden construirse después del circuito principal. La existencia de una tabla tampoco implica que su CRUD deba exponerse al público.

| Área | Operaciones propuestas para futura interfaz | Respaldo / decisión |
|---|---|---|
| Territorios | `GET/POST /admin/communities/`; `GET/PATCH /admin/communities/{id}/`; edición municipal/departamental si se autoriza. | D: catálogos y comunidad con estado activo, tipo y polígono. Definir permisos y datos oficiales; no borrar relaciones con casos. |
| Ámbitos de responsables | `GET/POST /admin/responsibility-scopes/`; `PATCH /admin/responsibility-scopes/{id}/`. | D/L: `asignaciones_responsables`, criterios opcionales con al menos uno, usuario y activo. Definir semántica de combinación y elegibilidad. |
| Iniciativas | `GET/POST /admin/initiatives/`; `GET/PATCH /admin/initiatives/{id}/`; operación de publicación. | D/L: estados/publicación y fechas; destacar solo si publicada según CHECK. |
| Ediciones | `GET/POST /admin/initiatives/{id}/editions/`; `GET/PATCH /admin/initiative-editions/{id}/`. | D: año único por programa, temporada, fechas y estado. No crear actividades directamente bajo el programa sin edición. |
| Indicadores/cobertura | Operaciones bajo `/admin/initiative-editions/{id}/indicators/` y `/communities/`. | D: valor/unidad/fecha/tipo de medición; comunidades únicas por edición. Acordar edición y validaciones. |
| Actividades y multimedia | Operaciones de actividades bajo edición y medios bajo iniciativa con `id_edicion` opcional. | D/L: multimedia no tiene `id_actividad`; no prometer relación de galería por jornada sin adaptación. |
| Vínculos con casos | Operaciones bajo `/admin/initiative-editions/{id}/cases/`. | D/L: `iniciativa_casos`, tipo de vínculo y unicidad; solo casos autorizados al publicar. |
| Revisión de propuestas | `GET /admin/initiative-proposals/`; `GET/PATCH /admin/initiative-proposals/{id}/`. | D/L: al aprobar/rechazar exige revisor y fecha; proteger contacto/respuesta y distinguir iniciativa solicitada de generada. |
| Moderación de comentarios | `GET /admin/comments/`; `POST /admin/comments/{id}/moderation/`. | D/L: estados `pendiente/aprobado/rechazado/oculto`. Definir moderación antes de habilitar el circuito público real. |
| Noticias y boletín | CRUD/publicación de noticias y suscripciones. | A: sin tablas. No implementarlos como si ya estuvieran dentro de las 30. |
| Borradores, casos seguidos y preferencias | Rutas propias de usuario cuando se apruebe su persistencia. | A: no hay tablas/campos. Borrador local no exige endpoint. |
| Radicación institucional | `POST /admin/cases/`. | D/L/A: definir propietario representado, permisos y aceptaciones. El botón actual está inactivo. |
| Alertas tempranas | Operaciones de alertas según alcance aprobado. | A: notificación genérica no equivale a entidad/flujo de alerta temprana. |
| Configuración institucional | Lectura/edición de claves permitidas bajo `/admin/site/`. | D/L: JSONB por clave; validación por esquema de clave y separación de configuración pública/privada. |

No pedir endpoints de producción para cargar ejemplos, restablecer simulaciones, cambiar tema, abrir/cerrar paneles, copiar enlaces, cancelar formularios o mostrar estados de sesión/403/404.

## 15. Mapa de integración de las vistas existentes

| Pantalla | Operaciones | Ajuste/condición principal |
|---|---|---|
| Inicio, Nosotros, encabezado y pie | PUB-01/PUB-02, PUB-05 y MAP-01/MAP-02. | Contenido verificado en configuración; noticias y cifras no respaldadas no se presentan como reales. |
| Noticias | CAT-07, PUB-03/PUB-04/PUB-09. | Solicitar persistencia de noticias y boletín (AMP-01/AMP-02); mantener demostración explícita hasta integrar. |
| Iniciativas | CAT-08, PUB-05 a PUB-08, INI-01 a INI-03. | Separar programa/edición y completar título/consentimiento de postulación. |
| Mapa | CAT-01 a CAT-06, MAP-01/MAP-02. | Sin cuencas salvo ampliación; ubicación exacta no se publica sin revisión. |
| Caso público | MAP-03/MAP-04/MAP-06/MAP-07. | Galería MAP-05 y seguimiento MAP-08 a MAP-10 condicionados. |
| Login/registro/recuperación | AUTH y ME-01. | Nombres/apellidos separados, hash compatible, JWT/roles únicos y política de aceptación. |
| Mis casos y radicación | CIT-01 a CIT-04, catálogos. | Radicado de servidor; resolver cantidades, consentimientos y obligatoriedad de coordenadas. |
| Expediente ciudadano | CIT-04 a CIT-08, MSG. | No exponer notas no públicas como si todas fueran ciudadanas; resolver aportes/correcciones/resultados. |
| Mensajes/notificaciones | MSG y NOT. | Destinatario real, lectura por participante y notificaciones del usuario. |
| Perfil | ME-01 a ME-05. | Solicitar perfil, foto y preferencias (AMP-04), además de adaptar nombres/límites. |
| Dashboard/casos administrativos | ADM y catálogos, USR-01 para candidatos. | UUID de estados reales, rol y ámbitos; reglas para campos no persistidos. |
| Informes | REP, catálogos. | Agregados/exportación completos, sin marcas de simulación. |
| Auditoría | AUD. | Referencia de fuente; antes/después no siempre existe. |
| Usuarios y roles | USR. | Rol único real, tres estados, nombres/apellidos y límites SQL. |

## 16. Petición concreta al equipo backend y orden de trabajo

### Primera entrega

1. Confirmar que este DDL representa la base/migraciones realmente utilizadas por Django y entregar OpenAPI o las rutas existentes. La revisión de un archivo no verifica una instancia desplegada.
2. Entregar AUTH, ME-01/ME-02, catálogos y lectura/radicación de casos con UUID/radicado y estado real. Cargar tipos de caso y territorios necesarios o permitir estados vacíos correctos.
3. Implementar las ampliaciones prioritarias de la sección 18 para visibilidad de seguimientos/evidencias, aportes, correcciones, resultados y consentimiento. Acordar contratos antes de habilitar funciones privadas; no aceptar silenciosamente campos sin guardar.
4. Entregar asignación transaccional y elegibilidad por ámbitos, estado único operativo y publicación separada; seguir con mensajes por destinatario, notificaciones, informes y auditoría.
5. Conectar iniciativas por programa/edición, indicadores, cobertura y postulación válida. Incorporar noticias, boletín, casos seguidos, foto y preferencias con sus ampliaciones; si se entrega por etapas, mantenerlas explícitamente pendientes hasta contar con soporte.
6. Ajustar los adaptadores/formularios Angular a contratos aprobados y retirar los datos/acciones de demostración del flujo real.

### Lo que debe incluir cada contrato entregado

- Método/URL definitiva, permisos, tablas/fuentes y efectos secundarios.
- Campos de lectura/escritura, requeridos/nulos, UUID, enumeraciones, límites y ejemplos de éxito/error.
- Parámetros de filtro, relaciones padre/hijo, orden, paginación y alcance de totales.
- Autenticación, caducidad, renovación, estado de usuario, autorización por objeto/ámbito y manejo de concurrencia.
- Multipart, atomicidad, idempotencia, validación/almacenamiento y descarga privada cuando hay archivos.
- Datos de prueba autorizados por cada rol real y casos en estados/visibilidades diferentes, sin depender de los fixtures del frontend.

### Verificaciones de aceptación

- Un registro tiene nombres/apellidos, correo normalizado y un rol real; ningún endpoint permite al ciudadano concederse privilegios.
- Un caso guarda solo campos respaldados/acordados, recibe un código único y no se duplica por reintentos controlados.
- Un caso tiene como máximo una asignación activa, con cambios transaccionales y ámbito elegible.
- Publicación aprobada cumple `fecha_aprobacion`; operación de cierre no aprueba automáticamente publicación ni revela archivos.
- El ciudadano no obtiene notas internas ni mensajes de otros participantes; endpoints públicos no exponen datos privados o coordenadas sensibles sin la política correspondiente.
- Una iniciativa muestra el año y métricas de la edición correcta; no mezcla programas y ejecuciones anuales.
- Una postulación inválida por título/contacto/territorio/consentimiento produce error de campo; una válida no crea automáticamente iniciativa.
- Informes y exportación cubren toda la selección autorizada; auditoría distingue las fuentes y no fabrica valores previos.

## 17. Fuentes y alcance de la comprobación

- `base de datos.md`: se revisaron las 30 definiciones de tabla, restricciones relevantes, índices, triggers, vistas y seeds. No se ejecutó el script ni se comprobó su despliegue.
- `src/app/app.routes.ts`, formularios de autenticación/ciudadano/administración y modelos de demostración: identifican los datos que hoy solicita la interfaz.
- `contexto.md` y documentación funcional en `docs/`: contexto de producto; ante diferencias de persistencia, este documento toma como base el DDL añadido y señala decisiones, sin reinterpretarlo como API publicada.
- `docker/nginx.conf`: proxy de `/api/`; circuito de medios por acordar.

**Cambios de código pendientes:** esta revisión actualiza la petición al backend. El frontend conserva sus demostraciones y aún debe adaptarse a rol único, nombres separados, límites, estados reales y ediciones cuando se aprueben los contratos. No se afirma que esas correcciones ya estén implementadas.

## 18. Tablas y campos adicionales solicitados al backend

Esta sección convierte las carencias identificadas en una **petición de ampliación**, con prioridad y relación con los endpoints. Los nombres y columnas siguientes son propuestas, no tablas existentes ni SQL para ejecutar. El backend puede ofrecer un modelo equivalente que conserve el comportamiento, las relaciones y la privacidad requeridos.

### 18.1. Tablas nuevas para funciones previstas

| ID / prioridad | Tabla o conjunto propuesto | Datos y relaciones mínimos solicitados | Endpoints afectados |
|---|---|---|---|
| AMP-01 · P1 | `categorias_noticias`, `noticias`, `noticia_multimedia` | Categoría con ID/nombre/slug; noticia con autor FK a usuarios, categoría, título, slug único, extracto, contenido, publicación, fecha de publicación, destacado y timestamps. Medios asociados con tipo, ruta, texto alternativo, descripción, orden y portada. Definir revisión y publicación, no solo un booleano de visible. | CAT-07, PUB-03/PUB-04, destacados de PUB-02 y futuro CRUD administrativo de noticias. |
| AMP-02 · P1 | `suscripciones_boletin` | ID, nombre, correo normalizado, estado de suscripción, fechas de solicitud/confirmación/baja y referencia a la aceptación de política. Unicidad de correo según política de altas/bajas; confirmación y baja con tokens seguros/expiración mediante servicio o persistencia definida, sin guardar tokens de enlace en claro. Definir conservación del historial al volver a suscribirse. | PUB-09/PUB-10/PUB-11 y preferencia de boletín de ME-05. |
| AMP-03 · P1 | `casos_seguidos` | FK usuario/caso, fecha, estado o fecha de baja y preferencias si el producto las admite. Relación activa única usuario/caso; comprobar que el caso se puede seguir. El alta no concede acceso a información privada. | MAP-08/MAP-09/MAP-10 y producción de notificaciones de novedades públicas. |
| AMP-04 · P1 | `perfiles_usuarios`, `preferencias_usuarios` | Relación uno a uno con usuario; perfil con referencia de fotografía y residencia mediante catálogos, sin confundir residencia con ámbitos del responsable. Preferencias de novedades de casos, mensajes y boletín, con fecha de actualización. Acordar representación de territorio parcial cuando se elija municipio sin comunidad y validar jerarquía. | ME-01 a ME-05 y formularios del perfil. |
| AMP-06 · P0 | `solicitudes_correccion` | Caso, solicitante autorizado, descripción/motivo, fecha, estado del requerimiento, respuesta/aporte relacionado, fecha de respuesta y resolución de revisión si aplica. Conservar historial y definir si puede haber más de una solicitud abierta. No reemplazarlo por cambiar publicación a `pendiente` sin requerimiento identificado. | ADM-07, CIT-04/CIT-08, historiales y notificaciones. |
| AMP-07 · P0 | `aportes_caso` y asociación de evidencias | Caso, autor, texto, fecha y solicitud de corrección opcional. Relacionar explícitamente cada archivo con su aporte: FK opcional en evidencia si cada archivo pertenece a un solo aporte, o tabla de asociación si se necesita reutilización. Validar que aporte, evidencia y corrección pertenecen al mismo caso. | CIT-08, CIT-05/CIT-06 y ADM-04/ADM-05. |
| AMP-09 · P0 | `documentos_legales`, `aceptaciones_legales` o equivalente verificable | Documento/tipo, versión, contenido o referencia inmutable y vigencia. Aceptación vinculada a versión, finalidad, fecha de servidor y usuario cuando exista; relación con caso, propuesta o suscripción mediante referencias validadas. Permitir solicitudes públicas sin inventar usuario. Definir trazabilidad y retención; no almacenar IP u otros datos adicionales por defecto sin necesidad acordada. | AUTH-01, CIT-03, PUB-08/PUB-09 y consulta de políticas vigentes en PUB-01. |

La numeración AMP identifica necesidades funcionales; AMP-05 y AMP-08 aparecen en las ampliaciones de tablas existentes. No supone que sea obligatorio crear una tabla independiente para cada necesidad.

### 18.2. Campos y relaciones que ampliar en tablas existentes

| ID / prioridad | Tabla actual | Ampliación solicitada | Reglas y endpoints afectados |
|---|---|---|---|
| AMP-05 · P0 | `casos` | Cantidad de familias afectadas y meses de afectación. | Enteros no negativos y definición explícita de desconocido frente a cero; coherencia de lectura/escritura. CIT-03/CIT-04, ADM-03 y resúmenes. No guardar estas cantidades únicamente dentro del texto narrativo. |
| AMP-08 · P0 | `seguimientos` | Título y audiencia explícita: público, ciudadano/equipo o interno. Posibilidad de tipificar el evento de seguimiento/resolución si se adopta para resultados. | Migrar con criterio conservador: un antiguo `visible_publicamente=false` no se transforma automáticamente en visible al ciudadano. MAP-04, CIT-05 y ADM-04/ADM-09. Sustituir o derivar el booleano desde la audiencia, sin mantener dos fuentes contradictorias. |
| AMP-10 · P0 | `evidencias` | Audiencia/visibilidad y estado de revisión/publicación; nombre original seguro, MIME, tamaño y estado de procesamiento cuando no exista un servicio persistente que los entregue. | Reserva inicial, autorización de cambio y publicación explícita; caso aprobado no basta para publicar archivos. MAP-05, CIT-06/CIT-07, ADM-05/ADM-06/ADM-11. Incluir validación de contenido y política de almacenamiento. |
| AMP-11 · P0 | `casos` y/o seguimiento de resolución | Resultado narrativo y referencia estable a la resolución vigente, autor y fecha. | Preferir una representación identificable de resolución/cierre que conserve historial: evento tipificado o entidad de resultados, según backend. No duplicar narración en varios sitios ni tomar el motivo genérico del trigger como resultado. ADM-10, CIT-04 y lectura pública solo cuando se autorice. |
| AMP-12 · P1 | `tipos_caso` | Naturaleza del caso separada de categoría temática, si se mantienen «problemática» y «proyecto/iniciativa» como filtro independiente. | Puede ser un catálogo o atributo controlado según backend. Seleccionar tipo determina una naturaleza coherente; no deducirla del texto del nombre. CAT-06, MAP-01/MAP-02, CIT-03 y ADM-02. |

Para AMP-06/AMP-07/AMP-11, los nuevos registros deben originarse en operaciones autorizadas y conservar sus vínculos. Una respuesta a corrección no cierra el requerimiento automáticamente si hace falta revisión del equipo: documentar estados y efectos.

### 18.3. Ampliaciones que necesitan una decisión funcional adicional

No son requisitos automáticos por el simple hecho de que un control aparezca en una demostración:

| ID | Ampliación posible | Cuándo pedirla |
|---|---|---|
| AMP-13 | `cuencas` y relaciones con municipios/comunidades | Si se confirma mantener consulta por cuenca/subcuenca y se dispone de una fuente territorial válida. Definir jerarquía y si una comunidad puede relacionarse con varias cuencas. CAT-04 queda pendiente de esta decisión, no se deduce de nombres. |
| AMP-14 | `usuarios_roles` y, si se requiere, catálogo de permisos/relación rol-permiso | Solo si se confirma conservar múltiples roles por usuario o permisos configurables. El SQL actual tiene rol único: migrar fuentes, reglas de combinación, auditoría y autorizaciones de forma coherente, sin mantener simultáneamente dos fuentes contradictorias. Mientras no se acuerde, sigue vigente USR-05 con rol único. No solicitar roles nuevos únicamente para copiar etiquetas de ejemplo. |
| AMP-15 | `borradores_caso` y archivos temporales relacionados | Si guardar borrador debe sobrevivir a recarga/cambio de dispositivo. Acordar expiración, limpieza y conversión atómica en radicación. El borrador temporal actual no exige una tabla por sí solo. |
| AMP-16 | `alertas_tempranas` y destinatarios/entregas | Cuando se defina el botón y recorrido institucional: contenido, revisión, canales, aprobación, recepción y trazabilidad. Una fila de notificación no representa todo ese proceso. |
| AMP-17 | Vínculo multimedia–actividad y publicación de edición/medio | Si se habilitan galerías por jornada o publicación independiente de ediciones/imágenes. La estructura actual solo asocia multimedia con programa/edición. Elegir FK o asociación según cardinalidad real. |

No hace falta agregar una tabla de dashboard, informes o conversaciones para cada endpoint: muchos son consultas/agregaciones sobre datos existentes. Tampoco se exige duplicar los cinco grupos de auditoría ni crear un almacén paralelo de usuarios si Django puede integrar el existente.

### 18.4. Requisitos de entrega de las ampliaciones

1. Entregar migraciones Django y esquema actualizado; incluir FKs, nulabilidad, restricciones, índices y estrategia para los datos ya existentes. No ejecutar el SQL integral de una base vacía sobre una base con datos para aplicar estos cambios.
2. Definir catálogos, enumeraciones y transiciones del dominio. Publicación de noticias, correcciones y revisión de archivos son propuestas hasta acordar sus valores, no códigos ya disponibles.
3. Actualizar OpenAPI y los contratos de los endpoints afectados con solicitudes/respuestas y errores de validación. No aceptar campos que se descarten silenciosamente.
4. Probar pertenencia y autorización en nuevas relaciones, audiencias y descargas. Las nuevas tablas no habilitan por sí solas exposición pública ni envío de mensajes/correos.
5. Conservar historial de aceptaciones, asignaciones, correcciones, resultados y eventos que lo necesiten; definir retiradas/bajas y evitar borrados que rompan trazabilidad.
6. Definir la relación entre preferencia de boletín del usuario y su suscripción real: un cambio de checkbox debe respetar confirmación, consentimiento y baja, sin crear dos estados contradictorios.
7. Priorizar AMP-05 a AMP-11 para completar casos y privacidad; entregar AMP-01 a AMP-04 para portal/perfil. Acordar el alcance y orden de las demás antes de implementar.

**Petición final al backend:** ampliar el modelo para cubrir las funciones previstas y entregar sus contratos, en lugar de limitar la API a las 30 tablas iniciales. La clasificación A/C del inventario expresa una dependencia técnica pendiente y no una renuncia a esas funciones.
