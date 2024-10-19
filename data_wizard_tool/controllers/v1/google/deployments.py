import json
from data_wizard_tool.main import get_logger

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from data_wizard_tool.database import get_db


router = APIRouter()


@router.post("/deploy_composer", tags=["gcp"])
async def deploy_cloud_composer(db: Session = Depends(get_db)):
    pass
