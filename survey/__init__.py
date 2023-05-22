from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    ########### Sapp_Harrod (1993) 9-Item scale Locus of Control [abbrev. of Levenson's 1974 - 7point Likert] ###################

    LOC_1 = models.IntegerField(
        label='My life is determined by my own actions.',
        choices=[1,2,3,4,5,6,7],
        widget=widgets.RadioSelect
    )

    LOC_2 = models.IntegerField(
        label='I am usually able to protect my personal interests.',
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelect
    )

    LOC_3 = models.IntegerField(
        label='I can pretty much determine what will happen in my life.',
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelect
    )

    LOC_4 = models.IntegerField(
        label='To a great extent, my life is controlled by accidental happenings.',
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelect
    )

    LOC_5 = models.IntegerField(
        label='Often there is no chance of protecting my personal interest from bad luck happenings.',
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelect
    )

    LOC_6 = models.IntegerField(
        label='When I get what I want, it\'s usually because I\'m lucky.',
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelect
    )

    LOC_7 = models.IntegerField(
        label='People like myself have little chance of protecting our personal interests where '
              'they conflict with those of strong pressure groups.',
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelect
    )

    LOC_8 = models.IntegerField(
        label='My life is chiefly controlled by powerful others.',
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelect
    )

    LOC_9 = models.IntegerField(
        label='I feel like what happens in my life is mostly determined by powerful people.',
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelect
    )

    ###########  Demographics ###################

    age = models.IntegerField(label='1. What is your age?', min=15, max=80)

    gender = models.IntegerField(
        label='2. How would you best describe yourself?',
        choices=[[1, 'Male'], [2, 'Female'], [3, 'In other way']],
        widget=widgets.RadioSelect
    )

    nationality = models.BooleanField(
        label='3. Were you born in Germany?',
        choices=[[True, 'Yes'], [False, 'No']]
    )

    migration = models.BooleanField(
        label='4. Have you spent most of your life in Germany?',
        choices=[[True, 'Yes'], [False, 'No']]
    )

    migration_parents = models.BooleanField(
        label='5. Is at least one of your parents raced and born in another country than Germany?',
        choices=[[True, 'Yes'], [False, 'No']]
    )

    soc_ladder = models.IntegerField(
        label='6. If you imagine status in society as a ladder, some groups could be described'
              ' as being closer to the top and others closer to the bottom. Thinking about yourself,'
              ' where would you place yourself in this scale?',
        choices=[[1, '1 (bottom)'], [2, '2'], [3, '3'], [4, '4'], [5, '5'],
                 [6, '6'], [7, '7'], [8, '8'], [9, '9'], [10, '10 (top)'], [-99, 'No answer']],
        widget=widgets.RadioSelectHorizontal
    )

    employment = models.IntegerField(
        label='7. Which of the following categories best describes your current employment status?',
        choices=[[1, 'Employed, Full-Time'], [2, 'Employed, Part-Time'],
                 [3, 'Unemployed, seeking for work'], [4, 'Unemployed, NOT seeking for work'],
                 [5, 'Student'], [6, 'Retired']],
    )

    income = models.IntegerField(
        label="8. What is your household's monthly available (net) income after taxes and social security?",
        choices=[[1, '0 - 520 EUR'], [2, '521 - 999 EUR'], [3, '1.000 - 1.999 EUR'],
                 [4, '2.000 - 2.999 EUR'], [5, '3.000 - 3.999 EUR'],
                 [6, '4.000 EUR or more'], [-99, 'No answer']],
    )


# FUNCTIONS
# PAGES

class LOC(Page):
    form_model = 'player'
    form_fields = ['LOC_1', 'LOC_2','LOC_3', 'LOC_4','LOC_5', 'LOC_6', 'LOC_7','LOC_8', 'LOC_9']



class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'nationality', 'migration',
                   'migration_parents', 'soc_ladder', 'employment',
                   'income']


class Summary_Payoff(Page):
    pass



page_sequence = [LOC, Demographics, Summary_Payoff]
