import customtkinter as ctk

class OptionsWindow(ctk.CTkToplevel):
    """Opens the options popup window."""
    def __init__(self, parent, viewmodel):
        super().__init__(parent)
        self.viewmodel = viewmodel
        self.instructions = "Enter your player names in the box to the left.\nEach name should be on a new line."

        ## Window Setup ##
        root_x = parent.winfo_x() + 10
        root_y = parent.winfo_y() + 10

        self.title("Names List")
        self.geometry(f"500x210+{root_x}+{root_y}")
        self.resizable(False, False)

        ## Text input ##
        self.names_box = ctk.CTkTextbox(self)
        self.names_box.grid(row = 0, rowspan = 5, column = 0, padx = (5, 5), pady = (5, 5))
        self.names_box.insert("0.0", "\n".join(self.viewmodel.saved_names))

        ## Label ##
        self.instruction_label = ctk.CTkLabel(self, text = self.instructions)
        self.instruction_label.grid(row = 0, column = 1, padx = (5, 5), pady = (5, 5))

        ## Button ##
        self.save_button = ctk.CTkButton(
            self, 
            text = "Save Names", 
            command = lambda: save_options(self))
        self.save_button.grid(row = 4, column = 1, padx = (5, 5), pady = (5, 5))

        ## Behaviour ##
        self.lift()
        self.attributes("-topmost", True)
        self.after(10, lambda: self.attributes("-topmost", False))
        self.transient(parent)
        self.focus()
        self.grab_set()

        def save_options(self):
            new_names = self.names_box.get("0.0", ctk.END).strip().split('\n')
            updated_names = [name.strip() for name in new_names]
            self.viewmodel.update_and_save_names(updated_names)
            self.destroy()

