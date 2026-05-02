# Vertice RH - MVP Django

Sistema leve e profissional para:
- Site institucional
- Publicacao de vagas
- Candidatura com envio de curriculo
- Painel interno para acompanhar e atualizar status

## 1) Como rodar

No terminal, dentro da pasta do projeto:

```bash
py manage.py runserver
```

Acesse:
- Site: `http://127.0.0.1:8000/`
- Admin Django: `http://127.0.0.1:8000/admin/`
- Painel interno: `http://127.0.0.1:8000/painel/`

## 2) Primeiro acesso (admin)

Crie um usuario administrador:

```bash
py manage.py createsuperuser
```

Depois entre no `/admin` e crie algumas vagas.

## 3) Fluxo completo (exemplo real)

1. **Cadastrar vaga**
   - Login no `/admin`
   - Menu `Jobs > Vagas > Add`
   - Preencha titulo, area, localizacao, descricao e requisitos
   - Marque `Ativa`

2. **Publicar e visualizar no site**
   - Acesse `/vagas/`
   - Clique em uma vaga para ver detalhes

3. **Candidato se aplica**
   - Botao `Candidatar-se`
   - Preenche formulario e anexa curriculo
   - Sistema salva em `Application`

4. **Equipe acompanha no painel**
   - Login em `/contas/login/`
   - Acesse `/painel/`
   - Filtre por status
   - Atualize status (Novo, Triagem, Entrevista, Aprovado, Reprovado)

## 4) Como o projeto esta organizado

- `config/`: configuracoes globais (settings, urls)
- `core/`: paginas institucionais (home, sobre, servicos, contato)
- `jobs/`: modelo e paginas de vagas
- `candidates/`: candidaturas e formulario
- `dashboard/`: painel interno com login
- `templates/`: HTML do projeto
- `static/css/style.css`: estilo leve e profissional

## 5) Conceitos Django em linguagem simples

- **Model**: tabela do banco (ex.: `Job`, `Application`)
- **View**: logica da rota (busca dados e renderiza pagina)
- **Template**: HTML com dados dinâmicos
- **URLconf**: mapa de urls para views
- **Admin**: painel pronto para gestao rapida de dados
- **Migration**: historico de mudancas no banco

## 6) Proximos passos sem pesar

- Dashboard com contadores (novos, triagem, entrevista)
- Campo de observacoes internas por candidato
- Exportacao CSV de candidaturas
- Permissoes por grupo (Admin e Recrutador)

## 7) Deploy de teste no Render

1. Coloque o codigo em um repositorio Git (GitHub ou GitLab) e envie todos os commits.
2. No [Render](https://render.com), crie um **PostgreSQL** (free e suficiente para testes).
3. Crie um **Web Service**, conecte o repositorio e escolha a pasta raiz do projeto Django.
4. **Build Command** (Linux no Render aceita assim):

```bash
chmod +x build.sh && ./build.sh
```

5. **Start Command**:

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

6. No Web Service, em **Environment**, associe o banco Postgres (Render preenche `DATABASE_URL`). Adicione tambem:

| Variavel | Exemplo |
|----------|---------|
| `SECRET_KEY` | Gere uma chave forte (evite usar a de desenvolvimento) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `meu-app.onrender.com` (sem `https://`, pode separar por virgula se tiver mais de um dominio) |
| `CSRF_TRUSTED_ORIGINS` | `https://meu-app.onrender.com` |

7. Deploy. Depois, no Render, abra **Shell** do Web Service e crie um usuario para login:

```bash
python manage.py createsuperuser
```

**Observacoes:**
- Curriculos em `media/` ficam no disco do servico: em reinicios ou novo deploy pode haver perda em plano gratuito; para producao grave use armazenamento em nuvem (S3, R2, etc.).
- Se o navegador mostrar erro de CSRF ao logar no painel, confira `CSRF_TRUSTED_ORIGINS` com `https://` igual a URL real do Render.
