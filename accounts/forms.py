from django.contrib.auth.forms import UserCreationForm
from django import forms
from datetime import date
from django.utils.dateparse import parse_date
from .models import CustomUser  # Model personalizat

class CustomUserCreationForm(UserCreationForm):
    telefon = forms.CharField(required=True)
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('telefon', 'adresa', 'data_nasterii', 'profesie', 'experienta')
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('Acest nume de utilizator este deja inregistrat')
        return username
    
    def clean_telefon(self):
        phone = self.cleaned_data.get('telefon')
        if not phone.startswith('07'):
            raise forms.ValidationError('Numarul de telefon trebuie sa înceapa cu 07')
        return phone
        
    def clean_data_nasterii(self):
        data_nasterii = self.cleaned_data.get('data_nasterii')
        varsta = (date.today() - data_nasterii).days // 365
        print(varsta)
        if varsta < 18 :
            raise forms.ValidationError('Varsa minima este de 18 ani')
        return data_nasterii
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
    

class CustomLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Nume utilizator'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Parola'}
        )
    )
    remember_me = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput()
    )

from django.contrib.auth.forms import PasswordChangeForm

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        field_settings = {
            'old_password': 'Parola actuală',
            'new_password1': 'Parola nouă',
            'new_password2': 'Confirmă parola nouă'
        }
        
        for field_name, placeholder in field_settings.items():
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control',
                'placeholder': placeholder
            })