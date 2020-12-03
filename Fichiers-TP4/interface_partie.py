"""
TODO: Ce fichier présente une ébauche d'interface pour le TP4. Vous pouvez le modifier à souhait.
N'oubliez pas de commenter le code!
"""
from tkinter import Tk, Frame, Button, messagebox
from tableau import Tableau
from bouton_case import BoutonCase


class InterfacePartie(Tk):
    def __init__(self):
        super().__init__()

        # Nom de la fenêtre.
        self.title("Démineur")
        self.resizable(0,0)

        self.tableau_mines = Tableau()

        bouton_frame = Frame(self)
        bouton_frame.grid()

        bouton_nouvelle_partie = Button(bouton_frame, text='Nouvelle partie', command=self.nouvelle_partie)
        bouton_nouvelle_partie.grid(row=0, column=0)

        #J'ai essayé le yexnocancel du site https://docs.python.org/3/library/tkinter.messagebox.html#module-tkinter.messagebox
        bouton_quitter = Tk.messagebox.askyernocancel(Bouton_frame, title = sexybox, message = coucou, **options)
        
        #C'est la ligne d'origine sauf la partie command qui est changé pour appoeler ma fonction plus bas
        #bouton_quitter = Button(bouton_frame, text="Quitter", command=self.bouton_quitter2) 
        bouton_quitter.grid(row=0, column=1)

        self.cadre = Frame(self)
        self.cadre.grid(padx=10, pady=10)

        self.dictionnaire_boutons = {}

        for i in range(self.tableau_mines.dimension_rangee):
            for j in range(self.tableau_mines.dimension_colonne):
                bouton = BoutonCase(self.cadre, i+1, j+1)
                bouton.grid(row=i, column=j)
                bouton.bind('<Button-1>', self.devoiler_case)
                self.dictionnaire_boutons[(i+1, j+1)] = bouton

    def devoiler_case(self, event):
        bouton = event.widget
        case = self.tableau_mines.obtenir_case(bouton.rangee_x, bouton.colonne_y)
        if case.est_minee:
            bouton['text'] = "M"
        else:
            bouton['text'] = case.nombre_mines_voisines

    def nouvelle_partie(self):
        self.tableau_mines = Tableau()

        for bouton in self.dictionnaire_boutons.values():
            bouton['text'] = " "


    """ def bouton_quitter2(self):
        Auteur: David
        
        Note:
            Fonction pour définir le bouton quitter

        Args:
            Inconnue

        Returns:
            None
        
        #bouton_quitter = Button(bouton_frame, text="Quitter", command=self.bouton_quitter2)
        #bouton_quitter2.grid(row=0, column=1)

        MsgBox = Tk.messagebox.askquestion ("Quittez l'application","VOulez-vous vraiment quitter le jeu super trop cool wow",icon = "warning")
        if MsgBox == "yes":
            root.destroy()
        else:
            Tk.messagebox.showinfo("Annuler","Bubye") """
           


