import databases
from schemas.appschema import *
settings=Settings()
url=settings.DATABASE_URL_ASYNC
db=databases.Database(url=url)