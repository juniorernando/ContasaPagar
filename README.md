# 💸 Sistema de Contas a Pagar

Sistema desenvolvido em Python com foco em **código limpo**, **orientação a objetos** e aplicação dos **princípios SOLID**. Utiliza infraestrutura da AWS com **Terraform**, **Lambda**, **SNS**, **SQS** e banco de dados **Aurora**.

---

## 🎯 Objetivo

Criar um sistema escalável e bem estruturado para **gerenciamento de contas a pagar**, utilizando boas práticas de engenharia de software e serviços em nuvem.

---

## 🧱 Funcionalidades

### 👥 Cadastro de Fornecedores
- Nome
- CNPJ/CPF
- E-mail
- Telefone

### 💰 Cadastro de Contas a Pagar
- Descrição
- Valor
- Data de vencimento
- Status: `Aberta`, `Paga`, `Atrasada`
- Fornecedor vinculado

### 📋 Listagens e Filtros
- Filtrar contas por status
- Filtrar contas por fornecedor
- Filtrar contas por data

### ✅ Ações
- Marcar conta como paga

---

## 🧠 Conceitos Aplicados

- Programação Orientada a Objetos (POO)
- Princípios SOLID
- Repository Pattern
- Service Layer
- Event-driven Architecture com AWS
- Clean Code e Clean Architecture

---

## ⚙️ Tecnologias Utilizadas

| Categoria          | Ferramenta/Serviço                |
|--------------------|-----------------------------------|
| Linguagem          | Python 3.10+                      |
| Infraestrutura     | Terraform                         |
| Banco de Dados     | Amazon Aurora (PostgreSQL)        |
| Backend Serverless | AWS Lambda                        |
| Mensageria         | AWS SQS, AWS SNS                  |
| ORM                | SQLAlchemy                        |
| Validação          | Pydantic                          |
| Testes             | Pytest, pytest-mock               |
| Observabilidade    | AWS CloudWatch, Loguru            |

---

## 🗂 Estrutura de Pastas

contas_a_pagar/
├── app/
│ ├── models/ # Entidades: Conta, Fornecedor
│ ├── services/ # Regras de negócio
│ ├── repositories/ # Acesso ao banco
│ ├── handlers/ # Lambdas SNS, SQS, API Gateway
│ ├── schemas/ # DTOs e validações
│ └── utils/ # Utilitários
│
├── infrastructure/
│ └── terraform/ # Código de infraestrutura AWS
│ ├── main.tf
│ ├── variables.tf
│ └── outputs.tf
│
├── tests/ # Testes unitários e integração
├── requirements.txt # Dependências
├── main.py # Execução local
└── README.md