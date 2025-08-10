output "aurora_cluster_arn" {
  description = "ARN do cluster Aurora"
  value       = aws_rds_cluster.aurora.arn
}

output "aurora_endpoint" {
  description = "Endpoint do cluster Aurora"
  value       = aws_rds_cluster.aurora.endpoint
}

output "secret_arn" {
  description = "ARN do secret para conexão com o banco"
  value       = aws_rds_cluster.aurora.master_user_secret[0].secret_arn
}

output "api_gateway_url" {
  description = "URL do API Gateway"
  value       = aws_api_gateway_deployment.main.invoke_url
}

output "sqs_conta_criada_url" {
  description = "URL da fila SQS para contas criadas"
  value       = aws_sqs_queue.conta_criada.url
}

output "sqs_processamento_url" {
  description = "URL da fila SQS para processamento"
  value       = aws_sqs_queue.processamento.url
}

output "sns_conta_criada_arn" {
  description = "ARN do tópico SNS para contas criadas"
  value       = aws_sns_topic.conta_criada.arn
}

output "sns_vencimentos_arn" {
  description = "ARN do tópico SNS para vencimentos"
  value       = aws_sns_topic.vencimentos.arn
}

output "sns_pagamentos_arn" {
  description = "ARN do tópico SNS para pagamentos"
  value       = aws_sns_topic.pagamentos.arn
}
