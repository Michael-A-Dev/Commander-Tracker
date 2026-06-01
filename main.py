#!/usr/bin/python 
import customtkinter as ctk 
from src.views.commander_tracker import CommanderTracker

## Window Settings ## 
ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("dark-blue") 


root = CommanderTracker() 
root.title("Commander Tracker") 
root.mainloop()