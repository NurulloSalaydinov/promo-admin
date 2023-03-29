from django import forms
from .models import Category, Promo, Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        labels = {
            "title": "Kategoriya nomi",
            "points": "Bal",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'A1'})
        self.fields['points'].widget.attrs.update({'class': 'form-control', 'placeholder': '10'})
        self.fields['title'].error_messages.update({
            'required': 'Kategoriya nomini kiriting!',
            'max_value': 'Kategoriya nomi qisqaroq bolishi kerak'
        })
        self.fields['points'].error_messages.update({
            'required': 'Balni togri kiriting!',
            'invalid': 'Iltimos raqamni togri kiriting!'
        })


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        labels = {
            "title": "Sovg'a nomi",
            "req_points": "Bal",
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Konditsioner'})
        self.fields['req_points'].widget.attrs.update({'class': 'form-control', 'placeholder': '20'})
        self.fields['title'].error_messages.update({
           'required': 'Sovga nomini kiriting!',
           'max_value': 'Sovga nomi qisqaroq bolishi kerak'
        })
        self.fields['req_points'].error_messages.update({
           'required': 'Balni togri kiriting!',
            'invalid': 'Iltimos raqamni togri kiriting!'
        })


class PromoForm(forms.ModelForm):
    class Meta:
        model = Promo
        fields = '__all__'

