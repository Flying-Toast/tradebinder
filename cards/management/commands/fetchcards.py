from datetime import date, datetime
from decimal import Decimal
import requests
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from cards import models


CARDDATA_URL = "https://archive.scryfall.com/json/scryfall-default-cards.json"
SETDATA_URL = "https://api.scryfall.com/sets"

def get_or_none(json, prop):
    if prop in json:
        return json[prop]
    else:
        return None

class Command(BaseCommand):
    help = "Updates MTG data in the database"

    def handle(self, *args, **options):
        self.stdout.write("Downloading set data...")
        set_data = requests.get(SETDATA_URL).json()["data"]
        self.stdout.write(self.style.SUCCESS("\tDone."))

        self.stdout.write("Downloading card data...")
        card_data = requests.get(CARDDATA_URL).json()
        self.stdout.write(self.style.SUCCESS("\tDone."))

        starttime = datetime.now()
        self.stdout.write(f"Processing set data ({len(set_data)} entries)...")
        num_excluded = 0
        for i in set_data:
            # skip mtgo-exclusive sets
            if i["digital"]:
                num_excluded += 1
                continue

            s = models.Set(
                    id=i["id"],
                    code=i["code"],
                    name=i["name"],
                    num_cards=i["card_count"],
                    release_date=get_or_none(i, "released_at"),
                    block_name=get_or_none(i, "block"),
                    block_code=get_or_none(i, "block_code"),
            )
            s.save()
        self.stdout.write(self.style.SUCCESS("\tDone."))
        self.stdout.write(f"\t{str(datetime.now() - starttime)[:-5]} elapsed")
        self.stdout.write(f"\t{num_excluded} entries excluded")

        starttime = datetime.now()
        self.stdout.write(f"Processing card data ({len(card_data)} entries)...")
        num_excluded = 0
        for i in card_data:
            #skip mtgo-exclusives
            if "paper" not in i["games"]:
                num_excluded += 1
                continue

            try:
                models.Set.objects.get(code=i["set"])
            except ObjectDoesNotExist:
                self.stderr.write(self.style.ERROR("\tERROR:", ending=""))
                self.stderr.write("There is no set '{i['set']}' (for the card '{i['name']}')")

            c = models.Card(
                    id=i["id"],
                    oracle_id=i["oracle_id"],
                    name=i["name"],
                    release_date=date.fromisoformat(i["released_at"]),
                    cmc=Decimal(i["cmc"]),
                    type_line=i["type_line"],
                    reserved=i["reserved"],
                    foil=i["foil"],
                    nonfoil=i["nonfoil"],
                    promo=i["promo"],
                    reprint=i["reprint"],
                    collector_number=i["collector_number"],
                    mana_cost=get_or_none(i, "mana_cost"),
                    set=models.Set.objects.get(code=i["set"]),
                    oracle_text=get_or_none(i, "oracle_text"),
                    flavor_text=get_or_none(i, "flavor_text"),
                    power=get_or_none(i, "power"),
                    toughness=get_or_none(i, "toughness"),
                    artist=get_or_none(i, "artist"),
                    loyalty=get_or_none(i, "loyalty"),
                    rarity=i["rarity"][0],
                    language=i["lang"],
                    white_identy=("W" in i["color_identity"]),
                    blue_identity=("U" in i["color_identity"]),
                    black_identity=("B" in i["color_identity"]),
                    red_identity=("R" in i["color_identity"]),
                    green_identity=("G" in i["color_identity"]),
            )
            c.save()

        self.stdout.write(self.style.SUCCESS("\tDone."))
        self.stdout.write(f"\t{str(datetime.now() - starttime)[:-5]} elapsed")
        self.stdout.write(f"\t{num_excluded} entries excluded")
