from google.cloud import secretmanager
from data_wizard_tool.config.config import GCP_PROJECT


def save_to_sm(secret_id, secret_content):
    client = secretmanager.SecretManagerServiceClient()
    parent = f"projects/{GCP_PROJECT}"
    name = f"{parent}/secrets/{secret_id}"

    try:
        # Attempt to get the secret
        client.get_secret(request={"name": name})
        # If no exception is raised, the secret exists
        # Add a new version
        version = client.add_secret_version(
            request={
                "parent": name,
                "payload": {"data": secret_content},
            }
        )
    except Exception:
        # Secret doesn't exist, create it
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


def get_from_sm(secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{GCP_PROJECT}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")
