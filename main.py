#!/usr/bin/python 
import customtkinter as ctk 
from src.views.commander_tracker_view import Commander_Tracker as Commander_Tracker

## Window Settings ## 
ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("dark-blue") 


root = Commander_Tracker() 
root.title("Commander Tracker") 
root.mainloop()