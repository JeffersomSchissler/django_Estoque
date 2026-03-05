"""
Serviço de IA para o Assistente Virtual do Sistema de Estoque
"""
import os
import json
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Produto, Categoria, Fornecedor, MovimentoEstoque
from django.contrib.auth import get_user_model

User = get_user_model()

# Configuração da API da OpenAI
# Defina sua API key como variável de ambiente ou insira diretamente (não recomendado para produção)
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')


class EstoqueAssistant:
    """
    Assistente virtual para gestão de estoque usando regras eIA
    """
    
    def __init__(self):
        self.context = """
Você é um assistente virtual especializado em gestão de estoque e inventario.
Seu papel é ajudar usuarios a gerenciar produtos, verificar estoque, e obter informações sobre o sistema.

Funcionalidades que voce pode ajudar:
1. Listar produtos - mostrar todos os produtos cadastrados
2. Buscar produto por nome - encontrar produtos especificos
3. Listar produtos por categoria - filtrar por categoria
4. Verificar estoque baixo - mostrar produtos com pouca quantidade
5. Ver historico de movimentos - mostrar entradas e saidas de estoque
6. Listar fornecedores - mostrar fornecedores cadastrados
7. Mostrar dashboard - estatisticas gerais do sistema
8. Criar alertas - notificar sobre produtos que precisam de reposicao

Sempre seja prestativo, amigavel e forneca informacoes claras e objetivas.
Quando askedo sobre dados, sempre forneca numeros especificos e detalhados.
"""
    
    def process_message(self, message):
        """Processa a mensagem do usuário e retorna uma resposta"""
        message = message.lower().strip()
        
        # Intent: Produtos com estoque baixo
        if any(palavra in message for palavra in ['estoque baixo', 'pouco estoque', 'falta produto', 'reposição', 'repor']):
            return self.get_estoque_baixo()
        
        # Intent: Listar todos os produtos
        elif any(palavra in message for palavra in ['listar produtos', 'todos os produtos', 'produtos cadastrados', 'mostrar produtos']):
            return self.get_todos_produtos()
        
        # Intent: Buscar produto por nome
        elif 'buscar' in message or 'procurar' in message or 'pesquisar' in message:
            return self.buscar_produto(message)
        
        # Intent: Produtos por categoria
        elif 'categoria' in message:
            return self.get_produtos_por_categoria(message)
        
        # Intent: Histórico de movimentos
        elif 'movimento' in message or 'historico' in message or 'entrada' in message or 'saída' in message:
            return self.get_historico_movimentos(message)
        
        # Intent: Fornecedores
        elif 'fornecedor' in message:
            return self.get_fornecedores()
        
        # Intent: Dashboard / Estatísticas
        elif 'dashboard' in message or 'estatística' in message or 'resumo' in message or 'relatório' in message:
            return self.get_dashboard()
        
        # Intent: Criar alerta
        elif 'alerta' in message:
            return self.criar_alerta(message)
        
        # Intent: Ajuda
        elif 'ajuda' in message or 'help' in message or 'o que você faz' in message:
            return self.get_ajuda()
        
        # Intent: Sabor
        elif 'oi' in message or 'olá' in message or 'hello' in message or 'ola' in message:
            return "Olá! Sou o assistente virtual do seu sistema de estoque. Posso ajudá-lo a:\n\n📦 Listar produtos\n🔍 Buscar produtos específicos\n⚠️ Verificar estoque baixo\n📊 Ver estatísticas do sistema\n📦 Listar fornecedores\n\nComo posso ajudá-lo hoje?"
        
        # Fallback
        else:
            return self.get_ajuda()
    
    def get_estoque_baixo(self, limite=10):
        """Retorna produtos com estoque baixo"""
        produtos = Produto.objects.filter(Inventory_quantity__lte=limite).order_by('Inventory_quantity')
        
        if not produtos.exists():
            return f"✅ Não há produtos com estoque abaixo de {limite} unidades!"
        
        resposta = f"⚠️ **Produtos com Estoque Baixo (≤{limite} unidades):**\n\n"
        
        for p in produtos:
            resposta += f"• **{p.name}** - {p.Inventory_quantity} unidades\n"
            resposta += f"  Categoria: {p.category.name} | Preço: R$ {p.unit_price}\n\n"
        
        return resposta
    
    def get_todos_produtos(self):
        """Retorna todos os produtos cadastrados"""
        produtos = Produto.objects.all().order_by('name')[:20]
        
        if not produtos.exists():
            return "Nenhum produto cadastrado no sistema!"
        
        resposta = "📦 **Produtos Cadastrados:**\n\n"
        
        for p in produtos:
            resposta += f"• **{p.name}**\n"
            resposta += f"  Estoque: {p.Inventory_quantity} | Preço: R$ {p.unit_price}\n"
            resposta += f"  Categoria: {p.category.name}\n\n"
        
        total = Produto.objects.count()
        if total > 20:
            resposta += f"... e mais {total - 20} produtos (mostrando os primeiros 20)"
        
        return resposta
    
    def buscar_produto(self, message):
        """Busca produtos por nome"""
        # Extrai o termo de busca da mensagem
        palavras = message.replace('buscar', '').replace('procurar', '').replace('pesquisar', '').strip()
        
        if not palavras:
            return "Por favor, informe o nome do produto que deseja buscar. Ex: 'buscar notebook'"
        
        produtos = Produto.objects.filter(name__icontains=palavras)
        
        if not produtos.exists():
            return f"❌ Nenhum produto encontrado com '{palavras}' no nome."
        
        resposta = f"🔍 **Resultados da busca por '{palavras}':**\n\n"
        
        for p in produtos:
            resposta += f"• **{p.name}**\n"
            resposta += f"  Estoque: {p.Inventory_quantity} | Preço: R$ {p.unit_price}\n"
            resposta += f"  Categoria: {p.category.name}\n\n"
        
        return resposta
    
    def get_produtos_por_categoria(self, message):
        """Retorna produtos de uma categoria específica"""
        # Tenta extrair o nome da categoria
        categoria_nome = message.replace('categoria', '').strip()
        
        if not categoria_nome:
            # Lista todas as categorias disponíveis
            categorias = Categoria.objects.all()
            if not categorias.exists():
                return "Nenhuma categoria cadastrada!"
            
            resposta = "📂 **Categorias Disponíveis:**\n\n"
            for c in categorias:
                resposta += f"• {c.name}\n"
            resposta += "\nPara ver produtos de uma categoria, digite: 'produtos da categoria [nome]'"
            return resposta
        
        try:
            categoria = Categoria.objects.get(name__icontains=categoria_nome)
            produtos = Produto.objects.filter(category=categoria)
            
            resposta = f"📂 **Produtos da categoria '{categoria.name}':**\n\n"
            
            for p in produtos:
                resposta += f"• **{p.name}** - {p.Inventory_quantity} unidades\n"
            
            return resposta
            
        except Categoria.DoesNotExist:
            return f"Categoria '{categoria_nome}' não encontrada. Digite 'categoria' para ver as disponíveis."
    
    def get_historico_movimentos(self, message, limite=10):
        """Retorna histórico de movimentos de estoque"""
        movimentos = MovimentoEstoque.objects.all().order_by('-movement_date')[:limite]
        
        if not movimentos.exists():
            return "Nenhum movimento de estoque registrado!"
        
        resposta = "📜 **Histórico de Movimentos:**\n\n"
        
        for m in movimentos:
            tipo = "➕ Entrada" if m.movement_type == 'I' else "➖ Saída"
            resposta += f"{tipo} - {m.product.name}\n"
            resposta += f"  Quantidade: {m.amount} | Data: {m.movement_date}\n"
            resposta += f"  Responsável: {m.responsible_user.username}\n\n"
        
        return resposta
    
    def get_fornecedores(self):
        """Retorna lista de fornecedores"""
        fornecedores = Fornecedor.objects.all()
        
        if not fornecedores.exists():
            return "Nenhum fornecedor cadastrado!"
        
        resposta = "🏢 **Fornecedores Cadastrados:**\n\n"
        
        for f in fornecedores:
            resposta += f"• **{f.name}**\n"
            resposta += f"  Email: {f.email} | Tel: {f.phone}\n"
            resposta += f"  Endereço: {f.address}\n\n"
        
        return resposta
    
    def get_dashboard(self):
        """Retorna estatísticas do sistema"""
        total_produtos = Produto.objects.count()
        total_categorias = Categoria.objects.count()
        total_fornecedores = Fornecedor.objects.count()
        
        # Produtos com estoque baixo
        estoque_baixo = Produto.objects.filter(Inventory_quantity__lte=10).count()
        
        # Total em estoque (valor)
        total_valor = sum(p.unit_price * p.Inventory_quantity for p in Produto.objects.all())
        
        # Movimentos de hoje
        hoje = timezone.now().date()
        movimentos_hoje = MovimentoEstoque.objects.filter(movement_date__date=hoje).count()
        
        resposta = "📊 **Dashboard - Resumo do Sistema:**\n\n"
        resposta += f"📦 **Total de Produtos:** {total_produtos}\n"
        resposta += f"📂 **Categorias:** {total_categorias}\n"
        resposta += f"🏢 **Fornecedores:** {total_fornecedores}\n"
        resposta += f"⚠️ **Estoque Baixo (≤10):** {estoque_baixo}\n"
        resposta += f"💰 **Valor Total em Estoque:** R$ {total_valor:,.2f}\n"
        resposta += f"📅 **Movimentos Hoje:** {movimentos_hoje}\n"
        
        return resposta
    
    def criar_alerta(self, message):
        """Cria um alerta de reposição"""
        # Procura por produtos com estoque baixo e cria um alerta
        produtos_baixo = Produto.objects.filter(Inventory_quantity__lte=10)
        
        if not produtos_baixo.exists():
            return "✅ Não há produtos com estoque baixo no momento!"
        
        resposta = "🔔 **Alerta de Reposição:**\n\n"
        resposta += "Os seguintes produtos precisam de reposição:\n\n"
        
        for p in produtos_baixo:
            resposta += f"⚠️ **{p.name}** - Apenas {p.Inventory_quantity} unidades\n"
        
        resposta += "\n💡 Recomendo fazer um pedido de reposição em breve!"
        
        return resposta
    
    def get_ajuda(self):
        """Retorna mensagem de ajuda"""
        return """
🤖 **Olá! Sou o Assistente Virtual do Sistema de Estoque!**

Posso ajudá-lo com as seguintes comandos:

📦 **Produtos:**
• "listar produtos" - Mostrar todos os produtos
• "buscar [nome]" - Buscar produto específico
• "produtos da categoria [nome]" - Filtrar por categoria

⚠️ **Estoque:**
• "estoque baixo" - Ver produtos com pouca quantidade
• "alerta" - Criar alerta de reposição

📊 **Informações:**
• "dashboard" - Ver estatísticas do sistema
• "fornecedores" - Listar fornecedores
• "movimentos" - Ver histórico de entradas/saídas

❓ "ajuda" - Mostrar esta mensagem

Como posso ajudá-lo?
"""


def process_user_message(message):
    """Função principal para processar mensagens do usuário"""
    assistant = EstoqueAssistant()
    return assistant.process_message(message)

