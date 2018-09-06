from django import forms
from . import models


valid_state = 'is-valid'
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

    def clean_title(self):
        valid_state = 'is-invalid'
        return self.cleaned_data['title']