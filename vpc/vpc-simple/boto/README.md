# vpc-simple - boto3

## Resources

- Niyazi Erdoğan's AWS, Python and Boto O'Reilly Course [[video]](https://learning.oreilly.com/videos/managing-ec2-and/9781838642938) [[github]](https://github.com/neocorp/python-boto3-vpc_and_ec2)
- Boto3 EC2 Docs [[link]](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html)
## Architecture
![architecture](architecture.png "The eventual output")


## To run VPC creation

    (venv) src $ python main.py preparevpc
    ...
    👌  SUCCESS 👌  Created VPC with VPC ID: vpc-0ee6cfdf688d225bb. Public Subnet ID: subnet-0e787e6d55f07c25b. Private Subnet ID: subnet-0a73dadc94905f409



## To run EC2 Instance creation

Then create an EC2 instance, with arguments:

* VPC ID from previous step
* Public Subnet ID from previous step
* Private Subnet ID from previous step

* AMI ID from the quickstart section of the [LaunchInstanceWizard]( ami-0089b31e09ac3fffc)

```
(venv) src $ python main.py prepareec2 vpc-0ee6cfdf688d225bb ami-0089b31e09ac3fffc subnet-0e787e6d55f07c25b subnet-0a73dadc94905f409

...
Launching EC2 Instance(s) within Subnet subnet-0e787e6d55f07c25b
👌  SUCCESS 👌 Launched Public EC2 Instance using AMI ami-0089b31e09ac3fffc i-05a20f2a32ca85ee9
...
Launching EC2 Instance(s) within Subnet subnet-0a73dadc94905f409
👌  SUCCESS 👌  Launched private EC2 Instance using AMI ami-0089b31e09ac3fffc i-05913fa83c79433e6
```