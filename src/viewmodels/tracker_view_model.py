from src.models.player import Player

class TrackerViewModel:
    """ ViewModel to represent the state of the tracker view """
    def __init__(self):
        self.players: list[Player] =[]

    def add_player(self) -> Player:
        """ Adds a player to the player list and returns the player object """
        player = Player("")
        self.players.append(player)
        return player
    
    def remove_player(self, player: Player) -> None:
        """ Removes a player from the player list """
        if len(self.players) > 1:
            print(f"Removing player {player.name}") # For Debugging purposes
            self.players.remove(player)

    def update_player_name(self, player: Player, new_name: str) -> None:
        """ Updates the name of a player """
        player.name = new_name
        print(f"Updated player name to {new_name}") # For Debugging purposes

    def update_player_damage_given(self, player: Player, damage: int) -> None:
        """ Updates the damage given of a player """
        player.damage_given = damage
        print(f"Updated player {player.name}'s damage given to {damage}") # For Debugging purposes

    def update_player_damage_taken(self, player: Player, damage: int) -> None:
        """ Updates the damage taken of a player """
        player.damage_taken = damage
        print(f"Updated player {player.name}'s damage taken to {damage}") # For Debugging purposes

    def reset_damage(self) -> None:
        """ Resets all players' damage given and taken to 0 """
        for player in self.players:
            player.damage_given = 0
            player.damage_taken = 0

    def reset_players(self) -> None:
        """ Resets all players' names to "" and damage given/taken to 0 """
        for player in self.players:
            player.name = ""
            player.damage_given = 0
            player.damage_taken = 0