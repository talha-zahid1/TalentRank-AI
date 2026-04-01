from fastapi import Depends, HTTPException, APIRouter, Form, UploadFile, File,Request
from schemas.appschema import *
from datetime import datetime
import middlewares as md
from repositries.apprepo import *
import services as sr
from fastapi.responses import RedirectResponse
import urllib.parse as up
import httpx
from pydantic import ValidationError
from typing import List

router = APIRouter()
setting=Settings()
client_id=setting.client_id
client_secret=setting.client_secret
redirect_url=setting.Redirect_url
auth_url=setting.Auth_url
token_url=setting.token_url
user_info_url=setting.user_info_url
@router.get("/")
def wel():
    return{
        "message":"TalentRank AI API is Running Successfully!"
    }
@router.get("/login-with-google")
def login():
    params={
        "client_id":client_id,
        "redirect_uri":redirect_url,
        "response_type":"code",
        "scope":"openid email profile"
    }
    url=auth_url+"?"+up.urlencode(params)
    return RedirectResponse(url)
@router.get("/callback")
async def callback(req:Request):
    code=req.query_params.get("code")
    async with httpx.AsyncClient() as client:
        token_res=await client.post(token_url,data={
            "client_id":client_id,
            "client_secret":client_secret,
            "code":code,
            "grant_type":"authorization_code",
            "redirect_uri":redirect_url
        },
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
            })
        token_data=token_res.json()
        access_token=token_data.get("access_token")
    async with httpx.AsyncClient() as client:
        user_res=await client.get(
            user_info_url,
            headers={
                "Authorization":f"Bearer {access_token}"
            }
        )
        user_data=user_res.json()
        if "error" in user_data:
            raise HTTPException(status_code=400, detail=user_data)
        email=user_data.get("email")
        user=await get_user(email=email)
        
        if not user :
            data={
                "name":user_data.get("name"),
                "role":"user",
                "email":email,
                "password":"Logged In With Google"
            }
            await register_user(user=data)
        token=md.create_token(email=email,role="user")
        
        sr.welcome_email(reciever_email=email)
        return{
            "token":token,
            "type":"Bearer"
        }

@router.post("/register")
async def regis(user: regist):
    row = await get_user(email=user.email)
    if row != None:
        raise HTTPException(status_code=400, detail="User Already Exist")
    hash_passw = sr.hash_pwd(password=user.password)
    role = ""
    if user.role == "recruiter":
        role = user.role
    else:
        role = "user"
    data = {
        "name": user.name,
        "role": role,
        "email": user.email,
        "password": hash_passw,
    }
    user_id = await register_user(user=data)
    if user_id:
        token = md.create_token(email=user.email, role=role)
        sr.welcome_email(reciever_email=user.email)
        return {"token": token, "token_type": "bearer", "user_id": user_id}


@router.post("/login")
async def log(user: logi):
    plnpasw = user.password
    row = await get_user(email=user.email)
    if row == None:
        raise HTTPException(
            status_code=401, detail="invalid User! Please Register First"
        )
    hsh_pwd = row.password
    if sr.verify_password(plain_pass=plnpasw, hashed_pass=hsh_pwd):
        user_id = row.user_id
        token = md.create_token(email=user.email, role=row.role)
        return {"token": token, "token_type": "bearer", "user_id": user_id}
    raise HTTPException(status_code=402, detail="Incorrect Password")


@router.post("/job-post")
async def rec(
    title: str = Form(...),
    description: str = Form(...),
    skills: List[str] = Form(..., multiple=True),
    location: str = Form(...),
    salary: float = Form(...),
    employement_type: str = Form(...),
    experience: str = Form(...),
    deadline: str = Form(...),
    data=Depends(md.rolechecker("recruiter")),
):
    try:
        email = data["email"]
        recruiter = await get_user(email=email)
        Job(
            title=title,
            description=description,
            skills=skills,
            location=location,
            salary=salary,
            employement_type=employement_type,
            experience=experience,
            deadline=deadline,
        )
        detail = {
            "recruiter_id": recruiter.user_id,
            "title": title,
            "description": description,
            "skills": ", ".join(skills),
            "location": location,
            "salary": salary,
            "employement_type": employement_type,
            "experience": experience,
            "deadline": deadline,
        }
        job_id = await add_job_details(details=detail)
        return {"job_id": job_id, "message": "The Job Data Has Been Saved in DB"}
    except ValidationError:
        raise HTTPException(status_code=400, detail="Invalid data")


@router.post("/upload-resumes")
async def appl(file: UploadFile = File(), data=Depends(md.rolechecker("user"))):

    if not (
        file.filename.lower().endswith(".docx")
        or file.filename.lower().endswith(".pdf")
    ):
        raise HTTPException(status_code=400, detail="Invalid file Type")
    email = data["email"]
    user = await get_user(email=email)
    file_name = await sr.upload_resumes(file=file)
    url = sr.get_file_path(file_name=file_name)
    metadata = {
        "file_name": file_name,
        "file_path": url,
        "upload_date": datetime.now().strftime("%I:%M:%p"),
        "candidate_id": user.user_id,
    }
    file_id = await add_metadata(metadata=metadata)
    return {
        "file_id": file_id,
        "message": f"The File {file_name} has been uploaded",
        "metadata": metadata,
    }


