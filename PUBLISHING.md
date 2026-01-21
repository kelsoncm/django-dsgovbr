# Publishing to PyPI

Este documento descreve como publicar o pacote `django-dsgovbr` no PyPI usando GitHub Actions.

## Configuração Inicial

### 1. Configurar Trusted Publishing no PyPI

O workflow usa o método de "Trusted Publishing" do PyPI, que é mais seguro que usar tokens.

#### Para PyPI (produção):

1. Acesse https://pypi.org/manage/account/publishing/
2. Clique em "Add a new pending publisher"
3. Preencha:
   - **PyPI Project Name**: `django-dsgovbr`
   - **Owner**: seu-usuario-github
   - **Repository name**: django-dsgovbr
   - **Workflow name**: `publish-to-pypi.yml`
   - **Environment name**: `pypi`
4. Clique em "Add"

#### Para TestPyPI (testes):

1. Acesse https://test.pypi.org/manage/account/publishing/
2. Siga os mesmos passos acima, mas com:
   - **Environment name**: `testpypi`

### 2. Configurar Environments no GitHub

1. Vá para Settings → Environments no seu repositório GitHub
2. Crie dois environments:
   - `pypi` - para publicação em produção
   - `testpypi` - para testes

Opcionalmente, adicione "Required reviewers" para o environment `pypi` para exigir aprovação manual antes da publicação.

## Como Publicar

### Método 1: Publicação Automática (Release)

A forma recomendada é criar uma release no GitHub:

1. Atualize a versão no arquivo `pyproject.toml` e `setup.py`
2. Commit e push das mudanças
3. Crie uma tag de versão:
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```
4. Vá para GitHub → Releases → "Create a new release"
5. Selecione a tag criada
6. Preencha as informações da release
7. Clique em "Publish release"

O workflow será acionado automaticamente e publicará o pacote no PyPI.

### Método 2: Publicação Manual

Para testar no TestPyPI ou forçar uma publicação manual:

1. Vá para Actions → "Publish to PyPI" → "Run workflow"
2. Selecione:
   - **Branch**: main (ou a branch desejada)
   - **Deploy target**: 
     - `testpypi` - para testar no Test PyPI
     - `pypi` - para publicar no PyPI oficial
3. Clique em "Run workflow"

## Testando a Publicação

Sempre teste primeiro no TestPyPI:

```bash
# Instalar do TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ django-dsgovbr

# Testar a instalação
python -c "import dsgovbr; print('OK')"
```

## Workflow de Versões

1. **Desenvolvimento**: trabalhe na branch `develop`
2. **Teste**: publique no TestPyPI usando workflow manual
3. **Produção**: crie uma release para publicar no PyPI

## Versionamento Semântico

Use [Semantic Versioning](https://semver.org/):

- **MAJOR**: mudanças incompatíveis na API (v1.0.0 → v2.0.0)
- **MINOR**: novas funcionalidades compatíveis (v1.0.0 → v1.1.0)
- **PATCH**: correções de bugs (v1.0.0 → v1.0.1)

## Checklist Antes de Publicar

- [ ] Atualizar versão em `pyproject.toml`
- [ ] Atualizar versão em `setup.py`
- [ ] Atualizar CHANGELOG.md (se existir)
- [ ] Testar localmente: `python -m build`
- [ ] Verificar o pacote: `twine check dist/*`
- [ ] Testar no TestPyPI primeiro
- [ ] Criar tag de versão no git
- [ ] Criar release no GitHub

## Estrutura de Arquivos

```
django_dsgovbr/
├── .github/
│   ├── workflows/
│   │   ├── publish-to-pypi.yml  # Workflow de publicação
│   │   └── test.yml              # Workflow de testes
│   └── dependabot.yml            # Atualizações automáticas
├── src/
│   └── dsgovbr/                  # Código do pacote
├── MANIFEST.in                   # Arquivos a incluir no pacote
├── pyproject.toml                # Configuração moderna do pacote
├── setup.py                      # Setup tradicional (compatibilidade)
├── README.md                     # Documentação
└── PUBLISHING.md                 # Este arquivo
```

## Solução de Problemas

### Erro: "Project name already exists"
O nome já está em uso no PyPI. Escolha outro nome ou contate o proprietário.

### Erro: "Trusted publishing not configured"
Configure o Trusted Publishing no PyPI seguindo a seção "Configuração Inicial".

### Erro no build
Verifique:
- `MANIFEST.in` inclui todos os arquivos necessários
- `pyproject.toml` está correto
- Não há erros de sintaxe no código

### Testando localmente

```bash
# Instalar dependências de build
pip install build twine

# Build
python -m build

# Verificar
twine check dist/*

# Testar instalação local
pip install dist/django_dsgovbr-0.1.0-py3-none-any.whl
```

## Referências

- [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/)
- [GitHub Actions for PyPI](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/)
- [Python Packaging Guide](https://packaging.python.org/)
