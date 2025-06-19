from typing import Optional

from pydantic import BaseModel


class BotPayload(BaseModel):
    accountId: str
    robotJid: str
    timestamp: int
    userId: str
    userJid: str
    userName: str
    toJid: Optional[str] = None


class BotInstalledPayloadModel(BaseModel):
    is_executive_user: Optional[bool] = False
    is_llm_executive_user: Optional[bool] = False
    is_dossier_executive_user: Optional[bool] = False
    user_id: Optional[str] = None
    event: str
    payload: BotPayload
