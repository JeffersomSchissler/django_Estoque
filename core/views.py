from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Produto
from .models import Fornecedor
from .forms import ProdutoForm
from .forms import CategoryForms
from .models import Categoria
from .ai_services import process_user_message

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
    total_produtos = Produto.objects.count()
    total_categorias = Categoria.objects.count()
    total_fornecedores = Fornecedor.objects.count()

    context = {
        'total_produtos': total_produtos,
        'total_categorias': total_categorias,
        'total_fornecedores': total_fornecedores
        }
    return render(request, 'dashboard.html', context)

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


@login_required
def listar_categorias(request):
    categoria = Categoria.objects.all()

    return render(request, 'tela_cadastro_de_categoria.html', {'category': categoria})

@login_required
def adicionar_novo_produto(request):
    return render(request, 'cadastrar_novo_produto.html')

def cadastrar_nova_categoria(request):
    return render(request, 'cadastro_categoria.html')

@login_required
def cadastrar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cadastro_de_produtos')  # altere para a URL da lista de produtos
    else:
        form = ProdutoForm()

    categorias = Categoria.objects.all()  # para preencher o select de categoria
    return render(request, 'cadastrar_novo_produto.html', {'form': form, 'categorias': categorias})

@login_required
def cadastrar_categoria(request):
    if request.method == 'POST':
        form = CategoryForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_categorias')  
    else:
        form = CategoryForms()

    return render(request, 'cadastro_categoria.html', {'form': form})

    


@login_required
@csrf_exempt
def ai_assistant_view(request):
    """
    View para processar mensagens do assistente de IA
    """
    if request.method == 'POST':
        import json
        try:
            data = json.loads(request.body)
            message = data.get('message', '')
            
            if not message:
                return JsonResponse({'error': 'Mensagem vazia'}, status=400)
            
            # Processa a mensagem usando o serviço de IA
            response = process_user_message(message)
            
            return JsonResponse({'response': response})
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    # Se for GET, retorna a página do assistente
    return render(request, 'ai_assistant.html')

