terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

# VPC e Networking
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "${var.project_name}-vpc"
  }
}

resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 1}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name = "${var.project_name}-private-subnet-${count.index + 1}"
  }
}

resource "aws_subnet" "public" {
  count                   = 2
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.${count.index + 10}.0/24"
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.project_name}-public-subnet-${count.index + 1}"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.project_name}-igw"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "${var.project_name}-public-rt"
  }
}

resource "aws_route_table_association" "public" {
  count          = length(aws_subnet.public)
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

data "aws_availability_zones" "available" {
  state = "available"
}

# Security Groups
resource "aws_security_group" "lambda" {
  name_prefix = "${var.project_name}-lambda-"
  vpc_id      = aws_vpc.main.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-lambda-sg"
  }
}

resource "aws_security_group" "aurora" {
  name_prefix = "${var.project_name}-aurora-"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.lambda.id]
  }

  tags = {
    Name = "${var.project_name}-aurora-sg"
  }
}

# Aurora Serverless v2 Cluster
resource "aws_rds_subnet_group" "aurora" {
  name       = "${var.project_name}-aurora-subnet-group"
  subnet_ids = aws_subnet.private[*].id

  tags = {
    Name = "${var.project_name}-aurora-subnet-group"
  }
}

resource "aws_rds_cluster" "aurora" {
  cluster_identifier      = "${var.project_name}-aurora-cluster"
  engine                  = "aurora-postgresql"
  engine_mode             = "provisioned"
  engine_version          = "15.4"
  database_name           = var.database_name
  master_username         = var.db_username
  manage_master_user_password = true
  
  db_subnet_group_name   = aws_rds_subnet_group.aurora.name
  vpc_security_group_ids = [aws_security_group.aurora.id]
  
  serverlessv2_scaling_configuration {
    max_capacity = 1
    min_capacity = 0.5
  }
  
  enable_http_endpoint = true
  skip_final_snapshot  = true

  tags = {
    Name = "${var.project_name}-aurora-cluster"
  }
}

resource "aws_rds_cluster_instance" "aurora" {
  cluster_identifier = aws_rds_cluster.aurora.id
  instance_class     = "db.serverless"
  engine             = aws_rds_cluster.aurora.engine
  engine_version     = aws_rds_cluster.aurora.engine_version
}

# SQS Queues
resource "aws_sqs_queue" "conta_criada" {
  name                      = "${var.project_name}-conta-criada"
  message_retention_seconds = 1209600 # 14 dias
  
  tags = {
    Name = "${var.project_name}-conta-criada-queue"
  }
}

resource "aws_sqs_queue" "processamento" {
  name                      = "${var.project_name}-processamento"
  message_retention_seconds = 1209600 # 14 dias
  
  tags = {
    Name = "${var.project_name}-processamento-queue"
  }
}

# SNS Topics
resource "aws_sns_topic" "conta_criada" {
  name = "${var.project_name}-conta-criada"
  
  tags = {
    Name = "${var.project_name}-conta-criada-topic"
  }
}

resource "aws_sns_topic" "vencimentos" {
  name = "${var.project_name}-vencimentos"
  
  tags = {
    Name = "${var.project_name}-vencimentos-topic"
  }
}

resource "aws_sns_topic" "pagamentos" {
  name = "${var.project_name}-pagamentos"
  
  tags = {
    Name = "${var.project_name}-pagamentos-topic"
  }
}

# IAM Role para Lambda
resource "aws_iam_role" "lambda_role" {
  name = "${var.project_name}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "lambda_policy" {
  name = "${var.project_name}-lambda-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect = "Allow"
        Action = [
          "rds-data:BeginTransaction",
          "rds-data:CommitTransaction",
          "rds-data:ExecuteStatement",
          "rds-data:RollbackTransaction"
        ]
        Resource = aws_rds_cluster.aurora.arn
      },
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret"
        ]
        Resource = aws_rds_cluster.aurora.master_user_secret[0].secret_arn
      },
      {
        Effect = "Allow"
        Action = [
          "sqs:SendMessage",
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes"
        ]
        Resource = [
          aws_sqs_queue.conta_criada.arn,
          aws_sqs_queue.processamento.arn
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "sns:Publish"
        ]
        Resource = [
          aws_sns_topic.conta_criada.arn,
          aws_sns_topic.vencimentos.arn,
          aws_sns_topic.pagamentos.arn
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "ec2:CreateNetworkInterface",
          "ec2:DescribeNetworkInterfaces",
          "ec2:DeleteNetworkInterface"
        ]
        Resource = "*"
      }
    ]
  })
}

