# 📋 Tarefas Pendentes - Sistema de Estoque

## ✅ Concluídos

### Layout e Frontend
- [x] Layout base com tema escuro (dark theme)
- [x] Menu lateral com navegação
- [x] Página de Dashboard
- [x] Página de Lista de Produtos (cadastro_produtos.html)
- [x] Página de Cadastro de Novo Produto (layout pronto)
- [x] Ícones de editar e excluir na tabela de produtos
- [x] Assistente Virtual com IA (chatbot)
- [x] Página de Login

### Backend Básico
- [x] Autenticação de usuários
- [x] Listagem de produtos
- [x] Busca de produtos com HTMX
- [x] View para processar mensagens da IA

---

## 🔴 Pendentes (Backlog)

### 1. Cadastro de Produtos (Backend)
- [x] Criar view para salvar novo produto
- [ ] Formatar/preencher categorias no select
- [ ] Formatar/preencher fornecedores no select
- [ ] Validações de formulário
- [ ] Mensagens de sucesso/erro

### 2. Edição de Produtos
- [ ] Criar página de edição de produto
- [ ] Criar view para atualizar produto
- [ ] Preencher formulário com dados existentes

### 3. Exclusão de Produtos
- [ ] Criar view para excluir produto
- [ ] Confirmação de exclusão
- [ ] Soft delete ou exclusão permanente

### 4. Categorias
- [ ] Página de listagem de categorias
- [ ] Página de cadastro de categorias
- [ ] Edição de categorias
- [ ] Exclusão de categorias

### 5. Fornecedores
- [ ] Página de listagem de fornecedores
- [ ] Página de cadastro de fornecedores
- [ ] Edição de fornecedores
- [ ] Exclusão de fornecedores

### 6. Movimentos de Estoque
- [ ] Página de histórico de movimentos
- [ ] Registrar entrada de estoque
- [ ] Registrar saída de estoque
- [ ] Atualizar quantidade do produto automaticamente

### 7. Dashboard
- [ ] Mostrar total de produtos
- [ ] Mostrar produtos com estoque baixo
- [ ] Mostrar movimentos recentes
- [ ] Gráficos de entrada/saída

### 8. Segurança e Permissões
- [ ] Controle de permissões por usuário
- [ ] Proteção de rotas (apenas admin)
- [ ] Logs de auditoria

### 9. Relatórios
- [ ] Exportar produtos em CSV
- [ ] Exportar produtos em PDF
- [ ] Relatório de estoque baixo
- [ ] Relatório de movimentos por período

### 10. Melhorias na IA
- [ ] Integrar com OpenAI API (ChatGPT)
- [ ] Mais intents/actions
- [ ] Notificações automáticas de estoque baixo

---

## 📝 Prioridades Sugeridas

### Alta Prioridade
1. Finalizar backend de cadastro de produtos
2. Criar edição e exclusão de produtos
3. Implementar movimentos de estoque

### Média Prioridade
4. Completar dashboard com estatísticas
5. CRUD de Categorias e Fornecedores
6. Relatórios básicos

### Baixa Prioridade
7. Gráficos e visualizações
8. Integração com API externa
9. Exportação de relatórios

---

## 📁 Arquivos Principais

| Arquivo | Descrição |
|---------|-----------|
| `core/views.py` | Views do sistema |
| `core/models.py` | Modelos do banco de dados |
| `core/urls.py` | Rotas URLs |
| `core/ai_services.py` | Serviço de IA |
| `core/templates/` | Templates HTML |
| `core/static/css/` | Arquivos CSS |

