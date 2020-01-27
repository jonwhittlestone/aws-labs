# aws-labs study guide

## Motivation

This repo contains my notes on practical explorations with using AWS services with implementation detail covering:
- SDK with boto3
- Config management with Ansible
- Immutable infrastructure with Docker + IAC with Terraform 

## Supporting Resources

- Toy Dockerized Flask RESTful API [[github]](https://github.com/jonwhittlestone/flask-rest-api)


## Table of Contents

* VPC/ECS
  * VPC and simple node web app from scratch [aws-cli](vpc/vpc-simple/aws-cli/README.md) | [boto](vpc/vpc-simple/boto/README.md) | [terraform](http://www.google.com)
  * Highly Available web app from scratch [boto](http://google.com)
* SNS
* Lambda
* ECS
* Deployment: CI/CD -> AWS
    * Gitlab
    * Bitbucket (Pipelines)
    * Github (Actions)