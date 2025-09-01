from otree.api import *
import time

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'A_Intro'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    EARNINGS_TEMPLATE = "A_Intro/C_Earnings.html"
    SHOCKS_TEMPLATE = "A_Intro/D_Shocks.html"
    DEMO_TEMPLATE = "A_Intro/E_Demo.html"
    PRIVACY_TEMPLATE = "A_Intro/T_Privacy.html"
    CALCULATOR_TEMPLATE = "A_Intro/T_Calculator.html"



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    formula_shown = models.BooleanField(doc="True if participant wanted to see the formula that explains earnings.",
                                        initial=False)

    CQ_1 = models.BooleanField(label='Wie viel Geld können Sie in diesem Experiment verdienen?',
                               choices=[
                                   [False, 'Genau die feste Teilnahmegebühr.'],
                                   [True, 'Das hängt von meinen Entscheidungen und den Entscheidungen anderer ab.'],
                                   [False, '20 Punkte.']
                               ],
                               blank=False)

    CQ_2 = models.BooleanField(label='Welche der folgenden Aussagen ist richtig?',
                               choices=[
                                   [True, 'Ich werde zehn Perioden spielen und dabei mit drei anderen Teilnehmern interagieren.'],
                                   [False, 'Ich werde mit zehn Teilnehmern interagieren und vier Perioden spielen.'],
                                   [False, 'Ich werde zehn Perioden spielen und dabei mit vier anderen Teilnehmern interagieren.'],
                                   [False, 'Keine der obigen Aussagen ist wahr.']
                               ],
                               blank=False)

    CQ_3 = models.BooleanField(label='Welche der folgenden Aussagen ist richtig?',
                               choices=[
                                   [False, 'Egal was passiert, ich erhalte in jeder Periode eine Ausstattung von 20 Punkten.'],
                                   [False, 'Meine Verdienste in den vorherigen Perioden werden meine Ausstattung der aktuellen Periode nicht beeinflussen.'],
                                   [True, 'Je höher meine Ausstattung (im Vergleich zu anderen), desto niedriger meine Ausschüttungsrate für Gruppenkonto.'],
                                   [False, 'Ich erhalte eine Ausschüttungsrate für genau die Anzahl der Punkte, die ich auf das Gruppenkonto ausgezahlt habe.']
                               ])

    CQ_4 = models.BooleanField(label='Welcher Teil der folgenden Aussage ist FALSCH?',
                               choices=[
                                   [False, 'Es gibt eine konstante Wahrscheinlichkeit, dass ein Ereignis eintritt.'],
                                   [False, 'Wenn ein Ereignis eintritt, kann ich bis zur Hälfte meiner Ausstattung verlieren.'],
                                   [False, 'Wie viel von meiner Ausstattung verloren geht, hängt von meiner Gruppe ab.'],
                                   [True, 'Ich habe jedoch keinen Einfluss auf den Schaden, wenn ein Ereignis eintritt.']
                               ])

    CQ_5 = models.BooleanField(label='Schauen Sie sich Ihre Entscheidungsoberfläche genauer an. Wie viele Punkte können Sie möglicherweise dem Gruppenkonto zuweisen?',
                               choices=[
                                   [True, '20'],
                                   [False, '46'],
                                   [False, '10']
                               ])


# PAGES
class A_Welcome(Page):
    pass


class B_Instructions_1(Page):
    form_model = "player"
    form_fields = ["CQ_1", "CQ_2"]

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.waited_too_long = False
        player.participant.wait_page_arrival = time.time()

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            redirect="",
            damage=int(player.session.config["damage"]*100),
            risk=int(player.session.config["risk"]*100),
            group_members=player.session.config["group_size"] - 1,
            min_mpcr=round((player.session.config["efficiency_factor"]/player.session.config["group_size"] - player.session.config["risk"]*player.session.config["damage"])*100, 1),
            max_mpcr=round((player.session.config["efficiency_factor"]/player.session.config["group_size"])*100, 1),
        )

class B_Instructions_2(Page):
    form_model = "player"
    form_fields = ["CQ_3"]

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.waited_too_long = False
        player.participant.wait_page_arrival = time.time()

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            redirect="",
            damage=int(player.session.config["damage"] * 100),
            risk=int(player.session.config["risk"] * 100),
            group_members=player.session.config["group_size"] - 1,
            min_mpcr=round((player.session.config["efficiency_factor"] / player.session.config["group_size"] -
                            player.session.config["risk"] * player.session.config["damage"]) * 100, 1),
            max_mpcr=round((player.session.config["efficiency_factor"] / player.session.config["group_size"]) * 100,
                           1),
        )

class B_Instructions_3(Page):
    form_model = "player"
    form_fields = ["formula_shown", "CQ_4"]

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.waited_too_long = False
        player.participant.wait_page_arrival = time.time()

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            redirect="",
            damage=int(player.session.config["damage"] * 100),
            risk=int(player.session.config["risk"] * 100),
            group_members=player.session.config["group_size"] - 1,
            min_mpcr=round((player.session.config["efficiency_factor"] / player.session.config["group_size"] -
                            player.session.config["risk"] * player.session.config["damage"]) * 100, 1),
            max_mpcr=round((player.session.config["efficiency_factor"] / player.session.config["group_size"]) * 100,
                           1),
        )

class B_Instructions_4(Page):
    form_model = "player"
    form_fields = ["CQ_5"]

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.waited_too_long = False
        player.participant.wait_page_arrival = time.time()

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            redirect="",
            damage=int(player.session.config["damage"] * 100),
            risk=int(player.session.config["risk"] * 100),
            group_members=player.session.config["group_size"] - 1,
            min_mpcr=round((player.session.config["efficiency_factor"] / player.session.config["group_size"] -
                            player.session.config["risk"] * player.session.config["damage"]) * 100, 1),
            max_mpcr=round((player.session.config["efficiency_factor"] / player.session.config["group_size"]) * 100,
                           1),
        )


class F_Debrief(Page):
    form_model = "player"

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            redirect="",
            damage=int(player.session.config["damage"] * 100),
            risk=int(player.session.config["risk"] * 100),
            group_members=player.session.config["group_size"] - 1,
            min_mpcr=round((player.session.config["efficiency_factor"] / player.session.config["group_size"] -
                            player.session.config["risk"] * player.session.config["damage"]) * 100, 1),
            max_mpcr=round((player.session.config["efficiency_factor"] / player.session.config["group_size"]) * 100,
                           1),
            correct=player.CQ_1 + player.CQ_2 + player.CQ_3 + player.CQ_4 + player.CQ_5 == 5
        )

class B_Instructions(Page):
    form_model = "player"
    # form_fields = ["formula_shown"]

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.waited_too_long = False
        player.participant.wait_page_arrival = time.time()

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            redirect="",
            damage=int(player.session.config["damage"] * 100),
            risk=int(player.session.config["risk"] * 100),
            group_members=player.session.config["group_size"] - 1,
            min_mpcr=round((player.session.config["efficiency_factor"] / player.session.config["group_size"] -
                            player.session.config["risk"] * player.session.config["damage"]) * 100, 1),
            max_mpcr=round((player.session.config["efficiency_factor"] / player.session.config["group_size"]) * 100,
                           1),
        )


page_sequence = [A_Welcome,
                 B_Instructions_1,
                 B_Instructions_2,
                 B_Instructions_3,
                 B_Instructions_4,
                 F_Debrief]
