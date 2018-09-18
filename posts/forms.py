from django import forms
from . import models
import bleach

VALID_TAGS = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'b', 'i']

class CreatePosts(forms.ModelForm):

    forms.error_css_class = "alert alert-danger"
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-md', 'placeholder': 'Title' ,'pattern':'.{10,}'}))
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control form-control-md', 'placeholder': 'Body' ,'minlength':'10'}))
    class Meta:
        model = models.Post
        fields = ['title','body']

    def clean(self):
        super().clean()
        title = self.cleaned_data.get('title')
        body = self.cleaned_data.get('body')
        if len(title) > len(body):
            raise forms.ValidationError("body should be longer than title")

    def clean_body(self):
        body = self.cleaned_data.get('body')
        sanitized_body = bleach.clean(body, tags=VALID_TAGS)
        return sanitized_body