import asyncio

from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from datetime import datetime
from asgiref.sync import async_to_sync, sync_to_async
import logging

from Calculations_v2.settings import BASE_DIR
from .models import *
from users.history import form_history
from formulas import contextBuilder, plots, mathem_extra_counter

# логирование
logger = logging.getLogger(__name__)
year = datetime.now().year


class CommonContextMixin:
    """Миксин для всех классов-представлений"""
    def get_user_context(self, **kwargs):
        context = kwargs
        context['year'] = datetime.now().year
        return context


class ScienceView(ListView, CommonContextMixin):
    context_object_name = "categories"
    template_name = 'science/science.html'
    model = Category

    def get_queryset(self):
        self.science = Science.objects.get(slug=self.kwargs['science_slug'])
        return Category.objects.filter(science__id=self.science.id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_user_context(**kwargs)
        context['science'] = self.science
        context[self.context_object_name] = self.get_queryset()
        context = dict(
            tuple(context.items()) + tuple(self.get_user_context().items())
        )
        return context


class CategoryView(ListView, CommonContextMixin):
    template_name = "science/category.html"
    context_object_name = "formulas"
    model = Formula

    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs['category_slug'])

        return Formula.objects.filter(category__id=self.category.id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_user_context(**kwargs)
        context['category'] = self.category
        context[self.context_object_name] = self.get_queryset()
        context = dict(
            tuple(context.items()) + tuple(self.get_user_context().items())
        )
        return context


@csrf_exempt
def formulaView(request, science_slug, formula_slug):
    context = asyncio.run(contextBuilder.build_template(request, science_slug, formula_slug))
    formula = Formula.objects.get(slug=formula_slug)
    context.update(
        formula=formula,
    )
    return render(request, "science/template_formula.html", context=context)


def plotsView(request):
    context = {
        "title": "Графики функций",

    }
    message = ""
    if request.method == "POST":
        if request.user:
            functions = []
            limit = 4
            for number in range(1, limit + 1):
                func = request.POST[f"function{number}"]
                if func:
                    functions.append(func)
            xmin = request.POST['xmin']
            xmax = request.POST['xmax']
            ymin = request.POST['ymin']
            ymax = request.POST['ymax']
            if all((xmin, xmax)):
                try:
                    plot = plots.Plot(
                        functions=functions,
                        xlim=(xmin, xmax),
                        ylim=(ymin, ymax)
                    )
                    plot_path = '/media/plots/' + f"{request.user.id}.png"
                    plot.save_plot(str(BASE_DIR) + plot_path)
                    context.update(image_url=plot_path)
                except Exception as e:
                    print(str(e))
                    message = "Неожиданная ошибка."
            else:
                message = "Неверная область значения и/или область определения."
        else:
            message = "Построение графиков доступно только авторизированным пользователям."
    return render(request, "science/plots.html", context=context)


def equationsView(request):
    context = {
        "title": "Уравнения",

    }
    if request.method == 'POST':
        equations = []
        limit = 4
        for number in range(1, limit + 1):
            eq = request.POST[f"equation1"]
            if eq:
                equations.append(eq)
        result = mathem_extra_counter.equation_system(equations)
        context.update(result=result)
        if request.user.is_authenticated:
            form_history(
                user=request.user,
                formula="",
                result=result,
                time_counted=datetime.now()
            )

    return render(request, "science/equations.html", context=context)


