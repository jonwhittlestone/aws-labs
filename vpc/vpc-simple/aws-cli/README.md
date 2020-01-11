# vpc-simple

`aws-cli` commands for creating and removing a imple VPC from scratch

**Resources**

* [Create an IPv4 VPC and Subnets using the AWS CLI](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-subnets-commands-example.html)
* [Creating a simple Hello World web application - Effective DevOps with AWS](https://learning.oreilly.com/library/view/effective-devops-with/9781789539974/792582d6-cf33-49f5-bd53-2c381cb4a19d.xhtml)
* ```aws ec2 describe-vpcs | grep VpcId```


## creation

0. Remove the default VPC (if applicable)
1. Do something else

        aws ec2 ...
...
9. Create a security group with name

                aws ec2 create-security-group \
                --group-name HelloWorld \
                --description "Hello World Demo" \
                --vpc-id vpc-08303a0d2664545da

10. Add inbound traffic for port 3000 (for node) and verify

                aws ec2 authorize-security-group-ingress \
                --group-name HelloWorld \
                --protocol tcp \
                --port 3000 \
                --cidr 0.0.0.0/0

                --vpc-id vpc-08303a0d2664545da

## app installation

0. SSH in to the newly created instance

        ssh -i ~/.ssh/EffectiveDevOpsAWS.pem ec2-user@3.8.98.27

1. OS update

        sudo yum update -y

2. Install and Enable EPEL repo on Amazon Linux 2

        sudo yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm

3. Install node

        sudo yum install --enablerepo=epel -y nodejs






## removal

9. Remove security group

                aws ec2 delete-security-group \
                --group-name HelloWorld \
                --vpc-id vpc-08303a0d2664545da