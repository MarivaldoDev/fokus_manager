from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def page_not_found(
    request: HttpRequest, exception: Exception | None = None
) -> HttpResponse:
    """Renderiza a página 404 personalizada."""
    return render(request, "404.html", status=404)


def server_error(
    request: HttpRequest, exception: Exception | None = None
) -> HttpResponse:
    """Renderiza a página 500 personalizada."""
    return render(request, "500.html", status=500)
