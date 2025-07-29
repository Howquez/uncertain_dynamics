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

    # Covariates
    comprehension_1 = models.IntegerField(
        doc="Overall, I understood the rules of the first task well.",
        label="Insgesamt habe ich die Regeln der ersten Aufgabe (d.h. der Allokationsstudie) gut verstanden.",
        widget=widgets.RadioSelect,
        choices=[1, 2, 3, 4, 5, 6, 7])

    comprehension_2 = models.IntegerField(
        doc="Overall, I understood the rules of the second task well.",
        label="Insgesamt habe ich die Regeln der zweiten (risikobezogenen) Aufgabe gut verstanden.",
        widget=widgets.RadioSelect,
        choices=[1, 2, 3, 4, 5, 6, 7])


    # Demographics
    age = models.IntegerField(label="Bitte geben Sie Ihr Alter ein",
                              min=18,
                              max=99)

    gender = models.IntegerField(
        label="Bitte wählen Sie Ihr Geschlecht aus.",
        choices=[
            [1, "Weiblich"],
            [2, "Männlich"],
            [3, "Andere"],
            [4, "Möchte ich nicht angeben"],
        ]
    )

    # OTF
    OTF = models.LongStringField(
        label="Haben Sie Anmerkungen oder hatten Sie Schwierigkeiten bei der Beantwortung der Studie?", blank=True)

    # gen AI
    genAI = models.StringField(
        doc="Did you use ChatGPT or any other generative AI to better understand the instructions? (Note: we will not reject your submission, if you did. We need the information to assess our overall data quality.)",
        label="Haben Sie ChatGPT oder eine andere generative KI verwendet, um die Instruktionen besser zu verstehen? (Hinweis: Wir werden Ihre Einreichung nicht ablehnen, falls Sie es getan haben. Wir benötigen diese Information, um unsere Datenqualität zu bewerten.)",
        widget=widgets.RadioSelect,
        choices=["Ja", "Nein"],
        blank=False)

    genAI_OTF = models.LongStringField(
        label="Falls ja, hat die KI Ihnen Empfehlungen gegeben, was Sie tun sollen? Sind Sie der Empfehlung gefolgt?", blank=True)

# PAGES
class Open_Text(Page):
    form_model = "player"
    form_fields = ['OTF']

    @staticmethod
    def is_displayed(player):
        if player.participant.is_dropout == False:
            if player.participant.waited_too_long == False:
                return True
            else:
                return False
        else:
            return False

class Covariates(Page):
    form_model = "player"
    form_fields = ['comprehension_1', 'comprehension_2']

    @staticmethod
    def is_displayed(player):
        if player.participant.is_dropout == False:
            if player.participant.waited_too_long == False:
                return True
            else:
                return False
        else:
            return False

class Demographics(Page):
    form_model = "player"
    form_fields = ['age', 'gender', 'genAI', 'genAI_OTF']

    @staticmethod
    def is_displayed(player):
        if player.participant.is_dropout == False:
            if player.participant.waited_too_long == False:
                return True
            else:
                return False
        else:
            return False


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


page_sequence = [Open_Text, Covariates, Demographics, Debriefing]
