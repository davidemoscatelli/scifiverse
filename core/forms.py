from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'content']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'class': 'w-full bg-[#1e1e1e] border border-gray-700 rounded-md p-3 text-white focus:border-[#829b93] focus:ring-1 focus:ring-[#829b93] outline-none transition',
                'step': '0.1', 'min': '0', 'max': '10', 'placeholder': 'es. 8.5'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full bg-[#1e1e1e] border border-gray-700 rounded-md p-3 text-white focus:border-[#829b93] focus:ring-1 focus:ring-[#829b93] outline-none transition',
                'rows': 4, 'placeholder': 'Scrivi la tua recensione...'
            }),
        }