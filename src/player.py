"""
Player class
Represents the player

Right now a base level 1 Paladin but will expand to make it customizable
"""
import random
import logging

from dnd_character.classes import Paladin, Wizard, Monk, Bard, Rogue, Druid
from dnd_character.equipment import Item

import fantasynames

logging.basicConfig(format="\n[%(asctime)s] %(name)s - %(levelname)s - %(message)s\n")


class Player:
    def __init__(self,
        first_name: str = "",
        last_name: str = "",
        char_class: str = "",
        race: str = "",
        alignment: str = "",
        level: int = -1,
        hit_points: int = -1,
        gender: str = "",
        description: str = "",
        background: str = "",
        strength: int = -1,
        dexterity: int = -1,
        constitution: int = -1,
        intelligence: int = -1,
        wisdom: int = -1,
        charisma: int = -1,
        age: int = -1
    ):
        # add in location tracking after adding in worlds
        # table
        # self.location = []
        
        # set player first name and last name
        if first_name != "" and last_name != "":
            self.player_first_name = first_name
            self.player_last_name = last_name
        else:
            # using fantasy human names
            ffull_name = fantasynames.human().split(" ")
            self.player_first_name = ffull_name[0]

            if ffull_name[1] == "of" or ffull_name[1] == "de":
                self.player_first_name += f" {ffull_name[1]}"
                self.player_last_name = ffull_name[2]
            else:
                self.player_last_name = ffull_name[1]
        
        # set player class
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
            ("Rouge", Rogue(name=f"{self.player_first_name} {self.player_last_name}")),
            ("Druid", Druid(name=f"{self.player_first_name} {self.player_last_name}")),
        ]
        
        if char_class != "":
            self.player_class = char_class
            pplayer = [x for x in self.possible_players if x[0] == self.player_class][0]
            self.dndc = pplayer[1]
        else:
            rand_player_select = random.choice(self.possible_players)
            self.player_class = rand_player_select[0]
            self.dndc = rand_player_select[1]

        # setup logging
        self.class_logger = logging.getLogger(__name__)
        self.class_logger.setLevel(logging.DEBUG)

        # give players starting equipment
        # need to add loading from item database by session
        if self.player_class == "Paladin":
            self.dndc.give_item(Item("longsword"))
            self.dndc.give_item(Item("shield"))
        elif self.player_class == "Wizard" or self.player_class == "Rouge":
            self.dndc.give_item(Item("dagger"))
        elif self.player_class == "Bard":
            self.dndc.give_item(Item("longsword"))

        self.dndc.give_item(Item("explorers-pack"))

        # set stats if any set
        if level > 0:
            self.dndc.level = level
        
        if hit_points > 0:
            self.dndc.current_hp = hit_points

        if strength >= 0:
            self.dndc.strength = strength

        if dexterity >= 0:
            self.dndc.dexterity = dexterity

        if constitution >= 0:
            self.dndc.constitution = constitution

        if intelligence >= 0:
            self.dndc.intelligence = intelligence

        if wisdom >= 0:
            self.dndc.wisdom = wisdom

        if charisma >= 0:
            self.dndc.charisma = charisma

        # set player race
        if race != "":
            self.dndc.race = race
        else:
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
            self.dndc.race = random.choice(dnd_races)

        # set player alignment
        if alignment != "":
            self.dndc.alignment = alignment
        else:
            dnd_alignments = ["LG", "NG", "CG", "LN", "TN", "CN", "LE", "NE", "CE"]
            self.dndc.alignment = random.choice(dnd_alignments)

        # set player age
        if age >= 0:
            self.dndc.age = age
        else:
            self.dndc.age = random.randint(18, 300)

        # set player gender
        if gender != "":
            self.dndc.gender = gender
        else:
            self.dndc.gender = random.choice(["Male", "Female"])

        # set player background
        if background != "":
            self.dndc.background = background
        else:
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
            self.dndc.background = random.choice(dnd_backgrounds)

        # set player descriptions
        if description != "":
            self.dndc.description = description
        else:
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
            self.dndc.description = random.choice(dnd_descriptions)

    def player_info(self) -> dict:
        """
        Return player stats as dict
        """

        stats_json = {
            "name": self.dndc.name,
            "age": self.dndc.age,
            "class": self.dndc.class_name,
            "level": self.dndc.level,
            "hit_points": self.dndc.current_hp,
            "race": self.dndc.race,
            "gender": self.dndc.gender,
            "alignment": self.dndc.alignment,
            "description": self.dndc.description,
            "background": self.dndc.background,
            "strength": self.dndc.strength,
            "dexterity": self.dndc.dexterity,
            "constitution": self.dndc.constitution,
            "intelligence": self.dndc.intelligence,
            "wisdom": self.dndc.wisdom,
            "charisma": self.dndc.charisma,
        }

        return stats_json

    def __str__(self):
        pinfo = ""
        pstats = self.player_info()

        for k, v in pstats.items():
            pinfo += f"{k}: {v}\n"
        
        return pinfo