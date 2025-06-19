from typing import List, Optional

from pydantic import BaseModel


class ActionItem(BaseModel):
    text: str
    value: str
    action: str


class SubHead(BaseModel):
    text: str


class Head(BaseModel):
    sub_head: Optional[SubHead] = None
    text: str


class Item(BaseModel):
    style: str
    text: str
    value: str


class BodyItem(BaseModel):
    text: Optional[str] = None
    type: str
    items: Optional[List[Item]] = None


class Original(BaseModel):
    head: Head
    body: List[BodyItem]


class Payload(BaseModel):
    accountId: str
    actionItem: ActionItem
    channelName: str
    messageId: str
    original: Original
    robotJid: str
    timestamp: int
    toJid: str
    triggerId: str
    userId: str
    userJid: str
    userName: str


class InteractiveMessageActionModel(BaseModel):
    is_executive_user: Optional[bool] = False
    is_llm_executive_user: Optional[bool] = False
    is_dossier_executive_user: Optional[bool] = False
    user_id: Optional[str] = None
    event: str
    payload: Payload
