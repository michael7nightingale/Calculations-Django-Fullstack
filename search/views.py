from datetime import datetime
from django.shortcuts import render
import logging

from .forms import SearchForm
from science.models import Formula, Category


year = datetime.now().year
logger = logging.getLogger(__name__)


def searchView(request):
    """Поиск по имени категории или формулы"""
    context = {"form": SearchForm,
               "title": "Поиск",
               "year": year,
               }
    if request.GET:
        where = request.GET['where']
        science = request.GET['science']
        name = request.GET['name']
        if where == 'Категории':
            queryset = Category.objects.filter(title__contains=name, science__title=science)
        elif where == 'Формулы':
            queryset = Formula.objects.filter(title__contains=name, category__science__title=science)
        else:
            assert True, "Неизвестная модель поиска"
        # формируем результат
        result = f"""<h1 class="white_text">{science} - {where}</h1><ul>"""
        if where == 'Формулы':
            for formula in queryset:
                result += ("<li>"
                           # f"<label class='white_text'> {formula.title} ({formula.category})</label>"
                           f"<a class='white_text' href='{formula.get_absolute_url()}'><h5>{formula.title} ({formula.category.title})</h5></a>"
                           "</li>")
        elif where == 'Категории':
            for category in queryset:
                result += ("<li>"
                           f"<a class='white_text' href='{category.get_absolute_url()}'><h5>{category.title}</h5></a>"
                           "</li>")
        result += "</ul>"
        context.update(result=result)
    return render(request, 'search/search.html', context=context)
