from supabase import create_client
import uuid
from fastapi import File, UploadFile, HTTPException
from schemas.appschema import *
from urllib.parse import urlparse

settings = Settings()
supabase = create_client(settings.supabase_url, settings.service_role_key)


async def upload_resumes(file: UploadFile = File()):
    content = await file.read()
    file_name = f"{uuid.uuid4()}_{file.filename}"
    try:
        response = supabase.storage.from_("resumes").upload(
            file_name, content, {"upsert": "true"}  # to overwrite
        )
    except:
        raise HTTPException(status_code=500, detail="Couldn't Upload File on Cloud")
    return file_name


def del_file(file_path):
    try:
        supabase.storage.from_("resumes").remove([file_path])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_file_path(file_name):
    url = supabase.storage.from_("resumes").get_public_url(file_name)
    parsed = urlparse(url)
    return parsed.path.split("/resumes/")[-1]


def get_file(filepath: str):

    data = supabase.storage.from_("resumes").download(filepath)
    if not data:
        raise HTTPException(status_code=500, detail="Couldn't Download File from CLoud")
    return data
