from aws.ec2_helper import EC2Helper
from aws.rosa_helper import ROSAHelper
from ostack.core import OpenStackHelper

# Helper function to handle the "help" command
def handle_help(say, user):
    say(
        f"Hello <@{user}>! I'm here to help. You can use the following commands:\n"
        "`create-rosa-cluster <cluster_name>`: Create an AWS OpenShift cluster.\n"
        "`create-openstack-vm <name> <image> <flavor> <network>`: Create an OpenStack VM.\n"
        "`hello`: Greet the bot."
    )

# Helper function to handle creating a ROSA cluster
def handle_create_rosa_cluster(say, user, text):
    cluster_name = text.replace("create-rosa-cluster", "").strip()
    rosa_helper = ROSAHelper(region="us-west-2")  # Set your region
    rosa_helper.create_rosa_cluster(cluster_name)

# Helper function to handle creating an OpenStack VM
def handle_create_openstack_vm(say, user, text):
    args = text.replace("create-openstack-vm", "").strip().split()
    os_helper = OpenStackHelper()
    os_helper.create_vm(args, say)

# Helper function to handle greeting
def handle_hello(say, user):
    say(f"Hello <@{user}>! How can I assist you today?")

# Helper function to handle creating an AWS EC2 instances
def handle_create_aws_vm(say, user):
    ec2_helper = EC2Helper(region="us-west-2")  # Set your region
    instance = ec2_helper.create_instance(
        "ami-0d2614eafc1b0e4d2",  # Replace with a valid AMI ID
        "t2.micro",
        "prabhakar",  # Replace with your key name
        "sg-0a698ca3494298d7d",  # Replace with your security group ID
        "subnet-0ca17bcc389bf108f",  # Replace with your subnet ID
    )
    say(f"Successfully created EC2 instance: {instance.id}")
