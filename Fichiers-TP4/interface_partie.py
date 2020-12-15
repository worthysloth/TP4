"""
TODO: Ce fichier présente une ébauche d'interface pour le TP4.
Vous pouvez le modifier à souhait.
N'oubliez pas de commenter le code!
"""

from tkinter import Tk, Frame, Button, messagebox, Entry, PhotoImage, Label
from tableau import Tableau
from bouton_case import BoutonCase


import time

from random import randrange


class InterfacePartie(Tk):
    def __init__(self):
        super().__init__()  # Comme root = Tk() !!

        # Nom de la fenêtre.
        self.title("Démineur")
        self.resizable(0, 0)

        bouton_frame = Frame(self)
        bouton_frame.grid()

        bouton_nouvelle_partie = Button(bouton_frame, text='Nouvelle partie',
                                        command=self.nouvelle_partie)
        bouton_nouvelle_partie.grid(row=0, column=0)

        bouton_quitter = Button(bouton_frame, text="Quitter",
                                command=self.demander_ouinon)
        bouton_quitter.grid(row=0, column=1)

        # Bouton info
        bouton_info = Button(bouton_frame, text = 'Info',command = self.afficher_intructions)
        bouton_info.grid(row=0, column=2)

        entree_nb_rangees = Entry(bouton_frame, width=10).grid(row=1, column=0)
        entree_nb_colonnes = Entry(
            bouton_frame, width=10).grid(row=1, column=1)
        entree_nb_mines = Entry(bouton_frame, width=10).grid(row=1, column=2)

        self.cadre = Frame(self)
        self.cadre.grid(padx=10, pady=10)
        self.defaite = False

        self.dictionnaire_boutons = {}
        self.tableau_mines = Tableau()

        for i in range(self.tableau_mines.dimension_rangee):
            for j in range(self.tableau_mines.dimension_colonne):
                bouton = BoutonCase(self.cadre, i+1, j+1)
                bouton.grid(row=i, column=j)
                bouton.bind('<Button-1>', self.devoiler_case)
                self.dictionnaire_boutons[(i+1, j+1)] = bouton

        #Code pour compteur de tour
        self.tour = 0
        self.compteur_tour()

        ######## Code pour le coutdown qui ne fonctionne pas encore parfaitement
        self.label = Label(self, text="Timer", width=10)
        self.label.grid()
        self.remaining = 0
        self.countdown(5000)

    def compteur_tour(self):
        phrase = f"Tour#{self.tour}"
        self.labeltour = Label(self, text= phrase, width=10)
        self.labeltour.grid(row=10)
        self.tour += 1

    def countdown(self, remaining=None):
        """
        Fonction pour le mode "contre-la-montre" qui affiche la solution
        si jamais l'utilisateur ne termine pas avant le temps impartie


        Args:
            remaining ([type], optional): [description]. Defaults to None.

        A faire:
        -S'assurer que la solution s'affiche dans tkinter et non CMD
        -replacer le timer quelque part de nice
        -Proposer au user de choisir ce mode
        """
        if remaining is not None:
            self.remaining = remaining

        if self.remaining <= 0:
            self.label.configure(text="Temps écoulé")
            self.tableau_mines.afficher_solution()
        else:
            self.label.configure(text="%d" % self.remaining)
            self.remaining = self.remaining - 1
            self.after(1000, self.countdown)

    #test3 = afficher_solution

    def devoiler_case(self, event):
        """
        NE FONCTIONNE PAS BIEN. LA SOLUTION S'AFFICHE DANS CMD ET NON TKINTER ET IL NE DÉTECTE PAS QUE LA GAME EST TERMINÉ

        Args:
            event ([type]): [description]
        """
        bouton = event.widget
        case = self.tableau_mines.obtenir_case(
            bouton.rangee_x, bouton.colonne_y)

        if case.est_minee:
            bouton['text'] = "M"
            if messagebox.askyesno(title="Lost", message="Ta perdu, voulez-vous recommencez?", command=self.afficher_solution()):
                self.nouvelle_partie()
            else:
                self.quit()
                
            self.defaite = True
        elif not case.est_minee:
            bouton['text'] = case.nombre_mines_voisines
            self.tableau_mines.nombre_cases_sans_mine_a_devoiler -= 1
            self.defaite = False

        if self.tableau_mines.nombre_cases_sans_mine_a_devoiler <= 0 and not self.defaite:
            print("patate")
            messagebox.showinfo(title="Winner", message="WINNER WINNER CHICKEN DINNER",command=self.afficher_solution())
        self.compteur_tour()

    def afficher_solution(self):
        for i in range(self.tableau_mines.dimension_rangee):
            for j in range(self.tableau_mines.dimension_colonne):
                case = self.tableau_mines.obtenir_case(i+1, j+1)
                self.tableau_mines.devoiler_case(i+1, j+1)
                bout = self.dictionnaire_boutons[(i+1, j+1)]
                if case.est_minee:
                    bout['text'] = 'M'
                else:
                    bout['text'] = case.nombre_mines_voisines

    def test2(self):
        print("patete")

    def nouvelle_partie(self):
        self.tableau_mines = Tableau()

        for bouton in self.dictionnaire_boutons.values():
            bouton['text'] = " "
        self.tour = 0
        self.compteur_tour()

    def demander_ouinon(self):
        """Auteur: David
        
        Note:
            Demande à l'utilisateur s'il veut vraiment quitter le jeu

        Args
            Inconnue

        Returns:
            None
        """
        question = messagebox.askyesno(
            title="Quitter", message="Voulez-vous vraiment quitter ?")
        if question == True:
            self.destroy()

    def afficher_intructions(self):
        """Auteur: Aryanne

        Note:
            Affiche les instructions du jeu

        Args:
            None

        Returns:
            None
        """
        messagebox.showinfo(title= 'Info', message= 'This is how u play')