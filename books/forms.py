from django import forms
from django.core.exceptions import ValidationError

from .models import Book, Review


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'status']  # поле user исключено
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'genre': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title'].strip()
        if len(title) < 2:
            raise ValidationError('Название должно содержать минимум 2 символа.')
        return title


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating', 'quote']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'quote': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 1 or rating > 5:
            raise ValidationError('Оценка должна быть строго от 1 до 5.')
        return rating

    def clean_text(self):
        text = self.cleaned_data['text'].strip()
        if not text:
            raise ValidationError('Текст рецензии не может быть пустым.')
        return text