# Django DSGovBR

[![PyPI version](https://badge.fury.io/py/django-dsgovbr.svg)](https://badge.fury.io/py/django-dsgovbr)
[![Python Versions](https://img.shields.io/pypi/pyversions/django-dsgovbr.svg)](https://pypi.org/project/django-dsgovbr/)
[![Django Versions](https://img.shields.io/badge/django-5.2-blue.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Pacote Django para integração com o [Design System do Governo Federal Brasileiro (DS Gov.BR)](https://www.gov.br/ds/home).

## 📋 Sobre

O **django-dsgovbr** facilita a implementação do Design System oficial do Governo Federal em projetos Django, inclusive no Django Admin, garantindo conformidade visual e de usabilidade com os padrões estabelecidos pelo gov.br.

### 🎨 Design System Gov.BR

O [DS Gov.BR](https://www.gov.br/ds/home) é o design system oficial do Governo Federal Brasileiro, criado para padronizar a experiência do usuário em todos os portais e sistemas governamentais.

**Links Oficiais:**
- 🏠 [Site Oficial](https://www.gov.br/ds/home)
- 📚 [Documentação](https://www.gov.br/ds/fundamentos-visuais/visao-geral)
- 🎨 [Fundamentos Visuais](https://www.gov.br/ds/fundamentos-visuais/introducao)
- 🧩 [Componentes](https://www.gov.br/ds/componentes/overview)
- 📐 [Padrões](https://www.gov.br/ds/padroes/introducao)
- 💾 [Download dos Assets](https://www.gov.br/ds/recursos/downloads)

### ✨ Recursos Visuais do DS Gov.BR

O Design System inclui:

#### Componentes Principais
- **Formulários**: Inputs, selects, checkboxes, radio buttons estilizados
- **Botões**: Primários, secundários, terciários com estados hover/active/disabled
- **Mensagens**: Alertas, notificações e mensagens de sistema
- **Navegação**: Headers, breadcrumbs, menus e abas
- **Tabelas**: Grades de dados responsivas e acessíveis
- **Cards**: Cartões informativos e de conteúdo
- **Modal**: Diálogos e janelas modais
- **Paginação**: Controles de navegação entre páginas

#### Características Visuais
- 🎨 **Paleta de Cores Oficial**: Azul Gov.BR (#071D41), cores de status e feedbacks
- 📱 **Design Responsivo**: Mobile-first, adaptável a todos os dispositivos
- ♿ **Acessibilidade**: WCAG 2.1 nível AA, suporte a leitores de tela
- 🔤 **Tipografia Rawline**: Fonte oficial do governo federal
- 📐 **Grid System**: Sistema de grid consistente (12 colunas)
- 🖼️ **Ícones**: Biblioteca Font Awesome com ícones customizados

#### Visual do DS Gov.BR

```
┌─────────────────────────────────────────────┐
│  🏛️  GOVERNO FEDERAL                        │
│  ═══════════════════════════════════        │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │  🔵 Botão Primário                  │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │  ⚪ Botão Secundário                │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  ℹ️  Mensagem Informativa                   │
│  ✓  Mensagem de Sucesso                     │
│  ⚠️  Mensagem de Aviso                      │
│  ✕  Mensagem de Erro                        │
│                                             │
└─────────────────────────────────────────────┘
```

> **Nota**: Para capturas de tela reais dos componentes, visite a [página de componentes oficial](https://www.gov.br/ds/componentes/overview) do DS Gov.BR.

## 🚀 Instalação

### Via PyPI (Recomendado)

```bash
pip install django-dsgovbr
```

## ⚙️ Configuração

### 1. Adicione ao INSTALLED_APPS

```python
# settings.py

INSTALLED_APPS = [
    # ... outras apps
    'dsgovbr',
    # ... suas apps
]
```

### 2. Configure os Context Processors (Opcional)

```python
# settings.py

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # ... outros context processors
                'dsgovbr.context_processors.dsgovbr',
            ],
        },
    },
]
```

### 3. Colete os Arquivos Estáticos

```bash
python manage.py collectstatic
```

## 📖 Uso

### Templates Base

Use os templates base do DSGovBR nos seus templates Django:

```django
{% extends "admin/base.html" %}
{% load static %}

{% block title %}Minha Página Gov.BR{% endblock %}

{% block content %}
<div class="br-container">
    <h1>Bem-vindo ao Sistema</h1>
    
    <!-- Botão Primário -->
    <button class="br-button primary" type="button">
        Ação Principal
    </button>
    
    <!-- Mensagem de Sucesso -->
    <div class="br-message success">
        <div class="icon">
            <i class="fas fa-check-circle"></i>
        </div>
        <div class="content">
            Operação realizada com sucesso!
        </div>
    </div>
    
    <!-- Card -->
    <div class="br-card">
        <div class="card-header">
            <h3>Título do Card</h3>
        </div>
        <div class="card-content">
            <p>Conteúdo do card seguindo o padrão Gov.BR</p>
        </div>
    </div>
</div>
{% endblock %}
```

### Formulários Django

Os formulários Django automaticamente usam os estilos do DS Gov.BR:

```python
# forms.py
from django import forms

class MeuFormulario(forms.Form):
    nome = forms.CharField(
        label="Nome Completo",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'br-input',
            'placeholder': 'Digite seu nome'
        })
    )
    
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={
            'class': 'br-input',
            'placeholder': 'seuemail@exemplo.gov.br'
        })
    )
    
    mensagem = forms.CharField(
        label="Mensagem",
        widget=forms.Textarea(attrs={
            'class': 'br-textarea',
            'rows': 5
        })
    )
```

### Admin do Django

O pacote fornece templates customizados para o Django Admin com visual Gov.BR:

```python
# admin.py
from django.contrib import admin
from .models import MeuModelo

@admin.register(MeuModelo)
class MeuModeloAdmin(admin.ModelAdmin):
    list_display = ['nome', 'status', 'data_criacao']
    list_filter = ['status']
    search_fields = ['nome']
```

## 🎨 Componentes Disponíveis

### Classes CSS Principais

```html
<!-- Botões -->
<button class="br-button primary">Primário</button>
<button class="br-button secondary">Secundário</button>
<button class="br-button tertiary">Terciário</button>

<!-- Mensagens -->
<div class="br-message info">Informação</div>
<div class="br-message success">Sucesso</div>
<div class="br-message warning">Aviso</div>
<div class="br-message error">Erro</div>

<!-- Cards -->
<div class="br-card">
    <div class="card-header">Cabeçalho</div>
    <div class="card-content">Conteúdo</div>
    <div class="card-footer">Rodapé</div>
</div>

<!-- Inputs -->
<input type="text" class="br-input" placeholder="Digite aqui...">
<textarea class="br-textarea"></textarea>
<select class="br-select">
    <option>Opção 1</option>
</select>
```

## 🔧 Desenvolvimento

### Requisitos

- Python 3.10+
- Django 5.2+

### Setup para Desenvolvimento

```bash
# Clone o repositório
git clone https://github.com/kelsoncm/django-dsgovbr.git
cd django-dsgovbr

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale as dependências de desenvolvimento
pip install -e ".[dev]"

# Execute os testes
python -m pytest
```

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👥 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📧 Contato

**Kelson da Costa Medeiros**
- Email: kelsoncm@gmail.com
- GitHub: [@kelsoncm](https://github.com/kelsoncm)

## 🔗 Links Úteis

- [Design System Gov.BR - Site Oficial](https://www.gov.br/ds/home)
- [DS Gov.BR - Componentes](https://www.gov.br/ds/componentes/overview)
- [DS Gov.BR - GitHub](https://github.com/govbr-ds)
- [Documentação Django](https://docs.djangoproject.com/)
- [Acessibilidade Gov.BR](https://www.gov.br/governodigital/pt-br/acessibilidade-digital)

## 📊 Status do Projeto

- ✅ Integração básica com Django Admin
- ✅ Templates base Gov.BR
- ✅ Componentes CSS principais
- ✅ Suporte a formulários Django
- 🔄 Em desenvolvimento: Widgets customizados
- 📋 Planejado: Componentes JavaScript interativos

---

**Desenvolvido com ❤️ para o ecossistema Gov.BR**
