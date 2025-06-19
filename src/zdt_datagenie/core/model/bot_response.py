from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel

from zdt_datagenie.core.model.interactive_message_action_payload import InteractiveMessageActionModel
from zdt_datagenie.core.model.on_click_submit_payload import OnClickSubmitModel


class Settings(BaseModel):
    form: bool
    form_id: str


class SubHead(BaseModel):
    text: str


class Head(BaseModel):
    type: str
    text: str
    sub_head: Optional[SubHead] = None


class Item(BaseModel):
    text: str
    value: str
    style: str
    submit: bool


class InitialOption(BaseModel):
    value: str
    text: str


class Option(BaseModel):
    value: str
    text: str
    style: Optional[str] = None


class SectionItems(BaseModel):
    type: str
    text: Optional[str] = None
    items: Optional[List[Option]] = None


class BodyItem1(BaseModel):
    type: str
    text: Optional[str] = None
    items: Optional[List[Item]] = None
    action_id: Optional[str] = None
    initial_option: Optional[InitialOption] = None
    options: Optional[List[Option]] = None
    placeholder: Optional[str] = None
    value: Optional[int] = None
    layout: Optional[str] = None
    sections: Optional[List[SectionItems]] = None


class Page(BaseModel):
    pageNo: int
    body: List[BodyItem1]


class BodyItem(BaseModel):
    type: str
    cur_page: int
    pages: List[Page]


class Content(BaseModel):
    settings: Settings
    head: Head
    body: List[BodyItem]


class Model(BaseModel):
    Content: Content


class BotResponseModel(BaseModel):
    robot_jid: str
    to_jid: str
    user_jid: str
    account_id: str
    visible_to_user: Optional[bool] = True
    content: Content
    is_markdown_support: bool = True


def generate_response(
    payload, customer: str, msg: str, is_command_required: bool = True
) -> BotResponseModel:

    sub_head = SubHead(text=payload.payload.object.submit_items[0].actionItem.value)
    head = Head(type="message", text=f"*{customer}*", sub_head=sub_head)

    settings = Settings(form=True, form_id="customizeValue")

    body_item_list1 = []

    message = BodyItem1(type="message", text=msg)
    body_item_list1.append(message)

    if is_command_required:
        action_groups_default = {
            "group1": ["Usage", "Adoption", "Support"],
            "group2": ["Oppty", "Risk", "Acct Team"],
        }

        for group in action_groups_default.values():
            items_list = [Item(value=item, style="Primary", text=item, submit=True) for item in group]
            body_item_list1.append(BodyItem1(type="actions", items=items_list))

            if payload.is_dossier_executive_user:

                dossier_section = [SectionItems(type="message", text="🔍 *For Account Research :*")]
                dossier_section.append(SectionItems(type="actions", items=[Option(text="Generate Acct Report", value="Generate Acct Report", style="Primary")]))
                body_item_list1.append(BodyItem1(type="section", layout="vertical", sections=dossier_section))

            if payload.is_llm_executive_user:

                body_item_list1.append(BodyItem1(type="message", text="Do you have other questions ? <https://docs.google.com/document/d/1-UFI326azW1cCznH2_3DlkhOolyATgrUDiJMzoBTpP8/edit|(Sample questions)> *BETA "))
                body_item_list1.append(BodyItem1(type="plain_text_input", action_id="query_submit_action", text="", placeholder="Type your questions here."))
                body_item_list1.append(BodyItem1(type="actions", items=[Item(value="Submit Question", style="Primary", text="Submit Question", submit=True)]))

    pages = [Page(pageNo=1, body=body_item_list1)]
    body_item = [BodyItem(type="page", cur_page=1, pages=pages)]
    content = Content(settings=settings, head=head, body=body_item)

    response_model = BotResponseModel(
        robot_jid=payload.payload.robotJid if payload.event in ("bot_notification", "interactive_message_actions") else payload.payload.object.robot_jid,
        to_jid=payload.payload.toJid if payload.event in ("bot_notification", "interactive_message_actions") else payload.payload.object.to_jid,
        user_jid=payload.payload.userJid if payload.event in ("bot_notification", "interactive_message_actions") else payload.payload.object.user_jid,
        account_id=payload.payload.accountId if payload.event in ("bot_notification", "interactive_message_actions") else payload.payload.account_id,
        content=content,
    )
    return response_model


def generate_response_multiple_accounts(
    payload, customer: str, msg: str, account_list
) -> BotResponseModel:
    sub_head = (
        SubHead(text=payload.payload.actionItem.text)
        if isinstance(payload, InteractiveMessageActionModel)
        else None
    )
    head = Head(type="message", text=f"*{customer}*", sub_head=sub_head)

    settings = Settings(form=True, form_id="customizeValue")

    body_item_list1 = []

    message = BodyItem1(type="message", text=msg)
    body_item_list1.append(message)

    radio_button_values = []
    for account in account_list:
        radio_button_values.append(Option(value=account, text=account))
    initial = InitialOption(value=account_list[0], text=account_list[0])
    body_item_list1.append(BodyItem1(type="radio_buttons", initial_option=initial, options=radio_button_values, action_id="radio_buttons123"))

    items_list = [Item(value="Submit", style="Primary", text="Submit", submit=True)]
    body_item_list1.append(BodyItem1(type="actions", items=items_list))

    pages = [Page(pageNo=1, body=body_item_list1)]
    body_item = [BodyItem(type="page", cur_page=1, pages=pages)]
    content = Content(settings=settings, head=head, body=body_item)

    response_model = BotResponseModel(
        robot_jid=payload.payload.robotJid if payload.event == "bot_notification" else payload.payload.object.robot_jid,
        to_jid=payload.payload.toJid if payload.event == "bot_notification" else payload.payload.object.to_jid,
        user_jid=payload.payload.userJid if payload.event == "bot_notification" else payload.payload.object.user_jid,
        account_id=payload.payload.accountId if payload.event == "bot_notification" else payload.payload.account_id,
        content=content,
    )
    return response_model


def generate_static_response(payload, customer: str, msg: str) -> BotResponseModel:
    sub_head = SubHead(text='Submit Question')
    head = Head(type="message", text=f"*{customer}*", sub_head=sub_head)

    settings = Settings(form=True, form_id="customizeValue")

    body_item_list1 = []

    message = BodyItem1(type="message", text=msg)
    body_item_list1.append(message)

    pages = [Page(pageNo=1, body=body_item_list1)]
    body_item = [BodyItem(type="page", cur_page=1, pages=pages)]
    content = Content(settings=settings, head=head, body=body_item)

    response_model = BotResponseModel(
        robot_jid=payload["payload"]["object"]["robot_jid"],
        to_jid=payload["payload"]["object"]["to_jid"],
        user_jid=payload["payload"]["object"]["user_jid"],
        account_id=payload["payload"]["account_id"],
        content=content,
    )

    return response_model
