import databases
from schemas.appschema import *
settings=Settings()
url=f"postgresql+asyncpg://{settings.DB_Username}:{settings.DB_password}@localhost:{settings.DB_portNumber}/{settings.DB_Name}"
db=databases.Database(url=url)