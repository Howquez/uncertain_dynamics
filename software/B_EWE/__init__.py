from otree.api import *
import math
import time
import random
from itertools import cycle



doc = """
Your app description
"""

# MODELS
class C(BaseConstants):
    NAME_IN_URL = 'EWE'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 10
    EARNINGS_TEMPLATE = "A_Intro/C_Earnings.html"
    SHOCKS_TEMPLATE = "A_Intro/D_Shocks.html"
    # INITIAL_ENDOWMENT = 20 called initial_endowment in session configs
    EFFICIENCY_FACTOR = 1.5
    DAMAGE = 0.5


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    residual = models.BooleanField(initial=False, doc="if true, group is incomplete")
    total_contribution = models.IntegerField(doc="sum of contributions in this round")
    average_contribution = models.FloatField(doc="average contribution in this round")
    individual_share = models.IntegerField(doc="individual share each player receives from this round's contributions")
    wealth = models.IntegerField(doc="sum of endowments at the beginning of a round")
    # extreme weather variables
    damage_prob = models.FloatField(doc="describes the probability with which an even occurs.")
    treatment = models.StringField(doc="treatment variable.")
    EWE = models.BooleanField(initial=False, doc="if true, extreme weather event occurred")
    damage_factor = models.FloatField(doc="how much of an individual's income will be destroyed by an EWE")
    bot_active_in_next_round = models.BooleanField(initial=False, doc="indicates whether a bot is active due to another group member's timeout.")


class Player(BasePlayer):
    wait_time_left = models.IntegerField(doc="denotes the time a player has to wait for others to arrive on WaitPage")
    endowment = models.IntegerField(doc="the player's endowment in this round (equals her stock of last round)")
    contribution = models.IntegerField(min=0, doc="the player's contribution in this round")
    stock = models.IntegerField(doc="accumulated earnings of played rounds")
    gain = models.IntegerField(doc="a round's earnings.")
    returns = models.IntegerField(initial=0, doc="earnings if there was no ewe")
    total_damage = models.IntegerField(initial=0, doc="damage caused by the ewe")
    MPCR = models.FloatField(doc="marginal per capita return")

    calculator_time=models.FloatField(doc="Counts the cumulative number of seconds the calculator was opened.",
                                      initial=0)
    dropout=models.BooleanField(doc="Documents whether a participant dropped out (e.g. due to a timeout).", initial=False)




# FUNCTIONS
def creating_session(subsession):
    for player in subsession.get_players():
        player.participant.is_dropout = False
    if subsession.round_number == 1:
        subsession.group_randomly()
    else:
        subsession.group_like_round(1)

def contribution_max(player: Player):
    if player.round_number == 1:
        return player.session.config["initial_endowment"]
    else:
        return int(math.ceil(player.in_round(player.round_number - 1).stock))

def set_group_variables(group: Group):
    if len(group.get_players()) == C.PLAYERS_PER_GROUP:
        for player in group.get_players():
            player.group.damage_prob = player.participant.damage_prob

        group.total_contribution = sum([p.contribution for p in group.get_players()])
        group.average_contribution = round(
            group.total_contribution / C.PLAYERS_PER_GROUP, 2
        )
        group.individual_share = int(
            math.ceil(
                group.total_contribution * group.session.config["efficiency_factor"] / C.PLAYERS_PER_GROUP
            )
        )
        # define wealth as the sum of stocks at the end of the previous (and thus, at the beginning of the current) round
        # wealth therefore is the maximum amount a group can possibly contribute.
        if group.round_number == 1:
            group.wealth = group.session.config["initial_endowment"] * C.PLAYERS_PER_GROUP
        else:
            group.wealth = sum([math.ceil(p.in_round(p.round_number - 1).stock) for p in group.get_players()])

        if group.wealth < 0:
            group.wealth = 0

        # define extreme weather events (i.e. damage events)
        if group.round_number == 3 or group.round_number == 8:
            group.EWE = True
        if group.damage_prob == 0:
            group.EWE = False
        group.damage_factor = 1 - (group.total_contribution / group.wealth)


def set_payoffs(group: Group):
    for p in group.get_players():
        if p.round_number == 1:
            p.endowment = p.session.config["initial_endowment"]
            p.participant.stock = [20]
        else:
            p.endowment = int(math.ceil(p.in_round(p.round_number - 1).stock))

        if p.endowment < 0:
            p.endowment = 0
            if p.participant.is_dropout == True:
                p.contribution = 0
        else:
            if p.participant.is_dropout == True:
                p.contribution = random.randint(0, p.endowment)

    set_group_variables(group)
    for p in group.get_players(): # calculate player-level-variables

        # prepare for bad weather
        p.MPCR = round(p.session.config["efficiency_factor"] / C.PLAYERS_PER_GROUP - (p.session.config["damage"] * p.group.damage_prob * p.endowment) / p.group.wealth, 3)
        p.returns = math.ceil(p.MPCR * p.group.total_contribution)
        p.stock = math.ceil(p.endowment - p.contribution + p.returns)
        if p.group.EWE:
            p.total_damage = math.floor(p.session.config["damage"] * p.endowment * group.damage_factor)
            p.stock = p.stock - p.total_damage

        p.gain = (p.stock - p.endowment)
        p.participant.stock.append(p.stock)
        # p.participant.vars["stock"].append(p.stock) # vars for visualization?
        # p.participant.vars["euros"].append(cu(p.stock).to_real_world_currency(group.session))
        if p.participant.is_dropout:
            p.payoff = 0
        else:
            if p.round_number == 1:
                p.payoff = cu(p.stock)
            elif p.round_number == C.NUM_ROUNDS: # we do this because we pretend as if the risk treatment had a different exchange rate. Hence, their income has to double at the end of the game.
                if p.group.damage_prob == 0:
                    p.payoff = cu(p.gain)
                else:
                    p.payoff = cu(p.gain + p.stock)

            else:
                p.payoff = cu(p.gain)
        # store payoff in participant var to display it across apps
        if group.round_number == C.NUM_ROUNDS:
            if p.group.damage_prob == 0:
                p.participant.vars["dPGG_payoff"] = cu(p.stock).to_real_world_currency(group.session)
            else:
                p.participant.vars["dPGG_payoff"] = cu(2 * p.stock).to_real_world_currency(group.session)
            # p.participant.vars["showup_fee"] = group.session.config["participation_fee"]


