from otree.api import *
from os import environ
import openai
import random
import json
from datetime import datetime

author = "Clint McKenna cmck@umich.edu"
# https://clintmckenna.com/blog/2023-03-29/

doc = """
a chatGPT interface for oTree
"""


class C(BaseConstants):
    NAME_IN_URL = 'chatGPT'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    PRIVACY_TEMPLATE = "oChat/T_Privacy.html"

    # chatGPT vars

    ## temperature (range 0 - 2)
    ## this sets the bot's creativity in responses, with higher values being more creative
    ## https://platform.openai.com/docs/api-reference/completions#completions/create-temperature
    TEMP = 1.2

    ## model
    ## this is which gpt model to use, which have different prices and ability
    ## https://platform.openai.com/docs/models
    MODEL = "gpt-3.5-turbo"


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    # set constants
    initial_prompt = "Please read the following text which are instruction that explain a dynamic public goods game to participants. " \
                     "Please explain the instructions if there are any particular questions. Do not tell people what to do or how to behave in the game. Do not answer any questions about the best strategies and which contributions to make. Just explain the rules, if asked." \
                     "You are about to participate in a decision-making experiment. If you follow the instructions carefully, you can earn a considerable amount of money that depends on your decisions and the decisions of three other participants. Your earnings will be transferred as bonus payments. Throughout the experiment you will make decisions about amounts of tokens. At the end of the experiment all tokens you have will be converted into Euros at the exchange rate €0.02 for 1 point in addition to a show-up fee of £2.00. The experiment will consist of 10 decision making periods as well as a brief questionnaire. At the beginning of the experiment, you will be matched with three other participants. Therefore, there are four people, including yourself, participating in your group. You will be matched with the same participants during the entire experiment. None of the participants knows anything about other participants' identities. All your decisions will be treated confidentially. This means that none of the other participants will know who you are and which decisions you made. Likewise, you will not be able to learn the identity of your group members. Whereas we will provide some information about each participant's previous decision, we will mask them to establish anonymity. Before the first period, each participant will be given an initial endowment of 20 tokens." \
                     "At the beginning of each period you will be asked to allocate your endowment between a private account and a group account. The tokens that you place in the private account have a return of 1. This means that, at the end of a given period, your private account will contain exactly the amount of tokens you put into the private account at the beginning of the period. Nobody except yourself benefits from your private account. The tokens that you place in the group account are summed together with the tokens that the other three members of your group place in the group account. Regardless of how many tokens you contributed to the group account, you as well as the other members of your group will get a share of that sum of tokens. The exact quota determining your individual share of the group account may vary from period to period, which is why we will display it on your decision screen in each period. More precisely, the return you receive from the group account depends on how your endowment compares to the whole group's endowments. In case you have an endowment while the other group members have nothing, the quota will be smaller. If, in contrast, you have no endowment but some other group member has an endowment, the quota will be higher. Hence, the lower your endowment in a given period (compared to others) the higher your individual share of the group account in that period. This relationship is visualized in the following figure." \
                     "Your endowment at the beginning of the second period will be equal to the amount of tokens you accumulated in the first period. Hence, you'll start the second period with all the tokens from your private account plus your individual share of the group account at the end of the first period. In the second period, you will be again asked to allocate the endowment you accumulated between a private account and a group account. Both the private and the group account work in exactly the same manner as in the first period. The structure of the experiment at all subsequent periods is identical: your endowment at the beginning of each period is equal to the amount of tokens in your private account plus your share of the group account at the end of the previous period. Your total income in the end of the experiment is equal to the amount of tokens in your private account and your share of the group account at the end of the last period." \
                     "There is a fixed chance of 20% that an event occurs. Such an event reduces your endowment to up to 50%. While you do not have any influence on the occurence of an event, you can affect the damage it evokes: The more you and the rest of your group contribute to the group account, the smaller the damage if an event occurs. Conversely, the lower the contributions, the higher the damage if an event occurs. More precisely, there won't be any damage if everybody in the group contributes his or her whole endowment to the group account – even if there was an event. If none of you contributes anything to the group account, an event will cause a damage of 50% of the endowments of each and every one of you. Note that we provide a calculator behind the calculator-symbol. It takes the abovementioned formula, as well as the quota and helps you to consider different cases. As such, it is most important that you understand that higher contributions lead to lower damage in case of an event."

    players = subsession.get_players()
    for p in players:
        p.msg = json.dumps([{"role": "system", "content": initial_prompt}])


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # chat condition and data log
    condition = models.StringField(blank=True)
    chatLog = models.LongStringField(blank=True)

    # password
    password = models.StringField()

    # input data for gpt
    msg = models.LongStringField(blank=True)


def password_error_message(player, value):
    if value != 'Torstrasse25':
        return 'Try again.'


# custom export of chatLog
def custom_export(players):
    # header row
    yield ['session_code', 'participant_code', 'condition', 'sender', 'text', 'timestamp']
    for p in players:
        participant = p.participant
        session = p.session

        # expand chatLog
        log = p.field_maybe_none('chatLog')
        if log:
            json_log = json.loads(log)
            print(json_log)
            for r in json_log:
                sndr = r['sender']
                txt = r['text']
                time = r['timestamp']
                yield [session.code, participant.code, p.condition, sndr, txt, time]


# openAI chat gpt key
CHATGPT_KEY = environ.get('CHATGPT_KEY')


# function to run messages
def runGPT(inputMessage):
    completion = openai.ChatCompletion.create(
        model=C.MODEL,
        messages=inputMessage,
        temperature=C.TEMP
    )
    return completion["choices"][0]["message"]["content"]


# PAGES
class A_Intro(Page):
    pass

class B_Instructions(Page):
    form_model = 'player'
    form_fields = ['password']

class C_Chat(Page):
    form_model = 'player'
    form_fields = ['chatLog']

    @staticmethod
    def get_timeout_seconds(player):
        return 300 # player.session.config['timer'] * 60

    @staticmethod
    def live_method(player: Player, data):

        # start GPT with prompt based on randomized condition
        # set chatgpt api key
        openai.api_key = CHATGPT_KEY

        # load msg
        messages = json.loads(player.msg)

        # functions for retrieving text from openAI
        if 'text' in data:
            # grab text that participant inputs and format for chatgpt
            text = data['text']
            inputMsg = {'role': 'user', 'content': text}

            # append messages and run chat gpt function
            messages.append(inputMsg)
            output = runGPT(messages)

            # also append messages with bot message
            botMsg = {'role': 'assistant', 'content': output}
            messages.append(botMsg)

            # write appended messages to database
            player.msg = json.dumps(messages)

            return {player.id_in_group: output}
        else:
            pass

    @staticmethod
    def before_next_page(player, timeout_happened):
        return {
        }


page_sequence = [
    A_Intro,
    B_Instructions,
    C_Chat,
]