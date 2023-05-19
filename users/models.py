from django.db import models
from django.contrib.auth.models import AbstractUser


def createScientist():
    sc = Scientist.objects.create(plot_path=None)
    sc.save()
    return sc.pk


class User(AbstractUser):
    username = models.CharField("Имя пользователя", max_length=40, unique=True)
    password = models.CharField("Хэшированный пароль", max_length=200)
    scientist = models.OneToOneField(to="Scientist", on_delete=models.CASCADE,
                                     null=True)
    email = models.CharField("Электронная почта", max_length=100, unique=True)

    def __str__(self):
        return self.username

    def get_scientist(self):
        return Scientist.objects.get(pk=self.pk)

    class Meta:
        unique_together = ("username", "email")
        abstract = False
        ordering = ('id', )


class Scientist(models.Model):
    plot_path = models.CharField("Путь до графика", blank=True, null=True)
    # user = models.OneToOneField(to="Scientist", unique=True,  on_delete=models.CASCADE, null=True)


class History(models.Model):
    formula = models.CharField("Формула", max_length=255)
    time_counted = models.DateTimeField("Время вычисления", auto_created=True)
    user = models.ForeignKey(to="User", on_delete=models.CASCADE)
    result = models.FloatField("Результат вычисления")

    def history_view(self):
        return f"{self.formula} | {self.result} | {self.time_counted}>"

    class Meta:
        verbose_name = "История вычислений"
        verbose_name_plural = "Истории вычислений"
        # ordering = ['-date_time']


class FormulaRequest(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название отображения", null=True)
    content = models.TextField(blank=True, verbose_name="Описание")
    science = models.ForeignKey("science.Science", on_delete=models.CASCADE)
    cat = models.ForeignKey("science.Category", on_delete=models.CASCADE)
    user = models.ForeignKey("User", db_index=True, on_delete=models.CASCADE, verbose_name="Пользователь", null=True)
    formula = models.CharField(max_length=100, verbose_name='Формула', null=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата запроса')

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('user', 'title')
        verbose_name = 'Предложенная формула'
        verbose_name_plural = 'Предложенные формулы'
        # ordering = ['-date']
