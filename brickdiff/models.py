from django.db import models

class LegoBricks(models.Model):
    """
    One specific class of brick.
    """
    # A unique identifier for the part.
    uid = models.CharField(max_length=32, primary_key=True, unique=True)

    # LEGO's identifier for this class of part.
    partno = models.CharField(max_length=32)

    # The specific color of the part.
    color = models.CharField(max_length=32)

    # A description of the part.
    description = models.CharField(max_length=128)

    # The category the part is in.
    image_url = models.CharField(max_length=192)


class LegoSets(models.Model):
    """
    Pairs brick / count for a kit or diff.
    """
    setno = models.CharField(max_length=32)
    count = models.IntegerField()
    brick = models.ForeignKey(LegoBricks)

