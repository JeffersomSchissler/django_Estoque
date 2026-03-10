from django.urls import path
from .views import login_view, dashboard, logout_view, search_bar_view,ProdutoUpdateView, ai_assistant_view, cadastrar_produto, cadastrar_categoria, listar_categorias

urlpatterns = [
    path('accounts/login/', login_view, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('cadastroItem/', search_bar_view, name='cadastro_de_produtos'),
    path('cadastroCategoria/', listar_categorias, name='listar_categorias'),
    path('editar/<int:pk>/', ProdutoUpdateView, name='editar_produto'),  
    path('produto/novo/', cadastrar_produto, name='cadastrar_produto'),
    path('categoria/novo/', cadastrar_categoria, name='cadastrar_categoria'),
    path('logout/', logout_view, name='logout'),
    path('ai-assistant/', ai_assistant_view, name='ai_assistant'),
]
