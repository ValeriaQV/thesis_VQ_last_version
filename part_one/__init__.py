from otree.api import *

# further packages
import random

doc = """
There are three different clusters of players (roles): JW, E and NE. 
JW participants ignore the existence of the world with inequalities for decision-making 
opportunities. UW participants (E + NE) ignore the existence of the world without ex-ante 
inequalities. Players receive a fix endowment and submit their risk preferences for four 
independent contexts. All scenarios are in the loss domain with different levels for the 
safe option. The risk-taking alternative remains constant across all four scenarios. 
"""


class C(BaseConstants):
    NAME_IN_URL = 'part_one'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1

    # Parameters
    ENDOWMENT = cu(800)
    RISK_LOW = cu(800)
    RISK_HIGH = cu(0)

    SAFE_OPTIONS = [cu(775), cu(600), cu(500), cu(400)]

    # Clusters
    JW_ROLE = "Just World"
    E_ROLE = "Elite"
    NE_ROLE = "Non Elite"

    # Templates
    CHOICES_TEMPLATE = "part_one/temp_choices.html"


###############################################################################################################
#########################################   CLASSES      ######################################################
###############################################################################################################


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

    #################################################################################
    ################   Assign everything at the PLAYER level      ###################
    #################################################################################


class Player(BasePlayer):
    # 4 choices per player --> 4 risk scenarios --> 4 bools since var of interest (C) is binary

    risk_1 = models.BooleanField(label="Scenario 1")
    risk_2 = models.BooleanField(label="Scenario 2")
    risk_3 = models.BooleanField(label="Scenario 3")
    risk_4 = models.BooleanField(label="Scenario 4")

    # Include comprehension questions
    quiz_1_all = models.IntegerField(label="1. How many scenarios will be presented in the First "
                                           "Part of the experiment?")
    quiz_2_all = models.IntegerField(label="2. How many decisions from the First Part will be "
                                           "implemented for your final payment?")

    # Vars for payoff
    scenario_random = models.IntegerField()

    risk_random = models.BooleanField()
    risk_random_str = models.StringField()
    safe_random_str = models.StringField()

    lottery_random = models.CurrencyField()
    lottery_random_str = models.StringField()


###############################################################################################################
##########################################     PAGES      #####################################################
###############################################################################################################

#########################################
##  Introduction for ALL participants  ##
#########################################

class Introduction(Page):
    pass


#########################################
##    Instructions JW participants     ##
#########################################

class Instructions_JW(Page):
    @staticmethod
    def is_displayed(participant):
        return participant.role == "Just World"


#########################################
##    Instructions UW participants     ##
#########################################

class Instructions_UW(Page):
    @staticmethod
    def is_displayed(participant):
        return participant.role != "Just World"


#########################################
##         ALL participants            ##
#########################################

class Comprehension_Quiz(Page):
    form_model = "player"
    form_fields = ["quiz_1_all", "quiz_2_all"]

    @staticmethod
    def error_message(player, values):
        solutions = {'quiz_1_all': 4, 'quiz_2_all': 1}

        if values != solutions:
            return "One or more answers were incorrect. Please correct your answers."


class Waiting_for_Others(WaitPage):
    pass


class Choices(Page):
    form_model = "player"
    form_fields = ["risk_1", "risk_2", "risk_3", "risk_4"]


class ResultsWaitPage(WaitPage):
    form_model = "player"
    form_fields = ["scenario_random", "risk_random", "lottery_random",
                   "risk_random_str", "safe_random_str", "lottery_random_str"]

    # Define payoffs part_one:
    @staticmethod
    def after_all_players_arrive(group: Group):

        # First, access players by groups
        p1_player_lists = group.get_players()

        # Second, select a random scenario for payment:
        for p in p1_player_lists:
            # First, generate random number
            p.scenario_random = random.randint(1, 4)
            # Second, create a list of the choices
            list_choices = [p.risk_1, p.risk_2, p.risk_3, p.risk_4]
            # Last, access the data from the selected scenario -> index: player.scenario_random-1
            p.risk_random = list_choices[p.scenario_random - 1]

            # Define risk_random as string --> for convenience while writing results template
            if p.risk_random:
                p.risk_random_str = "Risky Lottery"
                p.safe_random_str = " "
            else:
                p.risk_random_str = "Safe Option"
                p.safe_random_str = str(C.SAFE_OPTIONS[p.scenario_random - 1])

            if p.role == C.NE_ROLE:
                p.safe_random_str = " "

        # Third, assign a name to each type of player according to index within group
        p1_JW = p1_player_lists[0]
        p1_E = p1_player_lists[1]
        p1_NE = p1_player_lists[2]

        # Fourth, define payoffs according to role:
        # JW participants have no restriction --> option chosen, option realized
        if p1_JW.risk_random:
            p1_JW.lottery_random = random.choice([C.RISK_LOW, C.RISK_HIGH])
            p1_JW.payoff = C.ENDOWMENT - p1_JW.lottery_random
        else:
            p1_JW.payoff = C.ENDOWMENT - C.SAFE_OPTIONS[p1_JW.scenario_random - 1]

        # E participants have no restriction --> option chosen, option realized
        if p1_E.risk_random:
            p1_E.lottery_random = random.choice([C.RISK_LOW, C.RISK_HIGH])
            p1_E.payoff = C.ENDOWMENT - p1_E.lottery_random
        else:
            p1_E.payoff = C.ENDOWMENT - C.SAFE_OPTIONS[p1_E.scenario_random - 1]

        # NE participants ALWAYS lottery --> same payoff irrespective of choice
        p1_NE.lottery_random = random.choice([C.RISK_LOW, C.RISK_HIGH])
        p1_NE.payoff = C.ENDOWMENT - p1_NE.lottery_random

        # Last, store data at the participant level
        for p in group.get_players():
            participant = p.participant

            participant.p1_payoff = p.payoff
            participant.p1_group_id = group.id
            participant.c_role = p.role
            participant.p1_risk_1 = p.risk_1
            participant.p1_risk_2 = p.risk_2
            participant.p1_risk_3 = p.risk_3
            participant.p1_risk_4 = p.risk_4
            participant.p1_scenario_random = p.scenario_random
            participant.p1_risk_random = p.risk_random
            participant.p1_risk_random_str = p.risk_random_str
            participant.p1_safe_random_str = p.safe_random_str
            participant.p1_lottery_random = p.field_maybe_none("lottery_random")

            # Define lottery_random as string --> for convenience while writing results template
            p.lottery_random_str = str(p.field_maybe_none("lottery_random"))

            if p.lottery_random_str == "None":
                p.lottery_random_str = " "

            participant.p1_lottery_random_str = p.lottery_random_str


#########################################
##   UW learn assigned role: E / NE?   ##
#########################################

class Group_Assignment(Page):
    @staticmethod
    def is_displayed(participant):
        return participant.role != "Just World"



page_sequence = [Introduction,
                 Instructions_JW, Instructions_UW,
                 Comprehension_Quiz, Waiting_for_Others,
                 Choices, ResultsWaitPage, Group_Assignment,
                 Waiting_for_Others]
