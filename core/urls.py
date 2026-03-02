from django.urls import path
from .views import login_view, dashboard, logout_view, search_bar_view

urlpatterns = [
    path('accounts/login/', login_view, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('cadastroItem/', search_bar_view, name='cadastro_de_produtos'),
    path('logout/', logout_view, name='logout'),
]