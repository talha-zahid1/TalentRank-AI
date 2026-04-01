from models.appmodel import *
from fastapi import HTTPException
from dbcon import db


async def register_user(user):
    query = users.insert().values(
        name=user["name"],
        role=user["role"],
        email=user["email"],
        password=user["password"],
    )
    user_id = await db.execute(query=query)
    return user_id


async def get_user(email: str):
    query = users.select().where(users.c.email == email)
    row = await db.fetch_one(query=query)
    return row



async def add_job_details(details):
    query = job_detail.insert().values(
        recruiter_id=details["recruiter_id"],
        job_title=details["title"],
        job_description=details["description"],
        skills=details["skills"],
        location=details["location"],
        salary=details["salary"],
        employement_type=details["employement_type"],
        experience=details["experience"],
        deadline=details["deadline"],
    )
    job_id = await db.execute(query=query)
    return job_id


async def add_metadata(metadata):
    query = document_details.insert().values(
        file_name=metadata["file_name"],
        file_path=metadata["file_path"],
        upload_date=metadata["upload_date"],
        candidate_id=metadata["candidate_id"],
    )
    file_id = await db.execute(query=query)
    return file_id


async def get_app_data(user_id, job_id):
    query = applications.select().where(
        (applications.c.a_user_id == user_id) & (applications.c.a_job_id == job_id)
    )
    return await db.fetch_one(query=query)

from datetime import datetime
async def add_app_data(data):
    query = applications.insert().values(
        a_user_id=data.get("user_id"), a_job_id=data.get("job_id"),applied_at=datetime.utcnow()
    )
    return await db.execute(query=query)


async def resume_uploaded(user_id):
    query = document_details.select().where(document_details.c.candidate_id == user_id)
    return await db.fetch_one(query=query)


async def get_file_metadata(file_id):
    queryy = document_details.select().where(document_details.c.file_id == file_id)
    row = await db.fetch_one(query=queryy)
    if not row:
        raise HTTPException(status_code=400,detail="resume not uploaded")
    return row


async def get_all_files_metadata(user_id):
    queryy = document_details.select().where(document_details.c.candidate_id == user_id)
    rows = await db.fetch_all(query=queryy)
    return rows


async def del_docu(file_id):
    query = document_details.delete().where(document_details.c.file_id == file_id)
    return await db.execute(query=query)


async def get_job_posts():
    query = job_detail.select()
    return await db.fetch_all(query=query)


async def del_job_data(job_id):
    query = job_detail.delete().where(job_detail.c.job_id == job_id)
    return await db.execute(query=query)


async def get_job_details(job_id):
    query = job_detail.select().where(job_detail.c.job_id == job_id)
    row=await db.fetch_one(query=query)

    if not row:
        raise HTTPException(status_code=400,detail="Job Doesnot exist")
    return row
