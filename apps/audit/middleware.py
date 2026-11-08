from apps.audit.services import set_current_request_meta


class AuditContextMiddleware:
    """Captures client IP, User-Agent, and authenticated user for audit logging."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        ip_address = xff.split(',')[0].strip() if xff else request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        user = getattr(request, 'user', None)
        set_current_request_meta(ip_address, user_agent, user)
        response = self.get_response(request)
        set_current_request_meta(None, '', None)
        return response
