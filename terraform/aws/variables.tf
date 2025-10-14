variable "aws_region" {
  description = "The AWS region to deploy to."
  default     = "us-east-1"
}

variable "db_username" {
  description = "The username for the RDS database."
  type        = string
  sensitive   = true
}

variable "db_password" {
  description = "The password for the RDS database."
  type        = string
  sensitive   = true
}
