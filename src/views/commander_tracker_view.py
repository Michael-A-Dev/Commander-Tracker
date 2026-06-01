#!/usr/bin/python
import customtkinter as ctk
import CTkSpinbox
import json
import os
import sys
import tksvg
import src.views.Custom_Counter as Custom_Counter
from src.views.components.player_row import PlayerRow
import src.resources.mana as Mana
from src.viewmodels.tracker_view_model import TrackerViewModel


class Commander_Tracker(ctk.CTk):
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        self.instructions = "Enter your player names in the box to the left.\nEach name should be on a new line."
        self.viewmodel = TrackerViewModel()
        
        ## Load options from config ##
        self.config_file = "tracker_config.json"
        self.config_path = os.path.join(self.get_exe_path(), self.config_file)
        self.config = self.load_config()
        self.pos = self.config.get('pos', {'x': 100, 'y': 100})
        self.saved_names = self.config.get('names', ["","No Names"]) # renamed to saved_names to avoid confusion with player.name

        ## Set initial window settings ##
        self.geometry(f"400x250+{self.pos['x']}+{self.pos['y']}")
        self.title("Commander Tracker")
        self.resizable(False, False)

        ## Frames to separate dynamic and static content
        self.mana_frame = ctk.CTkFrame(self) # For mana/options/reset widgets
        self.mana_frame.grid(row = 0, column = 0, sticky = "nsew")
        self.mana_frame.grid_rowconfigure(0, weight = 1, minsize = 50)

        self.header_frame = ctk.CTkFrame(self) # For player table headers
        self.header_frame.grid(row = 1, column = 0, sticky = "nsew")
        self.header_frame.grid_columnconfigure(0, weight = 0, minsize = 25)
        self.header_frame.grid_columnconfigure([1], weight = 3, minsize = 160)
        self.header_frame.grid_columnconfigure([2, 3], weight = 2)
        
        self.player_frame = ctk.CTkFrame(self) # For the player damage details
        self.player_frame.grid(row = 2, column = 0, sticky = "nsew")
        self.player_frame.grid_columnconfigure(0, weight = 0, minsize = 25)
        self.player_frame.grid_columnconfigure([1], weight = 3, minsize = 160)
        self.player_frame.grid_columnconfigure([2, 3], weight = 2)
        
        ## Player Rows ##
        self.player_rows = []

        ## Bold version of default font ##
        self.bold_font = ctk.CTkFont()
        self.bold_font['weight'] = 'bold'

        ## Create mana frame ##
        ## Create clickable mana/counter symbols ##
        symbols = Mana.get_all_symbols()
        self.counters = []

        self.counter_frame = ctk.CTkFrame(self.mana_frame, fg_color="#242424", width = 285, height = 55)

        for i, symbol in enumerate(symbols):
            x = 15 + i * 35
            y = 20
            counter_symbol_svg = tksvg.SvgImage(data=symbol)
            counter_symbol = ctk.CTkLabel(self.counter_frame, text = "", image = counter_symbol_svg) # type: ignore
            counter_symbol.place(x = x + 4, y = y, anchor = ctk.CENTER)

            counter = ctk.IntVar(value = 0)
            self.counters.append(counter)

            counter_tracker = ctk.CTkLabel(self.counter_frame, textvariable = counter, text_color = "white", height = 18, width = 15)
            counter_tracker.place(x = x + 4, y = y + 22, anchor = ctk.CENTER)
    
            for c in [counter_symbol, counter_tracker]:
                c.bind("<Button-1>", lambda event, var=counter: self.event_handler(event, var))
                c.bind("<Button-3>", lambda event, var=counter: self.event_handler(event, var))
                c.bind("<Shift-Button-1>", lambda event, var=counter: self.event_handler(event, var))
                c.bind("<Control-Button-1>", lambda event, var=counter: self.event_handler(event, var))

        self.counter_frame.grid(row = 0, column = 0, columnspan = 2, sticky = "w")

        custom_counter = ctk.CTkButton(self.mana_frame, text = "Add Counter", command = lambda: self.custom_counter_window(), width = 100)
        custom_counter.grid(row = 0, column = 2, padx = (5,5))
        options_button = ctk.CTkButton(self.mana_frame, text = "Options", command = lambda: self.options_window(), width = 70)
        options_button.grid(row = 0, column = 3, padx = (5,5))

        vert_separator = ctk.CTkCanvas(self.mana_frame, height = 54, width = 1, bg = "#333333", highlightthickness = 0)
        vert_separator.place(x = 213, y = 0)
        vert_separator2 = ctk.CTkCanvas(self.mana_frame, height = 54, width = 1, bg = "#333333", highlightthickness = 0)
        vert_separator2.place(x = 283, y = 0)
        separator = ctk.CTkCanvas(self.mana_frame, height = 1, width = 800, bg = "#333333", highlightthickness = 0)
        separator.place(x = 0, y = 53)

        ## Reset Buttons ##
        reset_damage_button = ctk.CTkButton(self.mana_frame, text = "Reset Damage", command = self.reset_damage, width = 100)
        reset_damage_button.grid(row = 1, column = 2, padx = (5,5), pady = (10,5))
        reset_all_button = ctk.CTkButton(self.mana_frame, text = "Reset All", command = self.reset_all, width = 70)
        reset_all_button.grid(row = 1, column = 3, padx = (5,5), pady = (10,5))

        ## Create table header frame. ##
        self.add_player_button = ctk.CTkButton(self.header_frame, text = "+", command = self.add_player_row, width = 25, height = 25)
        self.add_player_button.grid(row = 0, column = 0, padx = (5,5), pady = (5,5))

        name_label = ctk.CTkLabel(self.header_frame, text = "Name", font = self.bold_font, width = 100)
        name_label.grid(sticky = "S", row = 0, column = 1, padx = (5,5), pady = (5,5))

        damage_dealt_label = ctk.CTkLabel(self.header_frame, text = "Damage Dealt", font = self.bold_font, width = 100)
        damage_dealt_label.grid(sticky = "S", row = 0, column = 2, columnspan = 2, padx = (5,5), pady = (5,5))

        damage_received_label = ctk.CTkLabel(self.header_frame, text = "Damage Received", font = self.bold_font, width = 100)
        damage_received_label.grid(sticky = "S", row = 0, column = 4, columnspan = 2, padx = (5,5), pady = (5,5))
        
        ## Adds 3 players by default. ##
        for i in range(3):
            self.add_player_row()

        self.protocol("WM_DELETE_WINDOW", lambda: self.on_close())

    def add_player_row(self):
        """ Adds a new player row and associated player to the ViewModel """
        
        player = self.viewmodel.add_player() # Add player to the ViewModel and get the player object back.
        
        row_index = len(self.player_rows)

        if row_index >= 9:
            self.add_player_button.configure(state = "disabled") # No more players beyond 10.

        row = PlayerRow(
            parent = self.player_frame,
            player = player,
            viewmodel = self.viewmodel,
            saved_names = self.saved_names,
            row_index = row_index,
            delete_callback = self.delete_player_row
        )

        self.player_rows.append(row)
        self.update_layout()       

    def delete_player_row(self, player):
        """Deletes a player row and associated player from the ViewModel"""
        if len(self.player_rows) == 1:
            return
        
        elif len(self.player_rows) == 10:
            self.add_player_button.configure(state = "normal") # Re-enable button once back under 10 players.
        
        # Remove the player row from the GUI
        for row in self.player_rows:
            if row.player is player:
                row.destroy()
                self.player_rows.remove(row)
                break
        
        for index, row in enumerate(self.player_rows): # Reconfigure the rows to close any gaps.
            row.update_row_index(index)

        self.viewmodel.remove_player(player) # Remove player from the ViewModel

        self.update_layout()

    def get_exe_path(self):
        """Gets the absolute path of the running script.
        
        This is used for saving/loading the config."""
        return os.path.dirname(os.path.abspath(sys.argv[0]))
    
    def load_config(self):
        """Load settings from a .json file"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {'pos': {'x': 100, 'y': 100}, 'names': [""]}
        return {'pos': {'x': 100, 'y': 100}, 'names': [""]}

    def save_config(self):
        """Save settings into a .json file"""
        config = {
            'pos': {'x': self.winfo_x(), 'y': self.winfo_y()},
            'names': self.saved_names
        }
        with open(self.config_path, 'w') as f:
            json.dump(config, f)
    
    def update_names(self):
        """Updates the available names in the player dropdown boxes"""
        for player in self.player_rows:
            for p in player:
                if type(p) == ctk.CTkComboBox:
                    p.configure(values = self.saved_names)

    def update_layout(self):
        """Forces an update and redraw of the window"""
        self.update_idletasks()
        self.geometry(f"{self.winfo_reqwidth()}x{self.winfo_reqheight()}")

    def reset_damage(self):
        """Reset all damage counters."""
        self.viewmodel.reset_damage()

        for row in self.player_rows:
            row.given_box.set(0)
            row.taken_box.set(0)

    def reset_all(self):
        """Resets all widgets to a completely blank state"""
        self.viewmodel.reset_players()
        
        for row in self.player_rows:
            row.given_box.set(0)
            row.taken_box.set(0)
            row.name_box.set("")
    
        self.clear_all_counters() # Resets mana/poison/energy counters to 0 as well.
    
    def event_handler(self, event, counter):
        """Handles click events on the mana/poison/energy counters"""
        if event.type == "4": # Button Press
            if event.num == 1: # Left click
                if event.state & 0x1: # with Shift
                    self.clear_counter(counter)
                elif event.state & 0x4: # with Ctrl
                    self.clear_all_counters()
                else:
                    self.uptick_counter(counter)
            elif event.num == 3: # Right click
                self.downtick_counter(counter)

    def uptick_counter(self, counter_var):
        current_value = counter_var.get()
        counter_var.set(current_value + 1)

    def downtick_counter(self, counter_var):
        current_value = counter_var.get()
        if current_value > 0:  # Prevent going below 0
            counter_var.set(current_value - 1)
        
    def clear_counter(self, counter_var):
        counter_var.set(0)

    def clear_all_counters(self):
        for counter in self.counters:
            counter.set(0)
        
    def options_window(self):
        """Opens the options popup window."""
        def save_options(self):
            new_names = names_box.get("0.0", ctk.END).strip().split('\n')
            updated_names = [name.strip() for name in new_names]
            self.saved_names.clear()
            self.saved_names.extend(updated_names)
            self.update_names()
            self.save_config()
            popup.destroy()
    
        root_x = self.winfo_x() + 10
        root_y = self.winfo_y() + 10
        popup = ctk.CTkToplevel(self)
        popup.title("Names List")
        popup.geometry(f"500x210+{root_x}+{root_y}")
        popup.resizable(False, False)
    
        names_box = ctk.CTkTextbox(popup)
        names_box.grid(row = 0, rowspan = 5, column = 0, padx = (5, 5), pady = (5, 5))
        names_box.insert("0.0", "\n".join(self.saved_names))
    
        instruction_label = ctk.CTkLabel(popup, text = self.instructions)
        instruction_label.grid(row = 0, column = 1, padx = (5, 5), pady = (5, 5))
    
        save_button = ctk.CTkButton(popup, text = "Save Names", command = lambda: save_options(self))
        save_button.grid(row = 4, column = 1, padx = (5, 5), pady = (5, 5))
    
        popup.transient(self)
        popup.focus()
        popup.grab_set()
    
    def custom_counter_window(self):
        """Opens the custom counter window and creates a customised counter"""
        def create_custom_counter(event = None):
            popup.destroy()
            if not name.get() == "":
                Custom_Counter.Custom_Counter(self, name.get())
    
        root_x = self.winfo_x() + 10
        root_y = self.winfo_y() + 10
        popup = ctk.CTkToplevel(self)
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

        popup.transient(self)
        popup.focus()
        popup.grab_set()

    def on_close(self):
        self.save_config()
        self.destroy()

if __name__ == "__main__":
    ## Window Settings ##
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    
    root = Commander_Tracker()
    root.mainloop()