from sqlalchemy.orm import Session
import json
from data_wizard_tool.models.user import User

from fastapi import HTTPException, UploadFile
from google.oauth2 import service_account
from data_wizard_tool.utils.gcp_utils import save_to_sm


# TODO: Replace with the actual user ID


async def upload_gcp_credentials(
    credentials_file: UploadFile, current_user, db: Session
):
    # Read the contents of the uploaded file
    credentials_content = await credentials_file.read()
    credentials_json = json.loads(credentials_content)

    # Verify the credentials (optional, but recommended)
    service_account.Credentials.from_service_account_info(
        credentials_json
    )
    version = save_to_sm(f"{current_user.id}-gcp-credentials",
                         credentials_content)

    db_user = db.query(User).filter(User.id == current_user.id).first()
    if db_user:
        db_user.gcp_secret_url = version.name
        db.commit()
        return version.name
    else:
        raise HTTPException(
            status_code=404, detail="User not found"
        )
