from django.db import models

class Furnizor(models.Model):
    nume = models.CharField(max_length=100)
    tara = models.CharField(max_length=100, blank=True, null=True)
    contact = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nume


class Tara(models.Model):
    nume_tara = models.CharField(max_length=100)
    cod_iso = models.CharField(max_length=3)

    def __str__(self):
        return self.nume_tara


class Contract(models.Model):
    TIP_CHOICES = [
        ('Cumpărare', 'Cumpărare'),
        ('Vânzare', 'Vânzare')
    ]
    tip = models.CharField(max_length=20, choices=TIP_CHOICES)
    furnizor = models.ForeignKey(Furnizor, on_delete=models.SET_NULL, null=True, blank=True)
    tara = models.ForeignKey(Tara, on_delete=models.SET_NULL, null=True, blank=True)
    volum_mwh = models.DecimalField(max_digits=10, decimal_places=2)
    pret_mwh = models.DecimalField(max_digits=10, decimal_places=2)
    data_inceput = models.DateField(blank=True, null=True)
    data_sfarsit = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.tip} - {self.volum_mwh} MWh"


class Retea(models.Model):
    TIP_CHOICES = [
        ('Stație Transformare', 'Stație Transformare'),
        ('Linie Înaltă Tensiune', 'Linie Înaltă Tensiune')
    ]
    tip = models.CharField(max_length=50, choices=TIP_CHOICES)
    locatie = models.CharField(max_length=100)
    capacitate_mwh = models.DecimalField(max_digits=10, decimal_places=2)
    stare = models.CharField(max_length=20, choices=[('Operațional', 'Operațional'), ('Neoperațional', 'Neoperațional')])

    def __str__(self):
        return f"{self.tip} - {self.locatie}"


class FluxEnergie(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    retea = models.ForeignKey(Retea, on_delete=models.CASCADE)
    data = models.DateField()
    volum_mwh = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.contract} - {self.retea} - {self.data}"


class PiataEnergie(models.Model):
    nume = models.CharField(max_length=100)
    pret_mwh = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()

    def __str__(self):
        return f"{self.nume} - {self.pret_mwh} RON/MWh"

