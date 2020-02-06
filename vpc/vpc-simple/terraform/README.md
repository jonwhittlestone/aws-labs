# vpc-simple - Terraform

## Resources

- Terraform: Up & Running (2nd Ed.) [[contents]](https://learning.oreilly.com/library/view/terraform-up/9781492046899/#toc) | [[github]](https://github.com/brikis98/terraform-up-and-running-code)
- neocorp's terraforming a VPC [[reference github]](https://github.com/jonwhittlestone/aws_vpc_ec2)

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

4. Get the public IP

        $ terraform output

        public_ip = 3.10.205.172

5. SSH to it using the existing keypair

        $ ssh -i ~/.ssh/ManualEC2-vpc-simple.pem 3.10.205.172
