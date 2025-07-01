from django.db import models

# Create your models here.

class llm(models.Model):
    id = models.AutoField
    qusetion  = models.TextField(default= "")
    answer = models.TextField(default= "")


    def __str__(self):
        return self.qusetion