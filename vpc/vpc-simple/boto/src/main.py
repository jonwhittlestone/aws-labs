import typer
from ec2.vpc import VPC
from ec2.ec2 import EC2
from client_locator import EC2Client
import time

app = typer.Typer()

MANUAL_KEYPAIR_NAME_FOR_SSH = 'ManualEC2-vpc-simple'

@app.command()
def prepareec2(vpc_id, ami_id, public_subnet_id, private_subnet_id, generate_keypair = True):
    typer.echo(f"Preparing EC2 Instance ..")
    ec2_client = EC2Client().get_client()
    ec2 = EC2(ec2_client)

    # Create a keypair
    key_pair_name = f'simple-vpc--boto-generatedkeypair-{time.time()}'
    key_pair_resp = ec2.create_key_pair(key_pair_name)
    typer.echo(f'* Created Key Pair with name {key_pair_name}: ' + str(key_pair_resp))
    print('')
    # /Create a keypair

    # Create a security group
    public_sg_name = 'simple-vpc--boto-publicsg'
    public_sg_description = 'Public security group for public subnet internet access'
    public_sg_resp = ec2.create_security_group(
        public_sg_name,
        public_sg_description,
        vpc_id)
    public_sg_id = public_sg_resp.get('GroupId')
    # /Create a security group

    # Add rule to security group to ALLOW internet IN
    ec2.add_inbound_rule_to_sg(public_sg_id)
    print(f'Added public access rule to Security Group: {public_sg_name}')
    print('')
    # /Add rule to security group to ALLOW internet IN

    # Prepare ec2 instance before launch with startup script #
    user_data = """#!/bin/bash
                sudo yum update -y
                sudo yum install -y docker git
                sudo usermod -a -G docker ec2-user
                useradd dockeradmin
                sudo service docker start
                sudo chkconfig docker on
                sudo git clone https://github.com/jonwhittlestone/flask-rest-api.git /var/www/flask-rest-api
                sudo docker build -t howapped-products /var/www/flask-rest-api
                sudo docker run -d -p 80:5000 howapped-products:latest"""
    # /Prepare ec2 instance before launch with startup script #

    # Launch public EC2 instance within public subnet #
    if generate_keypair == 'False':
        key_pair_name = MANUAL_KEYPAIR_NAME_FOR_SSH

    launch_publicec2_resp = ec2.launch_ec2_instance(ami_id, key_pair_name, 1, 1,
                            public_sg_id, public_subnet_id, user_data)
    public_ec2_instance_id = launch_publicec2_resp['Instances'][0]['InstanceId']
    print(f'👌  SUCCESS - public instance 👌 Launched Public EC2 Instance using AMI {ami_id} {public_ec2_instance_id}')
    print('')
    # /Launch public EC2 instance within public subnet #

    # Adding another security group for private EC2 instance
    private_security_group_name = 'simple-vpc--boto-privatesg'
    private_security_group_description = 'Private Security Group for Private Subnet'
    private_sg_response = ec2.create_security_group(
        private_security_group_name, private_security_group_description, vpc_id)
    private_security_group_id = private_sg_response['GroupId']
    # /Adding another security group for private EC2 instance

    # Add rule to private security group
    ec2.add_inbound_rule_to_sg(private_security_group_id)
    # /Add rule to private security group

    # launch private ec2 #
    launch_private_ec2resp = ec2.launch_ec2_instance(ami_id, key_pair_name, 1, 1,
                            private_security_group_id, private_subnet_id,"""""")

    private_ec2_instance_id = launch_private_ec2resp['Instances'][0]['InstanceId']
    typer.echo(
        f'👌  SUCCESS - private instance 👌  Launched private EC2 Instance using AMI {ami_id} {private_ec2_instance_id}')
    print('')
    # launch private ec2 #


    # I need a boto watcher because it takes
    # a while for a public IP to be ready
    # if generate_keypair == 'False':
    #     typer.echo(
    #         f'🖥  SSH into the public instance when ready:')
    #     print(f'> ssh -i ~/.ssh/ ssh -i ~/.ssh/ManualEC2-vpc-simple.pem ec2-user@52.56.203.216')





