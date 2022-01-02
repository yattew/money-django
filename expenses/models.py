from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
# Create your models here.


class Expense(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    ammount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    category = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.ammount} {self.category}"

    class Meta:
        ordering = ['-date']

class Category(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        return self.name

