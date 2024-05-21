import customtkinter as ctk
import CTkSpinbox

## Functions ##
def resetDamage():
    player1Given.set(0)
    player1Taken.set(0)
    
    player2Given.set(0)
    player2Taken.set(0)
    
    player3Given.set(0)
    player3Taken.set(0)

def resetAll():
    player1Name.set("")
    player1Given.set(0)
    player1Taken.set(0)
    
    player2Name.set("")
    player2Given.set(0)
    player2Taken.set(0)
    
    player3Name.set("")
    player3Given.set(0)
    player3Taken.set(0)

## Window Settings ##
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.geometry("400x200")
root.title("Commander Damage")
root.resizable(False, False)
root.grid_columnconfigure(0, weight = 1)
root.grid_columnconfigure([1, 2], weight = 2)

nameLabel = ctk.CTkLabel(root, text = "Name")
nameLabel.grid(row = 0, column = 0, padx = (5, 5), pady = (5,5))

givenLabel = ctk.CTkLabel(root, text = "Damage Given", width = 150)
givenLabel.grid(row = 0, column = 1, padx = (5,5), pady = (5,5))

takenLabel = ctk.CTkLabel(root, text = "Damage Taken", width = 150)
takenLabel.grid(row = 0, column = 2, padx = (5,5), pady = (5,5))

names = ["", "Al", "Brett", "Cain", "Dylan", "Michael", "Mitchell", "Nikki", "Other Alex"]

## Player 1 ##
player1Name = ctk.CTkComboBox(root, values = names)
player1Name.grid(row = 1, column = 0, padx = (5,5), pady = (5,5), sticky = "ew")

player1Given = CTkSpinbox.CTkSpinbox(root, start_value = 0, min_value = 0, max_value = 21, scroll_value = 1, \
                                     font = ("Segoe UI", 13), height = 30, border_width = 0, corner_radius = 100, button_corner_radius = 100)
player1Given.grid(row = 1, column = 1, padx = (5,5), pady = (5,5), sticky = "ew")

player1Taken = CTkSpinbox.CTkSpinbox(root, start_value = 0, min_value = 0, max_value = 21, scroll_value = 1, \
                                     font = ("Segoe UI", 13), height = 30, border_width = 0, corner_radius = 100, button_corner_radius = 100)
player1Taken.grid(row = 1, column = 2, padx = (5,5), pady = (5,5), sticky = "ew")

## Player 2 ##
player2Name = ctk.CTkComboBox(root, values = names)
player2Name.grid(row = 2, column = 0, padx = (5,5), pady = (5,5), sticky = "ew")

player2Given = CTkSpinbox.CTkSpinbox(root, start_value = 0, min_value = 0, max_value = 21, scroll_value = 1, \
                                     font = ("Segoe UI", 13), height = 30, border_width = 0, corner_radius = 100, button_corner_radius = 100)
player2Given.grid(row = 2, column = 1, padx = (5,5), pady = (5,5), sticky = "ew")

player2Taken = CTkSpinbox.CTkSpinbox(root, start_value = 0, min_value = 0, max_value = 21, scroll_value = 1, \
                                     font = ("Segoe UI", 13), height = 30, border_width = 0, corner_radius = 100, button_corner_radius = 100)
player2Taken.grid(row = 2, column = 2, padx = (5,5), pady = (5,5), sticky = "ew")

## Player 3 ##
player3Name = ctk.CTkComboBox(root, values = names)
player3Name.grid(row = 3, column = 0, padx = (5,5), pady = (5,5), sticky = "ew")

player3Given = CTkSpinbox.CTkSpinbox(root, start_value = 0, min_value = 0, max_value = 21, scroll_value = 1, \
                                     font = ("Segoe UI", 13), height = 30, border_width = 0, corner_radius = 100, button_corner_radius = 100)
player3Given.grid(row = 3, column = 1, padx = (5,5), pady = (5,5), sticky = "ew")

player3Taken = CTkSpinbox.CTkSpinbox(root, start_value = 0, min_value = 0, max_value = 21, scroll_value = 1, \
                                     font = ("Segoe UI", 13), height = 30, border_width = 0, corner_radius = 100, button_corner_radius = 100)
player3Taken.grid(row = 3, column = 2, padx = (5,5), pady = (5,5), sticky = "ew")

## Reset Buttons ##
resetDamageButton = ctk.CTkButton(root, text = "Reset Damage", command = resetDamage)
resetDamageButton.grid(row = 4, column = 0, padx = (5,5), pady = (5,5))
resetAllButton = ctk.CTkButton(root, text = "Reset All", command = resetAll)
resetAllButton.grid(row = 4, column = 2, padx = (5,5), pady = (5,5))

root.mainloop()