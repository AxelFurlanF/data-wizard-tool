import os

GCP_PROJECT = os.environ.get("GCP_PROJECT")

SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
ALGORITHM = "HS256"
