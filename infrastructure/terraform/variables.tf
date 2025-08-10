variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Nome do projeto"
  type        = string
  default     = "contas-a-pagar"
}

variable "database_name" {
  description = "Nome do banco de dados"
  type        = string
  default     = "contas_a_pagar"
}

variable "db_username" {
  description = "Username para o banco de dados"
  type        = string
  default     = "postgres"
}
