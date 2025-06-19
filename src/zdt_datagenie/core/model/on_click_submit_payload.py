from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class InitialOption(BaseModel):
    text: str
    value: str


class Option(BaseModel):
    text: str
    value: str


class Item(BaseModel):
    style: str
    submit: bool
    text: str
    value: str


class BodyItem1(BaseModel):
    text: Optional[str] = None
    type: str
    action_id: Optional[str] = None
    initial_option: Optional[InitialOption] = None
    options: Optional[List[Option]] = None
    items: Optional[List[Item]] = None


class Page(BaseModel):
    body: List[BodyItem1]
    pageNo: int


class BodyItem(BaseModel):
    cur_page: int
    pages: List[Page]
    type: str


class Head(BaseModel):
    text: str
    type: str


class Settings(BaseModel):
    form: bool
    form_id: str


class Original(BaseModel):
    body: List[BodyItem]
    head: Head
    settings: Settings


class ActionItem(BaseModel):
    text: str
    value: str
    action: str


class RadioButtonsItem(BaseModel):
    value: str
    text: str
    action_id: str


class PlainTextInput(BaseModel):
    text: str
    value: str
    action_id: str


class SubmitItem(BaseModel):
    actionItem: Optional[ActionItem] = None
    radio_buttons_item: Optional[RadioButtonsItem] = None
    plain_text_input: Optional[PlainTextInput] = None


class Object(BaseModel):
    bot_msg_id: str
    date_time: str
    id: str
    msg_time: int
    original: Original
    robot_jid: str
    submit_form_id: str
    submit_items: List[SubmitItem]
    timestamp: int
    to_jid: str
    trigger_id: str
    type: str
    user_jid: str


class Payload(BaseModel):
    account_id: str
    object: Object
    operator_id: str


class OnClickSubmitModel(BaseModel):
    is_executive_user: Optional[bool] = False
    is_llm_executive_user: Optional[bool] = False
    is_dossier_executive_user: Optional[bool] = False
    user_id: Optional[str] = None
    event: str
    event_ts: int
    payload: Payload
