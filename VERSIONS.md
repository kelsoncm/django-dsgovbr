# Histórico de Versões

## 5.2.2

### Melhorias na Interface Administrativa

- **Interface do Admin**: Refatoração completa dos templates do Django Admin com Design System GovBR
  - Reorganização do template base (`base.html`) com melhorias estruturais
  - Melhorias na listagem de aplicações (`app_list.html`) com melhor organização visual
  - Aprimoramento do formulário de alteração (`change_form.html`) com layout mais intuitivo
  - Otimização da linha de submissão (`submit_line.html`) com botões mais visíveis
  - Ajustes no fieldset (`includes/fieldset.html`) para melhor apresentação de campos
  - Isolamento de cada aplicação em seu próprio menu-folder para melhor navegação
  - Adição de home ao menu principal
  - Correção: rodapé agora é exibido corretamente no final da tela
  - Correção: campos só são apresentados como erro quando realmente possuem erro

### Novos Recursos

- **Favicons**: Implementação completa do sistema de favicons do GovBR
  - Adição de favicon padrão do GovBR (favicon.ico atualizado)
  - Inclusão de apple-touch-icon.png
  - Adição de favicons em múltiplos tamanhos (16x16, 32x32)
  - Inclusão de mstile-144x144.png para Windows
  - Adição de safari-pinned-tab.svg
  - Criação de site.webmanifest para PWA
  - Template dedicado para favicons (`dsgovbr/favicon.html`)

- **Assets GovBR**: Novos recursos visuais
  - Adição de logo GovBR em PNG e SVG (`vendors/serpro/govbr.png` e `govbr.svg`)

- **Estilos CSS**: Novo arquivo `dsgovbr.css` com estilos customizados
  - Ajustes de altura mínima do container
  - Estilos para mensagens de erro e feedback
  - Formatação de botões secundários pequenos
  - Estilização de fieldsets com br-card
  - Melhorias tipográficas em legendas e descrições

- **Template Tags**: Criação de template tags customizadas (`templatetags/dsgovbr.py`)
  - Novas tags para facilitar o uso do Design System

- **Context Processors**: Melhorias nos processadores de contexto
  - Leitura e disponibilização das settings para o tema
  - Melhor integração com configurações do Django

### Melhorias de Integração

- **Import/Export**: Ajustes no template de importação (`import_export/import.html`)
- **Simple History**: Otimização do template de histórico de objetos
- **Versionamento**: Numeração de versão agora indica a versão do Django suportada

### Atualizações de Dependências (GitHub Actions)

- Atualização do actions/checkout de v4 para v6
- Atualização do actions/setup-python de v5 para v6
- Atualização do actions/download-artifact de v4 para v7
- Atualização do actions/upload-artifact de v4 para v6
- Ajustes nos workflows de publicação no PyPI e testes

### Estatísticas

- **26 arquivos alterados**: 298 inserções(+), 227 deleções(-)
- **9 novos arquivos** adicionados (incluindo favicons, logos e templates)
- **Refatoração significativa** nos templates do Django Admin para melhor usabilidade
