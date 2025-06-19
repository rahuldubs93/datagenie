import os


class DatabaseConfig:
    def __init__(self):
        self.env = os.getenv("environment").lower()
        self.DBT_DB = None
        self.DBT_SCHEMA = None
        self.DBT_TABLE = None
        self._set_configs()

    def _set_configs(self):
        if self.env == "dev":
            self.DBT_DB = ""
            self.DBT_SCHEMA = ""
            self.DBT_TABLE = ""
            self.LLM_DBT_DB = ""
            self.LLM_DBT_SCHEMA = ""
            self.LLM_DBT_TABLE = ""
            self.AUTH_DB = ""
            self.AUTH_SCHEMA = ""
            self.AUTH_TABLE = ""
            self.MEMBERSHIP_TABLE = ""
        elif self.env == "prego":
            self.DBT_DB = ""
            self.DBT_SCHEMA = ""
            self.DBT_TABLE = ""
            self.LLM_DBT_DB = ""
            self.LLM_DBT_SCHEMA = ""
            self.LLM_DBT_TABLE = ""
            self.AUTH_DB = ""
            self.AUTH_SCHEMA = ""
            self.AUTH_TABLE = ""
            self.MEMBERSHIP_TABLE = ""
        elif self.env == "go":
            self.DBT_DB = ""
            self.DBT_SCHEMA = ""
            self.DBT_TABLE = ""
            self.LLM_DBT_DB = ""
            self.LLM_DBT_SCHEMA = ""
            self.LLM_DBT_TABLE = ""
            self.AUTH_DB = ""
            self.AUTH_SCHEMA = ""
            self.AUTH_TABLE = ""
            self.MEMBERSHIP_TABLE = ""
        else:
            # default values
            self.DBT_DB = ""
            self.DBT_SCHEMA = ""
            self.DBT_TABLE = ""
            self.LLM_DBT_DB = ""
            self.LLM_DBT_SCHEMA = ""
            self.LLM_DBT_TABLE = ""
            self.AUTH_DB = ""
            self.AUTH_SCHEMA = ""
            self.AUTH_TABLE = ""
            self.MEMBERSHIP_TABLE = ""

    def get_db(self):
        return self.DBT_DB

    def get_schema(self):
        return self.DBT_SCHEMA

    def get_table(self):
        return self.DBT_TABLE

    def get_db(self):
        return self.LLM_DBT_DB

    def get_schema(self):
        return self.LLM_DBT_SCHEMA

    def get_table(self):
        return self.LLM_DBT_TABLE

    def get_auth_db(self):
        return self.AUTH_DB

    def get_auth_schema(self):
        return self.AUTH_SCHEMA

    def get_auth_table(self):
        return self.AUTH_TABLE

    def get_membership_table(self):
        return self.MEMBERSHIP_TABLE
