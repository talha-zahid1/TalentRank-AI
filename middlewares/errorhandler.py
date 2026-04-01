from fastapi import HTTPException,Request
from starlette.responses import JSONResponse
def httpexception(req:Request,exc:HTTPException):
    return JSONResponse(status_code=exc.status_code,content={"error":exc.detail})
def exceptions(req:Request,exc:exceptions):
    return JSONResponse(status_code=500,content={"error":str(exc)})