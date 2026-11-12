# JobLink

Projeto Django para uma plataforma de empregos inspirada no LinkedIn. Empresas criam perfis e publicam vagas; candidatos criam perfis profissionais, pesquisam oportunidades e enviam candidaturas.

## Requisitos

- Python 3.12+
- Django 5.2
- Dependências em `requirements.txt`

## Instalação

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

O projeto usa SQLite por padrão, facilitando a execução local. Para PostgreSQL, defina a variável de ambiente `DATABASE_URL`.

## Migrações e execução

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/`.

## Funcionalidades

### Candidato
- Criar conta do tipo candidato
- Editar perfil profissional
- Pesquisar e filtrar vagas
- Visualizar detalhes de uma vaga
- Enviar uma candidatura
- Editar/cancelar candidatura
- Acompanhar o status das candidaturas

### Empresa
- Criar conta do tipo empresa
- Editar perfil da empresa
- Publicar, editar e excluir vagas
- Visualizar suas vagas e quantidade de candidaturas
- Consultar candidaturas recebidas

### Sistema
- Login, logout e alteração de senha
- `request.user.is_authenticated` nos templates
- `LoginRequiredMixin` e `GroupRequiredMixin`
- Relacionamento dos registros ao usuário autenticado com `form_valid()` e `get_queryset()`
- `ListView` paginada com `paginate_by`
- QuerySets com filtros e `Count`
- `select_related()` para reduzir consultas repetidas
- Django Debug Toolbar habilitada em desenvolvimento
- Template único `website/form.html` reutilizado por login, cadastro e operações CRUD
- Página "Sobre" com diagrama de caso de uso e diagrama de classes

## Modelos

- `Empresa`
- `Candidato`
- `Vaga`
- `Candidatura`
- `Notificacao` — avisos privados para o usuário, criados quando uma empresa recebe uma nova candidatura.
- `User` (Django)

A relação entre candidato e vaga é representada por `Candidatura`, permitindo guardar mensagem, status e datas.

## Grupos

Ao criar uma conta, o sistema adiciona automaticamente o usuário ao grupo `Empresa` ou `Candidato`. As views de publicação e gestão de vagas são protegidas para empresas; as views de candidatura são protegidas para candidatos.

## Verificações

```powershell
python manage.py check
python manage.py test website
```

## Debug Toolbar

A configuração está em `pw2026/settings.py` e a rota `__debug__/` está em `pw2026/urls.py`. Use a ferramenta para comparar consultas e verificar o efeito de `select_related()`.

## Diagramas

Os diagramas utilizados na página Sobre ficam em:

- `website/static/website/img/diagrama_caso_uso.png`
- `website/static/website/img/diagrama_classes.png`


## Requisitos do 3º trimestre — implementações adicionadas

- Propriedade por usuário: as views de listagem e detalhe de `Empresa` e `Candidato` exigem autenticação, grupo e filtram pelo usuário dono; as operações de criação, edição e exclusão também restringem a propriedade. Por isso, a área de perfis é privada por conta; as vagas ativas continuam públicas para consulta.
- Django Messages: operações de cadastro, edição e exclusão exibem mensagens no template base.
- Django Filter: filtro de vagas por palavra-chave, modalidade, tipo de contrato e cidade.
- Paginação com filtros: a template tag `query_transform` mantém os parâmetros da busca ao navegar entre páginas.
- Complementos jQuery: jQuery Mask (telefone), DataTables (tabela de candidatos) e Bootbox (confirmação de exclusão).
- Recuperação de acesso: recuperação de senha pelo fluxo nativo do Django e recuperação do nome de usuário por e-mail.
- Orientações para agentes: `AGENTS.md`.
- Skills: `.agents/skills/commit-message`, `.agents/skills/django-feature` e `.agents/skills/django-review`.

## E-mail

Em desenvolvimento, as mensagens são exibidas no terminal (`console.EmailBackend`). Em produção, configure variáveis de ambiente `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` e `DEFAULT_FROM_EMAIL`. Nunca salve senha de e-mail no Git.

## Deploy no Google App Engine

O `app.yaml` está preparado para Python 3.12 e Gunicorn, mas o deploy ainda depende de configurar o projeto Google Cloud, faturamento, banco persistente (recomendado PostgreSQL/Cloud SQL), `DJANGO_SECRET_KEY`, `DATABASE_URL`, credenciais SMTP e domínio permitido. O banco SQLite local não é adequado para persistência no App Engine.

Depois de configurar esses recursos e instalar/autorizar o Google Cloud CLI:
```bash
gcloud config set project ID_DO_SEU_PROJETO
python manage.py collectstatic --noinput
gcloud app deploy
gcloud app browse
```
O deploy e a validação na plataforma TestAI precisam ser realizados com as credenciais/conta do proprietário; não foram executados nesta cópia.


## Notificações (5º modelo)
O sistema possui o modelo `Notificacao`, vinculado diretamente ao usuário destinatário. Ao enviar uma candidatura, o JobLink cria uma notificação para a empresa dona da vaga. Cada usuário só pode listar, visualizar e excluir suas próprias notificações; a visualização marca o aviso como lido. A migração `0002_notificacao.py` cria a tabela correspondente.

Após atualizar o código, execute:
```bash
python manage.py migrate
python manage.py check
python manage.py test website
```

## Pendências externas
O código e o `app.yaml` deixam a aplicação preparada para o App Engine, mas a publicação real exige acesso ao projeto Google Cloud, faturamento, banco de dados persistente e segredos de produção. A validação TestAI exige acesso à conta/plataforma e deve ser feita após a publicação. Não é possível gerar um histórico Git verdadeiro sem o repositório e os commits executados pelo proprietário.
