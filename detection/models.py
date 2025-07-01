from django.db import models

# Create your models here.

class detection(models.Model):
    id = models.AutoField
    diseases  = models.CharField(max_length=50 ,default= "")
    image = models.ImageField(upload_to="detection/Images" ,max_length=255 ,default="")


    def __str__(self):
        return self.diseases