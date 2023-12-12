from .models import Post
from django import forms
from django.forms import TextInput, Textarea, Select

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title','author','text', 'type']

        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Заголовок',
            }),
            "text": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Содержание поста',
            }),
            "author": Select(attrs={
                'class': 'form-control',
                'placeholder': 'Имя автора'
            }),
            "type": Select(attrs={
                'class': 'form-control',
                'placeholder': 'Тип поста',
            }),
        }