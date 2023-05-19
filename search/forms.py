from django import forms

from package.utils import doubleTitle
from science.models import Science

class SearchForm(forms.Form):
    SCIENCES = (doubleTitle(i) for i in Science.objects.values("title"))
    CHOICES = (("Формулы", "Формулы"),
               ("Категории", "Категории"))

    science = forms.CharField(label="Наука",
                                widget=forms.Select(choices=SCIENCES))
    where = forms.CharField(label='Категория или формула',
                               widget=forms.Select(attrs={"class": "form-control"},
                                                   choices=CHOICES))
    name = forms.CharField(label="Название формулы или категории",
                           max_length=50,
                           widget=forms.TextInput())

    class Meta:
        fields = ('science', 'where', 'name')



