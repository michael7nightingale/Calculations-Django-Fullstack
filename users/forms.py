from django.contrib.auth import get_user_model
from django import forms

from .models import *
from science.models import Category, Science
from package.utils import doubleTitle

#
# User = get_user_model()


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(max_length=254,
                               label="Username",
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Username'}))
    email = forms.EmailField(label="Password",
                               widget=forms.EmailInput({
                                   'class': 'form-control',
                                   'placeholder': 'Email'}))
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class LoginUserForm(forms.Form):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               label="Username",
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Username'}))
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

    class Meta:
        fields = ('username', 'password')


class AddRequestForm(forms.ModelForm):
    science = forms.ChoiceField(label='Наука',
                                choices=(doubleTitle(i) for i in Science.objects.all().values('title')))
    category = forms.ChoiceField(label="Раздел науки",
                                 choices=(doubleTitle(i) for i in Category.objects.all().values('title')))
    title = forms.CharField(label='Название формулы', max_length=100, widget=forms.TextInput)
    content = forms.Field(label='Описание формулы', widget=forms.Textarea)
    formula = forms.CharField(label='Формула скрипта', widget=forms.TextInput)

    class Meta:
        model = FormulaRequest
        fields = ('title', 'content', 'formula', 'science', 'category')
