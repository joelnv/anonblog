from django.db import models
from django.core.validators import MinLengthValidator
from django import forms
from bs4 import BeautifulSoup
# Create your models here.

class Post(models.Model):
    title = models.CharField(validators=[MinLengthValidator(10, "The value should be more than %(limit_value)s.")],
                             max_length=100)
    body = models.TextField(validators=[MinLengthValidator(10, "The value should be more than %(limit_value)s.")])
    date = models.DateTimeField(auto_now_add=True)
    skey =models.CharField(max_length=9)

    def __str__(self):
        return self.title

    def snippet(self):
        return self.body[:75]

    def toc(self):
        body = self.body
        soup = BeautifulSoup(body, 'lxml')
        toc = ""
        for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            if tag.string:
                text = tag.string
                headtype = int(tag.name[1:])
                tag.string.replace_with("<ul>" * headtype + "<li>" + text + " </li>" + "</ul>" * headtype)
                toc += tag.string
        return toc
