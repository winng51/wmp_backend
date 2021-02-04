from django.db import models

# Create your models here.


class Tags(models.Model):
    title = models.CharField(max_length=30)
    create_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Goods(models.Model):
    title = models.CharField(max_length=30)
    create_time = models.DateField(auto_now_add=True)
    edit_time = models.DateField(auto_now=True)
    price = models.IntegerField(default=0)
    seal_price = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.title
