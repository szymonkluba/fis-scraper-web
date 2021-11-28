from django.db import models

RACE_KINDS = (
    ("team", "Team"),
    ("men", "Men"),
    ("women", "Women"),
    ("other", "Other"),
)


class Tournament(models.Model):
    name = models.CharField(max_length=100)


class Race(models.Model):
    place = models.CharField(max_length=50)
    tournament = models.ForeignKey("Tournament", related_name="races", on_delete=models.CASCADE)
    date = models.DateField()
    kind = models.CharField(max_length=50, choices=RACE_KINDS)
    hill_size = models.PositiveIntegerField()


class Jumper(models.Model):
    bib = models.PositiveIntegerField()
    fis_code = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    born = models.PositiveIntegerField()
    nation = models.ForeignKey("Country", related_name="jumpers", on_delete=models.CASCADE)


class Country(models.Model):
    fis_code = models.PositiveIntegerField()
    name = models.CharField(max_length=50)


class Jump(models.Model):
    distance = models.FloatField()
    points = models.FloatField()
    speed = models.FloatField(null=True, blank=True)
    judge_a = models.FloatField(null=True, blank=True)
    judge_b = models.FloatField(null=True, blank=True)
    judge_c = models.FloatField(null=True, blank=True)
    judge_d = models.FloatField(null=True, blank=True)
    judge_e = models.FloatField(null=True, blank=True)
    gate = models.IntegerField(null=True, blank=True)
    gate_points = models.FloatField(null=True, blank=True)
    wind = models.FloatField(null=True, blank=True)
    wind_points = models.FloatField(null=True, blank=True)
    rank = models.IntegerField()


class Participant(models.Model):

    jumper = models.ForeignKey("Jumper", related_name="participated", on_delete=models.CASCADE)
    jump_1 = models.ForeignKey(
        "Jump",
        null=True,
        blank=True,
        related_name="first_jumps",
        on_delete=models.CASCADE
    )
    jump_2 = models.ForeignKey(
        "Jump",
        null=True,
        blank=True,
        related_name="second_jumps",
        on_delete=models.CASCADE
    )
    race = models.ForeignKey("Race", on_delete=models.CASCADE)
    total_points = models.FloatField(null=True, blank=True)
    diff = models.FloatField(null=True, blank=True)
    disqualified = models.BooleanField(default=False)
