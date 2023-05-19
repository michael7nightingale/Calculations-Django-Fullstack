from datetime import datetime

from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "main/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = datetime.now().year
        return context


def error404(request, exception):
    return render(request, "main/404.html")


def error500(request):
    return render(request, "main/500.html")


def error403(request, exception):
    return render(request, "main/403.html")

