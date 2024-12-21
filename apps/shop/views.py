from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from .models import Instrument, Category
from .forms import ContactForm, InstrumentForm, filterForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.models import User
from django.db.models import Count

def index(request):
    return render(request, 'shop/index.html')

# Lab 4 task 2
def instruments_list(request):
    instruments = Instrument.objects.all()
   
    # Filtrara dupa model folosind field__icontains
    model_query = request.GET.get('model')
    if model_query:
        instruments = instruments.filter(model__icontains=model_query)
   
    # Filtrare dupa pret folosing field__gte si field__lte
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        instruments = instruments.filter(price__gte=min_price)
    if max_price:
        instruments = instruments.filter(price__lte=max_price)
   
    min_rating = request.GET.get('min_rating')
    if min_rating:
        instruments = instruments.filter(rating__gte=min_rating)
   
    category = request.GET.get('category')
    if category:
        instruments = instruments.filter(category__icontains=category)
   
    description = request.GET.get('description')
    if description:
        instruments = instruments.filter(description__icontains=description)
    
    items_per_page = 5 
    # daca nu gaseste param page in request, il seteaza pe 1
    # ca atunci cand se incarca pagina sa se afieze un page
    page_number = request.GET.get('page', 1) 
    paginator = Paginator(instruments, items_per_page)

    return render(request, 'shop/list_instruments.html', {'instruments':instruments})


# Adaugare instrument nou folosind un formular
def add_instrument(request):

    if not request.user.has_perm('perm_add_instrument'):
        print("N-ai voie!")
        return render(request, 'aplication/handlers/403.html')
    
    if request.method == 'GET':
        form = InstrumentForm()
    if request.method == 'POST':
        form = InstrumentForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'shop/add_instrument.html', {'form': form})



# Lab 4 task 1
def filter(request):

    """
        Vine pe server o cerere GET sau POST
        GET:
            - se preiau toate instrumentele din baza de date si se afiseaza in pagina
            - se afieaza formularul de filtrare gol
        POST:
            - se preiau toate instrumentele din baza de date
            - se preiau toate valorile din formularul de filtrare
            - se filtreaza instrumentele in functie de valorile din formular
            # in clean_data se afla valorile din formular-ul validat din request adica
            formularul(cu datele lui) daca respecta constrangerile date impuse 
            in clasa din forms vezi Lab 5 task 2
    """
    instruments = Instrument.objects.all()

    if request.method == 'GET':
        filter_form = filterForm()
        return render(request, 'shop/filter.html',{
            'instruments': instruments,
            'filter_form': filter_form
        })
    if request.method == 'POST':
        # Mai jos se filtreaza instrumentele in functie de valorile din formular
        if request.POST.get('model'):
            instruments = instruments.filter(model__icontains=request.POST.get('model'))
        
        if request.POST.get('min_price'):    
            instruments = instruments.filter(price__gte=request.POST.get('min_price'))
            
        if request.POST.get('max_price'):
            instruments = instruments.filter(price__lte=request.POST.get('max_price'))
            
        if request.POST.get('min_rating'):
            instruments = instruments.filter(rating__gte=request.POST.get('min_rating'))
            
        # if request.POST.get('category'):
        #     instruments = instruments.filter(category__exact=request.POST.get('category'))
            
        if request.POST.get('description'):
            instruments = instruments.filter(description__icontains=request.POST.get('description'))

        return JsonResponse({
            'status': 'success',
            'instruments': list(instruments.values())
        }, safe=False)

# Lab 5 task 2
def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'shop/contact.html', {'form': form})




from django.core.mail import send_mass_mail
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Vizualizare, Promotie
from .forms import PromotieForm

TEMPLATE_EMAILS = {
    'chitara': {
        'template': """
        Salut {nume},
        
        Avem o ofertă specială pentru chitare: {discount}% reducere!
        Folosește codul {cod} până la {data_expirare}.
        
        """,
    },
    'pian': {
        'template': """
        Dragă {nume},
        
        Nu rata oferta noastră pentru piane: {discount}% reducere!
        Cod promoțional: {cod}
        Valabil până la: {data_expirare}
        
        """,
    }
}


#@login_required
def adaugare_promotie(request):
    if request.method == 'GET':
        form = PromotieForm()
    if request.method == 'POST':
        form = PromotieForm(request.POST)
        if form.is_valid():
            form.save()
            #trimitere_promotii()
    return render(request, 'shop/adaugare_promotie.html', {'form': form})



def trimitere_promotii():
     
    emails = []
    K = 3  # Minim K vizualizări pentru a primi promoția
    promotii = Promotie.objects.all()

    for promotie in promotii:
        if promotie.categorii not in TEMPLATE_EMAILS:
            continue

        else:       
            for categorie in promotie.categorii:
                # Găsim utilizatorii care au vizualizat categoria de K ori
                utilizatori = User.objects.filter(
                    vizualizare__produs__category=categorie #JOIN vizualizare cu produs si category
                ).annotate(
                    nr_vizualizari=Count('vizualizare')
                ).filter(nr_vizualizari__gte=K).distinct()

            template = TEMPLATE_EMAILS[categorie]['template']
        
            for user in utilizatori:
                email_content = template.format(
                    nume=user.username,
                    discount=promotie.discount,
                    cod=promotie.cod_promotional,
                    data_expirare=promotie.data_expirare.strftime('%d/%m/%Y'),
                )
                
                emails.append((
                    email_content,
                    'noreply@example.com',
                    [user.email]
                ))
                
    if len(emails) > 0:
        send_mass_mail(emails, fail_silently=False)
