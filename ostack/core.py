from openstack import connection
from config import config


class OpenStackHelper:
    def __init__(
        self,
        auth_url=None,
        project_name=None,
        application_credential_id=None,
        application_credential_secret=None,
    ):
        self.conn = connection.Connection(
            auth_url=config.OS_AUTH_URL,
            project_id=config.OS_PROJECT_ID,
            application_credential_id=config.OS_APP_CRED_ID,
            application_credential_secret=config.OS_APP_CRED_SECRET,
            region_name=config.OS_REGION_NAME,
            interface=config.OS_INTERFACE,
            identity_api_version=config.OS_ID_API_VERSION,
            auth_type=config.OS_AUTH_TYPE,
        )

    def list_servers(self):
        """
        List all servers in OpenStack.
        """
        return [server.name for server in self.conn.compute.servers()]

    def create_vm(self, args, say):
        """
        Create an OpenStack VM with the specified parameters provided as a list of arguments.
        If `say` is provided, it will send messages back to Slack.

        :param args: List of arguments: [name, image, flavor, network]
        :param say: (optional) Slack messaging function for feedback
        :return: The created server object
        """
        if len(args) != 4:
            if say:
                say("Usage: `create-openstack-vm <name> <image> <flavor> <network>`")
                return

        name, image, flavor, network = args

        if say:
            say(f"Creating OpenStack VM: {name}...")

        try:
            server = self.conn.compute.create_server(
                name=name, image=image, flavor=flavor, networks=[{"uuid": network}]
            )
            if say:
                say(f"VM {server.name} created successfully in OpenStack!")
            return server
        except Exception as e:
            if say:
                say(f"Error creating OpenStack VM: {str(e)}")
            raise e
