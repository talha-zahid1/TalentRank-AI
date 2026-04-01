from pydantic import BaseModel,constr,confloat
from pydantic_settings import BaseSettings,SettingsConfigDict
from typing import List
class Settings(BaseSettings):
    AI_API_KEY:str
    supabase_url:str
    service_role_key:str
    DB_Username:str
    DB_password:str
    DB_portNumber:str
    DB_Name:str
    client_id:str
    client_secret:str
    Redirect_url:str
    Auth_url:str
    Elastic_endpoint:str
    Elastic_apiKey:str
    token_url:str
    user_info_url:str
    google_acc_password:str
    s_email:str
    model_config=SettingsConfigDict(env_file=r"C:\Users\TECHNEZO\OneDrive\Desktop\backendproj\.env", env_file_encoding='utf-8')
class logi(BaseModel):
    email:str
    role:str
    password:str
class regist(logi):
    name:str
    
class Job(BaseModel):
    title: str
    description: str
    skills:List[str]
    location:str
    salary: float
    employement_type:str
    experience:str
    deadline:str