from jinja2 import Template
from sqlalchemy import text

from zdt_datagenie.core.database.snowflake_connection import execute_query
from zdt_datagenie.core.model.interactive_message_action_payload import (
    InteractiveMessageActionModel,
)
from zdt_datagenie.core.model.bot_response import generate_response, BotResponseModel
from zdt_datagenie.core.strategy.base_cmd import Command
from zdt_datagenie.core.utils.logger import get_logger
from zdt_datagenie.core.database.db_config import DatabaseConfig

INTENT = "risk"

logger = get_logger(INTENT)
config = DatabaseConfig()

DBT_DB = config.get_db()
DBT_SCHEMA = config.get_schema()
DBT_TABLE = config.get_table()


class RiskCommand(Command):
    def __init__(self, payload: InteractiveMessageActionModel):
        self.__payload = payload
        self.__customer = payload.payload.object.original.head.text.strip("*")
        self.__sql = self.sql(INTENT)
        self.__template = Template(self.template(INTENT))

    def execute(self) -> BotResponseModel:
        try:
            unquoted_customer = self.__customer.replace("'", "")
            risk_query = self.__sql.replace("${customer}", unquoted_customer)
            risk_query = risk_query.replace("${DBT_DB}", DBT_DB)
            risk_query = risk_query.replace("${DBT_SCHEMA}", DBT_SCHEMA)
            risk_query = risk_query.replace("${DBT_TABLE}", DBT_TABLE)
            risk_query = text(risk_query)
            df = execute_query(risk_query, INTENT).head(1)
            if len(df) == 0:
                return generate_response(
                    self.__payload,
                    self.__customer,
                    "Risk data does not exist for the customer!",
                    is_command_required=False,
                )
            risk = df["risk"][0]
            explainability = df["explainability"][0]
            msg = self.__template.render(risk=risk, explainability=explainability)
            command_required = True
        except Exception as e:
            logger.error(e)
            msg = "There was an internal server error. Please contact the administrator for help!"
            command_required = False
        return generate_response(
            self.__payload, self.__customer, msg, is_command_required=command_required
        )
