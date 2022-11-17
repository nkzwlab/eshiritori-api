from django.db import models

# Create your models here.
class TestData(models.Model):
    testname = models.CharField(max_length=100)
    testvalue = models.IntegerField()

class Histories(models.Model):
    word = models.TextField()
    img = models.TextField()

    def __str__(self):
        return self.word