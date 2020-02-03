from django.db import models


class Set(models.Model):
    id = models.UUIDField(primary_key=True)
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    release_date = models.DateField()
    num_cards = models.IntegerField()
    block_code = models.CharField(max_length=10, null=True)
    block_name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Card(models.Model):
    RARITIES = (
        ("c", "common"),
        ("u", "uncommon"),
        ("r", "rare"),
        ("m", "mythic"),
    )

    id = models.UUIDField(primary_key=True)
    oracle_id = models.UUIDField()
    name = models.CharField(max_length=200)
    release_date = models.DateField()
    cmc = models.DecimalField(max_digits=10, decimal_places=3)
    type_line = models.CharField(max_length=200)
    oracle_text = models.TextField(null=True)
    flavor_text = models.TextField(null=True)
    power = models.CharField(max_length=10, null=True)
    toughness = models.CharField(max_length=10, null=True)
    reserved = models.BooleanField()
    foil = models.BooleanField()
    nonfoil = models.BooleanField()
    promo = models.BooleanField()
    reprint = models.BooleanField()
    collector_number = models.CharField(max_length=10)
    artist = models.CharField(max_length=200, null=True)
    loyalty = models.CharField(max_length=10, null=True)
    mana_cost = models.CharField(max_length=200, null=True)
    # `color_identity`s
    white_identy = models.BooleanField(default=False)
    blue_identity = models.BooleanField(default=False)
    black_identity = models.BooleanField(default=False)
    red_identity = models.BooleanField(default=False)
    green_identity = models.BooleanField(default=False)
    rarity = models.CharField(max_length=1, choices=RARITIES)
    language = models.CharField(max_length=10)
    set = models.ForeignKey(Set, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
