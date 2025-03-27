import boto3
from config import config
import subprocess


class AWSHelper:
    def __init__(self, region=None):
        self.region = region or config.AWS_DEFAULT_REGION
        self.session = boto3.Session(
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
            region_name=self.region,
        )

    def list_instances(self):
        """
        List all EC2 instances in the specified region.
        """
        ec2 = self.session.client("ec2")
        response = ec2.describe_instances()
        return response["Reservations"]

    def create_instance(
        self, image_id, instance_type, key_name, security_group_id, subnet_id
    ):
        """
        Create an EC2 instance with the given parameters.
        """
        ec2 = self.session.resource("ec2")
        try:
            instance_params = {
                "ImageId": image_id,
                "InstanceType": instance_type,
                "KeyName": key_name,
                "SecurityGroupIds": [security_group_id],
                "MinCount": 1,
                "MaxCount": 1,
            }
            if subnet_id:
                instance_params["SubnetId"] = subnet_id

            instances = ec2.create_instances(**instance_params)
            return instances[0]
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


class ROSAHelper(AWSHelper):
    def create_rosa_cluster(self, cluster_name, say):
        """
        Create a ROSA cluster using the ROSA CLI.
        If `say` is provided, it will send messages back to Slack.
        """
        if not cluster_name:
            if say:
                say(
                    "Please provide a cluster name. Usage: `create-aws-cluster <cluster_name>`"
                )
                return

        if say:
            say(
                f"Creating AWS OpenShift cluster: {cluster_name} in region {self.region}..."
            )

        try:
            command = [
                "rosa",
                "create",
                "cluster",
                "--cluster-name",
                cluster_name,
                "--region",
                self.region,
            ]
            subprocess.run(command, check=True)
            if say:
                say(f"Cluster {cluster_name} created successfully in AWS!")
        except subprocess.CalledProcessError as e:
            if say:
                say(f"Error creating AWS cluster: {str(e)}")
            raise e

    def list_rosa_clusters(self, say=None):
        """
        List all ROSA clusters using the ROSA CLI.
        If `say` is provided, it will send the list to Slack.
        """
        if say:
            say("Fetching ROSA clusters...")

        try:
            command = ["rosa", "list", "clusters"]
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            if say:
                say(f"ROSA Clusters:\n{result.stdout}")
            return result.stdout
        except subprocess.CalledProcessError as e:
            if say:
                say(f"Error fetching ROSA clusters: {str(e)}")
            raise e
