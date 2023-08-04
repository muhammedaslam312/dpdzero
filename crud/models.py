from django.db import models

# Create your models here.


class DataModel(models.Model):
    key = models.CharField(max_length=50, unique=True)
    value = models.CharField(max_length=50)

    def __str__(self):
        return self.key
