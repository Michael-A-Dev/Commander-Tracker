#!/usr/bin/python
import customtkinter as ctk
import Custom_Counter
import CTkSpinbox
import json
import Mana
import os
import sys
import tksvg


class Commander_Tracker(ctk.CTk):
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        self.instructions = "Enter your player names in the box to the left.\nEach name should be on a new line."
        
        self.config_file = "tracker_config.json"
        self.config_path = os.path.join(self.get_exe_path(), self.config_file)
        self.config = self.load_config()
        self.pos = self.config.get('pos', {'x': 100, 'y': 100})
        self.names = self.config.get('names', ["","No Names"])

        self.geometry(f"400x250+{self.pos['x']}+{self.pos['y']}")
        self.title("Commander Tracker")
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure([1, 2], weight = 2)

        self.bold_font = ctk.CTkFont()
        self.bold_font['weight'] = 'bold'

        counters_canvas = ctk.CTkCanvas(self, width = 400, height = 40, bg = "#1a1a1a", highlightthickness = 0)
        counters_canvas.grid(row = 0, column = 0, columnspan = 3, padx = (5,5), pady = (5,5), sticky = "ew")
        symbols = Mana.get_all_symbols()
        
        self.counters = []
        self.custom_counters = []

        for i, symbol in enumerate(symbols):
            x = 15 + i * 35
            y = 20
            counter_symbol_svg = tksvg.SvgImage(data=symbols[i])
            counter_symbol = ctk.CTkLabel(self, text = "", image = counter_symbol_svg)
            counter_symbol.place(x = x + 4, y = y, anchor = ctk.CENTER)

            counter = ctk.IntVar(value = 0)
            self.counters.append(counter)

            counter_tracker = ctk.CTkLabel(self, textvariable = counter, text_color = "white", height = 18, width = 15)
            counter_tracker.place(x = x + 4, y = y + 22, anchor = ctk.CENTER)
    
            for c in [counter_symbol, counter_tracker]:
                c.bind("<Button-1>", lambda event, var=counter: self.event_handler(event, var))
                c.bind("<Button-3>", lambda event, var=counter: self.event_handler(event, var))
                c.bind("<Shift-Button-1>", lambda event, var=counter: self.event_handler(event, var))
                c.bind("<Control-Button-1>", lambda event, var=counter: self.event_handler(event, var))

        custom_counter = ctk.CTkButton(self, text = "Custom Counter", command = lambda: self.custom_counter_window(), width = 80)
        custom_counter.place(x = 340, y = 27, anchor = ctk.CENTER)

        vert_separator = ctk.CTkCanvas(self, height = 54, width = 1, bg = "#333333", highlightthickness = 0)
        vert_separator.place(x = 213, y = 0)
        separator = ctk.CTkCanvas(self, height = 1, width = 400, bg = "#333333", highlightthickness = 0)
        separator.place(x = 0, y = 53)

        name_label = ctk.CTkLabel(self, text = "Name", font = self.bold_font)
        name_label.grid(sticky = "S", row = 1, column = 0, padx = (5,5), pady = (10,0))

        damage_dealt_label = ctk.CTkLabel(self, text = "Damage Dealt", font = self.bold_font, width = 150)
        damage_dealt_label.grid(sticky = "S", row = 1, column = 1, padx = (5,5), pady = (10,0))

        damage_received_label = ctk.CTkLabel(self, text = "Damage Received", font = self.bold_font, width = 150)
        damage_received_label.grid(sticky = "S", row = 1, column = 2, padx = (5,5), pady = (10,0))

        ## Player 1 ##
        self.player1_name = ctk.CTkComboBox(self, values = self.names)
        self.player1_name.grid(row = 2, column = 0, padx = (5,5), pady = (0,5), sticky = "ew")

        self.player1_given = CTkSpinbox.CTkSpinbox(self, start_value = 0, min_value = 0, max_value = 21, scroll_value = 1, \
                                             font = ("Segoe UI", 13), height = 30, border_width = 0, corner_radius = 100, button_corner_radius = 100)
        self.player1_given.grid(row = 2, column = 1, padx = (5,5), pady = (0,5), sticky = "ew")

        self.player1_taken = CTkSpinbox.CTkSpinbox(self, start_value = 0, min_value = 0, max_value = 21, scroll_value = 1, \
                                             font = ("Segoe UI", 13), height = 30, border_width = 0, corner_radius = 100, button_corner_radius = 100)
        self.player1_taken.grid(row = 2, column = 2, padx = (5,5), pady = (0,5), sticky = "ew")

        ## Player 2 ##
        self.player2_name = ctk.CTkComboBox(self, values = self.names)
        self.player2_name.grid(row = 3, column = 0, padx = (5,5), pady = (5,5), sticky = "ew")

        self.player2_given = CTkSpinbox.CTkSpinbox(self, start_value = 0, min_value = 0, max_value = 21, scroll_value = 1, \
                                             font = ("Segoe UI", 13), height = 30, border_width = 0, corner_radius = 100, button_corner_radius = 100)
        self.player2_given.grid(row = 3, column = 1, padx = (5,5), pady = (5,5), sticky = "ew")

        self.player2_taken = CTkSpinbox.CTkSpinbox(self, start_value = 0, min_value = 0, max_value = 21, scroll_value = 1, \
                                             font = ("Segoe UI", 13), height = 30, border_width = 0, corner_radius = 100, button_corner_radius = 100)
        self.player2_taken.grid(row = 3, column = 2, padx = (5,5), pady = (5,5), sticky = "ew")

        ## Player 3 ##
        self.player3_name = ctk.CTkComboBox(self, values = self.names)
        self.player3_name.grid(row = 4, column = 0, padx = (5,5), pady = (5,5), sticky = "ew")

        self.player3_given = CTkSpinbox.CTkSpinbox(self, start_value = 0, min_value = 0, max_value = 21, scroll_value = 1, \
                                             font = ("Segoe UI", 13), height = 30, border_width = 0, corner_radius = 100, button_corner_radius = 100)
        self.player3_given.grid(row = 4, column = 1, padx = (5,5), pady = (5,5), sticky = "ew")

        self.player3_given = CTkSpinbox.CTkSpinbox(self, start_value = 0, min_value = 0, max_value = 21, scroll_value = 1, \
                                             font = ("Segoe UI", 13), height = 30, border_width = 0, corner_radius = 100, button_corner_radius = 100)
        self.player3_given.grid(row = 4, column = 2, padx = (5,5), pady = (5,5), sticky = "ew")

        ## Reset Buttons ##
        reset_damage_button = ctk.CTkButton(self, text = "Reset Damage", command = self.reset_damage)
        reset_damage_button.grid(row = 5, column = 0, padx = (5,5), pady = (5,5))
        options_button = ctk.CTkButton(self, text = "Options", command = lambda: self.options_window())
        options_button.grid(row = 5, column = 1, padx = (5,5), pady = (5,5))
        reset_all_button = ctk.CTkButton(self, text = "Reset All", command = self.reset_all)
        reset_all_button.grid(row = 5, column = 2, padx = (5,5), pady = (5,5))

        self.protocol("WM_DELETE_WINDOW", lambda: self.on_close())
        
    def get_exe_path(self):
        return os.path.dirname(os.path.abspath(sys.argv[0]))
    
    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {'pos': {'x': 100, 'y': 100}, 'names': [""]}
        return {'pos': {'x': 100, 'y': 100}, 'names': [""]}

    def save_config(self):
        config = {
            'pos': {'x': self.winfo_x(), 'y': self.winfo_y()},
            'names': self.names
        }
        with open(self.config_path, 'w') as f:
            json.dump(config, f)

    def on_close(self):
        self.save_config()
        self.destroy()
    
    def options_window(self):
        def save_options(self):
            new_names = names_box.get("0.0", ctk.END).strip().split('\n')
            updated_names = [name.strip() for name in new_names]
            self.names.clear()
            self.names.extend(updated_names)
            self.update_names()
            self.save_config(self, self.names, self.config_path)
            popup.destroy()
    
        root_x = self.winfo_x() + 10
        root_y = self.winfo_y() + 10
        popup = ctk.CTkToplevel(self)
        popup.title("Names List")
        popup.geometry(f"500x210+{root_x}+{root_y}")
        popup.resizable(False, False)
    
        names_box = ctk.CTkTextbox(popup)
        names_box.grid(row = 0, rowspan = 5, column = 0, padx = (5, 5), pady = (5, 5))
        names_box.insert("0.0", "\n".join(self.names))
    
        instruction_label = ctk.CTkLabel(popup, text = self.instructions)
        instruction_label.grid(row = 0, column = 1, padx = (5, 5), pady = (5, 5))
    
        save_button = ctk.CTkButton(popup, text = "Save Names", command = save_options)
        save_button.grid(row = 4, column = 1, padx = (5, 5), pady = (5, 5))
    
        popup.grab_set()
        popup.focus()
        popup.transient(self)
    
    def update_names(self):
        self.player1_name.configure(values = self.names)
        self.player2_name.configure(values = self.names)
        self.player3_name.configure(values = self.names)

    def reset_damage(self):
        self.player1_given.set(0)
        self.player1_taken.set(0)
    
        self.player2_given.set(0)
        self.player2_taken.set(0)
    
        self.player3_given.set(0)
        self.player3_given.set(0)

    def reset_all(self):
        self.player1_name.set("")
        self.player1_given.set(0)
        self.player1_taken.set(0)
    
        self.player2_name.set("")
        self.player2_given.set(0)
        self.player2_taken.set(0)
    
        self.player3_name.set("")
        self.player3_given.set(0)
        self.player3_given.set(0)
    
        self.clear_all_counters()
    
    def event_handler(self, event, counter):
        """Handles click events on the mana/poison/energy counters"""
        if event.type == "4": # Button Press
            if event.num == 1: # Left click
                if event.state & 0x1: # with Shift
                    self.clear_counter(event, counter)
                elif event.state & 0x4: # with Ctrl
                    self.clear_all_counters()
                else:
                    self.uptick_counter(event, counter)
            elif event.num == 3: # Right click
                self.downtick_counter(event, counter)

    def uptick_counter(self, event, counter_var):
        current_value = counter_var.get()
        counter_var.set(current_value + 1)

    def downtick_counter(self, event, counter_var):
        current_value = counter_var.get()
        if current_value > 0:  # Prevent going below 0
            counter_var.set(current_value - 1)
        
    def clear_counter(self, event, counter_var):
        counter_var.set(0)

    def clear_all_counters(self):
        for counter in self.counters:
            counter.set(0)
        
    def custom_counter_window(self):
        def create_custom_counter(event = None):
            popup.destroy()
            if not name.get() == "":
                new_counter = Custom_Counter.Custom_Counter(self, name.get())
                self.custom_counters.append(new_counter)
    
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

if __name__ == "__main__":
    ## Window Settings ##
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    
    root = Commander_Tracker()
    root.mainloop()