from __future__ import annotations

from zdt_datagenie.core.strategy.account_info_cmd import AccountInfoCommand
from zdt_datagenie.core.strategy.adoption_cmd import AdoptionCommand
from zdt_datagenie.core.strategy.customer_cmd import CustomerInfoCommand
from zdt_datagenie.core.strategy.help_cmd import HelpCommand
from zdt_datagenie.core.strategy.risk_cmd import RiskCommand
from zdt_datagenie.core.strategy.usage_cmd import UsageCommand
from zdt_datagenie.core.strategy.submit_question_cmd import SubmitQuesCommand
from zdt_datagenie.core.strategy.opportunity_cmd import OpportunityCommand
from zdt_datagenie.core.strategy.support_cmd import SupportCommand
from zdt_datagenie.core.strategy.create_dossier_cmd import CreateDossierCommand


class Context:
    """
    Command selector
    """

    COMMANDS = {
        "HELP": HelpCommand,
        "RISK": RiskCommand,
    }

    @staticmethod
    def get_command_handler(cmd: str):
        for key in Context.COMMANDS:
            if key == cmd.upper():
                return Context.COMMANDS[key]
        raise Exception("Unknown Command!")
