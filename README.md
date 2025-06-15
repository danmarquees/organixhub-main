# 🌱 OrganyxHub Marketplace

Projeto de desenvolvimento de um **Marketplace de produtos sustentáveis e de impacto social**, com o objetivo de conectar **consumidores conscientes** a **pequenos produtores**, **empreendedores sociais** e **organizações de impacto positivo**.

---

## 🚀 Visão Geral

O **OrganyxHub** é uma plataforma web desenvolvida em **Django**, com foco em:

* Comércio de produtos sustentáveis
* Rastreabilidade de produtos
* Cadastro de usuários e produtores
* Gestão de pedidos e entregas
* Integração futura com meios de pagamento online (ex.: PayPal)

---

## 🧱 Estrutura do Projeto

**Principais Apps Django:**

| App      | Função Principal                           |
| -------- | ------------------------------------------ |
| cadastro | Cadastro de usuários, produtores, clientes |
| produtos | Listagem e gestão de produtos              |
| rastreio | Rastreabilidade dos pedidos                |
| users    | Gestão de autenticação de usuários         |

---

## ⚙️ Tecnologias Utilizadas

* **Backend:** Django 4.x
* **Banco de Dados:** PostgreSQL (pode ser alterado para outros durante desenvolvimento)
* **Front-end:** Templates Django + HTML/CSS + JS (Plano de migração futura para React ou similar)
* **Gerenciamento de Pacotes:** Pip + Virtualenv
* **Outros:** Django Admin, ORM nativo, Migrations Django

---

## 💻 Como Rodar Localmente

### Pré-requisitos:

* Python 3.10+
* PostgreSQL (ou SQLite para testes rápidos)
* Git

### Passo a passo:

```bash
# 1. Clone o repositório
git clone https://github.com/danmarquees/organixhub-main.git
cd organixhub-main

# 2. Crie o ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente (Exemplo no arquivo .env.example)

# 5. Rode as migrações do banco de dados
python manage.py migrate

# 6. Crie um superusuário (admin)
python manage.py createsuperuser

# 7. Rode o servidor de desenvolvimento
python manage.py runserver
```

---

## 📂 Estrutura de Pastas (Exemplo)

```
organixhub-main/
├── cadastro/
├── produtos/
├── rastreio/
├── users/
├── organixhub_main/
├── static/
├── templates/
├── manage.py
├── requirements.txt
└── .env.example
```

---

## 🧪 Testes Automatizados

*(Funcionalidade a ser implementada em breve)*

Futuramente, os testes serão organizados por app dentro de pastas `tests/`. Exemplo de como rodar:

```bash
python manage.py test
```

---

## 🐳 Docker (Em breve)

Planejamos criar um ambiente de desenvolvimento containerizado para facilitar o deploy.

---

## ✅ Roadmap Futuro

* [x] Estrutura inicial de apps
* [x] Cadastro de produtos e usuários
* [ ] Implementação de testes automatizados
* [ ] Configuração de Docker
* [ ] Integração com serviços de pagamento
* [ ] CI/CD via GitHub Actions
* [ ] Front-end com Tailwind ou React

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License**.

---

## 🙋‍♂️ Contato

Desenvolvido por **Danilo Marques**
LinkedIn: [https://www.linkedin.com/in/danmarquesdev/](https://www.linkedin.com/in/danmarquesdev/)

---

## ⭐ Se achar útil, dê uma estrela no repositório!
