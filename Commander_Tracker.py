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
def get_exe_path():
    return os.path.dirname(os.path.abspath(sys.argv[0]))
    
def load_config(config_path):
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {'pos': {'x': 100, 'y': 100}, 'names': [""]}
    return {'pos': {'x': 100, 'y': 100}, 'names': [""]}

def save_config(window, names, config_path):
    config = {
        'pos': {'x': window.winfo_x(), 'y': window.winfo_y()},
        'names': names
    }
    with open(config_path, 'w') as f:
        json.dump(config, f)

def on_close(window, names, config_path):
    save_config(window, names, config_path)
    window.destroy()
    
def options_window(root):
    def save_options():
        new_names = names_box.get("0.0", ctk.END).strip().split('\n')
        updated_names = [name.strip() for name in new_names]
        names.clear()
        names.extend(updated_names)
        update_names()
        save_config(root, names, config_path)
        popup.destroy()
    
    root_x = root.winfo_x() + 10
    root_y = root.winfo_y() + 10
    popup = ctk.CTkToplevel(root)
    popup.title("Names List")
    popup.geometry(f"500x210+{root_x}+{root_y}")
    popup.resizable(False, False)
    
    names_box = ctk.CTkTextbox(popup)
    names_box.grid(row = 0, rowspan = 5, column = 0, padx = (5, 5), pady = (5, 5))
    names_box.insert("0.0", "\n".join(names))
    
    instruction_label = ctk.CTkLabel(popup, text = instructions)
    instruction_label.grid(row = 0, column = 1, padx = (5, 5), pady = (5, 5))
    
    save_button = ctk.CTkButton(popup, text = "Save Names", command = save_options)
    save_button.grid(row = 4, column = 1, padx = (5, 5), pady = (5, 5))
    
    popup.grab_set()
    popup.focus()
    popup.transient(root)
    
def update_names():
    player1_name.configure(values = names)
    player2_name.configure(values = names)
    player3_name.configure(values = names)

def reset_damage():
    player1_given.set(0)
    player1_taken.set(0)
    
    player2_given.set(0)
    player2_taken.set(0)
    
    player3_given.set(0)
    player3_given.set(0)

def reset_all():
    player1_name.set("")
    player1_given.set(0)
    player1_taken.set(0)
    
    player2_name.set("")
    player2_given.set(0)
    player2_taken.set(0)
    
    player3_name.set("")
    player3_given.set(0)
    player3_given.set(0)
    
    clear_all_counters()
    
def uptick_counter(event, counter_var):
    current_value = counter_var.get()
    counter_var.set(current_value + 1)

def downtick_counter(event, counter_var):
    current_value = counter_var.get()
    if current_value > 0:  # Prevent going below 0
        counter_var.set(current_value - 1)
        
def clear_counter(event, counter_var):
    counter_var.set(0)

def clear_all_counters():
    for counter in counters:
        counter.set(0)
        
def custom_counter_window(root, custom_counters):
    def create_custom_counter(event = None):
        popup.destroy()
        if not name.get() == "":
            new_counter = Custom_Counter.Custom_Counter(root, name.get())
            custom_counters.append(new_counter)
    
    root_x = root.winfo_x() + 10
    root_y = root.winfo_y() + 10
    popup = ctk.CTkToplevel(root)
    popup.title("Name Counter")
    popup.geometry(f"150x110+{root_x}+{root_y}")
    popup.resizable(False, False)
    
    name_label = ctk.CTkLabel(popup, text = "Custom Counter Name")
    name_label.grid(row = 0, column = 0, padx = (5,5), pady = (0,5), sticky = "ew")
    
    name = ctk.StringVar()
    name_entry = ctk.CTkEntry(popup, textvariable = name, justify = ctk.CENTER)
    name_entry.grid(row = 1, column = 0, padx = (5,5), pady = (0,5), sticky = "ew")
    name_entry.bind('<Return>', create_custom_counter)
    
    create_button = ctk.CTkButton(popup, text = "Create Counter", command = create_custom_counter)
    create_button.grid(row = 3, column = 0, padx = (5, 5), pady = (5, 5), sticky = "ew")

    popup.transient(root)
    popup.focus()
    popup.grab_set()
    
## Window Settings ##
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

config_file = "tracker_config.json"
config_path = os.path.join(get_exe_path(), config_file)

config = load_config(config_path)
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

counters_canvas = ctk.CTkCanvas(root, width = 400, height = 40, bg = "#1a1a1a", highlightthickness = 0)
counters_canvas.grid(row = 0, column = 0, columnspan = 3, padx = (5,5), pady = (5,5), sticky = "ew")
symbols = [Mana.redManaSVG, Mana.greenManaSVG, Mana.whiteManaSVG, Mana.blueManaSVG, Mana.blackManaSVG, Mana.colourlessManaSVG, Mana.poisonSVG, Mana.energySVG]
counters = []
custom_counters = []

