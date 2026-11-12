# Orientações para agentes de IA — JobLink

## Contexto
JobLink é um projeto acadêmico em Python 3.12 e Django 5.2 para conectar candidatos e empresas. O idioma da aplicação é português brasileiro.

## Regras obrigatórias
- Antes de alterar, leia os arquivos envolvidos e preserve o padrão existente.
- Não remova funcionalidades existentes sem justificar e documentar.
- Não exponha segredos, senhas, tokens ou dados pessoais em código, logs ou commits.
- Não altere migrações já aplicadas; crie novas migrações para mudanças de modelos.
- Toda operação de escrita deve validar permissões e propriedade do registro no servidor.
- Use `select_related`/`prefetch_related` quando apropriado e mantenha paginação.
- Mensagens ao usuário devem usar `django.contrib.messages` e estar em português.
- Templates devem estender `website/modelo.html` e reutilizar `website/form.html` quando adequado.
- Não confie apenas em JavaScript para segurança; valide tudo no Django.
- Execute `python manage.py check` e `python manage.py test website` após mudanças.
- Ao adicionar dependências, atualize `requirements.txt` e explique a necessidade.
- Não execute deploy nem altere recursos remotos sem autorização explícita.

## Estrutura
- `pw2026/`: configurações e URLs do projeto.
- `website/`: modelos, views, forms, filtros, templates e testes.
- `.agents/skills/`: padrões de tarefas para agentes de IA.

## Git
Use a skill `commit-message` para escrever mensagens de commit. Prefira commits pequenos, focados e em português.
