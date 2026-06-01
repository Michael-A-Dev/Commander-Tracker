from src.resources.config import Config
from src.models.player import Player

class TrackerViewModel:
    """ ViewModel to represent the state of the tracker view """
    def __init__(self):
        self.players: list[Player] =[]
        self.config = Config()

    @property
    def saved_names(self):
        return self.config.saved_names

    @property
    def pos(self):
        return self.config.pos

    def add_player(self) -> Player:
        """ Adds a player to the player list and returns the player object """
        player = Player("")
        self.players.append(player)
        return player
    
    def remove_player(self, player: Player) -> None:
        """ Removes a player from the player list """
        if len(self.players) > 1:
            # print(f"Removing player {player.name}") # For Debugging purposes
            self.players.remove(player)

    def update_player_name(self, player: Player, new_name: str) -> None:
        """ Updates the name of a player """
        player.name = new_name
        # print(f"Updated player name to {new_name}") # For Debugging purposes

    def update_player_damage_given(self, player: Player, damage: int) -> None:
        """ Updates the damage given of a player """
        player.damage_given = damage
        # print(f"Updated player {player.name}'s damage given to {damage}") # For Debugging purposes

    def update_player_damage_taken(self, player: Player, damage: int) -> None:
        """ Updates the damage taken of a player """
        player.damage_taken = damage
        # print(f"Updated player {player.name}'s damage taken to {damage}") # For Debugging purposes

    def reset_damage(self) -> None:
        """ Resets all players' damage given and taken to 0 """
        for player in self.players:
            player.damage_given = 0
            player.damage_taken = 0
        # print("Reset all players' damage") # For Debugging purposes

    def reset_players(self) -> None:
        """ Resets all players' names to "" and damage given/taken to 0 """
        for player in self.players:
            player.name = ""
            player.damage_given = 0
            player.damage_taken = 0
        # print("Reset all players") # For Debugging purposes

    def update_and_save_names(self, names: list[str]):
        """ Updates the saved names in the config and saves the config """
        self.config.saved_names = names
        self.config.save_config()
        # print(f"Updated and saved names: {names}") # For Debugging purposes

    def save_window_position(self, x: int, y: int):
        self.config.pos = {"x": x, "y": y}
        self.config.save_config()
        # print(f"Saved window position: x={x}, y={y}") # For Debugging purposes