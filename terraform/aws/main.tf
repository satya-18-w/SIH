provider "aws" {
  region = var.aws_region
}

data "aws_availability_zones" "available" {}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "floatchat-vpc"
  }
}

resource "aws_subnet" "public" {
  count = 2
  vpc_id     = aws_vpc.main.id
  cidr_block = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index)
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name = "floatchat-public-subnet-${count.index + 1}"
  }
}

resource "aws_db_subnet_group" "main" {
  name       = "floatchat-db-subnet-group"
  subnet_ids = aws_subnet.public[*].id

  tags = {
    Name = "FloatChat DB Subnet Group"
  }
}

resource "aws_security_group" "db" {
  name        = "floatchat-db-sg"
  description = "Allow access to FloatChat DB"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = var.allowed_ips
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "floatchat-db-sg"
  }
}

resource "aws_eks_cluster" "main" {
  name     = "floatchat-eks-cluster"
  role_arn = "arn:aws:iam::123456789012:role/eks-cluster-role" # Replace with your IAM role ARN

  vpc_config {
    subnet_ids = aws_subnet.public[*].id
  }

  depends_on = [
    # IAM roles for EKS
  ]
}

resource "aws_db_instance" "main" {
  allocated_storage    = 20
  engine               = "postgres"
  engine_version       = "15.3"
  instance_class       = "db.t3.micro"
  name                 = "floatchatdb"
  username             = var.db_username
  password             = var.db_password
  parameter_group_name = "default.postgres15"
  skip_final_snapshot  = true
  db_subnet_group_name = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.db.id]
  publicly_accessible = true
}

resource "aws_s3_bucket" "main" {
  bucket = "floatchat-data-bucket-${random_id.bucket_suffix.hex}"
  
}

resource "random_id" "bucket_suffix" {
  byte_length = 8
}
