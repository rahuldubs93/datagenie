from fastapi import APIRouter
import os
from zdt_datagenie.api.datagenie_v0.endpoints import query

router = APIRouter()


@router.get("")
async def root():
    return {
        "Application": "Data Genie",
        "Environment": os.getenv("environment", default="dev"),
    }


router.include_router(query.router)
