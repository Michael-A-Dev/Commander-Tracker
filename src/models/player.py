""" 
A small class to represent a player object
"""
class Player:
    def __init__(self, name:str) -> None:
        self.name = name
        
        self.damage_given: int = 0
        self.damage_taken: int = 0