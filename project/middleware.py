from django.http import HttpResponseForbidden


class AdminStaffOnlyMiddleware:
    """Block access to /admin/ for users who are not staff.

    Allows the admin login view so staff can authenticate.
    Returns 403 for other admin URLs when the user isn't authenticated as staff.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if path.startswith("/admin/") and not path.startswith("/admin/login/"):
            user = getattr(request, "user", None)
            if not (user and user.is_authenticated and user.is_staff):
                return HttpResponseForbidden()
            elif user.is_authenticated and not user.is_staff:
                return HttpResponseForbidden()

        return self.get_response(request)
