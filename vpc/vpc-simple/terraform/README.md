# vpc-simple - Terraform

## Resources

- Terraform: Up & Running (2nd Ed.) [contents](https://learning.oreilly.com/library/view/terraform-up/9781492046899/#toc) | [code](https://github.com/brikis98/terraform-up-and-running-code)
- neocorp's terraforming a VPC [code](https://github.com/jonwhittlestone/aws_vpc_ec2) | [article](https://niyazierdogan.wordpress.com/2019/02/16/implementing-aws-virtual-private-cloud-vpc-infrastructure-with-terraform/)

## Prerequisites
- Export your AWS credentials

        export AWS_ACCESS_KEY_ID=XXXXXXX; \
        export AWS_SECRET_ACCESS_KEY=XXXXXXX

- Have imported locally, a private key of an EC2 Keypair  for `eu-west-2` called 'ManualEC2-vpc-simple'

- IAM user has the following managed policies

    * ```AmazonEC2FullAccess```
    * ```AmazonS3FullAccess```
    * ```AmazonDynamoDBFullAccess```
    * ```AmazonRDSFullAccess```
    * ```CloudWatchFullAccess```
    * ```IAMFullAccess```

- To run in a region with a default VPC
    - For reference, this example uses `eu-west-2`

## Steps

1. Initialise the backend to download the provider. The command is idempotent.

        $ terraform init

2. Preview any changes

        $ terraform plan


3. Apply the changes

        $ terraform apply

        ...
        aws_instance.example: Creation complete after 42s [id=i-0a0ec6ea9a414e8b3]

        Apply complete! Resources: 1 added, 0 changed, 0 destroyed.

        Outputs:

        eip_public_ip = 3.11.66.163
        public_ip = 18.130.225.99

4. After a few minutes, visit Public IP in a browser


        http://18.130.225.99


5. If you need, SSH to Public IP using the existing keypair

        $ ssh -i ~/.ssh/ManualEC2-vpc-simple.pem 18.130.225.99
