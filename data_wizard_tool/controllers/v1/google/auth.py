import json

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from data_wizard_tool.database import get_db
from data_wizard_tool.models.user import User
from data_wizard_tool.services.google import credentials
from data_wizard_tool.services import auth as auth_service

router = APIRouter()


@router.post("/gcp_credentials", tags=["gcp"])
async def upload_gcp_credentials(
        credentials_file: UploadFile = File(...),
        user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)):
    try:
        _ = await credentials.upload_gcp_credentials(credentials_file, user, db)
        return {"message": "GCP credentials uploaded successfully!"}

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid service account credentials")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
