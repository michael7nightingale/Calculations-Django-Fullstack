from django.urls import path, include
from django.views.decorators.cache import cache_page
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('<slug:science_slug>/', cache_page(120)(ScienceView.as_view()), name='science_science'),
    path('mathem/category/equations/', equationsView, name='science_equations'),
    path('mathem/category/plots/', plotsView, name='science_plots'),
    path('<slug:science_slug>/category/<slug:category_slug>/', cache_page(120)(CategoryView.as_view()), name='science_category'),

    path('<slug:science_slug>/formulas/<slug:formula_slug>/', formulaView, name='science_formula'),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
