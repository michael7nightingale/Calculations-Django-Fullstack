from django.http import FileResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, TemplateView, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import logout, login, get_user_model
from passlib.hash import django_pbkdf2_sha256
from datetime import datetime
import logging

from Calculations_v2.settings import BASE_DIR
from package import tables, exceptions
from users.forms import *
from users.models import *


User = get_user_model()
year = datetime.now().year
logger = logging.getLogger(__name__)


class UserDataMixin:
    """Миксин для общих данных:пользователь и дата"""
    def get_user_data(self, user):
        return {
            'user': user,
            'year': year,

        }


class RegisterUserView(CreateView):
    """Регистрация пользователя"""
    form_class = RegisterUserForm
    template_name = "users/register.html"

    def form_valid(self, form):
        hsh_psw = django_pbkdf2_sha256.hash(self.request.POST['password'])
        try:
            scientist = Scientist.objects.create(
                plot_path=None,
            )
            scientist.save()
            user = User.objects.create(
                password=hsh_psw,
                username=self.request.POST['username'],
                email=self.request.POST['email'],
                scientist=scientist
            )
            user.save()
            login(self.request, user)
            return redirect(reverse("home"))
        except Exception as e:
            print(str(e))
            return redirect(reverse("users_register"))


@login_required
def logoutView(request):
    """Выход пользователя из аккаунта"""
    logout(request)
    return redirect(reverse('home'))


def loginView(request):
    """Авторизация пользователя"""
    context = {
        "title": "Авторизация",
        "form": LoginUserForm,

    }
    if request.method == "POST":
        loginData = request.POST
        username = loginData['username']
        try:
            userTry = User.objects.get(username=username)
            password = loginData['password']
            print(userTry, django_pbkdf2_sha256.verify(password, userTry.password))
            if django_pbkdf2_sha256.verify(password, userTry.password):
                login(request, userTry)
                return redirect(reverse('home'))
            else:
                context.update(message="Неверный пароль")
        except User.DoesNotExist:
            context.update(message="Пользователя с таким именем не существует.")

    return render(request, "users/login.html", context=context)


class PersonalCabinetView(LoginRequiredMixin, TemplateView, UserDataMixin):
    """Личный кабинет пользователя."""
    login_url = '/login/'
    template_name = "users/personal_cabinet.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        logger.debug(self.request)
        context = super().get_context_data(**kwargs)
        context['title'] = 'Личный кабинет'
        return dict(
            tuple(context.items()) + tuple(self.get_user_data(self.request.user).items())
        )


class AddFormulaView(LoginRequiredMixin, CreateView, UserDataMixin):
    """Предложение формулы."""
    template_name = 'users/add_formula.html'
    form_class = AddRequestForm
    model = FormulaRequest

    def get_context_data(self, *, object_list=None, **kwargs):
        logger.debug(self.request)
        context = super().get_context_data(**kwargs)
        context['title'] = 'Предложить формулу'
        return dict(
            tuple(context.items()) + tuple(self.get_user_data(self.request.user).items())
        )

    def post(self, request, *args, **kwargs):
        science_ = Science.objects.get(title=self.request.POST['science'])
        category = Category.objects.get(title=self.request.POST['category'])
        formula_request = FormulaRequest.objects.create(title=self.request.POST['title'],
                                                        content=self.request.POST['content'],
                                                        cat=category,
                                                        science=science_,
                                                        user=self.request.user,
                                                        formula=self.request.POST['formula'])
        formula_request.save()
        # form.save()
        return redirect('users_cabinet')


class HistoryView(LoginRequiredMixin, ListView, UserDataMixin):
    """Просмотр журнала вычислений."""
    template_name = 'users/history.html'
    model = History
    context_object_name = 'history'

    def get_queryset(self):
        return History.objects.filter(user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        logger.debug(self.request)
        context = super().get_context_data(**kwargs)
        context['title'] = 'История вычислений'
        return dict(
            tuple(context.items()) + tuple(self.get_user_data(self.request.user).items())
        )


# ============================ДОБАВЛЕНИЕ=ФОРМУЛ====================#

class AcceptFormulasView(PermissionRequiredMixin, ListView, UserDataMixin):
    template_name = 'users/accept_formulas.html'
    permission_required = ('stuff', 'superuser')
    model = FormulaRequest
    context_object_name = 'formulas'

    def get_context_data(self, *, object_list=None, **kwargs):
        logger.debug(self.request)
        context = super().get_context_data(**kwargs)
        context['title'] = 'Предложенные формулы'
        return dict(
            tuple(context.items()) + tuple(self.get_user_data(self.request.user).items())
        )


class AcceptFormulaView(PermissionRequiredMixin, TemplateView, UserDataMixin):
    template_name = "users/accept_formula.html"
    permission_required = ('stuff', 'superuser')
    # form = AddFormulaForm

    def get_context_data(self, *, object_list=None, **kwargs):
        logger.debug(self.request)
        context = super().get_context_data(**kwargs)
        context['title'] = f"Предложение {self.kwargs['request_id']}"
        return dict(
            tuple(context.items()) + tuple(self.get_user_data(self.request.user).items())
        )

    def get_queryset(self):
        self.formulaRequest = FormulaRequest.objects.get(pk=self.kwargs['request_id'])
        return self.formulaRequest

    def get(self, request, *args, **kwargs):
        self.get_queryset()
        context = self.get_context_data()
        data = {
            "title": self.formulaRequest.title,
            "formula": self.formulaRequest.formula,
            "content": self.formulaRequest.content,
            "category": self.formulaRequest.cat,
            "science": self.formulaRequest.science,
            "user": self.formulaRequest.user,
            "date": self.formulaRequest.date
                }
        context['request'] = AddRequestForm(data=data)
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        if 'delete' not in request.POST:
            title = request.POST['title']
            formula = request.POST['formula']
            category = request.POST['category']
            content = request.POST['content']

        self.get_queryset().delete()
        return redirect("users_accept_formulas")


@login_required
def download_history_view(request):
    """Скачать историю вычислений в формате csv"""
    try:
        message = "Ошибка"
        user_id = request.user.id
        filename = request.POST['filename'] + '.csv'
        absolute_path = str(BASE_DIR) + '/media/' + filename
        history = History.objects.filter(user=user_id).values("formula", "result", "time_counted")
        # download history
        table = tables.CsvTableManager(filepath=absolute_path)
        table.init_data(("formula", "result", "time_counted"))
        for line in serialize_formulas(history):
            table.add_line(line_data=[str(i) for i in line.values()])
        table.save_data(absolute_path)
        file = open(absolute_path, 'rb')
        return FileResponse(
            file,
            as_attachment=True,
            filename=filename
        )
    except exceptions.EmptyDataError:
        return redirect(reverse("users_history"))


def serialize_formulas(query):
    for i in query:
        yield dict(i)


@login_required
def delete_history_view(request):
    """Удалить всю историю вычислений пользователя"""
    query = History.objects.filter(user=request.user.id)
    if query:
        query.delete()
    return redirect('users_history')
