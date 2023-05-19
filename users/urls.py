from django.urls import path, include
from .views import *


historyPatterns = [
    path('', HistoryView.as_view(), name='users_history'),
    path('download/', download_history_view, name='users_history_download'),
    path('delete/', delete_history_view, name='users_history_delete'),

]


cabinetPatterns = [
    path('', PersonalCabinetView.as_view(), name='users_cabinet'),
    path('history/', include(historyPatterns)),
    path('add_formula/', AddFormulaView.as_view(), name='users_add_formula'),
    path('accept_formulas/', AcceptFormulasView.as_view(), name='users_accept_formulas'),
    path('accept_formula/<int:user_id>/<int:request_id>/', AcceptFormulaView.as_view(), name='users_accept_formula'),

]


urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='users_register'),
    path('logout/', logoutView, name='users_logout'),
    path("login/", loginView, name='users_login'),
    path('cabinet/', include(cabinetPatterns)),

]



