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

variable "allowed_ips" {
  description = "A list of IP addresses allowed to access the database."
  type        = list(string)
  default     = ["0.0.0.0/0"] # WARNING: This allows access from any IP address. Replace with your IP address.
}
