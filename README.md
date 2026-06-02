# PRATICA +

Sistema web de gestão de carreira com login e cadastro de usuários, usando HTML, CSS, JavaScript e Python (Django).

# 🎓 Kappacita - Sistema de Apoio à Decisão Profissional e Gestão de Planos de Carreira Profissional



Este projeto é uma plataforma  de apoio e gestão profissional, com um agente virtual interativo, desenvolvido com páginas de login, cadastro, área de curso, área de profissões e KappaBot (Agente Virtual).



# Imagens

### [Tela de Login]

![Tela de Login](imagens/login.png)

### [Tela de Cadastro]

![Tela de Cadastro](imagens/cadastro.png)

### [Tela Inicial]

![Tela Inicial](imagens/inicio.jpeg)

### [Tela de Cursos]

![Tela Cursos](imagens/cursos.jpeg)

### [Tela de Profissões]

![Tela Profissões](imagens/profissoes.jpeg)

### [Tela de Favoritos]

![Tela Favoritos](imagens/favoritos.jpeg)

### [Tela de Questionário]

![Tela Questionário](imagens/questionario.jpeg)

### [Tela do KappaBot]

![Tela KappaBot](imagens/kappabot.png)



# 🚀 Funcionalidades

- Cadastro e login de usuários
- Página inicial com menu lateral
- Páginas sobre cursos e descrição
- Páginas sobre profissões e descrição
- Interações com o agente virtual KappaBot
- Possibilidade de favoritar ações


# 🧩 Estrutura do Projeto

```text
KAPPACITA/
│
├── categoriascursos/          # Aplicação responsável pelas categorias de cursos
├── categoriasprof/            # Aplicação responsável pelas categorias de professores
├── cursos/                    # Aplicação responsável pelo gerenciamento de ícones dos cursos
├── imagens/                   # Imagens utilizadas no sistema
│
├── kapp/                      # Aplicação principal do projeto
│   │
│   ├── __pycache__/           # Arquivos compilados do Python
│   ├── management/            # Comandos personalizados do Django
│   ├── migrations/            # Migrações do banco de dados
│   │
│   ├── templates/             # Templates HTML do sistema
│   │   ├── socialaccount/
│   │   │   └── signup.html
│   │   ├── artigos.html
│   │   ├── base.html
│   │   ├── cadastrarArea.html
│   │   ├── cadastrarFuncionalidades.html
│   │   ├── configuracoes.html
│   │   ├── cursos.html
│   │   ├── favoritos.html
│   │   ├── header.html
│   │   ├── homepage.html
│   │   ├── idiomas.html
│   │   ├── kappabot.html
│   │   ├── loginArea.html
│   │   ├── loginFuncionalidades.html
│   │   ├── meuprogresso.html
│   │   ├── navbar.html
│   │   ├── notificacoes.html
│   │   ├── privacidade.html
│   │   ├── profissoes.html
│   │   ├── questionario.html
│   │   ├── questionario2.html
│   │   ├── questionario3.html
│   │   ├── questionario4.html
│   │   └── questionario5.html
│   │
│   ├── __init__.py            # Inicialização da aplicação
│   ├── admin.py               # Configuração do painel administrativo
│   ├── apps.py                # Configuração da aplicação
│   ├── context_processors.py  # Contextos globais dos templates
│   ├── models.py              # Modelos do banco de dados
│   ├── signals.py             # Sinais do Django
│   ├── tests.py               # Testes da aplicação
│   ├── urls.py                # Rotas da aplicação
│   └── views.py               # Lógica das páginas
│
├── kappacita/                 # Configurações principais do projeto 
├── media/                     # Arquivos enviados pelos usuários
├── static/                    # Arquivos estáticos (CSS, JS e imagens)
├── venv/                      # Ambiente virtual Python
│
├── .env                       # Variáveis de ambiente
├── .gitignore                 # Arquivos ignorados pelo Git
├── db.sqlite3                 # Banco de dados SQLite
├── manage.py                  # Gerenciador do projeto Django
├── README.md                  # Documentação do projeto
└── requirements.txt           # Dependências do sistema
```



# 🛠️ Tecnologias Utilizadas

- HTML5
- CSS3
- JavaScript (ES6)
- Python (Django)



# ⚙️ Como Executar o Projeto

1. Clone o repositório:

```bash
git clone https://github.com/tcwendell/Kappacita.git
```

2. Acesse a pasta do projeto:

```bash
cd Kappacita
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute as migrações:

```bash
python manage.py migrate
```

5. Inicie o servidor:

```bash
python manage.py runserver
```

6. Acesse no navegador:

```text
http://127.0.0.1:8000/
```


# 👨‍💻 Autor

- [Daniele Oliveira da Cruz](https://github.com/Daniielecruz)
- [Diego Victor Medeiros Marialva](https://github.com/Gokugamerbr1777)
- [Jhennifer dos Santos Pereira](https://github.com/jhenni10)
- [Paulo Henrique Tavares Dias](https://github.com/SeroSp)
- [Tacio Wendell de Andrade Loiola](https://github.com/tcwendell)



# 👩‍🏫 Orientadora

- [Luana Leal](https://github.com/ProfaLuanaLeal)



💼 Projeto desenvolvido para estudos e prática em desenvolvimento web.


