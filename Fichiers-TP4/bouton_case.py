"""
TODO: Ajoutez les docstrings et modifier le code au besoin.
"""

from tkinter import Button

class BoutonCase(Button):
    def __init__(self, parent, rangee_x, colonne_y):
        self.rangee_x = rangee_x
        self.colonne_y = colonne_y
        self.image =""
        self.relief = "raised"
        super().__init__(parent,image=self.image, text=' ', padx=1, pady=3, height=1, width=3, relief=self.relief)
