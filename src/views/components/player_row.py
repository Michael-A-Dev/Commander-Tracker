import customtkinter as ctk
import CTkSpinbox

class PlayerRow:
    def __init__(self, parent, player, viewmodel, saved_names, row_index):
        self.player = player

        self.delete_button = ctk.CTkButton(
            parent,
            text="x",
            fg_color="darkred",
            width=25,
            height=25
        )

        self.name_box = ctk.CTkComboBox(
            parent,
            values=saved_names,
            width=150,
        )

        self.given_box = CTkSpinbox.CTkSpinbox(
            parent,
            start_value=player.damage_given,
            min_value=0,
            max_value=21,
            scroll_value=1,
            font=("Segoe UI", 13),
            width=100,
            height=30,
            border_width=0,
            corner_radius=100,
            button_corner_radius=100
        )

        self.taken_box = CTkSpinbox.CTkSpinbox(
            parent,
            start_value=player.damage_taken,
            min_value=0,
            max_value=21,
            scroll_value=1,
            font=("Segoe UI", 13),
            width=100,
            height=30,
            border_width=0,
            corner_radius=100,
            button_corner_radius=100
        )

        ## Bindings ##
        self.delete_button.configure(
            command=lambda: viewmodel.remove_player(player)
        )

        self.name_box.configure(
            command=lambda v: viewmodel.update_player_name(player, v)
        )

        self.name_box.set(player.name) # Set initial value to the player's name (default: "")

        self.name_box.bind(
            "<KeyRelease>",
            lambda e: viewmodel.update_player_name(player, self.name_box.get()) ## Updates on typing, not just on selection from dropdown.
        )

        self.given_box.configure(
            command=lambda v: viewmodel.update_player_damage_given(player, v)
        )

        self.taken_box.configure(
            command=lambda v: viewmodel.update_player_damage_taken(player, v)
        )

        ## Layout ## 
        self.delete_button.grid(row=row_index, column=0, padx=5, pady=5)
        self.name_box.grid(row=row_index, column=1, padx=5, pady=5, sticky="ew")
        self.given_box.grid(row=row_index, column=2, padx=5, pady=5, sticky="ew")
        self.taken_box.grid(row=row_index, column=3, padx=5, pady=5, sticky="ew")

    def destroy(self):       
        """ Destroys all widgets associated with this player row. Called when the player is removed."""
        self.delete_button.destroy()
        self.name_box.destroy()
        self.given_box.destroy()
        self.taken_box.destroy()
  
    def update_row_index(self, new_index):
        """ Updates the row index of the player's widgets. This is necessary when a player is removed, and the rows below it need to move up."""
        self.delete_button.grid_configure(row=new_index)
        self.name_box.grid_configure(row=new_index)
        self.given_box.grid_configure(row=new_index)
        self.taken_box.grid_configure(row=new_index)
        