@app.command()
def preparevpc():
    typer.echo(f"Creating VPC ..")
    ec2_client = EC2Client().get_client()
    vpc = VPC(ec2_client)

    # Create a VPC -----------------------
    vpc_response = vpc.create_vpc()
    typer.echo('* VPC created: ' + str(vpc_response))
    vpc_name = 'simple-vpc--boto-vpc'
    vpc_id = vpc_response.get('Vpc').get('VpcId')
    vpc.add_name_tag(vpc_id, vpc_name)
    typer.echo(f'* VPC name added: {vpc_name} to {vpc_id}')
    typer.echo('')
    # /Create a VPC -----------------------

    # Create an Internet Gateway ----------
    igw_response = vpc.create_internet_gateway()
    igw_id = igw_response['InternetGateway']['InternetGatewayId']
    typer.echo('')
    # /Create an Internet Gateway ----------

    # Create IGW to VPC --------------------
    vpc.attach_igw_to_vpc(igw_id, vpc_id)
    typer.echo('')
    # /Create IGW to VPC -------------------

    # Create public subnet -----------------
    public_subnet_resp = vpc.create_subnet(vpc_id, '10.0.1.0/24')
    public_subnet_id = public_subnet_resp.get('Subnet').get('SubnetId')
    typer.echo(f'* Subnet created for VPC {vpc_id}: {str(public_subnet_id)}')
    typer.echo('')
    # /Create public subnet ----------------

    # Create route table for public subnet
    public_route_tbl_resp = vpc.create_public_route_table(vpc_id)
    rtb_id = public_route_tbl_resp.get('RouteTable').get('RouteTableId')
    typer.echo('')
    # /Create route table for public subnet

    # Add internet gateway route to public subnet's route table
    vpc.create_igw_route_to_public_route_table(rtb_id, igw_id)
    typer.echo('')
    # /Add internet gateway route to public subnet's route table

    # Associate public subnet with public route table
    vpc.associate_subnet_with_route_table(public_subnet_id, rtb_id)
    typer.echo('')
    # /Associate public subnet with public route table

    # Allowing Auto-assign IP address to subnet
    vpc.allow_auto_assign_ip_addresses_for_subnet(public_subnet_id)
    typer.echo('')
    # /Allowing Auto-assign IP address to subnet

    # /Create a private subnet that is isolated / no public route tbl    # /Create a private subnet that is isolated / no public route tbl
    private_subnet_resp = vpc.create_subnet(vpc_id, '10.0.2.0/24')
    private_subnet_id = private_subnet_resp.get('Subnet').get('SubnetId')
    typer.echo(f'* Subnet created for VPC {vpc_id}: {str(private_subnet_id)}')
    typer.echo('')
    # /Create a private subnet that is isolated / no public route tbl

    # Add name tag to subnets
    vpc.add_name_tag(private_subnet_id, 'simple-vpc--boto-private-subnet')
    vpc.add_name_tag(public_subnet_id, 'simple-vpc--boto-public-subnet')
    # /Add name tag to private subnet

    typer.echo(
        f'👌  SUCCESS 👌  Created VPC with VPC ID: {vpc_id}. Public Subnet ID: {public_subnet_id}. Private Subnet ID: {private_subnet_id}')



@app.command()
def terminate_instance(instance_id):
    ec2_client = EC2Client().get_client()
    ec2 = EC2(ec2_client)
    ec2.terminate_instance(instance_id)


if __name__ == '__main__':
    """
        [x] Prepare VPC with Boto
        [x] Prepare EC2 with Boto
        [ ] Launch fresh AMI and Install docker
            - https://acloudxpert.com/how-toinstall-docker-on-amazon-linux-ami/
        [ ] Pull image and run Dockerfile
            - Write Dockerfile: https://nodejs.org/en/docs/guides/nodejs-docker-webapp/
            - wget the Dockerfile from this repo
            - build
            - run
    """
    app()
