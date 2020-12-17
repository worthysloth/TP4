"""
TODO: Ajoutez les docstrings et modifier le code au besoin.
"""

from tkinter import Button, PhotoImage
import os

class BoutonCase(Button):
    def __init__(self, parent, rangee_x, colonne_y):
        chemin_fichier = os.path.dirname(__file__)
        chemin_image = os.path.join(chemin_fichier,'images/tile_not.png')
        self.rangee_x = rangee_x
        self.colonne_y = colonne_y
        self.image = PhotoImage(file = chemin_image)
        self.relief = "raised"
        super().__init__(
        parent,
        image=self.image, 
        padx=1, 
        pady=3, 
        height=24, 
        width=24, 
        relief=self.relief)

