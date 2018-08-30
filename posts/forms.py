from django import forms
from . import models


class CreatePosts(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['title','body']

    def clean(self):
        super().clean()
        title = self.cleaned_data.get('title')
        body = self.cleaned_data.get('body')
        if len(title) > len(body):
            raise forms.ValidationError("body should be longer than title")

class UpdatePosts(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['title','body']

    def clean(self):
        super().clean()
        title = self.cleaned_data.get('title')
        body = self.cleaned_data.get('body')
        if len(title) > len(body):
            raise forms.ValidationError("body should be longer than title")