import random

from otree.api import *


author = 'Your name here'
doc = """
Inspired by https://github.com/felixholzmeister/mpl
"""


class Constants(BaseConstants):
    name_in_url = 'HLPL'
    players_per_group = None
    num_rounds = 1
    num_choices = 11
    lottery_price = 50


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    review_instructions = models.IntegerField(
        doc="Counts the number of times a player reviews instructions.", initial=0, blank=True
    )
    review_contact = models.IntegerField(
        doc="Counts the number of times a player reviews contact information.",
        initial=0,
        blank=True,
    )
    for j in range(1, Constants.num_choices + 1):
        locals()['choice_' + str(j)] = models.StringField()
    del j
    random_draw = models.IntegerField()
    choice_to_pay = models.StringField()
    option_to_pay = models.StringField()
    inconsistent = models.IntegerField()
    switching_row = models.IntegerField()


# FUNCTIONS
def creating_session(subsession: Subsession):
    n = Constants.num_choices
    for p in subsession.get_players():
        indices = [j for j in range(1, n + 1)]
        # indices.append(n)
        certainty_equivalents = [(k - 1) * 5 for k in indices]
        form_fields = ["choice_" + str(k) for k in indices]
        p.participant.vars["mpl_choices"] = list(zip(indices, form_fields, certainty_equivalents))
        p.participant.vars["mpl_index_to_pay"] = random.choice(indices)
        p.participant.vars["mpl_choice_to_pay"] = "choice_" + str(
            p.participant.vars["mpl_index_to_pay"]
        )
        p.participant.vars['mpl_choices_made'] = [None for j in range(1, n + 1)]


def set_payoffs(player: Player):
    player.random_draw = random.randint(0, 100)
    player.choice_to_pay = player.participant.vars["mpl_choice_to_pay"]
    player.option_to_pay = getattr(player, player.choice_to_pay)
    if player.option_to_pay == "lottery":
        if player.random_draw <= 50:
            payoff = Constants.lottery_price
        else:
            payoff = 0
    else:
        payoff = (player.participant.vars["mpl_index_to_pay"]-1) * 5

    if player.participant.damage_prob == 0:
        player.payoff = payoff
    else:
        player.payoff = 2 * payoff

    player.participant.vars["mpl_payoff"] = cu(player.payoff).to_real_world_currency(player.session)


def set_consistency(player: Player):
    n = Constants.num_choices
    # replace "lottery"s by 1's and "certainty"s by 0's
    player.participant.vars["mpl_choices_made"] = [
        1 if j == "lottery" else 0 for j in player.participant.vars["mpl_choices_made"]
    ]
    # check for multiple switching behavior
    for j in range(1, n):
        choices = player.participant.vars["mpl_choices_made"]
        player.inconsistent = 1 if choices[j] > choices[j - 1] else 0
        if player.inconsistent == 1:
            break


def set_switching_row(player: Player):
    # set switching point to row number of first "certainty" choice
    if player.inconsistent == 0:
        player.switching_row = sum(player.participant.vars["mpl_choices_made"]) + 1


# PAGES
class HLPL_Decision(Page):
    form_model = "player"

    # @staticmethod
    # def is_displayed(player: Player):
    #     if not player.participant.vars["is_residual_player"]:
    #         return True

    @staticmethod
    def get_form_fields(player: Player):
        # unzip list of form_fields from <mpl_choices> list
        form_fields = [list(t) for t in zip(*player.participant.vars['mpl_choices'])][1]
        form_fields.extend(["review_instructions", "review_contact"])
        return form_fields

    @staticmethod
    def vars_for_template(player: Player):
        return dict(choices=player.participant.vars["mpl_choices"])

    @staticmethod
    def js_vars(player: Player):
        return dict(
            template="risk",
        )

    @staticmethod
    def get_timeout_seconds(player: Player):
        if player.participant.vars.get("is_dropout"):
            return 1  # instant timeout, 1 second

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        form_fields = [list(t) for t in zip(*player.participant.vars['mpl_choices'])][1]
        indices = [list(t) for t in zip(*player.participant.vars['mpl_choices'])][0]
        for j, choice in zip(indices, form_fields):
            choice_i = getattr(player, choice)
            player.participant.vars['mpl_choices_made'][j - 1] = choice_i
        # set payoff
        set_payoffs(player)
        # determine consistency
        set_consistency(player)
        # set switching row
        set_switching_row(player)


page_sequence = [HLPL_Decision]
