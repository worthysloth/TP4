"""
TODO: Ce fichier présente une ébauche d'interface pour le TP4.
Vous pouvez le modifier à souhait.
N'oubliez pas de commenter le code!
"""

from tkinter import Tk, Frame, Button, messagebox, Entry, PhotoImage, Label, Menu, Toplevel, StringVar
from tableau import Tableau
from bouton_case import BoutonCase

import json
import time

from random import randrange


class InterfacePartie(Tk):
    def __init__(self):
        super().__init__()  # Comme root = Tk() !! root = self ici

        # Nom de la fenêtre.
        self.title("Démineur")
        self.resizable(0, 0)
        self.nombre_rangees_partie = 5
        self.nombre_colonnes_partie = 5
        self.nombre_mines_partie = 5

        ## Bloc qui ajoute un menu ======================================================================
        ## On crée un item barre_menu qui représente un menu de sélection
        barre_menu = Menu(self)

        ## On crée ensuite les différents menus
        menu_partie = Menu(barre_menu, tearoff=0)
        menu_partie.add_command(label="Configurer la partie", command = self.configurer_partie)
        menu_partie.add_command(label="Nouvelle partie", command=self.nouvelle_partie)
        menu_partie.add_command(label="Charger une partie")
        menu_partie.add_command(label="Sauvegarde la partie")

        ## On ajoue les menus a barre_menu
        barre_menu.add_cascade(label="Partie", menu = menu_partie)

        ## On place la barre_menu avec config parce qu'on utilise grid (peut pas faire barre_menu.grid())
        self.configure(menu=barre_menu)
         ## Fin Du Bloc qui ajoute un menu ======================================================================

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

        self.cadre = Frame(self)
        self.cadre.grid(padx=10, pady=10)
        self.defaite = False

        # self.dictionnaire_boutons = {}
        # self.tableau_mines = Tableau(self.nombre_rangees_partie,self.nombre_colonnes_partie,self.nombre_mines_partie)

        # for i in range(self.tableau_mines.dimension_rangee):
        #     for j in range(self.tableau_mines.dimension_colonne):
        #         bouton = BoutonCase(self.cadre, i+1, j+1)
        #         bouton.grid(row=i, column=j)
        #         bouton.bind('<Button-1>', self.devoiler_case)
        #         self.dictionnaire_boutons[(i+1, j+1)] = bouton

        self.tour = 0
        self.compteur_tour()

        ######## Code pour le coutdown qui ne fonctionne pas encore parfaitement
        self.label = Label(self, text="Timer", width=10)
        self.label.grid()
        self.remaining = 0
        self.countdown(5000)
        self.nouvelle_partie()
        #Code pour compteur de tour

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
            #self.tableau_mines.afficher_solution() # C'est quoi ca David ? ALEX
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
        self.dictionnaire_boutons = {}
        self.cadre.destroy()
        self.cadre = Frame(self)
        self.cadre.grid(padx=10, pady=10)
        print(self.dictionnaire_boutons)
        self.tableau_mines = Tableau(self.nombre_rangees_partie, self.nombre_colonnes_partie, self.nombre_mines_partie)
        for i in range(self.tableau_mines.dimension_rangee):
            for j in range(self.tableau_mines.dimension_colonne):
                bouton = BoutonCase(self.cadre, i+1, j+1)
                bouton.grid(row=i, column=j)
                bouton.bind('<Button-1>', self.devoiler_case)
                self.dictionnaire_boutons[(i+1, j+1)] = bouton
        print(self.dictionnaire_boutons)

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
            title="Quitter",
            message="Voulez-vous vraiment quitter ?")

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

    def maj_donnees(self, nb_rangees, nb_colonnes, nb_mines):
        self.nombre_rangees_partie = nb_rangees
        self.nombre_colonnes_partie = nb_colonnes
        self.nombre_mines_partie = nb_mines
        
    def configurer_partie(self):
        fenetre = Toplevel()
        fenetre.wm_title('Fenetre Test')
        
        fenetre_frame = Frame(fenetre, height = 200, width = 200)
        fenetre_frame.grid(padx=10, pady=10)

        ## On cree le label et entry pour rangee
        label_rangee = Label(fenetre_frame, text="Rangee: ")
        label_rangee.grid(row = 0, column = 0)
        entry_rangee = Entry(fenetre_frame, width = 5)
        entry_rangee.grid(row = 0, column = 1)

        ## On cree le label et entry pour colonne
        label_colonne = Label(fenetre_frame, text="Colonne: ")
        label_colonne.grid(row = 1, column = 0)
        entry_colonne = Entry(fenetre_frame, width = 5)
        entry_colonne.grid(row = 1, column = 1)
        
        ## On cree le label et entry pour mine
        label_mines = Label(fenetre_frame, text="Mines: ")
        label_mines.grid(row = 2, column = 0)
        entry_mine = Entry(fenetre_frame, width = 5)
        entry_mine.grid(row = 2, column = 1)

        # self.nombre_rangees_partie = entry_rangee.get()
        # self.nombre_colonnes_partie = entry_colonne.get()
        # self.nombre_mines_partie = entry_mine.get()
        # self.nouvelle_partie()

        ## Le lamba permet de passer une commande aves des arguments:
            ## A Implementer:
                #[ ] command => self.nouvelle_partie(va falloir figure out comment passer des arguments a nouvelle partie pour ensuie les passer a Tableau())
        bouton_soumission = Button(fenetre_frame, text="Go!", command=lambda:[
            self.maj_donnees(int(entry_rangee.get()), int(entry_colonne.get()), int(entry_mine.get())),
            print(self.nombre_rangees_partie, self.nombre_colonnes_partie, self.nombre_mines_partie),
            fenetre.destroy(),
            self.nouvelle_partie()
        ])
        bouton_soumission.grid(row=3, column = 0, columnspan = 2)
