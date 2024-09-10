#!/usr/bin/python
import customtkinter as ctk
import CTkSpinbox
import json
import Mana
import os
import sys
import tksvg

instructions = "Enter your player names in the box to the left.\nEach name should be on a new line."

## Functions ##
def getExePath():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.abspath(sys.argv[0]))
    
def loadConfig(configPath):
    if os.path.exists(configPath):
        with open(configPath, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {'pos': {'x': 100, 'y': 100}, 'names': [""]}
    return {'pos': {'x': 100, 'y': 100}, 'names': [""]}

def saveConfig(window, names, configPath):
    config = {
        'pos': {'x': window.winfo_x(), 'y': window.winfo_y()},
        'names': names
    }
    with open(configPath, 'w') as f:
        json.dump(config, f)

def onClose(window, names, configPath):
    saveConfig(window, names, configPath)
    window.destroy()
    
def nameUpdatePopup(root):
    def saveNames():
        newNames = namesBox.get("0.0", ctk.END).strip().split('\n')
        updatedNames = [name.strip() for name in newNames]
        names.clear()
        names.extend(updatedNames)
        updateNames()
        saveConfig(root, names, configPath)
        popup.destroy()
    
    rootX = root.winfo_x() + 10
    rootY = root.winfo_y() + 10
    popup = ctk.CTkToplevel(root)
    popup.title("Names List")
    popup.geometry(f"500x210+{rootX}+{rootY}")
    popup.resizable(False, False)
    
    namesBox = ctk.CTkTextbox(popup)
    namesBox.grid(row = 0, rowspan = 5, column = 0, padx = (5, 5), pady = (5, 5))
    namesBox.insert("0.0", "\n".join(names))
    
    instructionLabel = ctk.CTkLabel(popup, text = instructions)
    instructionLabel.grid(row = 0, column = 1, padx = (5, 5), pady = (5, 5))
    
    saveButton = ctk.CTkButton(popup, text = "Save Names", command = saveNames)
    saveButton.grid(row = 4, column = 1, padx = (5, 5), pady = (5, 5))
    
    popup.grab_set()
    popup.focus()
    popup.transient(root)
    
def updateNames():
    player1Name.configure(values = names)
    player2Name.configure(values = names)
    player3Name.configure(values = names)

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
    
    resetCounters()
    
def updateCounter(event, counter_var):
    current_value = counter_var.get()
    if event.num == 1:  # Left click
        counter_var.set(current_value + 1)
    elif event.num == 3:  # Right click
        if current_value > 0:  # Prevent going below 0
            counter_var.set(current_value - 1)

def resetCounters():
    for counter in counters:
        counter.set(0)

## Window Settings ##
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

configFile = "tracker_config.json"
configPath = os.path.join(getExePath(), configFile)

config = loadConfig(configPath)
pos = config.get('pos', {'x': 100, 'y': 100})
names = config.get('names', ["","No Names"])

root = ctk.CTk()
root.geometry(f"400x250+{pos['x']}+{pos['y']}")
root.title("Commander Tracker")
root.resizable(False, False)
root.grid_columnconfigure(0, weight = 1)
root.grid_columnconfigure([1, 2], weight = 2)

manaDots = ctk.CTkCanvas(root, width = 400, height = 40, bg = "#1a1a1a", highlightthickness = 0)
manaDots.grid(row = 0, column = 0, columnspan = 3, padx = (5,5), pady = (5,5), sticky = "ew")
colours = ["#db8664", "#93b483", "#f0f2c0", "#b5cde3", "#aca29a", "#beb9b2"]
symbols = [Mana.redManaSVG, Mana.greenManaSVG, Mana.whiteManaSVG, Mana.blueManaSVG, Mana.blackManaSVG, Mana.colourlessManaSVG]
counters = []

for i, colour in enumerate(colours):
    x = 20 + i * 50
    y = 20
    manaSymbolSVG = tksvg.SvgImage(data=symbols[i])
    manaSymbol = ctk.CTkLabel(root, text = "", image = manaSymbolSVG)
    manaSymbol.place(x = x + 4,y = y, anchor = ctk.CENTER)

    counter = ctk.IntVar(value = 0)
    counters.append(counter)

    manaTracker = ctk.CTkLabel(root, textvariable = counter, text_color = "white", height = 18, width = 15)
    manaTracker.place(x = x + 4, y = y + 22, anchor = ctk.CENTER)
    
    manaTracker.bind("<Button-1>", lambda event, var=counter: updateCounter(event, var))
    manaTracker.bind("<Button-3>", lambda event, var=counter: updateCounter(event, var))

resetMana = ctk.CTkButton(root, text = "Reset Mana", command = resetCounters, width = 80)
resetMana.place(x = 350, y = 30, anchor = ctk.CENTER)

separator = ctk.CTkCanvas(root, height = 1, width = 400, bg = "#333333", highlightthickness = 0)
separator.place(x = 0, y = 53)

nameLabel = ctk.CTkLabel(root, text = "Name")
nameLabel.grid(row = 1, column = 0, padx = (5, 5), pady = (5,5))

givenLabel = ctk.CTkLabel(root, text = "Damage Given", width = 150)
givenLabel.grid(row = 1, column = 1, padx = (5,5), pady = (5,5))

takenLabel = ctk.CTkLabel(root, text = "Damage Taken", width = 150)
takenLabel.grid(row = 1, column = 2, padx = (5,5), pady = (5,5))

## Player 1 ##
player1Name = ctk.CTkComboBox(root, values = names)
player1Name.grid(row = 2, column = 0, padx = (5,5), pady = (5,5), sticky = "ew")

player1Given = CTkSpinbox.CTkSpinbox(root, start_value = 0, min_value = 0, max_value = 21, scroll_value = 1, \
                                     font = ("Segoe UI", 13), height = 30, border_width = 0, corner_radius = 100, button_corner_radius = 100)
player1Given.grid(row = 2, column = 1, padx = (5,5), pady = (5,5), sticky = "ew")

player1Taken = CTkSpinbox.CTkSpinbox(root, start_value = 0, min_value = 0, max_value = 21, scroll_value = 1, \
                                     font = ("Segoe UI", 13), height = 30, border_width = 0, corner_radius = 100, button_corner_radius = 100)
player1Taken.grid(row = 2, column = 2, padx = (5,5), pady = (5,5), sticky = "ew")

## Player 2 ##
player2Name = ctk.CTkComboBox(root, values = names)
player2Name.grid(row = 3, column = 0, padx = (5,5), pady = (5,5), sticky = "ew")

player2Given = CTkSpinbox.CTkSpinbox(root, start_value = 0, min_value = 0, max_value = 21, scroll_value = 1, \
                                     font = ("Segoe UI", 13), height = 30, border_width = 0, corner_radius = 100, button_corner_radius = 100)
player2Given.grid(row = 3, column = 1, padx = (5,5), pady = (5,5), sticky = "ew")

player2Taken = CTkSpinbox.CTkSpinbox(root, start_value = 0, min_value = 0, max_value = 21, scroll_value = 1, \
                                     font = ("Segoe UI", 13), height = 30, border_width = 0, corner_radius = 100, button_corner_radius = 100)
player2Taken.grid(row = 3, column = 2, padx = (5,5), pady = (5,5), sticky = "ew")

## Player 3 ##
player3Name = ctk.CTkComboBox(root, values = names)
player3Name.grid(row = 4, column = 0, padx = (5,5), pady = (5,5), sticky = "ew")

player3Given = CTkSpinbox.CTkSpinbox(root, start_value = 0, min_value = 0, max_value = 21, scroll_value = 1, \
                                     font = ("Segoe UI", 13), height = 30, border_width = 0, corner_radius = 100, button_corner_radius = 100)
player3Given.grid(row = 4, column = 1, padx = (5,5), pady = (5,5), sticky = "ew")

player3Taken = CTkSpinbox.CTkSpinbox(root, start_value = 0, min_value = 0, max_value = 21, scroll_value = 1, \
                                     font = ("Segoe UI", 13), height = 30, border_width = 0, corner_radius = 100, button_corner_radius = 100)
player3Taken.grid(row = 4, column = 2, padx = (5,5), pady = (5,5), sticky = "ew")

## Reset Buttons ##
resetDamageButton = ctk.CTkButton(root, text = "Reset Damage", command = resetDamage)
resetDamageButton.grid(row = 5, column = 0, padx = (5,5), pady = (5,5))
optionsButton = ctk.CTkButton(root, text = "Options", command = lambda: nameUpdatePopup(root))
optionsButton.grid(row = 5, column = 1, padx = (5,5), pady = (5,5))
resetAllButton = ctk.CTkButton(root, text = "Reset All", command = resetAll)
resetAllButton.grid(row = 5, column = 2, padx = (5,5), pady = (5,5))

root.protocol("WM_DELETE_WINDOW", lambda: onClose(root, names, configPath))

root.mainloop()