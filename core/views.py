from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Produto, Fornecedor, Categoria
from .forms import ProdutoForm, CategoryForms
from .ai_services import process_user_message
from django.db.models import Count, Sum
from django.core.paginator import Paginator
import json

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
    soma_de_valores_unitarios = Produto.objects.aggregate(total=Sum('unit_price'))['total'] or 0

    #5 produtos com mais estoque kkk
    ordena_produtos_por_quatidade = Produto.objects.order_by('-Inventory_quantity')
    primeiros_registros = ordena_produtos_por_quatidade[:5]

    # Valor total do estoque
    soma_em_estoque = total_produtos + soma_de_valores_unitarios
    
    # Gráfico de produtos por categoria
    produtos_por_categoria = Categoria.objects.annotate(total_produtos=Count('produto'))
    
    # Gráfico de produtos com estoque baixo (ex: < 10 unidades)
    produtos_estoque_baixo = Produto.objects.filter(Inventory_quantity__lt=11)


    context = {
        'total_produtos': total_produtos,
        'total_categorias': total_categorias,
        'total_fornecedores': total_fornecedores,
        'produtos_por_categoria_labels': json.dumps([c.name for c in produtos_por_categoria]),
        'produtos_por_categoria_data': json.dumps([c.total_produtos for c in produtos_por_categoria]),
        'produtos_estoque_baixo_labels': json.dumps([p.name for p in produtos_estoque_baixo]),
        'produtos_estoque_baixo_data': json.dumps([p.Inventory_quantity for p in produtos_estoque_baixo]),
        'total_em_estoque': soma_em_estoque,
        'ordena_registros': json.dumps([produto.Inventory_quantity for produto in primeiros_registros]),
        'primeiros_registros': json.dumps([produto.name for produto in primeiros_registros]),
    }

    return render(request, 'dashboard.html', context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('/accounts/login/') 


class ProdutoUpdateView(UpdateView):
    model = Produto
    fields = ['name', 'unit_price', 'category', 'sku', 'Inventory_quantity']
    template_name = 'editar_produto.html'
    success_url = reverse_lazy('cadastro_de_produtos')

@login_required
def product_view(request):
    product = Produto.objects.all()
    paginator = Paginator(product, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'cadastro_produtos.html',
        {
        'product': page_obj
            })


@login_required
def search_bar_view(request):
    from django.core.paginator import Paginator
    query = request.GET.get('q')
    page_number = request.GET.get('page', 1)

    if query:
        product_qs = Produto.objects.filter(name__icontains=query)
    else:
        product_qs = Produto.objects.all()

    paginator = Paginator(product_qs, 20)
    page_obj = paginator.get_page(page_number)

    # Verifica se a requisição veio do HTMX
    is_htmx = request.headers.get('HX-Request') == 'true'

    context = {'product': page_obj}

    if is_htmx:
        # Retorna apenas o fragmento da tabela + paginação (sem header/base)
        return render(request, 'carrega_produtos.html', context)
    
    # Requisição normal - retorna página completa
    return render(request, 'cadastro_produtos.html', context)


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
            return redirect('cadastro_de_produtos')
    else:
        form = ProdutoForm()

    categorias = Categoria.objects.all() 
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

