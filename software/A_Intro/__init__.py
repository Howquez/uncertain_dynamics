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



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    formula_shown = models.BooleanField(doc="True if participant wanted to see the formula that explains earnings.",
                                        initial=False)

    CQ_1 = models.BooleanField(label='How much money can you earn in this experiment?',
                               choices=[
                                   [False, 'Exactly the fixed participation fee.'],
                                   [True, 'That depends on my decisions and the decisions of others.'],
                                   [False, '20 tokens.']
                               ],
                               blank=False)

    CQ_2 = models.BooleanField(label='Which of the following statements is correct?',
                               choices=[
                                   [True, 'I will play ten periods while being matched with three other participants.'],
                                   [False, 'I will be matched with ten participants and play four periods.'],
                                   [False, 'I will play ten periods while being matched with four other participants'],
                                   [False, 'None of the above is true.']
                               ],
                               blank=False)

    CQ_3 = models.BooleanField(label='Which of the following statements is correct?',
                               choices=[
                                   [False, 'No matter what happens, I will receive an endowment of 20 tokens in each period'],
                                   [False, 'My earnings in the previous periods will not affect my endwoment of the current period.'],
                                   [True, 'The higher my endowment (compared to others), the lower my quota, the lower my share from the group account.']
                               ])

    CQ_4 = models.BooleanField(label='Which part of the following statement is false?',
                               choices=[
                                   [False, 'There a constant chance that an event occurs...'],
                                   [False, '...If an event occurs, I may lose up to half of my endwoment...'],
                                   [False, '...How much of my endowment will be lost, depends on my group...'],
                                   [True, '...I, however, have no control over the damage if an event occurs.']
                               ])

    CQ_5 = models.BooleanField(label='Take a closer look at your decision interface. How many tokens can you possibly allocate to the group account?',
                               choices=[
                                   [True, '20'],
                                   [False, '46.67'],
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
