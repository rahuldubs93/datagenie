from sqlalchemy import text
from zdt_datagenie.core.database.snowflake_connection import execute_query
from zdt_datagenie.core.database.db_config import DatabaseConfig

EXECUTIVES = []
LLM_EXECUTIVES = []
DOSSIER_EXECUTIVES = []
AUTH_LIST = []
USERJID_TO_USERNAME = {}

config = DatabaseConfig()

DBT_DB = config.get_auth_db()
DBT_SCHEMA = config.get_auth_schema()
DBT_TABLE = config.get_auth_table()
MEMBERSHIP_TABLE = config.get_membership_table()


def setup_rbac():
    def add_executives():
        sql = <fetch_executive_users>
        global EXECUTIVES
        EXECUTIVES = execute_query(text(sql), "get_executive_users")[
            "user_jid"
        ].tolist()

    def add_all_users():
        sql = <fetch_all_users>
        global AUTH_LIST

        if AUTH_LIST is None:  # Ensure it's initialized
            AUTH_LIST = []

        general_user_membership = execute_query(text(sql), "get_all_users")
        for index, row in general_user_membership.iterrows():
            user_jid = row["user_jid"]
            AUTH_LIST.append(user_jid)
            user_id = row["user_name"]
            USERJID_TO_USERNAME[user_jid] = user_id

    def add_llm_executives():
        sql = <fetch_llm_users>
        global LLM_EXECUTIVES
        LLM_EXECUTIVES = execute_query(text(sql), "get_llm_executive_users")[
            "user_jid"
        ].tolist()

    def add_dossier_executives():
        sql = <fetch_dossier_users>
        global DOSSIER_EXECUTIVES
        DOSSIER_EXECUTIVES = execute_query(text(sql), "get_dossier_executive_users")[
            "user_jid"
        ].tolist()

    add_executives()
    add_llm_executives()
    add_dossier_executives()
    add_all_users()


setup_rbac()


class PoorMansAuth:
    def __init__(self, signature: str, user_jid: str, intent: str, secret_token: str):
        self.signature = signature
        self.secret_token = secret_token
        self.user_jid = user_jid.lower()
        self.intent = intent.upper()
        self.is_executive = False
        self.is_llm_executive = False
        self.is_dossier_executive = False
        self.is_authorized = False

    def __auth_signature(self):
        return self.signature == self.secret_token

    def get_user_id(self):
        return USERJID_TO_USERNAME[self.user_jid]

    def __is_executive(self):
        self.is_executive = any(
            list(
                filter(
                    lambda userjid: True if userjid in self.user_jid else False,
                    EXECUTIVES,
                )
            )
        )
        return self.is_executive

    def __is_authz(self):
        self.is_authorized = any(
            list(
                filter(
                    lambda userjid: True if userjid in self.user_jid else False,
                    AUTH_LIST,
                )
            )
        )
        return self.is_authorized

    def authorize(self):
        if self.__auth_signature():
            return self.__is_executive or self.__is_authz()

    def __is_llm_executive(self):
        self.is_llm_executive = any(
            list(
                filter(
                    lambda userjid: True if userjid in self.user_jid else False,
                    LLM_EXECUTIVES,
                )
            )
        )
        return self.is_llm_executive

    def llm_authorize(self):
        if self.__auth_signature():
            return self.__is_llm_executive()

    def __is_dossier_executive(self):
        self.is_dossier_executive = any(
            list(
                filter(
                    lambda userjid: True if userjid in self.user_jid else False,
                    DOSSIER_EXECUTIVES,
                )
            )
        )
        return self.is_dossier_executive

    def dossier_authorize(self):
        if self.__auth_signature():
            return self.__is_dossier_executive()
