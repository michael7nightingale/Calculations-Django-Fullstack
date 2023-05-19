from django.db import models
from django.urls import reverse


class Science(models.Model):
    title = models.CharField("Название науки", max_length=40, unique=True)
    content = models.TextField("О науке")
    slug = models.SlugField("Слаг науки", unique=True)

    def get_absolute_url(self):
        return reverse('science_science', kwargs={'science_slug': self.slug})

    def __str__(self):
        return self.slug

    class Meta:
        unique_together = ('title', 'slug')


class Category(models.Model):
    title = models.CharField("Название раздела", max_length=100, unique=True)
    content = models.TextField("О разделе")
    science = models.ForeignKey(to='Science', on_delete=models.CASCADE)
    slug = models.SlugField("Слаг раздела", unique=True)

    def get_science_url(self):
        return self.science.get_absolute_url()

    def get_absolute_url(self):
        return reverse("science_category", kwargs={"science_slug": self.science.slug,
                                                    "category_slug": self.slug})

    def __str__(self):
        return self.slug

    class Meta:
        unique_together = ('title', 'slug')


class Formula(models.Model):
    title = models.CharField("Название формулы", max_length=200, unique=True)
    content = models.TextField("О формуле")
    formula = models.CharField("Формула", unique=True, max_length=255)
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE)
    slug = models.SlugField("Слаг формулы", unique=True)

    def __str__(self):
        return self.formula

    def get_science_url(self):
        return self.category.science.get_absolute_url()

    def get_category_url(self):
        return self.category.get_absolute_url()

    def get_absolute_url(self):
        return reverse("science_formula", kwargs={"science_slug": self.category.science.slug,
                                                  "formula_slug": self.slug})

    class Meta:
        unique_together = ('title', 'slug', "formula")




