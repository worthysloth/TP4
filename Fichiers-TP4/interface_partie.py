"""
TODO: Ce fichier présente une ébauche d'interface pour le TP4. 
Vous pouvez le modifier à souhait.
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

        bouton_nouvelle_partie = Button(bouton_frame, text='Nouvelle partie',\
             command=self.nouvelle_partie)
        bouton_nouvelle_partie.grid(row=0, column=0)

        bouton_quitter = Button(bouton_frame, text="Quitter", \
            command=self.demander_ouinon)
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
      
    #test3 = afficher_solution    
    def devoiler_case(self, event):
        """
        NE FONCTIONNE PAS BIEN. LA SOLUTION S'AFFICHE DANS CMD ET NON TKINTER ET IL NE DÉTECTE PAS QUE LA GAME EST TERMINÉ

        Args:
            event ([type]): [description]
        """
        bouton = event.widget
        case = self.tableau_mines.obtenir_case\
            (bouton.rangee_x, bouton.colonne_y)
        if case.est_minee:
            bouton['text'] = "M"
            #buttonerror = Button(command=self.victoire_defaite)
            #answer = messagebox.askyesno(title="Lost", message= "ta perdu")
            messagebox.askyesno(title="Lost", message= "ta perdu", command=self.tableau_mines.afficher_solution())
            #if answer == True:
            #    self.afficher_solution
            #afficher_solition fonctionne mais juste dans CMD
        elif self.tableau_mines.nombre_cases_sans_mine_a_devoiler <= 0:
            print ("patate")        
        else:
            bouton['text'] = case.nombre_mines_voisines

    def test2(self):
        print ("patete")



    """ def victoire_defaite(self):
        if self.devoiler_case == True:
            print("patate")
            messagebox.showerror(title="Lost", message= "ta perdu") """



    def nouvelle_partie(self):
        self.tableau_mines = Tableau()

        for bouton in self.dictionnaire_boutons.values():
            bouton['text'] = " "

    def demander_ouinon(self):
        """Auteur: David
        
        Note:
            Demande à l'utilisateur s'il veut vraiment quitter le jeu

        Args:
            Inconnue

        Returns:
            None
        """
        question = messagebox.askyesno(title = "Quitter", message = \
            "Voulez-vous vraiment quitter ?")
        if question == True:
            self.destroy()
           


