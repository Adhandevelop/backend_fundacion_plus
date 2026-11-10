import mimetypes
import os
from django.core.files.storage import default_storage
from django.http import FileResponse, Http404
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView


class PublicMediaServeView(APIView):
    """
    Entrega autorizada de archivos multimedia públicos a través de `/api/v1/public/media/<path:file_path>`.
    Compatible con configuraciones Nginx donde solo `/api/` se reenvía al contenedor backend.
    - Permite carpetas públicas: `profiles/`, `news/`, `initiatives/`.
    - Para `cases/evidence/`, verifica en base de datos que la evidencia pertenezca a un caso con
      `estado_publicacion='aprobado'` y que la evidencia tenga `audiencia='publico'` y `estado_revision='aprobada'`.
    - Cualquier evidencia privada o en revisión es bloqueada con 403/404.
    """
    permission_classes = [permissions.AllowAny]

    PUBLIC_PREFIXES = ('profiles/', 'news/', 'initiatives/', 'site/')

    @extend_schema(
        parameters=[
            OpenApiParameter(
                'file_path',
                OpenApiTypes.STR,
                OpenApiParameter.PATH,
                description='Ruta relativa del recurso multimedia público (ej. profiles/foto.jpg, news/portada.webp).',
            ),
        ],
        responses={200: OpenApiTypes.BINARY},
        summary='Servir archivo multimedia público verificado (fotos de perfil, portadas y evidencias públicas aprobadas)',
    )
    def get(self, request, file_path: str):
        normalized = (file_path or '').replace('\\', '/').lstrip('/')
        if not normalized or '..' in normalized.split('/'):
            raise Http404('Ruta de archivo inválida.')

        is_allowed_public = normalized.startswith(self.PUBLIC_PREFIXES)
        if not is_allowed_public:
            if normalized.startswith('cases/evidence/'):
                from apps.cases.models import Case, CaseEvidence

                is_public_evidence = CaseEvidence.objects.filter(
                    ruta_archivo=normalized,
                    audiencia=CaseEvidence.Audiencia.PUBLICO,
                    estado_revision=CaseEvidence.EstadoRevision.APROBADA,
                    caso__estado_publicacion=Case.EstadoPublicacion.APROBADO,
                ).exists()
                if not is_public_evidence:
                    raise PermissionDenied('Este archivo de evidencia no es de acceso público.')
            else:
                raise PermissionDenied('Este directorio de medios no es de acceso público.')

        if not default_storage.exists(normalized):
            raise Http404('El archivo solicitado no existe.')

        content_type, _ = mimetypes.guess_type(normalized)
        file_handle = default_storage.open(normalized, 'rb')
        response = FileResponse(
            file_handle,
            as_attachment=False,
            filename=os.path.basename(normalized),
            content_type=content_type or 'application/octet-stream',
        )
        return response
