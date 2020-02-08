# aws-labs study guide

## Motivation

This repo contains my notes on practical explorations with using AWS services with implementation detail covering:
- SDK with boto3
- Config management with Ansible
- Immutable infrastructure with Docker + IAC with Terraform 

## Resources

- Toy Dockerized Flask RESTful API [[github]](https://github.com/jonwhittlestone/flask-rest-api)
- Configuration management scripts [[ansible]](ansible/README.md)
- Effective DevOps with AWS [[contents]](https://learning.oreilly.com/library/view/effective-devops-with/9781789539974/2fb577d6-6318-490b-80d3-365e90105060.xhtml) | [[github]](https://github.com/yogeshraheja/Effective-DevOps-with-AWS)

## Table of Contents

* VPC
  * VPC and simple Flask web app from scratch [aws-cli](vpc/vpc-simple/aws-cli/README.md) | [boto](vpc/vpc-simple/boto/README.md) | [terraform](vpc/vpc-simple/terraform/README.md)
* RDS
  * Simple Flask app persisted to RDS [boto](vpc/vpc-simple/boto/README.md) | [terraform](http://www.google.com)
* HA
  * Load Balanced Flask App [boto](http://google.com) | [terraform](http://www.google.com)
  * Load Balanced Flask App with Multi A-Z [boto](http://google.com) | [terraform](http://www.google.com)

More to come ..

* SNS
* Lambda
* ECS
* Deployment: CI/CD -> AWS
    * Gitlab
    * Bitbucket (Pipelines)
    * Github (Actions)

## SSH Config Snippet

Add the following to the `$HOME/.ssh/config` file to avoid having to specify `--private-key` on Ansible commands etc

    IdentityFile ~/.ssh/ManualEC2-vpc-simple.pem
    User ec2-user 
    StrictHostKeyChecking no
    PasswordAuthentication no
    ForwardAgent yes