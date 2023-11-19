from otree.api import *
import math
import time
import random



doc = """
Your app description
"""

# MODELS
class C(BaseConstants):
    NAME_IN_URL = 'EWE'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 10
    EARNINGS_TEMPLATE = "A_Intro/C_Earnings.html"
    SHOCKS_TEMPLATE = "A_Intro/D_Shocks.html"
    PATIENCE = 1
    PATIENCE_BONUS = 20
    # INITIAL_ENDOWMENT = 20 called initial_endowment in session configs
    EFFICIENCY_FACTOR = 1.5
    TIMEOUT = 4
    # extreme weather constants
    # DANGER = 0.2 called risk in session configs
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

    formula_shown = models.BooleanField(doc="True if participant wanted to see the formula that explains earnings.",
                                        initial=False)
    calculator_time=models.FloatField(doc="Counts the cumulative number of seconds the calculator was opened.",
                                      initial=0)
    dropout=models.BooleanField(doc="Documents whether a participant dropped out (e.g. due to a timeout).", initial=False)




# FUNCTIONS
def creating_session(subsession):
    # read data (from seesion config)
    for player in subsession.get_players():
        player.participant.is_dropout = False

def waiting_too_long(player):
    participant = player.participant
    import time
    # assumes you set wait_page_arrival in PARTICIPANT_FIELDS.
    return time.time() - participant.wait_page_arrival > C.PATIENCE*60

def group_by_arrival_time_method(subsession, waiting_players):
    if len(waiting_players) >= C.PLAYERS_PER_GROUP:
        return waiting_players[:C.PLAYERS_PER_GROUP]
    for player in waiting_players:
        player.wait_time_left = int(math.ceil(C.PATIENCE - (time.time() - player.participant.wait_page_arrival) / 60))
        if waiting_too_long(player):
            player.participant.waited_too_long = True
            # make a single-player group.
            return [player]

def contribution_max(player: Player):
    if player.round_number == 1:
        return player.session.config["initial_endowment"]
    else:
        return int(math.ceil(player.in_round(player.round_number - 1).stock))

def set_group_variables(group: Group):
    if len(group.get_players()) == C.PLAYERS_PER_GROUP:
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

        # extreme weather events
        a = random.randint(0, 100)
        if a < group.session.config["risk"] * 100:
            group.EWE = True
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
        p.MPCR = round(p.session.config["efficiency_factor"] / C.PLAYERS_PER_GROUP - p.session.config["damage"] * p.session.config["risk"] * p.endowment / p.group.wealth, 2)
        p.returns = math.ceil(p.MPCR * p.group.total_contribution)
        p.stock = math.ceil(p.endowment - p.contribution + p.returns)
        if p.group.EWE:
            p.total_damage = math.floor(p.session.config["damage"] * p.endowment * group.damage_factor)
            p.stock = p.stock - p.total_damage

        p.gain = (p.stock - p.endowment)
        p.participant.stock.append(p.stock)
        # p.participant.vars["stock"].append(p.stock) # vars for visualization?
        # p.participant.vars["euros"].append(cu(p.stock).to_real_world_currency(group.session))
        if p.round_number == 1:
            p.payoff = cu(p.stock)
        else:
            p.payoff = cu(p.gain)
        # store payoff in participant var to display it across apps
        if group.round_number == C.NUM_ROUNDS:
            p.participant.vars["dPGG_payoff"] = cu(p.stock).to_real_world_currency(group.session)
            # p.participant.vars["showup_fee"] = group.session.config["participation_fee"]


# PAGES
class A_InitialWaitPage(WaitPage):
    template_name = "B_EWE/A_InitialWaitPage.html"
    group_by_arrival_time = True

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.participant.waited_too_long == True:
            return upcoming_apps[0]


class B_Decision(Page):
    form_model = "player"
    form_fields = ["contribution", "formula_shown", "calculator_time"]

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
            mpcr= str(round(100*(player.session.config["efficiency_factor"] / C.PLAYERS_PER_GROUP - player.session.config["damage"] * player.session.config["risk"] * endowment / wealth), 2)) +  "%",
            total_damage = total_damage,
            damage=int(player.session.config["damage"]*100),
            risk=int(player.session.config["risk"]*100),
            group_members=player.session.config["group_size"] - 1,
            min_mpcr=round((player.session.config["efficiency_factor"]/player.session.config["group_size"] - player.session.config["risk"]*player.session.config["damage"])*100, 1),
            max_mpcr=round((player.session.config["efficiency_factor"]/player.session.config["group_size"])*100, 1)
        )

    @staticmethod
    def js_vars(player: Player):
        timeout = C.TIMEOUT
        if player.round_number == 1:
            timeout = 2.5 * C.TIMEOUT
            stock = player.session.config["initial_endowment"]
            endowment = player.session.config["initial_endowment"]
            wealth = player.session.config["initial_endowment"] * C.PLAYERS_PER_GROUP
        else:
            stock = player.participant.stock
            endowment = int(math.ceil(player.in_round(player.round_number - 1).stock))
            wealth = sum([p.in_round(p.round_number - 1).stock for p in player.group.get_players()])
        return dict(
            timeout=timeout,
            template="decision",
            current_round=player.round_number,
            stock=stock,
            endowment=endowment,
            num_rounds=C.NUM_ROUNDS,
            num_players=C.PLAYERS_PER_GROUP,
            wealth=wealth,
            damage=player.session.config["damage"],
            factor=round(player.session.config["efficiency_factor"] / C.PLAYERS_PER_GROUP - player.session.config["damage"] * player.session.config["risk"] * endowment / wealth, 2),
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


page_sequence = [A_InitialWaitPage,
                 B_Decision,
                 C_ResultsWaitPage,
                 D_Results]
