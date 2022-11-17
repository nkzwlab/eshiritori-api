from django.db import models

# Create your models here.
class Histories(models.Model):
    word = models.TextField()
    img = models.TextField()

    def __str__(self):
        return self.word