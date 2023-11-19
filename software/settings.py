from os import environ

SESSION_CONFIGS = [
    dict(
        name="EWE",
        app_sequence=["A_Intro", "B_EWE", "C_HLPL", "D_Outro"],
        num_demo_participants=2,
        num_rounds=10,
        group_size=2,
        efficiency_factor=1.5,
        risk=0.2,
        damage=0.5,
        initial_endowment=20,
    ),
    dict(name='HLPL',
         app_sequence=['C_HLPL'],
         num_demo_participants=2,
         num_rounds=1
         ),
    dict(name='ochat',
         app_sequence=['oChat'],
         num_demo_participants=2,
         num_rounds=1
         )
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.02,
    participation_fee=2.00,
    timeout_seconds = [300, 180, 150, 150, 150, 150, 150, 150, 150, 150],
    doc=""
)

PARTICIPANT_FIELDS = ["wait_page_arrival",
                      "is_dropout",
                      "waited_too_long",
                      "stock",
                      "euros",
                      "showup_fee",
                      "dPGG_payoff",
                      'mpl_choices',
                      'mpl_index_to_pay',
                      'mpl_choice_to_pay',
                      'mpl_choices_made',
                      'mpl_payoff',
                      'finished']

SESSION_FIELDS = ['prolific_completion_url']


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = "en"

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = "GBP"
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '2501627228529'
