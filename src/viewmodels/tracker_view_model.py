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
            self.players.remove(player)