# Lambda Functions
resource "aws_lambda_function" "create_conta" {
  filename         = "lambda_create_conta.zip"
  function_name    = "${var.project_name}-create-conta"
  role            = aws_iam_role.lambda_role.arn
  handler         = "handler_create_conta.lambda_handler"
  runtime         = "python3.10"
  timeout         = 30

  vpc_config {
    subnet_ids         = aws_subnet.private[*].id
    security_group_ids = [aws_security_group.lambda.id]
  }

  environment {
    variables = {
      AURORA_CLUSTER_ARN    = aws_rds_cluster.aurora.arn
      AURORA_SECRET_ARN     = aws_rds_cluster.aurora.master_user_secret[0].secret_arn
      DATABASE_NAME         = var.database_name
      SQS_CONTA_CRIADA_URL  = aws_sqs_queue.conta_criada.url
    }
  }

  tags = {
    Name = "${var.project_name}-create-conta"
  }
}

resource "aws_lambda_function" "processa_fila" {
  filename         = "lambda_processa_fila.zip"
  function_name    = "${var.project_name}-processa-fila"
  role            = aws_iam_role.lambda_role.arn
  handler         = "handler_processa_fila.lambda_handler"
  runtime         = "python3.10"
  timeout         = 300

  vpc_config {
    subnet_ids         = aws_subnet.private[*].id
    security_group_ids = [aws_security_group.lambda.id]
  }

  environment {
    variables = {
      AURORA_CLUSTER_ARN     = aws_rds_cluster.aurora.arn
      AURORA_SECRET_ARN      = aws_rds_cluster.aurora.master_user_secret[0].secret_arn
      DATABASE_NAME          = var.database_name
      SNS_CONTA_CRIADA_TOPIC = aws_sns_topic.conta_criada.arn
      SNS_VENCIMENTOS_TOPIC  = aws_sns_topic.vencimentos.arn
      SNS_PAGAMENTO_TOPIC    = aws_sns_topic.pagamentos.arn
    }
  }

  tags = {
    Name = "${var.project_name}-processa-fila"
  }
}

# Event Source Mapping para SQS
resource "aws_lambda_event_source_mapping" "sqs_conta_criada" {
  event_source_arn = aws_sqs_queue.conta_criada.arn
  function_name    = aws_lambda_function.processa_fila.arn
  batch_size       = 10
}

resource "aws_lambda_event_source_mapping" "sqs_processamento" {
  event_source_arn = aws_sqs_queue.processamento.arn
  function_name    = aws_lambda_function.processa_fila.arn
  batch_size       = 10
}

# API Gateway
resource "aws_api_gateway_rest_api" "main" {
  name = "${var.project_name}-api"
  
  tags = {
    Name = "${var.project_name}-api"
  }
}

resource "aws_api_gateway_resource" "contas" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_rest_api.main.root_resource_id
  path_part   = "contas"
}

resource "aws_api_gateway_method" "create_conta" {
  rest_api_id   = aws_api_gateway_rest_api.main.id
  resource_id   = aws_api_gateway_resource.contas.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "create_conta" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  resource_id = aws_api_gateway_resource.contas.id
  http_method = aws_api_gateway_method.create_conta.http_method

  integration_http_method = "POST"
  type                   = "AWS_PROXY"
  uri                    = aws_lambda_function.create_conta.invoke_arn
}

resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.create_conta.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.main.execution_arn}/*/*"
}

resource "aws_api_gateway_deployment" "main" {
  depends_on = [
    aws_api_gateway_integration.create_conta
  ]

  rest_api_id = aws_api_gateway_rest_api.main.id
  stage_name  = "prod"
}

# CloudWatch Event para verificação periódica
resource "aws_cloudwatch_event_rule" "verificar_vencimentos" {
  name                = "${var.project_name}-verificar-vencimentos"
  description         = "Verifica contas vencendo diariamente"
  schedule_expression = "cron(0 9 * * ? *)" # Todo dia às 9h
}

resource "aws_cloudwatch_event_target" "sqs_verificar_vencimentos" {
  rule      = aws_cloudwatch_event_rule.verificar_vencimentos.name
  target_id = "SendToSQS"
  arn       = aws_sqs_queue.processamento.arn

  sqs_parameters {
    message_group_id = "verificacao-vencimentos"
  }
}
