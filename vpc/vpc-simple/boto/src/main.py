from ec2.vpc import VPC
from client_locator import EC2Client

def main():
    # Create a VPC -----------------------
    ec2_client = EC2Client().get_client()
    vpc = VPC(ec2_client)
    vpc_response = vpc.create_vpc()
    print('VPC created: ' + str(vpc_response))
    # /Create a VPC -----------------------

if __name__ == '__main__':
    main()