# PAGES
class A_InitialWaitPage(WaitPage):

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        probs = [0, player.session.config["risk"]]
        selected_prob = probs[player.group.id_in_subsession % 2]
        player.participant.damage_prob = selected_prob
        player.group.damage_prob = selected_prob

        # create more descriptive treatment variable
        if player.group.damage_prob == 0:
            player.group.treatment = "no_risk"
        else:
            player.group.treatment = "risk"

        if player.participant.waited_too_long == True:
            player.participant.vars["dPGG_payoff"] = C.PATIENCE_BONUS
            player.participant.vars["mpl_payoff"] = 0
            return upcoming_apps[-1]

# class A_InitialPage(Page):
#     form_model = "player"
#
#     @staticmethod
#     def is_displayed(player):
#         return player.round_number == 1
#
#     @staticmethod
#     def get_timeout_seconds(player):
#         if player.participant.is_dropout:
#             return 1  # instant timeout, 1 second
#         else:
#             return 120
#
#     @staticmethod
#     def before_next_page(player, timeout_happened):
#         if timeout_happened:
#             player.dropout = True
#             player.participant.is_dropout = True
#             player.group.bot_active_in_next_round = True


class B_Decision(Page):
    form_model = "player"
    form_fields = ["contribution", "calculator_time"]

    @staticmethod
    def vars_for_template(player: Player):
        endowment = player.session.config["initial_endowment"]
        diff = 0
        bot_active = False
        ewe = False
        wealth = player.session.config["initial_endowment"] * C.PLAYERS_PER_GROUP
        total_damage = 0
        if player.round_number > 1:
            endowment = int(math.ceil(player.in_round(player.round_number - 1).stock))
            diff = player.in_round(player.round_number - 1).gain
            bot_active = player.in_round(player.round_number - 1).group.bot_active_in_next_round
            ewe = player.in_round(player.round_number - 1).group.EWE
            wealth = sum([p.in_round(p.round_number - 1).stock for p in player.group.get_players()])
            total_damage = player.in_round(player.round_number - 1).total_damage
        return dict(
            redirect="",
            endowment=endowment,
            diff=diff,
            bot_active=bot_active,
            previous_round=player.round_number - 1,
            ewe=ewe,
            mpcr= str(int(round(100*(player.session.config["efficiency_factor"] / C.PLAYERS_PER_GROUP - player.session.config["damage"] * player.participant.damage_prob * endowment / wealth), 0))) +  "%",
            total_damage = total_damage,
            damage=int(player.session.config["damage"]*100),
            risk=int(player.participant.damage_prob*100),
            group_members=player.session.config["group_size"] - 1
        )

    @staticmethod
    def js_vars(player: Player):
        if player.round_number == 1:
            stock = player.session.config["initial_endowment"]
            endowment = player.session.config["initial_endowment"]
            wealth = player.session.config["initial_endowment"] * C.PLAYERS_PER_GROUP
        else:
            stock = player.participant.stock
            endowment = int(math.ceil(player.in_round(player.round_number - 1).stock))
            wealth = sum([p.in_round(p.round_number - 1).stock for p in player.group.get_players()])
        return dict(
            template="decision",
            current_round=player.round_number,
            stock=stock,
            endowment=endowment,
            num_rounds=C.NUM_ROUNDS,
            num_players=C.PLAYERS_PER_GROUP,
            wealth=wealth,
            damage=player.session.config["damage"],
            factor=round(player.session.config["efficiency_factor"] / C.PLAYERS_PER_GROUP - player.session.config["damage"] * player.participant.damage_prob * endowment / wealth, 2),
        )

    @staticmethod
    def get_timeout_seconds(player):
        if player.participant.is_dropout:
            return 1  # instant timeout, 1 second
        else:
            return player.session.config['timeout_seconds'][player.round_number - 1]

    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.dropout = True
            player.participant.is_dropout = True
            player.group.bot_active_in_next_round = True
            if player.round_number == C.NUM_ROUNDS:
                player.participant.vars["dPGG_payoff"] = 0
                player.participant.vars["mpl_payoff"] = 0

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.round_number == C.NUM_ROUNDS:
            if player.participant.is_dropout == True:
                return upcoming_apps[-1]


class C_ResultsWaitPage(WaitPage):
    @staticmethod
    def get_timeout_seconds(player):
        if player.participant.is_dropout:
            return 1  # instant timeout, 1 second
        else:
            return player.session.config['timeout_seconds'][player.round_number - 1] + 60

    after_all_players_arrive = "set_payoffs"


class D_Results(Page):
    @staticmethod
    def is_displayed(player):
        if player.round_number == C.NUM_ROUNDS:
            return True

    @staticmethod
    def js_vars(player: Player):
        stock = player.participant.stock
        return dict(
            template="results",
            current_round=player.round_number,
            stock=stock,
            num_rounds=C.NUM_ROUNDS,

        )
        @staticmethod
        def before_next_page(player, timeout_happened):
            player.payoff


page_sequence = [A_InitialWaitPage,
                 B_Decision,
                 C_ResultsWaitPage,
                 D_Results]
