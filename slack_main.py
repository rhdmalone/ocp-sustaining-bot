from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from config import config
from aws.ec2_helper import EC2Helper
from aws.rosa_helper import ROSAHelper
from ostack.core import OpenStackHelper
import re

app = App(token=config.SLACK_BOT_TOKEN)


# helper function to handle the "help" command
def handle_help(say, user):
    say(
        f"Hello <@{user}>! I'm here to help. You can use the following commands:\n"
        "`create-rosa-cluster <cluster_name>`: Create an AWS OpenShift cluster.\n"
        "`create-openstack-vm <name> <image> <flavor> <network>`: Create an OpenStack VM.\n"
        "`hello`: Greet the bot."
    )

# helper function to handle creating a ROSA cluster
def handle_create_rosa_cluster(say, user, text):
    cluster_name = text.replace("create-rosa-cluster", "").strip()
    rosa_helper = ROSAHelper(region="us-west-2")  # Set your region
    rosa_helper.create_rosa_cluster(cluster_name)

# helper function to handle creating an OpenStack VM
def handle_create_openstack_vm(say, user, text):
    args = text.replace("create-openstack-vm", "").strip().split()
    os_helper = OpenStackHelper()
    os_helper.create_vm(args, say)

# helper function to handle greeting
def handle_hello(say, user):
    say(f"Hello <@{user}>! How can I assist you today?")

# helper function to handle creating an AWS EC2 instance
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

# Define the main event handler function
@app.event("app_mention")
@app.event("message")
def mention_handler(body, say):
    user = body.get("event", {}).get("user")
    text = body.get("event", {}).get("text", "").strip()

    # Create a command mapping
    commands = {
        r"\bhelp\b": lambda: handle_help(say, user),
        r"^create-rosa-cluster": lambda: handle_create_rosa_cluster(say, user, text),
        r"^create-openstack-vm": lambda: handle_create_openstack_vm(say, user, text),
        r"\bhello\b": lambda: handle_hello(say, user),
        r"\bcreate_aws_vm\b": lambda: handle_create_aws_vm(say, user),
    }

    # Check for command matches and execute the appropriate handler
    for pattern, handler in commands.items():
        if re.search(pattern, text, re.IGNORECASE):
            handler()  # Execute the handler
            return

    # If no match is found, provide a default message
    say(
        f"Hello <@{user}>! I couldn't understand your request. Please try again or type 'help' for assistance."
    )


# Main Entry Point
if __name__ == "__main__":
    print("Starting Slack bot...")
    handler = SocketModeHandler(app, config.SLACK_APP_TOKEN)
    handler.start()