for i, symbol in enumerate(symbols):
    x = 15 + i * 35
    y = 20
    counter_symbol_svg = tksvg.SvgImage(data=symbols[i])
    counter_symbol = ctk.CTkLabel(root, text = "", image = counter_symbol_svg)
    counter_symbol.place(x = x + 4,y = y, anchor = ctk.CENTER)

    counter = ctk.IntVar(value = 0)
    counters.append(counter)

    counter_tracker = ctk.CTkLabel(root, textvariable = counter, text_color = "white", height = 18, width = 15)
    counter_tracker.place(x = x + 4, y = y + 22, anchor = ctk.CENTER)
    
    counter_symbol.bind("<Button-1>", lambda event, var=counter: uptick_counter(event, var))
    counter_symbol.bind("<Button-3>", lambda event, var=counter: downtick_counter(event, var))
    counter_symbol.bind("<Shift-Button-1>", lambda event, var=counter: clear_counter(event, var))
    counter_symbol.bind("<Control-Button-1>", lambda event, var=counter: clear_all_counters())
    counter_tracker.bind("<Button-1>", lambda event, var=counter: uptick_counter(event, var))
    counter_tracker.bind("<Button-3>", lambda event, var=counter: downtick_counter(event, var))
    counter_tracker.bind("<Shift-Button-1>", lambda event, var=counter: clear_counter(event, var))
    counter_tracker.bind("<Control-Button-1>", lambda event, var=counter: clear_all_counters())

custom_counter = ctk.CTkButton(root, text = "Custom Counter", command = lambda: custom_counter_window(root, custom_counters), width = 80)
custom_counter.place(x = 340, y = 27, anchor = ctk.CENTER)

vert_separator = ctk.CTkCanvas(root, height = 54, width = 1, bg = "#333333", highlightthickness = 0)
vert_separator.place(x = 213, y = 0)
separator = ctk.CTkCanvas(root, height = 1, width = 400, bg = "#333333", highlightthickness = 0)
separator.place(x = 0, y = 53)

name_label = ctk.CTkLabel(root, text = "Name", font = bold_font)
name_label.grid(sticky = "S", row = 1, column = 0, padx = (5,5), pady = (10,0))

damage_dealt_label = ctk.CTkLabel(root, text = "Damage Dealt", font = bold_font, width = 150)
damage_dealt_label.grid(sticky = "S", row = 1, column = 1, padx = (5,5), pady = (10,0))

damage_received_label = ctk.CTkLabel(root, text = "Damage Received", font = bold_font, width = 150)
damage_received_label.grid(sticky = "S", row = 1, column = 2, padx = (5,5), pady = (10,0))

## Player 1 ##
player1_name = ctk.CTkComboBox(root, values = names)
player1_name.grid(row = 2, column = 0, padx = (5,5), pady = (0,5), sticky = "ew")

player1_given = CTkSpinbox.CTkSpinbox(root, start_value = 0, min_value = 0, max_value = 21, scroll_value = 1, \
                                     font = ("Segoe UI", 13), height = 30, border_width = 0, corner_radius = 100, button_corner_radius = 100)
player1_given.grid(row = 2, column = 1, padx = (5,5), pady = (0,5), sticky = "ew")

player1_taken = CTkSpinbox.CTkSpinbox(root, start_value = 0, min_value = 0, max_value = 21, scroll_value = 1, \
                                     font = ("Segoe UI", 13), height = 30, border_width = 0, corner_radius = 100, button_corner_radius = 100)
player1_taken.grid(row = 2, column = 2, padx = (5,5), pady = (0,5), sticky = "ew")

## Player 2 ##
player2_name = ctk.CTkComboBox(root, values = names)
player2_name.grid(row = 3, column = 0, padx = (5,5), pady = (5,5), sticky = "ew")

player2_given = CTkSpinbox.CTkSpinbox(root, start_value = 0, min_value = 0, max_value = 21, scroll_value = 1, \
                                     font = ("Segoe UI", 13), height = 30, border_width = 0, corner_radius = 100, button_corner_radius = 100)
player2_given.grid(row = 3, column = 1, padx = (5,5), pady = (5,5), sticky = "ew")

player2_taken = CTkSpinbox.CTkSpinbox(root, start_value = 0, min_value = 0, max_value = 21, scroll_value = 1, \
                                     font = ("Segoe UI", 13), height = 30, border_width = 0, corner_radius = 100, button_corner_radius = 100)
player2_taken.grid(row = 3, column = 2, padx = (5,5), pady = (5,5), sticky = "ew")

## Player 3 ##
player3_name = ctk.CTkComboBox(root, values = names)
player3_name.grid(row = 4, column = 0, padx = (5,5), pady = (5,5), sticky = "ew")

player3_given = CTkSpinbox.CTkSpinbox(root, start_value = 0, min_value = 0, max_value = 21, scroll_value = 1, \
                                     font = ("Segoe UI", 13), height = 30, border_width = 0, corner_radius = 100, button_corner_radius = 100)
player3_given.grid(row = 4, column = 1, padx = (5,5), pady = (5,5), sticky = "ew")

player3_given = CTkSpinbox.CTkSpinbox(root, start_value = 0, min_value = 0, max_value = 21, scroll_value = 1, \
                                     font = ("Segoe UI", 13), height = 30, border_width = 0, corner_radius = 100, button_corner_radius = 100)
player3_given.grid(row = 4, column = 2, padx = (5,5), pady = (5,5), sticky = "ew")

## Reset Buttons ##
reset_damage_button = ctk.CTkButton(root, text = "Reset Damage", command = reset_damage)
reset_damage_button.grid(row = 5, column = 0, padx = (5,5), pady = (5,5))
options_button = ctk.CTkButton(root, text = "Options", command = lambda: options_window(root))
options_button.grid(row = 5, column = 1, padx = (5,5), pady = (5,5))
reset_all_button = ctk.CTkButton(root, text = "Reset All", command = reset_all)
reset_all_button.grid(row = 5, column = 2, padx = (5,5), pady = (5,5))

root.protocol("WM_DELETE_WINDOW", lambda: on_close(root, names, config_path))

root.mainloop()