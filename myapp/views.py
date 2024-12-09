from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from .models import Instrument, Category
from .forms import ContactForm, InstrumentForm, FilterForm
from django.core.paginator import Paginator
from django.db.models import Q

def index(request):
    return HttpResponse("Hello, World!")    

# Lab 5 task 1
def FormFilerInstr(request):

    """
        Vine pe server o cerere GET sau POST
        GET:
            - se preiau toate instrumentele din baza de date si se afiseaza in pagina
            - se afieaza formularul de filtrare gol
        POST:
            - se preiau toate instrumentele din baza de date
            - se preiau toate valorile din formularul de filtrare
            - se filtreaza instrumentele in functie de valorile din formular
    """
    instruments = Instrument.objects.all()

    if request.method == 'GET':
        filter_form = FilterForm(request.GET)
        return render(request, 'filterInstrWithForm.html',{
            'instruments': instruments,
            'filter_form': filter_form
        })
    if request.method == 'POST':
       
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
            print(form.cleaned_data)
    return render(request, 'Contact.html', {'form': form})


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

    return render(request, 'Filtrare.html', {'instruments':instruments})


def instrument_form(request):
    if request.method == 'GET':
        form = InstrumentForm()
    if request.method == 'POST':
        form = InstrumentForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'instrument_form.html', {'form': form})