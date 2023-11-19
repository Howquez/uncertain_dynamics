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

    # Interface
    interface_1 = models.IntegerField(
        doc="Overall, this interface worked very well technically.",
        label="Overall, this interface worked very well technically.",
        widget=widgets.RadioSelect,
        choices=[1, 2, 3, 4, 5, 6, 7])

    interface_2 = models.IntegerField(
        doc="Visually, this interface resembled other interfaces I think highly of.",
        label="Visually, this interface resembled other interfaces I think highly of.",
        widget=widgets.RadioSelect,
        choices=[1, 2, 3, 4, 5, 6, 7])

    interface_3 = models.IntegerField(
        doc="this interface was simple to navigate.",
        label="This interface was simple to navigate.",
        widget=widgets.RadioSelect,
        choices=[1, 2, 3, 4, 5, 6, 7])

    interface_4 = models.IntegerField(
        doc="With this interface, it was very easy to submit my decision.",
        label="With this interface, it was very easy to submit my decision.",
        widget=widgets.RadioSelect,
        choices=[1, 2, 3, 4, 5, 6, 7])

    interface_5 = models.IntegerField(
        doc="This interface allowed me to efficiently communicate my decision.",
        label="This interface allowed me to efficiently communicate my decision.",
        widget=widgets.RadioSelect,
        choices=[1, 2, 3, 4, 5, 6, 7])

    interface_6 = models.IntegerField(
        doc="This interface was somewhat intimidating to me.",
        label="This interface was somewhat intimidating to me.",
        widget=widgets.RadioSelect,
        choices=[1, 2, 3, 4, 5, 6, 7])

    interface_7 = models.IntegerField(
        doc="It scared me to think that I could provide a wrong answer using this interface.",
        label="It scared me to think that I could provide a wrong answer using this interface.",
        widget=widgets.RadioSelect,
        choices=[1, 2, 3, 4, 5, 6, 7])

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
class Interface(Page):
    form_model = "player"

    @staticmethod
    def get_form_fields(player: Player):
        form_fields = ["interface_1", "interface_2", "interface_3", "interface_4", "interface_5", "interface_6",
                       "interface_7"]
        random.shuffle(form_fields)
        return form_fields


class Open_Text(Page):
    form_model = "player"
    form_fields = ['OTF']


class Demographics(Page):
    form_model = "player"
    form_fields = ['age', 'gender']

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


page_sequence = [Interface, Open_Text, Demographics, Debriefing]
