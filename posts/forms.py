from django import forms
from . import models


class CreatePosts(forms.ModelForm):
    forms.error_css_class = "alert alert-danger"
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}))
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Body'}))
    class Meta:
        model = models.Post
        fields = ['title','body']

    def clean(self):
        super().clean()
        title = self.cleaned_data.get('title')
        body = self.cleaned_data.get('body')
        if len(title) > len(body):
            raise forms.ValidationError("body should be longer than title")