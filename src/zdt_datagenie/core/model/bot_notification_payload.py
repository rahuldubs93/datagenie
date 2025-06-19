from typing import Optional

from pydantic import BaseModel


class BotPayload(BaseModel):
    accountId: str
    channelName: str
    cmd: str
    robotJid: str
    timestamp: int
    toJid: str
    triggerId: str
    userId: str
    userJid: str
    userName: str


class BotNotificationPayloadModel(BaseModel):
    is_executive_user: Optional[bool] = False
    is_llm_executive_user: Optional[bool] = False
    is_dossier_executive_user: Optional[bool] = False
    user_id: Optional[str] = None
    event: str
    payload: BotPayload
