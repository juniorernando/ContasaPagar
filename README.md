# 💸 Sistema de Contas a Pagar

Sistema desenvolvido em Python com foco em **código limpo**, **orientação a objetos** e aplicação dos **princípios SOLID**. Utiliza infraestrutura da AWS com **Terraform**, **Lambda**, **SNS**, **SQS** e banco de dados **Aurora**.

---

## ✅ **PROJETO IMPLEMENTADO E FUNCIONAL**

✅ **Orientação a Objetos** - Classes bem definidas com encapsulamento e composição  
✅ **Princípios SOLID** - SRP, OCP, DIP aplicados nos serviços e repositórios  
✅ **Repository Pattern** - Interfaces abstratas e implementações concretas  
✅ **Service Layer** - Lógica de negócio separada da persistência  
✅ **Schemas Pydantic** - Validação de dados robusta  
✅ **Handlers Lambda** - API Gateway, SQS e SNS implementados  
✅ **Infraestrutura Terraform** - Aurora, VPC, Lambda, SQS, SNS, API Gateway  
✅ **Testes Unitários** - Pytest com mocks para validação  
✅ **Logs Estruturados** - Loguru configurado para desenvolvimento e produção  

---

## 🎯 Objetivo

Criar um sistema escalável e bem estruturado para **gerenciamento de contas a pagar**, utilizando boas práticas de engenharia de software e serviços em nuvem.

---

## 🧱 Funcionalidades

### 👥 Cadastro de Fornecedores
- Nome, CNPJ/CPF, E-mail, Telefone
- Validação de documento único
- Operações CRUD completas

### 💰 Cadastro de Contas a Pagar
- Descrição, Valor, Data de vencimento
- Status: `Aberta`, `Paga`, `Atrasada`
- Fornecedor vinculado
- Validações de negócio

### 📋 Listagens e Filtros
- Filtrar contas por status, fornecedor, data
- Contas vencendo nos próximos X dias
- Atualização automática de status

### ✅ Ações
- Marcar conta como paga
- Processamento assíncrono via SQS
- Notificações via SNS

---

## 🧠 Conceitos Aplicados

- **Programação Orientada a Objetos (POO)**
- **Princípios SOLID**
- **Repository Pattern**
- **Service Layer Pattern**
- **Event-driven Architecture**
- **Clean Code e Clean Architecture**
- **Dependency Injection**
- **Test-Driven Development (TDD)**

---

## ⚙️ Tecnologias Utilizadas

| Categoria          | Ferramenta/Serviço                |
|--------------------|-----------------------------------|
| Linguagem          | Python 3.10+                      |
| Infraestrutura     | Terraform                         |
| Banco de Dados     | Amazon Aurora (PostgreSQL)        |
| Backend Serverless | AWS Lambda                        |
| Mensageria         | AWS SQS, AWS SNS                  |
| API                | AWS API Gateway                   |
| ORM                | SQLAlchemy                        |
| Validação          | Pydantic                          |
| Testes             | Pytest, pytest-mock               |
| Observabilidade    | AWS CloudWatch, Loguru            |

---

## 🗂 Estrutura de Pastas

```
contas_a_pagar/
├── app/
│   ├── models/          # Entidades: Conta, Fornecedor
│   ├── services/        # Regras de negócio
│   ├── repositories/    # Acesso ao banco
│   ├── handlers/        # Lambdas SNS, SQS, API Gateway
│   ├── schemas/         # DTOs e validações
│   └── utils/           # Utilitários AWS, Logger, Database
│
├── infrastructure/
│   └── terraform/       # Código de infraestrutura AWS
│       ├── main.tf      # Recursos principais
│       ├── variables.tf # Variáveis
│       └── outputs.tf   # Outputs
│
├── tests/               # Testes unitários
│   ├── test_services.py
│   ├── test_schemas.py
│   └── test_handlers.py
│
├── requirements.txt     # Dependências
├── main.py             # Execução local
├── DEPLOY.md           # Guia de deploy
└── README.md
```

---

## 🚀 Como Executar

### 1. **Instalação Local**
```bash
# Clonar o repositório
git clone <repo-url>
cd ContasaPagar

# Instalar dependências
pip install -r requirements.txt

# Executar sistema localmente (sem banco)
python main.py
```

### 2. **Executar Testes**
```bash
# Todos os testes
pytest

# Testes específicos
pytest tests/test_services.py -v
pytest tests/test_schemas.py -v
pytest tests/test_handlers.py -v
```

### 3. **Deploy na AWS**
```bash
# Consultar guia detalhado
cat DEPLOY.md
```

---

## 📊 Resultados dos Testes

```
tests/test_schemas.py::TestContaSchema::test_conta_create_valida PASSED
tests/test_schemas.py::TestContaSchema::test_conta_create_valor_negativo PASSED
tests/test_schemas.py::TestContaSchema::test_conta_update_parcial PASSED
tests/test_schemas.py::TestFornecedorSchema::test_fornecedor_create_valido PASSED
tests/test_schemas.py::TestFornecedorSchema::test_fornecedor_email_invalido PASSED
tests/test_schemas.py::TestFornecedorSchema::test_fornecedor_update_parcial PASSED

tests/test_services.py::TestServicoConta::test_criar_conta_sucesso PASSED
tests/test_services.py::TestServicoConta::test_criar_conta_fornecedor_inexistente PASSED
tests/test_services.py::TestServicoConta::test_criar_conta_valor_negativo PASSED
tests/test_services.py::TestServicoConta::test_marcar_como_paga PASSED
tests/test_services.py::TestServicoFornecedor::test_criar_fornecedor_sucesso PASSED
tests/test_services.py::TestServicoFornecedor::test_criar_fornecedor_documento_duplicado PASSED

tests/test_handlers.py::TestHandlerCreateConta::test_lambda_handler_sucesso PASSED
tests/test_handlers.py::TestHandlerCreateConta::test_lambda_handler_dados_invalidos PASSED

============= 14 TESTES PASSANDO =============
```

---

## 🏗️ Arquitetura AWS

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   API Gateway   │ -> │  Lambda Create  │ -> │   Aurora DB     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   SNS Topics    │ <- │  Lambda Process │ <- │   SQS Queues    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 🛡️ Princípios SOLID Aplicados

### **S**ingle Responsibility Principle
- `Conta` - apenas entidade
- `ServicoConta` - apenas lógica de negócio
- `ContaRepository` - apenas persistência

### **O**pen/Closed Principle
- Interfaces `IRepositorioConta` permitem extensão sem modificação

### **D**ependency Inversion Principle
- Serviços dependem de abstrações (`IRepositorioConta`)
- Injeção de dependência no construtor

---

## 📝 Próximos Passos

- [ ] Implementar autenticação JWT
- [ ] Adicionar cache Redis
- [ ] Métricas customizadas CloudWatch
- [ ] Pipeline CI/CD GitHub Actions
- [ ] Documentação API com OpenAPI
- [ ] Testes de integração
- [ ] Monitoramento com AWS X-Ray

---

## 👨‍💻 Desenvolvido por

**Junior** - Sistema completo de Contas a Pagar seguindo melhores práticas de desenvolvimento.

**Tecnologias**: Python, AWS, Terraform, Docker, Pytest