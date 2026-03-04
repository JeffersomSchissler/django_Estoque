from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from .models import Produto

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuário ou senha inválidos')
            return redirect('login')
        
    return render(request, 'login.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')  


@login_required
def product_view(request):
    product = Produto.objects.all()

    return render(request, 'cadastro_produtos.html',
        {
        'product': product
            })


@login_required
def search_bar_view(request):
    query = request.GET.get('q')

    if query:
        product = Produto.objects.filter(name__icontains=query)
    else:
        product = Produto.objects.all()

    # Verifica se a requisição veio do HTMX
    is_htmx = request.headers.get('HX-Request') == 'true'

    if is_htmx:
        # Retorna apenas o fragmento da tabela (sem header/base)
        return render(request, 'carrega_produtos.html', {'product': product})
    
    # Requisição normal - retorna página completa
    return render(request, 'cadastro_produtos.html', {'product': product})

