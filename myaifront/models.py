from django.db import models

# Create your models here.
class Topmenu(models.Model):
    title=models.CharField(default='',blank=True,null=True,max_length=20)
    url = models.CharField(default='', blank=True, null=True, max_length=20)
    def __str__(self):
        return self.title
class Banner(models.Model):
    img=models.ImageField(blank=True,null=True)
    def __int__(self):
        return self.id