import json

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from data_wizard_tool.database import get_db

from data_wizard_tool.services.google import auth


router = APIRouter()


class User:
    def __init__(self, id):
        self.id = id


current_user = User(id=1)


@router.post("/gcp_credentials", tags=["gcp"])
async def upload_gcp_credentials(credentials_file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        version_name = await auth.upload_gcp_credentials(credentials_file, current_user, db)
        return {"message": f"GCP credentials uploaded successfully {version_name}!"}

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid service account credentials")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
