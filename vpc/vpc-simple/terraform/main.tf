provider "aws" {
  region = var.region
  version = "~> 2.48"
}

resource "aws_vpc" "production-vpc" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true

  tags = {
    Name = "Production-VPC"
  }
}

resource "aws_subnet" "public-subnet-1" {
  cidr_block        = var.public_subnet_1_cidr
  vpc_id            = aws_vpc.production-vpc.id
  availability_zone = "eu-west-2a"

  tags = {
    Name = "Public-Subnet-1"
  }
}

resource "aws_route_table" "public-route-table" {
  vpc_id = aws_vpc.production-vpc.id
  tags = {
    Name = "Public-Route-Table"
  }
}
resource "aws_route_table_association" "public-route-1-association" {
  route_table_id = aws_route_table.public-route-table.id
  subnet_id      = aws_subnet.public-subnet-1.id
}

resource "aws_subnet" "private-subnet-1" {
  cidr_block        = var.private_subnet_1_cidr
  vpc_id            = aws_vpc.production-vpc.id
  availability_zone = "eu-west-2a"

  tags = {
    Name = "Private-Subnet-1"
  }
}


resource "aws_route_table" "private-route-table" {
  vpc_id = aws_vpc.production-vpc.id
  tags = {
    Name = "Private-Route-Table"
  }
}
resource "aws_route_table_association" "private-route-1-association" {
  route_table_id = aws_route_table.private-route-table.id
  subnet_id      = aws_subnet.private-subnet-1.id
}

resource "aws_eip" "elastic-ip-for-nat-gw" {
  vpc                       = true
  associate_with_private_ip = "10.0.0.5"

  tags = {
    Name = "Production-EIP"
  }
}

resource "aws_nat_gateway" "nat-gw" {
  allocation_id = aws_eip.elastic-ip-for-nat-gw.id
  subnet_id     = aws_subnet.public-subnet-1.id

  tags = {
    Name = "Production-NAT-GW"
  }

  depends_on = [aws_eip.elastic-ip-for-nat-gw]
}

resource "aws_route" "nat-gw-route" {
  route_table_id         = aws_route_table.private-route-table.id
  nat_gateway_id         = aws_nat_gateway.nat-gw.id
  destination_cidr_block = "0.0.0.0/0"
}

resource "aws_internet_gateway" "production-igw" {
  vpc_id = aws_vpc.production-vpc.id
  tags = {
    Name = "Production-IGW"
  }
}

resource "aws_route" "public-internet-igw-route" {
  route_table_id         = aws_route_table.public-route-table.id
  gateway_id             = aws_internet_gateway.production-igw.id
  destination_cidr_block = "0.0.0.0/0"
}

# INSTANCE

resource "aws_instance" "example" {  
  ami           = "ami-0389b2a3c4948b1a0"
  instance_type = "t2.micro" 
  subnet_id     = aws_subnet.public-subnet-1.id
  associate_public_ip_address = true
  vpc_security_group_ids = [aws_security_group.instance.id]
  key_name                = "ManualEC2-vpc-simple"

  user_data = <<EOF
      #!/bin/bash
      sudo yum update -y
      sudo yum install -y git python-pip
      pip install ansible
      ansible-pull -U https://github.com/jonwhittlestone/aws-labs ansible/simple-vpc.yml -i localhost --sleep 60
    EOF
  }

  resource "aws_security_group" "instance" {  
    name = "terraform-example-instance"  
    vpc_id        = aws_vpc.production-vpc.id
    
    ingress {    
      from_port   = 80    
      to_port     = 80    
      protocol    = "tcp"    
      cidr_blocks = ["0.0.0.0/0"]  
      }

    ingress {    
      from_port   = 8080    
      to_port     = 8080    
      protocol    = "tcp"    
      cidr_blocks = ["0.0.0.0/0"]  
      }

    ingress {    
      from_port   = 22    
      to_port     = 22    
      protocol    = "tcp"    
      cidr_blocks = ["0.0.0.0/0"]  
      }

    egress {    
      from_port   = 0    
      to_port     = 65535    
      protocol    = "tcp"    
      cidr_blocks = ["0.0.0.0/0"]  
      }
    }