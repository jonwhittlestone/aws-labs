provider "aws" {
  # region = "eu-west-2"
  region = "eu-west-2"

  # Allow any 2.x version of the AWS provider
  version = "~> 2.0"
}

resource "aws_instance" "example" {  
  # ami           = var.euwest1_ami_idV
  ami           = "ami-0089b31e09ac3fffc"
  instance_type = "t2.micro" 
  vpc_security_group_ids = [aws_security_group.instance.id]
  key_name                = "ManualEC2-vpc-simple"

  user_data = <<-EOF
              #!/bin/bash
              echo "Hello, World" > index.html
              nohup busybox httpd -f -p 8080 &
              EOF

  tags = {
    Name = "terraform-example"
  }
}


resource "aws_security_group" "instance" {  
  name = "terraform-example-instance"  
  
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
  }