from fastapi import FastAPI
from dbcon import db
from routes.approuters import router
from middlewares.errorhandler import*
app=FastAPI()
app.include_router(router=router)
app.add_exception_handler(Exception,exceptions)
app.add_exception_handler(HTTPException,httpexception)
@app.on_event("startup")
async def con():
    await db.connect()
    print("DataBase has been connected")
@app.on_event("shutdown")
async def discon():
    print("DataBase has been disconnected")
    await db.disconnect()