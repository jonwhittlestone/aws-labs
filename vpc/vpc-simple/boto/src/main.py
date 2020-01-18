from ec2.vpc import VPC
from client_locator import EC2Client


def main():
    """
        [x] Prepare VPC with Boto
        [ ] Prepare EC2 with Boto
        [ ] Allow command line removal of VPC
        [ ] Launch fresh AMI and Install docker
        [ ] Pull image and run Dockerfile
    """
    # Create a VPC -----------------------
    ec2_client = EC2Client().get_client()
    vpc = VPC(ec2_client)
    vpc_response = vpc.create_vpc()
    print('* VPC created: ' + str(vpc_response))
    vpc_name = 'simple-vpc--boto-vpc'
    vpc_id = vpc_response.get('Vpc').get('VpcId')
    vpc.add_name_tag(vpc_id, vpc_name)
    print(f'* VPC name added: {vpc_name} to {vpc_id}')
    print('')
    # /Create a VPC -----------------------

    # Create an Internet Gateway ----------
    igw_response = vpc.create_internet_gateway()
    igw_id = igw_response['InternetGateway']['InternetGatewayId']
    print('')
    # /Create an Internet Gateway ----------

    # Create IGW to VPC --------------------
    vpc.attach_igw_to_vpc(igw_id, vpc_id)
    print('')
    # /Create IGW to VPC -------------------

    # Create public subnet -----------------
    public_subnet_resp = vpc.create_subnet(vpc_id, '10.0.1.0/24')
    public_subnet_id = public_subnet_resp.get('Subnet').get('SubnetId')
    print(f'* Subnet created for VPC {vpc_id}: {str(public_subnet_id)}')
    print('')
    # /Create public subnet ----------------

    # Create route table for public subnet
    public_route_tbl_resp = vpc.create_public_route_table(vpc_id)
    rtb_id = public_route_tbl_resp.get('RouteTable').get('RouteTableId')
    print('')
    # /Create route table for public subnet

    # Add internet gateway route to public subnet's route table
    vpc.create_igw_route_to_public_route_table(rtb_id, igw_id)
    print('')
    # /Add internet gateway route to public subnet's route table

    # Associate public subnet with public route table
    vpc.associate_subnet_with_route_table(public_subnet_id, rtb_id)
    print('')
    # /Associate public subnet with public route table

    # Allowing Auto-assign IP address to subnet
    vpc.allow_auto_assign_ip_addresses_for_subnet(public_subnet_id)
    print('')
    # /Allowing Auto-assign IP address to subnet

    # /Create a private subnet that is isolated / no public route tbl    # /Create a private subnet that is isolated / no public route tbl
    private_subnet_resp = vpc.create_subnet(vpc_id, '10.0.2.0/24')
    private_subnet_id = private_subnet_resp.get('Subnet').get('SubnetId')
    print(f'* Subnet created for VPC {vpc_id}: {str(private_subnet_id)}')
    print('')
    # /Create a private subnet that is isolated / no public route tbl

    # Add name tag to subnets
    vpc.add_name_tag(private_subnet_id, 'simple-vpc--boto-private-subnet')
    vpc.add_name_tag(public_subnet_id, 'simple-vpc--boto-public-subnet')
    # /Add name tag to private subnet



if __name__ == '__main__':
    main()
