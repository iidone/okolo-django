from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.decorators import login_required
from .forms import AdForm
from django.shortcuts import get_object_or_404
from .models import CATEGORY_CHOICES, CONDITION_CHOICES, Ad, ExchangeProposal
from django.core.paginator import Paginator
from django.db.models import Q


def index(request, category=None):
    ads = Ad.objects.all().order_by('-created_at')
    
    search_query = request.GET.get('q')
    if search_query:
        ads = ads.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(contact_info__icontains=search_query)
        )
    
    if category:
        ads = ads.filter(category=category)
    elif request.GET.get('category'):
        ads = ads.filter(category=request.GET.get('category'))
    
    if request.GET.get('condition'):
        ads = ads.filter(condition=request.GET.get('condition'))
    
    paginator = Paginator(ads, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    current_category_name = None
    if category:
        current_category_name = dict(CATEGORY_CHOICES).get(category)
    
    context = {
        'ads': page_obj,
        'current_category': current_category_name,
        'category_slug': category,
        'CATEGORY_CHOICES': CATEGORY_CHOICES,
        'CONDITION_CHOICES': CONDITION_CHOICES,
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'main/index.html', context)
    
    return render(request, 'main/index.html', context)

def registration(request):

    context = {
        'errors': {},
        'form_data': {},
        'global_error': None
    }

    if request.method == 'POST':

        form_data = {
            'username': request.POST.get('username'),
            'email': request.POST.get('email'),
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
        }
        context['form_data'] = form_data
        
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        errors = {}
        

        if not form_data['username']:
            errors['username'] = 'Обязательное поле'
        elif User.objects.filter(username=form_data['username']).exists():
            errors['username'] = 'Имя пользователя занято'
        

        if not form_data['email']:
            errors['email'] = 'Обязательное поле'
        else:
            try:
                validate_email(form_data['email'])
                if User.objects.filter(email=form_data['email']).exists():
                    errors['email'] = 'Email уже используется'
            except ValidationError:
                errors['email'] = 'Некорректный email'
        

        if not password1:
            errors['password1'] = 'Обязательное поле'
        elif len(password1) < 8:
            errors['password1'] = 'Пароль слишком короткий (минимум 8 символов)'
        
        if not password2:
            errors['password2'] = 'Обязательное поле'
        elif password1 != password2:
            errors['password2'] = 'Пароли не совпадают'
        

        if not errors:
            try:
                user = User.objects.create_user(
                    username=form_data['username'],
                    email=form_data['email'],
                    password=password1,
                    first_name=form_data['first_name'],
                    last_name=form_data['last_name']
                )
                
                login(request, user)
                return redirect('home')
                
            except Exception as e:
                context['global_error'] = f'Ошибка регистрации: {str(e)}'
        else:
            context['errors'] = errors
    context['hide_search'] = True
    return render(request, 'main/registration.html', context)

def autorization(request):
    context = {
        'errors': {},
        'form_data': {},
        'global_error': None
    }

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password1')
        
        form_data = {
            'email': email,
        }
        context['form_data'] = form_data
        
        errors = {}
        
        if not email:
            errors['email'] = 'Обязательное поле'
        else:
            try:
                validate_email(email)
            except ValidationError:
                errors['email'] = 'Некорректный email'
        
        if not password:
            errors['password1'] = 'Обязательное поле'
        
        if not errors:
            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    errors['password1'] = 'Неверный пароль'
                    context['errors'] = errors
            except User.DoesNotExist:
                errors['email'] = 'Пользователь с таким email не найден'
                context['errors'] = errors
        else:
            context['errors'] = errors

    context['hide_search'] = True
    return render(request, 'main/autorization.html', context)


def logout(request):
    auth_logout(request)
    return redirect('home')

@login_required
def profile(request):
    sort_by = request.GET.get('sort', 'all')
    
    incoming = ExchangeProposal.objects.filter(ad_receiver__user=request.user)
    outgoing = ExchangeProposal.objects.filter(ad_sender__user=request.user)
    
    if sort_by == 'incoming':
        proposals = incoming.order_by('-created_at')
    elif sort_by == 'outgoing':
        proposals = outgoing.order_by('-created_at')
    elif sort_by == 'pending':
        proposals = incoming.filter(status='pending').order_by('-created_at')
    elif sort_by == 'accepted':
        proposals = incoming.filter(status='accepted').order_by('-created_at')
    elif sort_by == 'rejected':
        proposals = incoming.filter(status='rejected').order_by('-created_at')
    else:
        proposals = (incoming | outgoing).order_by('-created_at')
    
    context = {
        'user': request.user,
        'user_ads': Ad.objects.filter(user=request.user).order_by('-created_at'),
        'proposals': proposals,
        'current_sort': sort_by,
        'hide_search': True
    }
    return render(request, 'main/profile.html', context)

@login_required
def update_proposal(request, proposal_id, status):
    proposal = get_object_or_404(ExchangeProposal, id=proposal_id, ad_receiver__user=request.user)
    
    if status in ['accepted', 'rejected', 'pending']:
        proposal.status = status
        proposal.save()
        messages.success(request, f'Предложение {proposal.get_status_display().lower()}')
    
    return redirect('profile')

@login_required
def add_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('current_ad', ad_id=ad.id)
    else:
        form = AdForm()
    
    context = {
        'form': form,
        'editing': False,
        'hide_search': True
    }
    return render(request, 'main/add_ad.html', context)

from .forms import ExchangeProposalForm

def current_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    user_ads = None
    selected_ad_id = None
    
    if request.method == 'POST' and 'exchange_proposal' in request.POST:
        form = ExchangeProposalForm(request.POST, user=request.user, receiver_ad=ad)
        selected_ad_id = request.POST.get('selected_ad')
        
        if selected_ad_id and form.is_valid():
            try:
                sender_ad = Ad.objects.get(id=selected_ad_id, user=request.user)
                exchange = form.save(commit=False)
                exchange.ad_sender = sender_ad
                exchange.ad_receiver = ad
                exchange.status = 'pending'
                exchange.save()
                messages.success(request, 'Предложение обмена отправлено!')
                return redirect('current_ad', ad_id=ad.id)
            except Ad.DoesNotExist:
                messages.error(request, 'Выберите ваше объявление для обмена')
        else:
            messages.error(request, 'Заполните все поля')
    else:
        form = ExchangeProposalForm(user=request.user, receiver_ad=ad)
        if request.user.is_authenticated:
            user_ads = Ad.objects.filter(user=request.user).exclude(id=ad.id)
    
    return render(request, 'main/current_ad.html', {
        'ad': ad,
        'hide_search': True,
        'exchange_form': form if request.user.is_authenticated else None,
        'user_ads': user_ads,
        'selected_ad_id': selected_ad_id
    })

@login_required
def edit_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)

    if ad.user != request.user:
        return redirect('current_ad', ad_id=ad.id)
    
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('current_ad', ad_id=ad.id)
    else:
        form = AdForm(instance=ad)
    
    context = {
        'form': form,
        'ad': ad,
        'editing': True,
        'hide_search': True
    }
    return render(request, 'main/add_ad.html', context)

@login_required
def delete_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    
    if ad.user != request.user:
        return redirect('current_ad', ad_id=ad.id)
    
    if request.method == 'POST':
        ad.delete()
        return redirect('home')
    
    return redirect('current_ad', ad_id=ad.id)

@login_required
def exchange_proposals(request):
    received = ExchangeProposal.objects.filter(ad_receiver__user=request.user)
    sent = ExchangeProposal.objects.filter(ad_sender__user=request.user)
    
    return render(request, 'main/exchange_proposals.html', {
        'received_proposals': received,
        'sent_proposals': sent
    })