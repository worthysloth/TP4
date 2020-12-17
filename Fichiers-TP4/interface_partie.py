"""
TODO: Ce fichier présente une ébauche d'interface pour le TP4.
Vous pouvez le modifier à souhait.
N'oubliez pas de commenter le code!
"""

from tkinter import Tk, Frame, Button, messagebox, Entry, PhotoImage, Label, Menu, Toplevel, Message, StringVar
from tableau import Tableau
from bouton_case import BoutonCase
import os
import json
import time
from random import randrange

class InterfacePartie(Tk):
    def __init__(self):
        super().__init__()

        # Nom de la fenêtre.
        self.title("Démineur")
        self.resizable(0, 0)
        # Attributs
        self.nombre_rangees_partie = 5
        self.nombre_colonnes_partie = 5
        self.nombre_mines_partie = 5
        self.cadre = Frame(self)
        self.cadre.grid(padx=10, pady=10)
        self.dictionnaire_boutons = {}
        self.defaite = False
        self.tour = 0
        self.liste_images_nombres = []

        for i in range(8):
            chemin = os.path.dirname(__file__)
            chemin_img = os.path.join(chemin, f'images/tile_{str(i)}.png')
            image_actuelle = PhotoImage(file = chemin_img)
            self.liste_images_nombres.append(image_actuelle)

        ## Bloc qui ajoute un menu ======================================================================
        ## On crée un item barre_menu qui représente un menu de sélection
        barre_menu = Menu(self)

        ## On crée ensuite les différents menus
        menu_partie = Menu(barre_menu, tearoff=0)
        menu_partie.add_command(label="Nouvelle partie", command=self.nouvelle_partie)
        menu_partie.add_command(label="Charger une partie", command=self.charger_partie)
        menu_partie.add_command(label="Sauvegarde la partie", command=self.sauvegarde_partie)
        menu_partie.add_command(label="Configurer la partie", command = self.configurer_partie)
        menu_partie.add_separator()
        menu_partie.add_command(label="Quitter", command=self.demander_ouinon)

        menu_info = Menu(barre_menu, tearoff=0)
        menu_info.add_command(label="Règlements", command=self.afficher_intructions)
        menu_info.add_command(label="Créateurs", command=self.afficher_createurs)


        ## On ajoue les menus a barre_menu
        barre_menu.add_cascade(label="Partie", menu = menu_partie)
        barre_menu.add_cascade(label="Info", menu = menu_info)

        ## On place la barre_menu avec config parce qu'on utilise grid (peut pas faire barre_menu.grid())
        self.configure(menu=barre_menu)
        ## Fin Du Bloc qui ajoute un menu ======================================================================

        ######## Code pour le coutdown qui ne fonctionne pas encore parfaitement
        self.label = Label(self, text="Timer", width=10)
        self.label.grid()
        self.remaining = 0
        # self.countdown(5000)
        self.labeltour = Label(self, text=f"TourPENIS#{self.tour}", width=10)
        self.labeltour.grid()

        chemin_fichier = os.path.dirname(__file__)
        chemin_bombe = os.path.join(chemin_fichier, 'images/bomb2.png')
        self.image_bombe = PhotoImage(file = chemin_bombe)
        # A la fin on lance la partie une partie
        self.nouvelle_partie()

    def ajouter_tour(self):
        self.labeltour.destroy()
        self.labeltour = Label(self, text=f"Tour#{self.tour}", width=10)
        self.labeltour.grid(row=0)
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

    def devoiler_case(self, event):
        """
        NE FONCTIONNE PAS BIEN. LA SOLUTION S'AFFICHE DANS CMD ET NON TKINTER ET IL NE DÉTECTE PAS QUE LA GAME EST TERMINÉ

        Args:
            event ([type]): [description]
        """
        bouton = event.widget
        case = self.tableau_mines.obtenir_case(bouton.rangee_x, bouton.colonne_y)
        if not case.est_devoilee and not self.defaite:
            case.devoiler()
            self.ajouter_tour()
            if case.est_minee:
                bouton['image'] = self.image_bombe
                bouton['height'] = self.image_bombe.height()
                bouton['width'] = self.image_bombe.width()
                self.afficher_defaite()

            elif not case.est_minee:
                bouton['image'] = self.liste_images_nombres[case.nombre_mines_voisines]
                self.tableau_mines.nombre_cases_sans_mine_a_devoiler -= 1

            if self.tableau_mines.nombre_cases_sans_mine_a_devoiler <= 0 and not self.defaite:
                print('PU DE MINES!')
                self.afficher_victoire()
            

    def afficher_defaite(self):
        msgbox = Toplevel()
        msgbox.grid()
        message = Message(msgbox, text="Vous avez perdu! Appuyer sur OK!",anchor='center',justify='center')
        message.grid(row=0, column=0,columnspan=3)
        bouton_ok = Button(msgbox, text="Ok",command=lambda:[msgbox.destroy(), self.afficher_solution()])
        bouton_ok.grid(row=2, column=1)
        self.defaite = True

    def afficher_victoire(self):
        msgbox = Toplevel()
        message = Message(msgbox, text="Vous avez gagné! Appuyer sur OK!",anchor='center',justify='center')
        message.pack()
        bouton_ok = Button(msgbox, text="Ok",command=lambda:[msgbox.destroy(), self.afficher_solution()])
        bouton_ok.pack()

    def afficher_solution(self):
        for i in range(self.tableau_mines.dimension_rangee):
            for j in range(self.tableau_mines.dimension_colonne):
                case = self.tableau_mines.obtenir_case(i+1, j+1)
                self.tableau_mines.devoiler_case(i+1, j+1)
                bout = self.dictionnaire_boutons[(i+1, j+1)]
                bout['relief'] = 'raised'
                if case.est_minee:
                    bout['image'] = self.image_bombe
                    bout['height'] = self.image_bombe.height()
                    bout['width'] = self.image_bombe.width()
                else:
                    bout['image'] = self.liste_images_nombres[case.nombre_mines_voisines]

    def test2(self):
        print("patete")

    def nouvelle_partie(self):
        self.countdown(5000)
        self.dictionnaire_boutons = {}
        self.cadre.destroy()
        self.tour = 0
        self.ajouter_tour()
        self.cadre = Frame(self)
        self.cadre.grid(padx=10, pady=10)
        self.defaite = False
        self.tableau_mines = Tableau(self.nombre_rangees_partie, self.nombre_colonnes_partie, self.nombre_mines_partie)
        for i in range(self.tableau_mines.dimension_rangee):
            for j in range(self.tableau_mines.dimension_colonne):
                bouton = BoutonCase(self.cadre, i+1, j+1)
                bouton.grid(row=i, column=j)
                bouton.bind('<Button-1>', self.devoiler_case)
                self.dictionnaire_boutons[(i+1, j+1)] = bouton

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
        self.fenetre = Toplevel()
        self.fenetre.wm_title('Configuration de la partie')
        
        fenetre_frame = Frame(self.fenetre, height = 200, width = 200)
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

        self.label_erreur_configuration = Label(fenetre_frame, text='')
        self.label_erreur_configuration.grid(row=3,column=0,columnspan=2)

        bouton_soumission = Button(fenetre_frame, text="Go!", command=lambda:[
            self.maj_donnees(entry_rangee.get(),entry_colonne.get(),entry_mine.get()),
            self.valider_configuration(entry_rangee.get(),entry_colonne.get(),entry_mine.get(),fenetre_frame)
        ])
        bouton_soumission.grid(row=4, column = 0, columnspan = 2)

    def valider_configuration(self, nb_rangees, nb_colonnes, nb_mines, widget):
        # AJOUTER EQUATION POUR NOMBRE DEMINE AVEC UN EXCEPT 
        try:
            if not self.nombre_rangees_partie.isnumeric() or not self.nombre_colonnes_partie.isnumeric() or not self.nombre_mines_partie.isnumeric():
                raise ValueError 

            self.nouvelle_partie()
            print("🏆")
            self.fenetre.destroy()
        except ValueError:
            self.label_erreur_configuration.config(text="ERREUR")

    def sauvegarde_partie(self):
        donnees = {}
        donnees['rangees'] = self.nombre_rangees_partie
        donnees['colonnes'] = self.nombre_colonnes_partie
        donnees['mines'] = self.nombre_mines_partie
        donnees['tours'] = self.tour
        donnees['tableau'] = {}
        donnees['defaite'] = self.defaite

  
        for i in range(self.tableau_mines.dimension_rangee):
            for j in range(self.tableau_mines.dimension_colonne):
                case = self.tableau_mines.obtenir_case(i+1, j+1)
                donnees['tableau'][f"({i+1}, {j+1})"] = {
                "minee": case.est_minee,
                "devoilee":case.est_devoilee,
                "nombre_voisins":case.nombre_mines_voisines
                }

        with open("fichier_sauvegarde.txt", "w") as fichier_sauvegarde:
            json.dump(donnees, fichier_sauvegarde)

    def charger_partie(self):
        self.cadre.destroy()
        self.cadre = Frame(self)
        self.cadre.grid(padx=10, pady=10)

        with open("fichier_sauvegarde.txt", "r") as fichier_sauvegarde:
            donnees = json.load(fichier_sauvegarde)
        
        self.nombre_rangees_partie = donnees['rangees']
        self.nombre_colonnes_partie = donnees['colonnes']
        self.nombre_mines_partie = donnees['mines']
        self.tour = donnees['tours'] - 1
        self.defaite = donnees['defaite']

        self.tableau_mines = Tableau(self.nombre_rangees_partie, self.nombre_colonnes_partie,self.nombre_mines_partie)
        self.countdown(5000)
        self.ajouter_tour()

        for i in range(self.tableau_mines.dimension_rangee):
            for j in range(self.tableau_mines.dimension_colonne):
                bouton = BoutonCase(self.cadre, i+1, j+1)
                bouton.grid(row=i, column=j)
                bouton.bind('<Button-1>', self.devoiler_case)
                self.dictionnaire_boutons[(i+1, j+1)] = bouton
                case = self.tableau_mines.obtenir_case(i+1, j+1)
                case.est_minee = donnees['tableau'][f"({i+1}, {j+1})"]['minee']
                case.est_devoilee = donnees['tableau'][f"({i+1}, {j+1})"]['devoilee']
                case.nombre_mines_voisines = donnees['tableau'][f"({i+1}, {j+1})"]['nombre_voisins']
                if case.est_devoilee:
                    self.tableau_mines.devoiler_case(i+1, j+1)
                    if case.est_minee:
                        bouton['image'] = self.image_bombe
                    else:
                        bouton['image'] = self.liste_images_nombres[case.nombre_mines_voisines]

    def afficher_createurs(self):
        print("Aryanne Pommerleau, David Côté, Alex Caissy")
