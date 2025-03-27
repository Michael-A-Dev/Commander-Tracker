import customtkinter as ctk
import CTkSpinbox

class Custom_Counter(object):
    def __init__(self, parent, name):
        self.parent = parent
        self.root = ctk.CTkToplevel(self.parent)
        self.root.title(name)
        
        self.bold_font = ctk.CTkFont()
        self.bold_font['weight'] = 'bold'
        
        self.name = ctk.CTkLabel(self.root, text = name, font = self.bold_font)
        self.counter = CTkSpinbox.CTkSpinbox(self.root, start_value = 0, min_value = 0, scroll_value = 1, \
                       font = ("Segoe UI", 13), \
                       height = 30, width = 120, \
                       border_width = 0, corner_radius = 100, button_corner_radius = 100)
        
        self.parent_x = self.parent.winfo_x() - 130
        self.parent_y = self.parent.winfo_y()
        self.root.geometry(f"130x75+{self.parent_x}+{self.parent_y}")
        self.root.resizable(False, False)
        
        self.name.grid(row = 0, column = 0, padx = (5,5), pady = (0,5), sticky = "ew")
        self.counter.grid(row = 1, column = 0, padx = (5,5), pady = (0,5), sticky = "ew")
        
        self.root.focus()
        self.root.transient(self.parent)
        
    def destroy(self):
        self.root.destroy()