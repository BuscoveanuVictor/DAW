from django import forms
import re
import datetime
from myapp.models import Instrument
from decimal import Decimal

from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import JsonResponse


# Lab 5 task 1
class FilterForm(forms.Form):
    model = forms.CharField(required=False, label='Model')
    min_price = forms.DecimalField(required=False, label='Preț minim')
    max_price = forms.DecimalField(required=False, label='Preț maxim')
    min_rating = forms.DecimalField(required=False, label='Rating minim')
    category = forms.CharField(required=False, label='Categorie')
    description = forms.CharField(required=False, label='Descriere')

# Lab 5 task 2
class ContactForm(forms.Form):
    nume = forms.CharField(max_length=100, label='Nume')
    prenume = forms.CharField(max_length=100, label='Prenume')
    data_nasterii = forms.DateField(label='Data nasterii', error_messages={
            'invalid': 'Date trebuie sa fie in formatul an.luna.zi'
        }
    )
    email = forms.EmailField(label='Email', error_messages={
            'invalid': 'Introduceți o adresă de email validă.'
        }
    )
    confirm_email = forms.EmailField(label='Confirmare Email',required=True)
    tip_mesaj = forms.ChoiceField(label='Tip mesaj', 
    choices=[('1', 'Reclamatie'), ('2', 'Intrebare'), ('3', 'Review'),
             ('4', 'Cerere' ),('5', 'Programare')])
    subject = forms.CharField(max_length=100, label='Subiect', required=True)
    minim_zile_asteptare = forms.IntegerField(label='Minim zile asteptare')
    mesaj = forms.CharField(widget=forms.Textarea, label='Mesaj', required=True)


    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        confirm_email = cleaned_data.get("confirm_email")
        if email and confirm_email and email != confirm_email:
            raise forms.ValidationError("Adresele de email nu coincid.")

        # VALIDARE VARSTA
        data_nastere = cleaned_data.get("data_nasterii")
        print(data_nastere)
        if data_nastere:  # verificăm dacă data există
            varsta = (datetime.date.today() - data_nastere).days // 365
            if varsta < 18:
                raise forms.ValidationError("Trebuie sa ai minim 18 ani.")
        else:
            raise forms.ValidationError("Data nașterii este obligatorie.")

        # VALIDARE MESAJ
        mesaj = cleaned_data.get("mesaj")
        re.sub(r'\W+', ' ', mesaj)
        lista_cuvinte =  mesaj.split();
        if len(lista_cuvinte) < 5:
            raise forms.ValidationError("Trebuie sa ai minim 5 cuvinte.")
        elif len(lista_cuvinte) > 100:
            raise forms.ValidationError("Trebuie sa ai maxim 100 de cuvinte.")
        
        for cuvant in lista_cuvinte:
            if not cuvant.isalnum():
                raise forms.ValidationError("Cuvintele trebuie sa fie alfanumerice.")
            if cuvant.find("http") != -1:
                raise forms.ValidationError("Cuvintele nu trebuie sa contin linkuri.")
            if cuvant[-1] != cleaned_data.get("nume"):
                raise forms.ValidationError("Mesajul trebuie sa se termine cu semnatura dumneavoastra.")
            
        print(lista_cuvinte)
        
        return cleaned_data
    
# Lab 5 task 3
class InstrumentForm(forms.ModelForm):
  
    discount_percentage = forms.IntegerField(
        label='Procentaj reducere',
        help_text='Introduceti un numar intre 0 si 100',
        error_messages={
            'required': 'Acest camp este obligatoriu',
            'invalid': 'Va rugam introduceti un numar intreg'
        }
    )
    
    cost_productie= forms.DecimalField(
        label='Cost de productie',
        error_messages={
            'required': 'Costul de productie este obligatoriu',
            'invalid': 'Introduceti o valoare numerica valida'
        }
    )

    class Meta:
        model = Instrument
        fields = ['model', 'category', 'description']
        labels = {
            'model': 'Modelul instrumentului',
            'category': 'Categoria',
            'description': 'Descriere'
        }
        error_messages = {
            'model': {
                'required': 'Modelul este obligatoriu',
                'max_length': 'Numele modelului este prea lung'
            },
            'category': {
                'required': 'Categoria este obligatorie'
            },
            'description': {
                'required': 'Descrierea este obligatorie'
            }
        }

    def clean_discount_percentage(self):
        discount = self.cleaned_data.get('discount_percentage')
        if discount < 0 or discount > 80:
            raise forms.ValidationError('Reducerea trebuie să fie între 0 și 80%')
        return discount

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description.split()) < 10:
            raise forms.ValidationError('Descrierea trebuie să contina cel putin 10 cuvinte')
        return description

    def clean_model(self):
        model = self.cleaned_data.get('model')
        if not any(char.isdigit() for char in model):
            raise forms.ValidationError('Modelul trebuie sa contina cel putin o cifra')
        return model

    def clean(self):
        cleaned_data = super().clean()
        cost_productie = cleaned_data.get('cost_productie')
        discount = cleaned_data.get('discount_percentage')

        if cost_productie and discount:
            if cost_productie > 1000 and discount > 50:
                raise forms.ValidationError(
                    'Nu se poate aplica o reducere mai mare de 50% pentru produse cu cost mai mare de 1000'
                )
        return cleaned_data

    def save(self, commit=True):
        # din lab : commit=False pentru a prelua datele din campurile aditionale si pentru a fi procesate
        # adica instanta este un fel de copie a formularului care poate fi salvat in baza de date
        instance = super().save(commit=False)
        
        cost_productie = self.cleaned_data.get('cost_productie')
        discount = self.cleaned_data.get('discount_percentage')
        
        # produsele aduc un profit de 30%
        pret_baza = float(cost_productie) * 1.3
        instance.price = pret_baza * (1 - discount / 100)
        
        if cost_productie > 1000:
            instance.rating = 4.5
        else:
            instance.rating = 4.0

        if commit:
            instance.save()
        return instance