from django.shortcuts import render


def page_not_found(request, exception=None):
    """Renderiza a página 404 personalizada."""
    return render(request, "404.html", status=404)


def server_error(request, exception=None):
    """Renderiza a página 500 personalizada."""
    return render(request, "500.html", status=500)
