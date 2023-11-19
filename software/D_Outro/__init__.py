from otree.api import *
import random

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'D_Outro'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    completed_survey = models.BooleanField(doc="indicates whether a participant has completed the survey.",
                                           initial=False,
                                           blank=True)

    # Demographics
    age = models.IntegerField(label="Please enter your age",
                              min=18,
                              max=99)

    gender = models.IntegerField(
        label="Please select your gender.",
        choices=[
            [1, "Female"],
            [2, "Male"],
            [3, "Other"],
            [4, "Prefer not to say"],
        ]
    )

    # OTF
    OTF = models.LongStringField(
        label="Did you encounter any difficulties answering the study or do you have any comments?", blank=False)


# PAGES
class Open_Text(Page):
    form_model = "player"
    form_fields = ['OTF']

    @staticmethod
    def is_displayed(player):
        return player.participant.is_dropout == False


class Demographics(Page):
    form_model = "player"
    form_fields = ['age', 'gender']

    @staticmethod
    def is_displayed(player):
        return player.participant.is_dropout == False

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.finished = True
        player.completed_survey = player.participant.finished


class Debriefing(Page):
    form_model = 'player'

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            final_payoff=player.participant.payoff_plus_participation_fee().to_real_world_currency(player.session),
        )


page_sequence = [Open_Text, Demographics, Debriefing]
