# Configuration Management with Ansible

> Note: This is only currently tested with Amazon Linux 2 AMIs. Other versions of Linux, YMMV

## Resources

- Mastering Ansible [[contents]](https://learning.oreilly.com/library/view/mastering-ansible-/9781789951547/b684fd64-63ba-4ecf-bf3d-3acf1a74cf39.xhtml) | [[github]](https://github.com/PacktPublishing/Mastering-Ansible-Third-Edition)

## Role development workflow

Use `--check` to make sure everything's going swimmingly

    ansible-playbook simple-vpc.yml --private-key ~/.ssh/ManualEC2-vpc-simple.pem -e targe
    t=18.130.226.86 --check

## Basics

0. Ensure your VPC and EC2 instances are running and your machine has the private SSH key
1. To get a list of resources on your AWS account, run
    
        (venv) ansible $ ./ec2.py

2. Using Ansible's `ping` module which will give you the IP address
        
        ansible ec2 -m ping

3. Check instance disk usage

        ansible '18.130.226.86*' -a 'df -h'

4. Verify the playbook's target

        ansible-playbook simple-vpc.yml --private-key ~/.ssh/ManualEC2-vpc-simple.pem -e target=ec2 --list-hosts

5. Do a dry-run / `--check` mode

        ansible-playbook simple-vpc.yml --private-key ~/.ssh/ManualEC2-vpc-simple.pem -e target=18.130.226.86 --check

6. `ansible-pull` mode for running playbooks on the remote instance

        ansible-pull -U https://github.com/jonwhittlestone/aws-labs ansible/simple-vpc.yml -i localhost --sleep 60




