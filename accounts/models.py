from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, RegexValidator, EmailValidator

class CustomUser(AbstractUser):
    # Implicit clasa User are urm atribute(laboratorul6):
    # username, first_name, last_name, email, password
    # s_staff: indică dacă utilizatorul poate accesa interfața de administrare.
    # is_superuser: indică dacă utilizatorul are toate permisiunile.
    # is_active: indică dacă contul este activ.

    # Timp și metadate:
    # last_login: ultima autentificare.
    # date_joined: data creării contului.

    telefon = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Numarul de telefon trebuie sa contina numai cifre'"
            )
        ],
        help_text="Numarul de telefon trebuie sa fie in format: '07x xxx xxx'"
    )
    adresa = models.TextField(max_length=255)
    data_nasterii = models.DateField(
        help_text="Data nasterii trebuie sa fie in formatul an.luna.zi"
    )
    profesie = models.CharField(max_length=100)
    experienta = models.IntegerField(
        validators=[
            MinValueValidator(0)
        ],
        help_text="Experienta este exprimata in ani si trebuie sa fie un numar intreg pozitiv"
    )
