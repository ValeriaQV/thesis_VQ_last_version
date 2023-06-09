from otree.api import *

import random
import itertools

doc = """
Participants keep their roles from the first part. Now they will submit their preferences after 
learning the existence of the other "world". To measure treatment effects, I include a control 
group which does NOT know about the other "world". Participants learn about the other "world" 
through a short text. The control group gets a narrative with IRRELEVANT information for the 
decision-making process. On the other hand, treatment groups get a narrative with RELEVANT 
information. The two treatment groups differ in the kind of narrative presented. Treatment 
group 1 receives a personal narrative, while Treatment group 2 an impersonal one. For the 
personal narrative I create a fictional character. To test the hypothesis that the sex of the 
character might influence the decision, participants in Treatment group 1 randomly receive either
a female or male character.
"""


class C(BaseConstants):
    NAME_IN_URL = 'part_two'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1

    # Parameters
    ENDOWMENT = cu(800)
    RISK_LOW = cu(800)
    RISK_HIGH = cu(0)

    SAFE_OPTIONS = [cu(775), cu(600), cu(500), cu(400)]

    TREATMENTS = ["T0", "T1", "T2"]
    CHARACTERS = ["Samantha", "Daniel"]
    CHARACTERS_SEX = ["she", "he"]

    # Templates
    CHOICES_TEMPLATE = "part_one/temp_choices.html"
    NARRATIVES = "part_two/temp_narratives.html"
    FINAL_RESULTS_TEMPLATE = "part_two/temp_final_results.html"


###############################################################################################################
#########################################   CLASSES      ######################################################
###############################################################################################################


class Subsession(BaseSubsession):
    pass

    #################################################################################
    ################              Create Subsession               ###################
    #################################################################################


# Randomly allocate the 3 treatments at the group level:
@staticmethod
def creating_session(subsession):
    # First, Since we want balanced groups use itertools
    treatments = itertools.cycle(C.TREATMENTS)
    is_fem_character = itertools.cycle(C.CHARACTERS)

    for group in subsession.get_groups():
        group.t_groups = next(treatments)

        # Second, since we want to test whether the sex of the fictional character plays a role,
        # split only T1 participants into "Samantha" group and "Daniel" group
        if group.t_groups == "T1":
            group.character_random = next(is_fem_character)

            if group.character_random == C.CHARACTERS[0]:
                group.character_sex = C.CHARACTERS_SEX[0]
            else:
                group.character_sex = C.CHARACTERS_SEX[1]
        else:
            group.character_random = None
            group.character_sex = None

        # Last, store group level data into player data.
        for p in group.get_players():
            p.treatment_0 = group.t_groups == "T0"
            p.treatment_1 = group.t_groups == "T1"
            p.treatment_2 = group.t_groups == "T2"


# Contrary to the first part, in this app we need data at the group level
class Group(BaseGroup):
    t_groups = models.StringField(initial="-")
    character_random = models.StringField()
    character_sex = models.StringField()


# Same scenarios as in part_one plus additional models
class Player(BasePlayer):
    risk_1 = models.BooleanField(label="Scenario 1")
    risk_2 = models.BooleanField(label="Scenario 2")
    risk_3 = models.BooleanField(label="Scenario 3")
    risk_4 = models.BooleanField(label="Scenario 4")

    treatment_0 = models.BooleanField(initial=False)
    treatment_1 = models.BooleanField(initial=False)
    treatment_2 = models.BooleanField(initial=False)

    scenario_random = models.IntegerField()

    risk_random = models.BooleanField()
    risk_random_str = models.StringField()
    safe_random_str = models.StringField()

    lottery_random = models.CurrencyField()
    lottery_random_str = models.StringField()


###############################################################################################################
##########################################     PAGES      #####################################################
###############################################################################################################


class Instructions(Page):
    pass


class Narratives(Page):
    pass


class Choices(Page):
    form_model = "player"
    form_fields = ["risk_1", "risk_2", "risk_3", "risk_4"]


class ResultsWaitPage(WaitPage):
    form_model = "player"
    form_fields = ["scenario_random", "risk_random", "lottery_random",
                   "risk_random_str", "safe_random_str", "lottery_random_str"]

    # Define payoffs part_two:
    @staticmethod
    def after_all_players_arrive(group: Group):

        # Analogous to Part I
        p2_player_lists = group.get_players()

        # Select a random scenario for payment:
        for p in p2_player_lists:
            p.scenario_random = random.randint(1, 4)
            list_choices = [p.risk_1, p.risk_2, p.risk_3, p.risk_4]
            p.risk_random = list_choices[p.scenario_random - 1]

            if p.risk_random:
                p.risk_random_str = "Risky Lottery"
                p.safe_random_str = " "
            else:
                p.risk_random_str = "Safe Option"
                p.safe_random_str = str(C.SAFE_OPTIONS[p.scenario_random - 1])

            if p.participant.c_role == "Non Elite":
                p.safe_random_str = " "

        p2_JW = p2_player_lists[0]
        p2_E = p2_player_lists[1]
        p2_NE = p2_player_lists[2]

        # JW participants have no restriction --> option chosen, option realized
        if p2_JW.risk_random:
            p2_JW.lottery_random = random.choice([C.RISK_LOW, C.RISK_HIGH])
            p2_JW.payoff = C.ENDOWMENT - p2_JW.lottery_random
        else:
            p2_JW.payoff = C.ENDOWMENT - C.SAFE_OPTIONS[p2_JW.scenario_random - 1]

        # E participants have no restriction --> option chosen, option realized
        if p2_E.risk_random:
            p2_E.lottery_random = random.choice([C.RISK_LOW, C.RISK_HIGH])
            p2_E.payoff = C.ENDOWMENT - p2_E.lottery_random
        else:
            p2_E.payoff = C.ENDOWMENT - C.SAFE_OPTIONS[p2_E.scenario_random - 1]

        # NE participants ALWAYS lottery --> same payoff irrespective of choice
        p2_NE.lottery_random = random.choice([C.RISK_LOW, C.RISK_HIGH])
        p2_NE.payoff = C.ENDOWMENT - p2_NE.lottery_random

        # Store data at the participant level
        for p in group.get_players():
            participant = p.participant

            participant.p2_payoff = p.payoff
            participant.p2_risk_1 = p.risk_1
            participant.p2_risk_2 = p.risk_2
            participant.p2_risk_3 = p.risk_3
            participant.p2_risk_4 = p.risk_4
            participant.p2_scenario_random = p.scenario_random
            participant.p2_risk_random = p.risk_random
            participant.p2_risk_random_str = p.risk_random_str
            participant.p2_safe_random_str = p.safe_random_str
            participant.p2_lottery_random = p.field_maybe_none("lottery_random")

            p.lottery_random_str = str(p.field_maybe_none("lottery_random"))

            if p.lottery_random_str == "None":
                p.lottery_random_str = " "

            participant.p2_lottery_random_str = p.lottery_random_str


class Final_Results(Page):
    pass




page_sequence = [Instructions, Narratives, Choices, ResultsWaitPage, Final_Results]
