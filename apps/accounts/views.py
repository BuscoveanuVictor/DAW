from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomLoginForm
from .models import CustomUser

from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from .forms import CustomPasswordChangeForm

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from django.core.mail import mail_admins
from django.core.cache import cache
from datetime import datetime
import logging
logger = logging.getLogger('django')

def index_view(request):
    return render(request, 'accounts/index.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            logger.info(f"Încercare de înregistrare pentru email: {form.cleaned_data['email']}")
            message = validate_email_view(request,form)
            return redirect(reverse('status_email', kwargs={'message': message}))
    else:
        logger.debug("Formular de înregistrare accesat")
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})

def validate_email_view(request,form):
    # Form.save(commit=False) intoarce un obiect de tipul User
    # (adica formularul de tipul CustomUserCreationForm) care fost
    # completat, dar care nu e salvat in baza de date
    
    try:
        user = form.save(commit=False) 
        user.cod = user.generate_confirmation_code()
        # Il salvam in baza de date cu tot cu codul de confirmare
        # si odata ce e salvat, trimitem email-ul de confirmare 
        user.save()
        logger.info(f"User salvat in baza de date cu codul de confirmare: {user.cod}")

        context = {
            'user': user,
            # Trimitem link-ul de confirmare in email la adresa de mail
            # link care contine codul de confirmare si care face referire
            # la functia confirma_mail 
            'confirmation_link': f"{request.scheme}://{request.get_host()}/accounts/confirm-email/{user.cod}/"
        }
    
        email_html = render_to_string('accounts/email_confirmation.html', context)
        send_mail(
        'Confirmare cont',
        'Please confirm your email',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=email_html,
            fail_silently=False,
        )
        #messages.success(request, 'Te rugam sa-ti confirmi adresa de email!')
        message = f'Un email de confirmare a fost trimis la adresa {user.email}!'
    except Exception as e:
        logger.error(f"Eroare la înregistrarea utilizatorului: {str(e)}")
        html_message = f"""
        <h1 style="color: red;">Eroare la înregistrarea utilizatorului</h1>
        <p style="background-color: red; color: white; padding: 10px;">
            {str(e)}
        </p>
        """
        mail_admins(
            subject="Eroare la înregistrarea utilizatorului",
            message=f"S-a produs urmatoarea eroare: {str(e)}",
            html_message=html_message
        )
        message = f'S-a produs o eroare la trimiterea email-ului'

    return message

# Pagina pe care sunt redirectionat de link-ul de confirmare din email
def confirm_mail_view(request, code):
    try:
        # Cautam in baza de date userul cu codul de confirmare
        user = CustomUser.objects.get(cod=code)
        # Ii setam email-ul confirmat
        user.email_confirmat = True
        # Salvam userul cu email-ul confirmat in baza de date
        user.save()  
        message = 'Email-ul tau a fost confirmat cu succes!'
        # messages.success(request, 'Email-ul tau a fost confirmat cu succes!')
    except CustomUser.DoesNotExist:
        #messages.error(request, 'Cod de confirmare invalid!')
        message = 'S-a produs o eroare: Cod de confirmare invalid!'

    return redirect(reverse('status_email', kwargs={'message': message}))


# Pagina de status dupa ce trimitem email-ul de confirmare
# adica s-a trimis email-ul de confirmare, s-a produs o eroare
# sau un mesaj de succes ca user-ul a fost adaugat in baza de date
def status_email_view(request, message):
    return render(request,'accounts/status_email.html',{'message': message})

def login_view(request):
    if request.method == 'POST':
        # Creeam un formular de tipul CustomLoginForm cu datele din request
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            # Luam datele din formularul validat
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']
            # Si autentificam userul
            user = authenticate(username=username, password=password)
            if user:
                # Daca user-ul a fost autentificat il logam
                login(request, user)
                # Daca user-ul a ales sa se logheze si sa aiba sesiunea
                # setam expirarea sesiunii la 24 de ore
                if remember_me:
                    request.session.set_expiry(24*60*60)  #24 de ore in secunde
                else:
                    request.session.set_expiry(0)
                return redirect('profile')
            # Daca user-ul nu se poate autentifica se afiseaza un mesaj de eroare
            else:
                logger.error(f"Eroare la autentificarea utilizatorului: {username}")
                messages.error(request, 'Username-ul sau parola sunt incorecte')
                suspicious_login_attempts_view(request, username)
                
    else:
        form = CustomLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def suspicious_login_attempts_view(request, username):
    logger.critical(f"Tentative de login cu username-ul {username} de la adresa IP: {request.META.get('REMOTE_ADDR')}")
    # Daca user-ul a incercat sa se logheze de mai multe ori cu acelasi username
    # se trimite un email la admini
    ip = request.META.get('REMOTE_ADDR')
    cache_key = f'login_attempts_{ip}_{username}'
    attempts = cache.get(cache_key, [])
    current_time = datetime.now()
    
    # Adăugăm încercarea curentă
    attempts.append(current_time)
    # Păstrăm doar încercările din ultimele 2 minute
    attempts = [t for t in attempts if (current_time - t).total_seconds() <= 120]
    cache.set(cache_key, attempts, 120)  # Expirare după 2 minute
                
    if len(attempts) >= 3:
        mail_admins(
            subject=f"Tentative de login cu username-ul {username}",
            message=f"Tentative de login cu username-ul {username} de la adresa IP: {request.META.get('REMOTE_ADDR')}",
            html_message=f'<p>Tentative de login cu username-ul "{username}" de la adresa IP: {request.META.get("REMOTE_ADDR")}</p>'
        )

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Te-ai deconectat cu succes!')
    return redirect('index')  

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

@login_required 
def password_change_view(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.warning(request, 'Parola a fost schimbată cu succes!')
            return redirect('profile')
        else:
            messages.error(request, 'Te rog corectează erorile de mai jos.')
            logger.error(f"Eroare la schimbarea parolei: {form.errors}")
    else:
        form = CustomPasswordChangeForm(user=request.user)
    
    return render(request, 'accounts/change_password.html', {'form': form})


