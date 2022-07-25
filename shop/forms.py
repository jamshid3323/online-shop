from django import forms
from .models import ProductColorModel


class ColorModelAdminForm(forms.ModelForm):
    code = forms.CharField(widget=forms.TextInput(attrs={'type': 'color'}))

    class Meta:
        model = ProductColorModel
        fields = '__all__'
