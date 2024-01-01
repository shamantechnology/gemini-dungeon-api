"""
Player class
Represents the player

Right now a base level 1 Paladin but will expand to make it customizable
"""
import random
import logging

from dnd_character.classes import (
    Paladin,
    Wizard,
    Monk,
    Bard
)

from dnd_character.equipment import Item

logging.basicConfig(format="\n[%(asctime)s] %(name)s - %(levelname)s - %(message)s\n")


class Player:
    def __init__(self, first_name: str = "", last_name: str = ""):
        self.location = []
        self.player_first_name = first_name if first_name != "" else "Player"
        self.player_last_name = last_name if last_name != "" else "One"

        self.possible_players = [
            ("Paladin", Paladin(name=f"{self.player_first_name} {self.player_last_name}")),
            ("Wizard", Wizard(name=f"{self.player_first_name} {self.player_last_name}")),
            ("Monk", Monk(name=f"{self.player_first_name} {self.player_last_name}")),
            ("Bard", Bard(name=f"{self.player_first_name} {self.player_last_name}"))
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
        elif self.player_class == "Wizard":
            self.player.give_item(Item("dagger"))
        elif self.player_class == "Bard":
            self.player.give_item(Item("longsword"))
        
        self.player.give_item(Item("explorers-pack"))

    def player_sheet(self) -> str:
        """
        Generate a player sheet for the AI to use
        """
        return str(self.player).replace("\n", " ")
