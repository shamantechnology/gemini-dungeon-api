"""
Player class
Represents the player

Right now a base level 1 Paladin but will expand to make it customizable
"""

from dnd_character.classes import Paladin
from dnd_character.equipment import Item
import logging

logging.basicConfig(format="\n[%(asctime)s] %(name)s - %(levelname)s - %(message)s\n")


class Player:
    def __init__(self, first_name: str = "", last_name: str = ""):
        self.location = []
        self.player_first_name = first_name if first_name != "" else "Hacker"
        self.player_last_name = last_name if last_name != "" else "McHackerface"
        self.player = Paladin(name=f"{self.player_first_name} {self.player_last_name}")

        # setup logging
        self.class_logger = logging.getLogger(__name__)
        self.class_logger.setLevel(logging.DEBUG)

        # give players starting equipment
        self.player.give_item(Item("longsword"))
        self.player.give_item(Item("shield"))
        self.player.give_item(Item("explorers-pack"))

        # self.player_stats = {
        #     "strength": 0,
        #     "wisdom": 0,
        #     "dexterity": 0,
        #     "intelligence": 0,
        #     "constitution": 0,
        #     "chrisma": 0,
        # }

        # self.player_modifiers = {
        #     "strength_modifier": 0,
        #     "wisdom_modifier": 0,
        #     "dexterity_modifier": 0,
        #     "intelligence_modifier": 0,
        #     "constitution_modifier": 0,
        #     "chrisma_modifier": 0,
        # }

        # # roll 4d6 and remove the smallest number
        # rolled_dice = list(dice.roll("4d6"))
        # rolled_dice = sorted(rolled_dice, reverse=True)
        # rolled_dice.pop()

        # # randomly choose stats to assign
        # for stat in random.choice(list(self.player_stats.keys())):
        #     self.player_stats[stat] = random.choice(rolled_dice)

        # # assign modifiers
        # for mod in list(self.player_modifiers.keys()):
        #     stat = mod.replace("_modifier", "")
        #     self.player_modifiers[mod] = math.floor((self.player_stats[stat] - 10) / 2)

        # self.player_race = "Human"
        # self.player_class = "Paladin"
        # self.player_alignment = "Lawfully Good"
        # self.player_speed = 30
        # self.initiative = (
        #     int(dice.roll("1d20")) + self.player_modifiers["dexterity_modifier"]
        # )
        # self.gold = sum(list(dice.roll("5d4"))) * 10
        # self.player_skills = ["perception", "athletics"]
        # self.player_proficiency_bonus = 2

        # self.player_level = 1
        # self.player_hp = 10 + self.player_modifiers["constitution_modifier"]
        # self.player_hit_dice = "1d10"

        # self.player_armor_class = 10 + self.player_stats["dexterity"]

        # self.player_death_saving_throws = {"passed": [0, 0, 0], "failed": [0, 0, 0]}

        # self.player_inventory = [
        #     {
        #         "name": "longsword",
        #         "type": "weapon",
        #         "damage": "1d8",
        #         "damage_type": "slashing",
        #         "weight": "3lb",
        #         "modifier": "strength_modifier",
        #         "proficiency": True,
        #     },
        #     {
        #         "name": "shield",
        #         "type": "armor",
        #         "ac": 2,
        #         "str_req": 0,
        #         "stealth": None,
        #         "weight": "6lb",
        #     },
        # ]

        # self.player_weapon_1 = {
        #     "name": "longsword",
        #     "type": "weapon",
        #     "damage": "1d8",
        #     "damage_type": "slashing",
        #     "weight": "3lb",
        #     "modifier": "strength_modifier",
        #     "proficiency": True,
        # }

        # self.player_weapon_2 = {
        #     "name": "shield",
        #     "type": "armor",
        #     "ac": 2,
        #     "str_req": 0,
        #     "stealth": None,
        #     "weight": "6lb",
        # }

    # def roll_initiative(self) -> int:
    #     dex_check = int(dice.roll("1d20")) + self.player_modifiers["dexterity_modifier"]
    #     return dex_check

    # def attack_roll(self) -> int:
    #     hit_roll = int(dice.roll("1d20"))

    #     if self.player_weapon_1["proficiency"]:
    #         hit_roll += self.player_proficiency_bonus

    #     return hit_roll

    def player_sheet(self) -> str:
        """
        Generate a player sheet for the AI to use
        """
        return str(self.player).replace("\n", " ")
