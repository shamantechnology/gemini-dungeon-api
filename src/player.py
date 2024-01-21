"""
Player class
Represents the player

Right now a base level 1 Paladin but will expand to make it customizable
"""
import random
import logging

from dnd_character.classes import Paladin, Wizard, Monk, Bard
from dnd_character.equipment import Item

import fantasynames

logging.basicConfig(format="\n[%(asctime)s] %(name)s - %(levelname)s - %(message)s\n")


class Player:
    def __init__(self, first_name: str = "", last_name: str = ""):
        self.location = []
        self.player_first_name = first_name if first_name != "" else "Player"
        self.player_last_name = last_name if last_name != "" else "One"

        if first_name and last_name:
            self.player_first_name = first_name
            self.player_last_name = last_name
        else:
            # using fantasy human names
            ffull_name = fantasynames.human().split(" ")
            self.player_first_name = ffull_name[0]
            self.player_last_name = ffull_name[1]

        self.possible_players = [
            (
                "Paladin",
                Paladin(name=f"{self.player_first_name} {self.player_last_name}"),
            ),
            (
                "Wizard",
                Wizard(name=f"{self.player_first_name} {self.player_last_name}"),
            ),
            ("Monk", Monk(name=f"{self.player_first_name} {self.player_last_name}")),
            ("Bard", Bard(name=f"{self.player_first_name} {self.player_last_name}")),
            ("Rouge", Bard(name=f"{self.player_first_name} {self.player_last_name}")),
            ("Druid", Bard(name=f"{self.player_first_name} {self.player_last_name}")),
        ]

        rand_player_select = random.choice(self.possible_players)
        self.player_class = rand_player_select[0]
        self.player = rand_player_select[1]

        # setup logging
        self.class_logger = logging.getLogger(__name__)
        self.class_logger.setLevel(logging.DEBUG)

        # give players starting equipment
        if self.player_class == "Paladin":
            self.player.give_item(Item("longsword"))
            self.player.give_item(Item("shield"))
        elif self.player_class == "Wizard" or self.player_class == "Rouge":
            self.player.give_item(Item("dagger"))
        elif self.player_class == "Bard":
            self.player.give_item(Item("longsword"))

        self.player.give_item(Item("explorers-pack"))

        # set player race
        dnd_races = [
            "Human",
            "Elf",
            "Dwarf",
            "Halfling",
            "Gnome",
            "Half-Elf",
            "Half-Orc",
            "Tiefling",
            "Dragonborn",
        ]
        self.player.race = random.choice(dnd_races)

        # set player alignment
        dnd_alignments = ["LG", "NG", "CG", "LN", "TN", "CN", "LE", "NE", "CE"]
        self.player.alignment = random.choice(dnd_alignments)

        # set player age
        self.player.age = random.randint(18, 300)

        # set player gender
        self.player.gender = random.choice(["Male", "Female"])

        # set player background
        dnd_backgrounds = [
            "Novice Adventurer",
            "Caring Medical Doctor",
            "Cheating Theif",
            "Depressed Traveling Musician",
            "Optimistic Scientst",
            "Town Square Influencer",
            "Haunted Librarian Scholar",
            "Wandering Folk Hero",
            "Cunning Street Urchin",
            "Mysterious Court Jester",
            "Arcane Eldritch Investigator",
            "Noble Wilderness Tracker",
            "Sneaky Pirate Captain",
            "Divine Acolyte of Light",
            "Enigmatic Shadowy Infiltrator",
        ]
        self.player.background = random.choice(dnd_backgrounds)

        # set player descriptions
        dnd_descriptions = [
            "Mysterious wanderer with a dark past",
            "Energetic and optimistic aspiring hero",
            "Wise sage with ancient knowledge",
            "Sly and cunning trickster",
            "Noble with a strong sense of duty",
            "Fearless and battle-hardened warrior",
            "Enigmatic spellcaster with arcane secrets",
            "Curious explorer always seeking adventure",
            "Loyal and protective guardian of the weak",
            "Charismatic and charming diplomat",
            "Brooding loner haunted by inner demons",
        ]
        self.player.description = random.choice(dnd_descriptions)

    def player_info(self) -> dict:
        """
        Return player stats as dict
        """

        stats_json = {
            "name": self.player.name,
            "class": self.player.class_name,
            "level": self.player.level,
            "hit_points": self.player.current_hp,
            "race": self.player.race,
            "alignment": self.player.alignment,
            "description": self.player.description,
            "background": self.player.background,
            "strength": self.player.strength,
            "dexterity": self.player.dexterity,
            "constitution": self.player.constitution,
            "intelligence": self.player.intelligence,
            "wisdom": self.player.wisdom,
            "charisma": self.player.charisma,
        }

        return stats_json
