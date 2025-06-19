import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from zdt_datagenie.api.datagenie_v0.api import router as datagenie_v0_router

load_dotenv()

root_path = os.getenv("ENV", default="")
app = FastAPI(root_path=f"/{root_path}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add or comment out the following lines of code to include a new version of
# API or deprecate an old version
app.include_router(datagenie_v0_router, prefix="/datagenie/v0")


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
