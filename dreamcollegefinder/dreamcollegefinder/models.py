from django.db import models


NUMBER_OPTIONS = (
    ('', ''),
    ('1', 1),
    ('2', 2),
    ('3', 3),
    ('4', 4),
    ('5', 5),
    ('6', 6),
    ('7', 7),
    ('8', 8),
    ('9', 9),
    ('10', 10)
)

PRICE_RANGE = (
    (1, '< 15k'),
    (2, '15k-25k'),
    (3, '25k-35k'),
    (4, '> 35k')
)

class Quiz(models.Model):
    question_1 = models.CharField("How important is location for you?", max_length=2, choices=NUMBER_OPTIONS, default='')
    question_2 = models.CharField("Introduce your preferred state (Two letter code)", max_length=2, default='')
    question_3 = models.CharField("How important is having more probability of getting accepted?", max_length=2, choices=NUMBER_OPTIONS, default='')
    question_4 = models.CharField("Introduce which price range better adjusts to your budget: ", max_length=2, choices=PRICE_RANGE, default='')
    question_5 = models.CharField("How important is your budget?", max_length=2, choices=NUMBER_OPTIONS, default='')
    question_6 = models.CharField("Introduce your SAT score (or predicted score)", max_length=4, default='')
    question_7 = models.CharField("Do you want to rule out those schools for which your SAT is not enough? (Y/N)", max_length=2, default='')
    
    question_8 = models.CharField("How important is student life for you?", max_length=2, choices=NUMBER_OPTIONS, blank=True, default='')
    question_9 = models.CharField("How important is academics for you?", max_length=2, choices=NUMBER_OPTIONS, blank=True, default='')
    question_10 = models.CharField("How important is athletics for you?", max_length=2, choices=NUMBER_OPTIONS, blank=True, default='')
    question_11 = models.CharField("How important is diversity for you?", max_length=2, choices=NUMBER_OPTIONS, blank=True, default='')
    question_12 = models.CharField("How important is proffessor quality for you?", max_length=2, choices=NUMBER_OPTIONS, blank=True, default='')
    question_13 = models.CharField("How important is safety for you?", max_length=2, choices=NUMBER_OPTIONS, blank=True, default='')
    question_14 = models.CharField("How important is value for money for you?", max_length=2, choices=NUMBER_OPTIONS, blank=True, default='')

class Rankings(models.Model):
    name = models.CharField(max_length=70)
    athletics = models.IntegerField()
    academics = models.IntegerField()
    diversity = models.IntegerField()
    professors = models.IntegerField()
    safety = models.IntegerField()
    rank = models.IntegerField(null=True)
    collegeLife = models.IntegerField(null=True)

    def __str__(self):
        return self.name

class SchoolInfo(models.Model):
    name = models.CharField(max_length=70)
    location = models.CharField(max_length=50)
    acceptanceRate = models.CharField(max_length=10)
    netPrice = models.CharField(max_length=12)
    rangeSAT = models.CharField(max_length=15)

    def __str__(self):
        return self.name
