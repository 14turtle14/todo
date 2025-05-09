import uvicorn
import logging

from app.models import models
from app.routers import targets, tasks, users
from database import engine
from fastapi import FastAPI

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
app = FastAPI()

app.include_router(users.router)
app.include_router(targets.router)
app.include_router(tasks.router)

@app.add_event_handler("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

if __name__ == '__main__':
    uvicorn.run(app)