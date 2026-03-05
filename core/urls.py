from django.urls import path
from .views import login_view, dashboard, logout_view, search_bar_view, ai_assistant_view, cadastrar_produto

urlpatterns = [
    path('accounts/login/', login_view, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('cadastroItem/', search_bar_view, name='cadastro_de_produtos'),
    path('produto/novo/', cadastrar_produto, name='cadastrar_produto'),
    path('logout/', logout_view, name='logout'),
    path('ai-assistant/', ai_assistant_view, name='ai_assistant'),
]
