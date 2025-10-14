output "eks_cluster_name" {
  value = aws_eks_cluster.main.name
}

output "db_instance_address" {
  value = aws_db_instance.main.address
}

output "s3_bucket_name" {
  value = aws_s3_bucket.main.bucket
}
