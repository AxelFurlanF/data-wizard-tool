from app.main import logger
from fastapi import APIRouter, File, UploadFile, HTTPException
from google.oauth2 import service_account
import json

router = APIRouter()


@router.post("/gcp_credentials", tags=["gcp"])
async def upload_gcp_credentials(credentials_file: UploadFile = File(...)):
    try:
        # Read the contents of the uploaded file
        credentials_content = await credentials_file.read()
        credentials_json = json.loads(credentials_content)

        # Verify the credentials (optional, but recommended)
        credentials = service_account.Credentials.from_service_account_info(
            credentials_json
        )
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
