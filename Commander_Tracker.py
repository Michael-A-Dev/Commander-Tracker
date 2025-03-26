#!/usr/bin/python
import customtkinter as ctk
import Custom_Counter
import CTkSpinbox
import json
import Mana
import os
import sys
import tksvg

instructions = "Enter your player names in the box to the left.\nEach name should be on a new line."

## Functions ##
def getExePath():
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
    
    clearAllCounters()
    
def uptickCounter(event, counter_var):
    current_value = counter_var.get()
    counter_var.set(current_value + 1)

def downtickCounter(event, counter_var):
    current_value = counter_var.get()
    if current_value > 0:  # Prevent going below 0
        counter_var.set(current_value - 1)
        
def clearCounter(event, counter_var):
    counter_var.set(0)

def clearAllCounters():
    for counter in counters:
        counter.set(0)
        
def openCustomCounter(root, custom_counters):
    def createCounter(event = None):
        popup.destroy()
        if not name.get() == "":
            new_counter = Custom_Counter.Custom_Counter(root, name.get())
            custom_counters.append(new_counter)
    
    rootX = root.winfo_x() + 10
    rootY = root.winfo_y() + 10
    popup = ctk.CTkToplevel(root)
    popup.title("Name Counter")
    popup.geometry(f"150x110+{rootX}+{rootY}")
    popup.resizable(False, False)
    
    nameLabel = ctk.CTkLabel(popup, text = "Custom Counter Name")
    nameLabel.grid(row = 0, column = 0, padx = (5,5), pady = (0,5), sticky = "ew")
    
    name = ctk.StringVar()
    nameEntry = ctk.CTkEntry(popup, textvariable = name, justify = ctk.CENTER)
    nameEntry.grid(row = 1, column = 0, padx = (5,5), pady = (0,5), sticky = "ew")
    nameEntry.bind('<Return>', createCounter)
    
    createButton = ctk.CTkButton(popup, text = "Create Counter", command = createCounter)
    createButton.grid(row = 3, column = 0, padx = (5, 5), pady = (5, 5), sticky = "ew")

    popup.transient(root)
    popup.focus()
    popup.grab_set()
    
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

bold_font = ctk.CTkFont()
bold_font['weight'] = 'bold'

manaDots = ctk.CTkCanvas(root, width = 400, height = 40, bg = "#1a1a1a", highlightthickness = 0)
manaDots.grid(row = 0, column = 0, columnspan = 3, padx = (5,5), pady = (5,5), sticky = "ew")
symbols = [Mana.redManaSVG, Mana.greenManaSVG, Mana.whiteManaSVG, Mana.blueManaSVG, Mana.blackManaSVG, Mana.colourlessManaSVG, Mana.poisonSVG, Mana.energySVG]
counters = []
custom_counters = []

for i, symbol in enumerate(symbols):
    x = 15 + i * 35
    y = 20
    manaSymbolSVG = tksvg.SvgImage(data=symbols[i])
    manaSymbol = ctk.CTkLabel(root, text = "", image = manaSymbolSVG)
    manaSymbol.place(x = x + 4,y = y, anchor = ctk.CENTER)

    counter = ctk.IntVar(value = 0)
    counters.append(counter)

    manaTracker = ctk.CTkLabel(root, textvariable = counter, text_color = "white", height = 18, width = 15)
    manaTracker.place(x = x + 4, y = y + 22, anchor = ctk.CENTER)
    
    manaSymbol.bind("<Button-1>", lambda event, var=counter: uptickCounter(event, var))
    manaSymbol.bind("<Button-3>", lambda event, var=counter: downtickCounter(event, var))
    manaSymbol.bind("<Shift-Button-1>", lambda event, var=counter: clearCounter(event, var))
    manaSymbol.bind("<Control-Button-1>", lambda event, var=counter: clearAllCounters())
    manaTracker.bind("<Button-1>", lambda event, var=counter: uptickCounter(event, var))
    manaTracker.bind("<Button-3>", lambda event, var=counter: downtickCounter(event, var))
    manaTracker.bind("<Shift-Button-1>", lambda event, var=counter: clearCounter(event, var))
    manaTracker.bind("<Control-Button-1>", lambda event, var=counter: clearAllCounters())

newCounter = ctk.CTkButton(root, text = "Custom Counter", command = lambda: openCustomCounter(root, custom_counters), width = 80)
newCounter.place(x = 340, y = 27, anchor = ctk.CENTER)

vert_separator = ctk.CTkCanvas(root, height = 54, width = 1, bg = "#333333", highlightthickness = 0)
vert_separator.place(x = 213, y = 0)
separator = ctk.CTkCanvas(root, height = 1, width = 400, bg = "#333333", highlightthickness = 0)
separator.place(x = 0, y = 53)

nameLabel = ctk.CTkLabel(root, text = "Name", font = bold_font)
nameLabel.grid(sticky = "S", row = 1, column = 0, padx = (5,5), pady = (10,0))

givenLabel = ctk.CTkLabel(root, text = "Damage Dealt", font = bold_font, width = 150)
givenLabel.grid(sticky = "S", row = 1, column = 1, padx = (5,5), pady = (10,0))

takenLabel = ctk.CTkLabel(root, text = "Damage Received", font = bold_font, width = 150)
takenLabel.grid(sticky = "S", row = 1, column = 2, padx = (5,5), pady = (10,0))

## Player 1 ##
player1Name = ctk.CTkComboBox(root, values = names)
player1Name.grid(row = 2, column = 0, padx = (5,5), pady = (0,5), sticky = "ew")

player1Given = CTkSpinbox.CTkSpinbox(root, start_value = 0, min_value = 0, max_value = 21, scroll_value = 1, \
                                     font = ("Segoe UI", 13), height = 30, border_width = 0, corner_radius = 100, button_corner_radius = 100)
player1Given.grid(row = 2, column = 1, padx = (5,5), pady = (0,5), sticky = "ew")

player1Taken = CTkSpinbox.CTkSpinbox(root, start_value = 0, min_value = 0, max_value = 21, scroll_value = 1, \
                                     font = ("Segoe UI", 13), height = 30, border_width = 0, corner_radius = 100, button_corner_radius = 100)
player1Taken.grid(row = 2, column = 2, padx = (5,5), pady = (0,5), sticky = "ew")

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