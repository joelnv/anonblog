from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.
class Post(models.Model):
    title = models.CharField(validators=[MinLengthValidator(10,"The value should be lesser than %(limit_value)s.")],max_length=100)
    body = models.TextField(validators=[MinLengthValidator(10,"The value should be lesser than %(limit_value)s.")])
    date = models.DateTimeField(auto_now_add=True)
    skey =models.CharField(max_length=9)


    def __str__(self):
        return self.title


    def snippet(self):
        return self.body[:75]

