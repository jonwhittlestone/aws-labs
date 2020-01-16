from ec2.vpc import VPC
from client_locator import EC2Client


def main():
    # Create a VPC -----------------------
    ec2_client = EC2Client().get_client()
    vpc = VPC(ec2_client)
    vpc_response = vpc.create_vpc()
    print('VPC created: ' + str(vpc_response))
    vpc_name = 'simple-vpc--boto'
    vpc_id = vpc_response.get('Vpc').get('VpcId')
    vpc.add_name_tag(vpc_id, vpc_name)
    print(f'VPC name added: {vpc_name} to {vpc_id}')
    print('')
    print('')
    # /Create a VPC -----------------------

    # Create an Internet Gateway ----------
    igw_response = vpc.create_internet_gateway()
    igw_id = igw_response['InternetGateway']['InternetGatewayId']
    print('')
    print('')
    # /Create an Internet Gateway ----------

    # Create IGW to VPC --------------------
    vpc.attach_igw_to_vpc(igw_id, vpc_id)
    print('')
    print('')
    # /Create IGW to VPC -------------------


if __name__ == '__main__':
    main()