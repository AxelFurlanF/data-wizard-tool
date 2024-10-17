import json

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from google.oauth2 import service_account
from sqlalchemy.orm import Session

from data_wizard_tool.config.config import GCP_PROJECT
from data_wizard_tool.database import get_db
from data_wizard_tool.main import logger

from data_wizard_tool.utils.gcp_utils import save_to_secrets_manager

router = APIRouter()

# TODO: Replace with the actual user ID


class User:
    def __init__(self, username):
        self.username = username


current_user = User(username="test_user")


@router.post("/gcp_credentials", tags=["gcp"])
async def upload_gcp_credentials(credentials_file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Read the contents of the uploaded file
        credentials_content = await credentials_file.read()
        credentials_json = json.loads(credentials_content)

        # Verify the credentials (optional, but recommended)
        credentials = service_account.Credentials.from_service_account_info(
            credentials_json
        )
        save_to_secrets_manager(f"{current_user.username}-gcp-credentials",
                                credentials_content)
        # You can add additional verification here, like checking for
        # specific permissions or accessing a GCP service to validate.

        # TODO: Store the credentials securely

        logger.info(credentials_json)
        return {"message": "GCP credentials uploaded successfully!"}

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid service account credentials")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
