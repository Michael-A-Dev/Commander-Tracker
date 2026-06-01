class Player:
    """ Model to represent a player in the game """
    def __init__(self, name:str = "") -> None:
        self.name = name

        self.damage_given: int = 0
        self.damage_taken: int = 0