# Deploy do projeto para AWS

## Pré-requisitos

1. **AWS CLI configurado**
   ```bash
   aws configure
   ```

2. **Terraform instalado**
   ```bash
   # Instalar Terraform (Windows)
   choco install terraform
   ```

3. **Python e dependências**
   ```bash
   pip install -r requirements.txt
   ```

## Steps de Deploy

### 1. Preparar Lambda Functions
```bash
# Criar pacotes Lambda
cd app/handlers
zip -r ../../infrastructure/terraform/lambda_create_conta.zip handler_create_conta.py ../
zip -r ../../infrastructure/terraform/lambda_processa_fila.zip handler_processa_fila.py ../
cd ../../
```

### 2. Deploy da Infraestrutura
```bash
cd infrastructure/terraform

# Inicializar Terraform
terraform init

# Verificar plano
terraform plan

# Aplicar mudanças
terraform apply
```

### 3. Configurar Variáveis de Ambiente

Após o deploy, configure as seguintes variáveis com os outputs do Terraform:

```bash
# Copiar exemplo de configuração
cp .env.example .env

# Editar com os valores do Terraform
# AURORA_CLUSTER_ARN=<terraform output aurora_cluster_arn>
# AURORA_SECRET_ARN=<terraform output secret_arn>
# SQS_CONTA_CRIADA_URL=<terraform output sqs_conta_criada_url>
# etc...
```

### 4. Testar API

```bash
# Criar uma conta via API Gateway
curl -X POST https://your-api-id.execute-api.us-east-1.amazonaws.com/prod/contas \
  -H "Content-Type: application/json" \
  -d '{
    "descricao": "Conta teste",
    "valor": 100.50,
    "vencimento": "2024-12-31",
    "fornecedor_id": 1
  }'
```

## Monitoramento

- **CloudWatch Logs**: Logs das Lambda functions
- **CloudWatch Metrics**: Métricas de performance
- **AWS X-Ray**: Rastreamento distribuído (opcional)

## Cleanup

```bash
# Destruir infraestrutura
terraform destroy
```
