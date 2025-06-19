from jinja2 import Template

from zdt_datagenie.core.model.bot_response import generate_response, BotResponseModel
from zdt_datagenie.core.strategy.base_cmd import Command

INTENT = "help"


class HelpCommand(Command):
    def __init__(self, payload):
        self.__payload = payload
        self.__template = Template(self.template(INTENT))

    def execute(self) -> BotResponseModel:
        self.__payload.payload.toJid = self.__payload.payload.userJid
        msg = self.__template.render()
        return generate_response(
            self.__payload, "Greetings from Data Genie", msg, is_command_required=False
        )
