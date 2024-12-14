from django.contrib.auth.forms import UserCreationForm
from django import forms
from datetime import date
from .models import CustomUser 
from django.core.mail import mail_admins

class CustomUserCreationForm(UserCreationForm):
    telefon = forms.CharField(required=True)
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 
                  'telefon', 'adresa', 'data_nasterii', 'profesie', 'experienta',
                  'password1', 'password2')
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username.lower() == 'admin':
            print("ceva")
            mail_admins(
                subject="Cineva incearca sa ne preia site-ul",
                message=f"Cineva a încercat să se înregistreze cu username-ul 'admin'.",
                html_message =
                f"""
                    <h1 style="color: red;">Cineva încearcă să ne preia site-ul</h1>
                    <p>Cineva a încercat să se înregistreze cu username-ul 'admin'.</p>
                    <p>Email-ul folosit: {self.cleaned_data.get('email')}</p>
                """
            )
            raise forms.ValidationError('Acest username nu este permis')

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
            'old_password': 'Parola actuala',
            'new_password1': 'Parola noua',
            'new_password2': 'Confirm parola noua'
        }
        
        for field_name, placeholder in field_settings.items():
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control',
                'placeholder': placeholder
            })