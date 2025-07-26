import uvicorn
import logging

from routers import auth, targets, tasks, users
from database.database import startup
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://frontend:8080", 
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(targets.router)
app.include_router(tasks.router)
app.include_router(auth.router)
app.add_event_handler("startup", startup)


if __name__ == '__main__':
    uvicorn.run(app)