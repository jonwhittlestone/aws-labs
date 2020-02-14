variable "region" {
  default = "eu-west-2"
}

# INFRA

variable "vpc_cidr" {
  description = "CIDR Block for VPC"
  default = "10.0.0.0/16"
}
variable "public_subnet_1_cidr" {
  description = "CIDR Block for Public Subnet 1"
  default = "10.0.1.0/24"
}

variable "private_subnet_1_cidr" {
  description = "CIDR Block for Private Subnet 1"
  default = "10.0.2.0/24"
}

output "public_ip" {
  value       = aws_instance.example.public_ip
  description = "The public IP of the Instance"
}

output "eis_public_ip" {
  value       = aws_eip.elastic-ip-for-nat-gw.public_ip
  description = "The Elastic IP for the NAT Gateway. Visit this in a web browser"
}