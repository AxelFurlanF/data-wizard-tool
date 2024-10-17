from google.cloud import secretmanager
from data_wizard_tool.config.config import GCP_PROJECT


def save_to_secrets_manager(secret_id, secret_content):
    client = secretmanager.SecretManagerServiceClient()
    parent = f"projects/{GCP_PROJECT}"  # Replace with your project ID
    secret = client.create_secret(
        request={
            "parent": parent,
            "secret_id": secret_id,
            "secret": {"replication": {"automatic": {}}},
        }
    )
    version = client.add_secret_version(
        request={
            "parent": secret.name,
            "payload": {"data": secret_content},
        }
    )

    return version