@router.post("/parse-resumes/{file_id}/{job_id}")
async def resume_parsing(
    file_id: int, job_id: int, data=Depends(md.rolechecker("recruiter"))
):
    filedata = await get_file_metadata(file_id=file_id)
    filename = filedata.file_name
    file_url = sr.get_file_path(file_name=filename)
    file_in_Bytes = sr.get_file(filepath=file_url)
    fetched_skills: List[str] = []
    if filename.lower().endswith(".pdf"):
        content = sr.pdf_opener(file=file_in_Bytes)
        clean_content = {
            "filename": filename,
            "extracted_text": sr.cleaning_text(text=content),
        }
        fetched_skills = sr.get_skills(resume_text=clean_content.get("extracted_text"))
    elif filename.lower().endswith(".docx"):
        content = sr.python_docx(file=file_in_Bytes)
        clean_content = {
            "filename": filename,
            "extracted_text": sr.cleaning_text(text=content),
        }
        fetched_skills = sr.get_skills(resume_text=clean_content.get("extracted_text"))
    job_details = await get_job_details(job_id=job_id)
    
    skills:List[str] = job_details["skills"].split(",")
    matched_skills = []
    Unmatched_skills = []
    lower_job_skills = []
    lower_cv_skills = []
    for ele in skills:
        lower_job_skills.append(ele.lower().strip())
    for ele in fetched_skills:
        lower_cv_skills.append(ele.lower().strip())

    for skill in lower_cv_skills:
        if skill in lower_job_skills:
            matched_skills.append(skill)
    for skill in lower_job_skills:
        if skill not in lower_cv_skills:
            Unmatched_skills.append(skill)
    
    matched_percentage = (len(matched_skills) / len(skills)) * 100
    unmatched_percentage = (len(Unmatched_skills) / len(skills)) * 100
    docu = {
        "file_id": file_id,
        "job_id": job_id,
        "candidate_id": filedata.candidate_id,
        "job_skills": lower_job_skills,
        "extracted_text": clean_content.get("extracted_text"),
        "matched_skills": matched_skills,
        "matched_percentage": matched_percentage,
    }
    sr.add_into_es(doc=docu)
    return {
        "matched_percentage": matched_percentage,
        "matched_skills": matched_skills,
        "unmatched_percentage": unmatched_percentage,
        "unmatched_skills": Unmatched_skills,
    }


@router.get("/job-posts")
async def job_posts(data=Depends(md.rolechecker("user"))):
    return await get_job_posts()


@router.get("/resume-searching/{job_id}")
def filtering(job_id: int, data=Depends(md.rolechecker("recruiter"))):
    documents = sr.get_documents(job_id=job_id)
    return documents


@router.get("/my-resumes")
async def get_my_app(data=Depends(md.rolechecker("user"))):
    user = await get_user(email=data.get("email"))
    return await get_all_files_metadata(user_id=user.user_id)


@router.delete("/del-resume/{file_id}")
async def del_res(file_id: int, data=Depends(md.rolechecker("user"))):
    user = await get_user(email=data.get("email"))
    file_data = await get_file_metadata(file_id=file_id)
    if file_data.candidate_id != user.user_id:
        raise HTTPException(status_code=403, detail="Not allowed")
    file_path = sr.get_file_path(file_name=file_data.file_name)
    await del_docu(file_id=file_id)
    sr.del_file(file_path=file_path)
    sr.del_frm_es(file_id=file_id)
    return {
        "message":"resume has been deleted",
        "resume_id":file_id
    }


@router.post("/apply-job/{job_id}")
async def apply(job_id: int, data=Depends(md.rolechecker("user"))):
    user = await get_user(email=data.get("email"))
    status = await get_app_data(user_id=user.user_id, job_id=job_id)
    if status:
        raise HTTPException(status_code=409, detail="Already Applied for this job")
    resume_up_status = await resume_uploaded(user_id=user.user_id)
    if not resume_up_status:
        raise HTTPException(status_code=400, detail="Resume Not uploaded")
    data = {"user_id": user.user_id, "job_id": job_id}
    app_id = await add_app_data(data=data)
    return {"application_id": app_id, "message": "The application has been recorded"}


@router.delete("/del-job/{job_id}")
async def del_res(job_id: int, data=Depends(md.rolechecker("recruiter"))):
    job = await get_job_details(job_id=job_id)
    user = await get_user(email=data.get("email"))
    if job.recruiter_id != user.user_id:
        raise HTTPException(status_code=403, detail="Not allowed")
    await del_job_data(job_id=job_id)
    return {
        "message":"Job Post  has been deleted",
        "job_id":job_id
    }
@router.get('/send-selection-email/{user_email}')
def send_sel_email(user_email:str,data=Depends(md.rolechecker("recruiter"))):
    sr.job_selection_email(user_email)
    return {"message": "Selection email sent"}