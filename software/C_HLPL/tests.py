from otree.api import Currency as c, currency_range
from . import *
from otree.api import Bot

import random


class PlayerBot(Bot):
    def play_round(self):
        yield HLPL_Decision, dict(choice_1="lottery",
                                             choice_2="lottery",
                                             choice_3="lottery",
                                             choice_4="lottery",
                                             choice_5="lottery",
                                             choice_6= random.choice(["lottery", "certainty"]),
                                             choice_7="certainty",
                                             choice_8="certainty",
                                             choice_9="certainty",
                                             choice_10="certainty",
                                             choice_11="certainty")
