# 📦 Sistema de Gestão de Estoque

## 1. Models (Tabelas)

### 1.1 Produto

| Campo             | Tipo                               | Observações                     |
|------------------|-----------------------------------|---------------------------------|
| id               | AutoField (PK)                    | Chave primária                  |
| nome             | CharField(150)                    | Nome do produto                 |
| descricao        | TextField (opcional)              | Descrição detalhada             |
| quantidade       | IntegerField                       | Quantidade disponível           |
| preco_unitario   | DecimalField (max_digits=10, decimal_places=2) | Preço unitário |
| categoria        | ForeignKey para Categoria          | Categoria do produto            |
| data_criacao     | DateTimeField (auto_now_add=True) | Data de criação                 |
| data_atualizacao | DateTimeField (auto_now=True)     | Última atualização              |

### 1.2 Categoria

| Campo     | Tipo                | Observações           |
|-----------|-------------------|---------------------|
| id        | AutoField (PK)     | Chave primária      |
| nome      | CharField(100)     | Nome da categoria   |
| descricao | TextField (opcional)| Descrição da categoria |

### 1.3 Fornecedor

| Campo         | Tipo           | Observações          |
|---------------|---------------|--------------------|
| id            | AutoField (PK) | Chave primária     |
| nome          | CharField(150) | Nome do fornecedor |
| contato_email | EmailField     | E-mail de contato  |
| telefone      | CharField(20)  | Telefone           |
| endereco      | CharField(200) | Endereço completo  |

### 1.4 MovimentoEstoque

| Campo          | Tipo                        | Observações                       |
|----------------|----------------------------|----------------------------------|
| id             | AutoField (PK)             | Chave primária                   |
| produto        | ForeignKey para Produto    | Produto movimentado              |
| tipo           | CharField (entrada/saida)  | Tipo de movimento                |
| quantidade     | IntegerField               | Quantidade movimentada           |
| data_movimento | DateTimeField (auto_now_add=True) | Data do movimento         |
| responsavel    | ForeignKey para User       | Usuário responsável              |

---

## 2. Plugins / Bibliotecas Recomendadas

- **[Django REST Framework](https://www.django-rest-framework.org/)** – para APIs.
- **django-crispy-forms** – formulários responsivos e bonitos.
- **django-widget-tweaks** – customização de formulários nos templates.
- **django-extensions** – comandos úteis para desenvolvimento.
- **django-allauth** – autenticação avançada.
- **django-guardian** – controle de permissões por objeto.

---

## 3. Páginas / Views

### 3.1 Dashboard
- Visão geral do estoque:
  - Total de produtos
  - Produtos com estoque baixo
  - Movimentos recentes
  - Gráficos de entrada/saída

### 3.2 Lista de Produtos
- Tabela paginada com filtros:
  - Nome, Categoria, Quantidade
- Funcionalidades:
  - Adicionar, Editar, Remover produto

### 3.3 Verificação de Produtos
- Consulta rápida de produtos
- Busca por nome ou QR code/barcode

### 3.4 Movimentos do Estoque
- Histórico de entradas e saídas
- Filtros por:
  - Data
  - Produto
  - Responsável

### 3.5 Cadastro de Fornecedores e Categorias
- CRUD completo
- Gestão de informações complementares

---

## 4. Segurança

- Autenticação via Django `User` ou `django-allauth`
- Controle de permissões:
  - Administradores: CRUD completo
  - Usuários comuns: apenas visualização
- Proteção contra SQL Injection e CSRF
- Logs de movimentações para auditoria

---

## 5. Eficiência para o Usuário

- Interface limpa e responsiva
- Formulários com validação inline
- Busca e filtros rápidos
- Paginação em tabelas grandes
- Alertas visuais para produtos com estoque baixo
- Exportação de relatórios em CSV/PDF

---
