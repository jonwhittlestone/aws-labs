variable "euwest1_ami_id" {
  description = "eu-west-1 AMI ID"
  type        = string
  default       = "ami-0713f98de93617bb4"
}


output "public_ip" {
  value       = aws_instance.example.public_ip
  description = "The public IP of the Instance"
}