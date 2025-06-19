import hmac
import hashlib
import os
import json
from datetime import datetime
from timeit import default_timer as timer
from fastapi import APIRouter, status, Request, Depends, HTTPException

from zdt_datagenie.core.authz.poor_mans_auth import PoorMansAuth, setup_rbac
from zdt_datagenie.core.model.bot_installed_payload import BotInstalledPayloadModel
from zdt_datagenie.core.model.bot_notification_payload import BotNotificationPayloadModel
from zdt_datagenie.core.model.on_click_submit_payload import OnClickSubmitModel
from zdt_datagenie.core.model.bot_response import BotResponseModel
from zdt_datagenie.core.model.interactive_message_action_payload import InteractiveMessageActionModel
from zdt_datagenie.core.strategy.context import Context
from zdt_datagenie.core.utils.external_api_call import send_chatbot_message, chatbot_auth_token, update_chatbot_message
from zdt_datagenie.core.utils.logger import get_logger
from zdt_datagenie.core.model.bot_response import generate_static_response

router = APIRouter(prefix="/bot", tags=["Bot"])

BOT_INSTALLED_EVENT = "bot_installed"
BOT_NOTIFICATION_EVENT = "bot_notification"
INTERACTIVE_MESSAGE_ACTION_EVENT = "interactive_message_actions"
HELP_COMMAND = "HELP"
CUSTOMER_COMMAND = "CUSTOMER"
SUBMIT_EVENT = "chat_message.submit"

logger = get_logger("datagenie_query")

# cache the chatbot auth token
chatbot_token = None


# -- Auth logic code start --
async def get_secret_auth(request: Request):
    return request.headers.get("x-zm-signature")


async def get_secret_ts(request: Request):
    return request.headers.get("x-zm-request-timestamp")


# -- Auth logic code end --
async def get_payload(request: Request):
    return await request.json()


@router.post("", status_code=status.HTTP_200_OK, response_model=BotResponseModel)
async def root(
    json_payload: bytes = Depends(get_payload), secret_ts: str = Depends(get_secret_ts), secret_auth_token: str = Depends(get_secret_auth)
):
    global chatbot_token
    start = timer()
    event = json_payload["event"]
    user_jid = json_payload["payload"]["userJid"]

    if event == BOT_INSTALLED_EVENT:
        payload_model = BotInstalledPayloadModel.model_validate(json_payload)
        intent = HELP_COMMAND
    elif event == BOT_NOTIFICATION_EVENT:
        payload_model = BotNotificationPayloadModel.model_validate(json_payload)
        intent = (
            HELP_COMMAND
            if HELP_COMMAND in payload_model.payload.cmd.upper()
            else CUSTOMER_COMMAND
        )
    elif event == INTERACTIVE_MESSAGE_ACTION_EVENT:
        payload_model = InteractiveMessageActionModel.model_validate(json_payload)
        intent = payload_model.payload.actionItem.text
    elif event == SUBMIT_EVENT:
        payload_model = OnClickSubmitModel.model_validate(json_payload)
        intent = (
            CUSTOMER_COMMAND if payload_model.payload.object.submit_items[0].actionItem.value.upper() == 'SUBMIT'
            else payload_model.payload.object.submit_items[0].actionItem.value.upper()
        )
    else:
        raise HTTPException(400, "Unknown Bot Message...")

    # Auth Logic Code
    crypto_message = f"v0:{secret_ts}:{json.dumps(json_payload, separators=(',', ':'), ensure_ascii=False)}"
    crypto_key = os.getenv("secret_authorization")
    hmac_hash = hmac.new(crypto_key.encode(), crypto_message.encode(), hashlib.sha256).hexdigest()
    signature = f"v0={hmac_hash}"
    poor_man_authz = PoorMansAuth(signature, user_jid, intent, secret_auth_token)

    if not poor_man_authz.authorize():
        raise HTTPException(403, "Access denied!")

    payload_model.is_executive_user = poor_man_authz.is_executive
    payload_model.user_id = poor_man_authz.get_user_id()
    payload_model.is_llm_executive_user = poor_man_authz.llm_authorize()
    payload_model.is_dossier_executive_user = poor_man_authz.dossier_authorize()

    # refresh the chatbot auth token
    chatbot_token = chatbot_token if chatbot_token else await chatbot_auth_token()

    if intent == "SUBMIT QUESTION":

        customer = json_payload["payload"]["object"]["original"]["head"]["text"]
        message = 'Processing request...'
        message_id = ""

        cmd_response = generate_static_response(json_payload, customer, message)
        cmd_response_as_json = cmd_response.model_dump(mode="json")
        try:
            message_id = await send_chatbot_message(cmd_response_as_json, chatbot_token)
        except HTTPException as e:
            if e.status_code == 401:
                chatbot_token = await chatbot_auth_token()
                message_id = await send_chatbot_message(cmd_response_as_json, chatbot_token)
            else:
                logger.critical(e)

        cmd_strategy = Context.get_command_handler(intent)
        cmd_response = cmd_strategy(payload_model).execute()
        cmd_response_as_json = cmd_response.model_dump(mode="json")
        try:
            await update_chatbot_message(cmd_response_as_json, chatbot_token, message_id)
        except HTTPException as e:
            if e.status_code == 401:
                chatbot_token = await chatbot_auth_token()
                await update_chatbot_message(cmd_response_as_json, chatbot_token, message_id)
            else:
                cmd_response = generate_static_response(json_payload, customer, "Internal Error... Please try again")
                cmd_response_as_json = cmd_response.model_dump(mode="json")
                await update_chatbot_message(cmd_response_as_json, chatbot_token, message_id)
                logger.critical(f"Exception encountered : {e}")
        except Exception as e:
            cmd_response = generate_static_response(json_payload, customer, "Internal Error... Please try again")
            cmd_response_as_json = cmd_response.model_dump(mode="json")
            await update_chatbot_message(cmd_response_as_json, chatbot_token, message_id)
            logger.critical(f"Exception encountered : {e}")

    else:
        cmd_strategy = Context.get_command_handler(intent)
        cmd_response = cmd_strategy(payload_model).execute()
        cmd_response_as_json = cmd_response.model_dump(mode="json")

    # send the response to chatbot
        try:
            await send_chatbot_message(cmd_response_as_json, chatbot_token)
        except HTTPException as e:
            if e.status_code == 401:
                chatbot_token = await chatbot_auth_token()
                await send_chatbot_message(cmd_response_as_json, chatbot_token)
            else:
                logger.critical(f"Exception encountered : {e}")
        except Exception as e:
            logger.critical(f"Exception encountered : {e}")

    end = timer()
    logger.critical(f"API took {(end - start)} secs to respond")
    return cmd_response


@router.get("", status_code=status.HTTP_200_OK)
async def init(request: Request):
    setup_rbac()
    return {"Status": "Success"}
