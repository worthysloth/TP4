"""
TODO: Ce fichier présente une ébauche d'interface pour le TP4.
Vous pouvez le modifier à souhait.
N'oubliez pas de commenter le code!
"""

from tkinter import Tk, Frame, Button, messagebox, Entry, PhotoImage, Label,\
    Menu, Toplevel, Message, filedialog
from tableau import Tableau
from bouton_case import BoutonCase

import os
import json
import time
import simpleaudio as sa

class InterfacePartie(Tk):
    """
    Jeu de démineur implémenté avec Tkinter

    Args:
        Tk (): module de tkinter pour l'affichage du jeu
    """
    def __init__(self):
        """
        Initialisation de l'objet tableau

        Attributes:
            nombre_rangees_partie (int): Nombre de rangees dans la partie
            nombre_colonnes_partie (int) : Nombre de colonnes dans la partie
            nombre_mines_partie (int) : Nombre de mines dans la partie
            cadre (Frame) : Cadre du jeu Tkinter
            dictionnaire_boutons (dict): Dictionnaire contenant tout 
                                         les boutons du jeu
            defaite (bool) : État du jeu au niveau de la defaite
            victoire (bool) : État du jeu au niveau de la victoire
            tour (int) : Valeur du nombre de tour dans le jeu
            temps (int) : Valeur du temps dans le jeu
            liste_images_nombres (list) : Liste contetnant les images concernant 
                                            les nombres seulement
            chemin (str): Chemin d'accès du fichier principal
            image_drapeau (PhotoImage) : Image contenant le drapeau
            image_bombe (PhotoImage) : Image contenant la bombe
            sondevoile (str) : Son pour le devoilement des cases
            sonexplosion (str) : Son pour le devoilement des mines
            

        """
        super().__init__()

        # Nom de la fenêtre.
        self.title("Démineur 3.0")
        self.resizable(0, 0)
        # Attributs
        self.nombre_rangees_partie = 5
        self.nombre_colonnes_partie = 5
        self.nombre_mines_partie = 5
        self.cadre = Frame(self)
        self.cadre.grid(padx=10, pady=10)
        self.dictionnaire_boutons = {}
        self.defaite = False
        self.victoire = False
        self.tour = 0
        self.temps = 0
        self.liste_images_nombres = []
        self.chemin = os.path.dirname(__file__)
        chemin_red_flag = os.path.join(self.chemin, 'images/flag2.png')
        self.image_drapeau = PhotoImage(file = chemin_red_flag)
        chemin_bombe = os.path.join(self.chemin, 'images/bomb2.png')
        self.image_bombe = PhotoImage(file = chemin_bombe)
        self.sondevoile = os.path.join(self.chemin, 'son/Gun.wav')
        self.sonexplosion = os.path.join(self.chemin, 'son/explosion2.wav')
        ## Importation des images que nous allons utiliser
        for i in range(8):
            chemin_img = os.path.join(self.chemin, f'images/tile_{str(i)}.png')
            image_actuelle = PhotoImage(file = chemin_img)
            self.liste_images_nombres.append(image_actuelle)
            
        ## On crée un item barre_menu qui représente un menu de sélection
        barre_menu = Menu(self)

        ## On crée ensuite les différents menus
        menu_partie = Menu(barre_menu, tearoff=0)
        menu_partie.add_command(label="Nouvelle partie", 
        command=self.nouvelle_partie)
        menu_partie.add_command(label="Charger une partie",
            command=self.charger_partie)
        menu_partie.add_command(label="Sauvegarde la partie",
            command=self.sauvegarde_partie)
        menu_partie.add_command(label="Configurer la partie",
            command = self.configurer_partie)
        menu_partie.add_separator()
        menu_partie.add_command(label="Quitter", command=self.demander_ouinon)

        menu_info = Menu(barre_menu, tearoff=0)
        menu_info.add_command(label="Règlements",
            command=self.afficher_intructions)
        menu_info.add_command(label="Créateurs",
            command=self.afficher_createurs)

        ## On ajoute les menus a barre_menu
        barre_menu.add_cascade(label="Partie", menu = menu_partie)
        barre_menu.add_cascade(label="Info", menu = menu_info)

        ## On place la barre_menu
        self.configure(menu=barre_menu)

        # On crée les labels qu'on va devoir utilise (initialisation vide)
        self.label_temps = Label(self)
        self.label_tour = Label(self)

        # A la fin on lance la partie une partie
        self.nouvelle_partie()

    def ajouter_tour(self):
        """
        Fonction qui compte le nombre de tour dans le jeu
        """
        self.label_tour.destroy()
        self.label_tour = Label(self, text=f"Tour#{self.tour}", width=10)
        self.label_tour.grid(row=1,column=0)
        self.tour += 1

    def afficher_chronometre(self):
        """
        Fonction qui initialise le chronometre de jeu
        """
        self.label_temps.destroy()
        self.label_temps = Label(self, text=f"Temps: {self.temps}")
        self.label_temps.grid(row=0,column=0)
        if self.temps == 0:
            print('0')
            self.maj_chronometre()
            self.afficher_chronometre()
        else:
            self.label_temps.after(1000,self.maj_chronometre)
        
    def maj_chronometre(self):
        """
        Fonction qui met à jour le chronometre
        """
        self.temps += 1        
        self.afficher_chronometre()

    def trouver_case(self,event):
        """
        Fonction que trouve les coordonnées de la case sur laquelle on a 
        appuyeée.

        Args:
            event (<Button-1>): Clic gauche sur la case de notre choix.
        """
        # On place les coordonnés en attributs et on dévoile la case
        self.case_appuyer_rangee = event.widget.rangee_x
        self.case_appuyer_colonne = event.widget.colonne_y
        #Si la case n'est pas devoilee et minee on ajoute un tour et on devoile
        case_appuyer = self.tableau_mines.obtenir_case(self.case_appuyer_rangee,
            self.case_appuyer_colonne)
        if not case_appuyer.est_devoilee and not case_appuyer.est_minee:
            self.ajouter_tour()
            #Execution du son
            sa.WaveObject.from_wave_file(self.sondevoile).play()
        self.devoiler_case()

    def devoiler_case(self):
        """
        Fonction qui dévoile une case. Si la case contient aucune mine, un
        effet de cascade est déclenché pour dévoiler les autres cases voisines
        qui n'ont pas de mines.
        """
        # On obtiens la case sur laquelle on appuie
        case = self.tableau_mines.obtenir_case(self.case_appuyer_rangee,
            self.case_appuyer_colonne)

        # On valide que la case n'est pas déjà dévoilée si elle ne l'ai pas,
        # on ajoute un tour au compteur
        if not case.est_devoilee and not self.defaite:
            case.devoiler()

            # On vérifie si la case est minée. Si oui, on affiche une bombe et
            # on affiche un message de défaite
            if case.est_minee:
                self.dictionnaire_boutons[self.case_appuyer_rangee,\
                    self.case_appuyer_colonne]['image'] = self.image_bombe
                sa.WaveObject.from_wave_file(self.sonexplosion).play()
                self.afficher_defaite()

            # Si la case n'est pas minée, on met l'image correspondante au
            # nombre de mines voisines de cette case
            elif not case.est_minee and case.est_devoilee:
                self.dictionnaire_boutons[self.case_appuyer_rangee,\
                    self.case_appuyer_colonne]['image'] = \
                        self.liste_images_nombres[case.nombre_mines_voisines]
                
                self.tableau_mines.nombre_cases_sans_mine_a_devoiler -= 1

                # Si on a découvert toutes les mines on gagne
                if self.tableau_mines.nombre_cases_sans_mine_a_devoiler == 0:
                    self.afficher_victoire()

                # Si la case n'a pas de mines voisines, on déclenche l'effet
                # cascade pour dévoiler les case voisines sans mines.
                if case.nombre_mines_voisines == 0: # Condition d'arrêt
                    liste_voisin = self.tableau_mines.obtenir_voisins(
                        self.case_appuyer_rangee, self.case_appuyer_colonne)
                    for voisin in liste_voisin:
                        rangee, colonne = voisin
                        case_voisine = self.tableau_mines.obtenir_case(
                            rangee,colonne)
                        if not case_voisine.est_minee:
                            self.case_appuyer_rangee = rangee
                            self.case_appuyer_colonne = colonne
                            self.devoiler_case() # Récursion
                            
    def afficher_defaite(self):
        """
        Fonction qui affiche le message de défaite.
        """
        # Attributs
        msgbox = Toplevel()
        msgbox.grid()
        # Message qui nous affiche la défaite et 
        # appelle la fonction afficher_solution
        message = Message(msgbox, text="Vous avez perdu! Appuyer sur OK!",
        anchor='center',justify='center')
        message.grid(row=0, column=0,columnspan=3)
        bouton_ok = Button(msgbox, text="Ok",command=lambda:[msgbox.destroy(),
        self.afficher_solution()])
        bouton_ok.grid(row=2, column=1)
        #On défini defaite à True
        self.defaite = True

    def afficher_victoire(self):
        """
        Fonction qui affiche le message de victoire.
        """
        # Attributs
        boite = Toplevel()
        #Message qui affiche notre victoire et appelle la fonction 
        #afficher_solution
        message = Message(boite, text="Vous avez gagné! Appuyer sur OK!",
        anchor='center',justify='center')
        message.pack()
        bouton_ok = Button(boite, text="Ok",command=lambda:[boite.destroy(),
        self.afficher_solution()])
        bouton_ok.pack()
        #On defini victoire à True
        self.victoire = True

    def afficher_solution(self):
        """
        Fonction qui affiche la solution complète
        """
        # On parcours le tableau
        for i in range(self.tableau_mines.dimension_rangee):
            for j in range(self.tableau_mines.dimension_colonne):
                case = self.tableau_mines.obtenir_case(i+1, j+1)
                self.tableau_mines.devoiler_case(i+1, j+1)
                bouton = self.dictionnaire_boutons[(i+1, j+1)]

                # On affiche les images en fonctions des cases
                if case.est_minee:
                    bouton['image'] = self.image_bombe
                else:
                    bouton['image'] = self.liste_images_nombres\
                        [case.nombre_mines_voisines]

    def nouvelle_partie(self):
        """
        Fonciton qui initialise une nouvelle partie.
        """
        self.dictionnaire_boutons = {}
        self.cadre.destroy()
        self.tour = 0
        self.temps = 0
        self.ajouter_tour()
        self.afficher_chronometre()
        self.cadre = Frame(self)
        self.cadre.grid(padx=10, pady=10)
        self.defaite = False
        self.tableau_mines = Tableau(self.nombre_rangees_partie,\
            self.nombre_colonnes_partie, self.nombre_mines_partie)

        # On parcours le nouveau tableau pour y placer les mines
        for i in range(self.tableau_mines.dimension_rangee):
            for j in range(self.tableau_mines.dimension_colonne):
                bouton = BoutonCase(self.cadre, i+1, j+1)
                bouton.grid(row=i, column=j)
                bouton.bind('<Button-1>', self.trouver_case)
                bouton.bind('<Button-3>', self.mettre_drapeau_rouge)
                self.dictionnaire_boutons[(i+1, j+1)] = bouton

    def demander_ouinon(self):
        """
        Fonction qui demande à l'utilisateur s'il veut vraiment quitter le 
        jeu. Si oui, le jeu termine.
        """
        if messagebox.askyesno(title="Quitter",\
            message="Voulez-vous vraiment quitter ?"):
            self.destroy()

    def afficher_intructions(self):
        """
        Fonction qui affiche les instructions du jeu.
        """
        regle = """Les règles du jeu sont les suivantes :
        1. Si le joueur choisit une case où une mine est cachée, 
        la mine explose et la partie est terminée.
        2. Si le joueur choisit une case avec un nombre caché, 
        la case est dévoilée et le nombre devient visible.
        3. Si le joueur choisit une case vide
        (donc qui n’a ni mine ni nombre caché), il y a un effet en cascade qui 
        fait le dévoilement de toutes les cases vides dans le voisinage jusqu’à
        ce que la limite du tableau soit atteinte ou qu’une case avec un numéro
        caché soit atteinte.
        L’objectif du jeu est d’identifier, par la logique, toutes les cases
        contenant des mines, sans en déclencher aucune."""
        messagebox.showinfo(title= 'Info', message= regle)

    def maj_donnees(self, nb_rangees, nb_colonnes, nb_mines):
        """
        Fonction qui met à jour le nombre de rangee, le nombre de colonne ainsi
        que le nomre de mine pour configurer le tableau.

        Args:
            nb_rangees (int): Nombre de rangées pour le tableau
            nb_colonnes (int): Nombre de colonnes pour le tableau
            nb_mines (int): Nombre de mines pour le tableau
        """
        self.nombre_rangees_partie = nb_rangees
        self.nombre_colonnes_partie = nb_colonnes
        self.nombre_mines_partie = nb_mines
        
    def configurer_partie(self):
        """
        Fonction qui permet de redimensionner le tableau. Une fenêtre apparaît
        et l'utilisateur peux entrer les configurations qu'il désire.
        """
        # On crée une fenêtre dans laquel mettre le tous
        self.fenetre = Toplevel()
        self.fenetre.wm_title('Configuration de la partie')
        self.fenetre.geometry("%dx%d%+d%+d" % (150, 200, 0, 0))
        self.fenetre.resizable(width = 0,height=0)
        
        # On met un Frame dans la fenêtre
        fenetre_frame = Frame(self.fenetre)
        fenetre_frame.grid(padx=15, pady=10)

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

        # On crée un label pour le message d'erreur
        self.label_erreur_configuration = Label(fenetre_frame, text='')
        self.label_erreur_configuration.grid(row=3,column=0,columnspan=2)
        
        # On crée un bouton de soumission
        bouton_soumission = Button(fenetre_frame, text="Go!", command=lambda:
            self.valider_configuration(entry_rangee.get(),entry_colonne.get(),
            entry_mine.get(),fenetre_frame))
        bouton_soumission.grid(row=4, column = 0, columnspan = 2)

    def valider_configuration(self, nb_rangees, nb_colonnes, nb_mines, widget):
        """
        Fonction qui valide l'entré des données lors de la configuration du
        tableau. La fonction valide que l'entré est bien un entier positif.

        Args:
            nb_rangees (int): Nombre de rangées
            nb_colonnes (int): Nombre de colonnes
            nb_mines (int): Nombre de mines
            widget (tkinter.Frame): Fenêtre dans laquelle se trouve les widgets
                                    d'entrées.

        Raises:
            ValueError: Erreur de valeur si l'usager entre un caractère non
                        numérique.
            NombreMinesInvalide: Erreur d'entrée invalide si l'usager entre un
                        entier inférieur à zéro.
        """
        # On valide que les entrées sont >= 0 et que le tableau ne fait pas 0x0
        try:
            self.maj_donnees(int(nb_rangees), int(nb_colonnes), int(nb_mines))
            if not self.nombre_rangees_partie > 0 or\
                not self.nombre_colonnes_partie > 0 or\
                    not self.nombre_mines_partie >= 0:
                raise ValueError
            elif self.nombre_mines_partie > self.nombre_rangees_partie * \
                self.nombre_colonnes_partie - 1:
                raise NombreMinesInvalide
            self.fenetre.destroy()
            self.nouvelle_partie()
        #Si l'utilisateur entre un entiers non positifs on soulève ValueError
        except ValueError:
            self.label_erreur_configuration.config(
                text="Veuillez entrer\ndes entiers positifs!")
        #Si l'utilisateur entre un nombre de mines plus élevé que de case, on 
        # soulève NombreMinesInvalide
        except NombreMinesInvalide:
            self.label_erreur_configuration.config(
                text="Veuillez entrer\nmoins de mines\nque de cases!")

    def sauvegarde_partie(self):
        """
        Fonction qui effectue la sauvegarde d'une partie en fichier texte.
        """

        # On crée un dictionnaire de données pour y mettre l'information
        donnees = {}
        # On remplit le dictionnaire
        donnees['rangees'] = self.nombre_rangees_partie
        donnees['colonnes'] = self.nombre_colonnes_partie
        donnees['mines'] = self.nombre_mines_partie
        donnees['tours'] = self.tour
        donnees['defaite'] = self.defaite
        donnees['tableau'] = {}
        donnees['case_a_devoiler'] = \
            self.tableau_mines.nombre_cases_sans_mine_a_devoiler
        #On défini les données dans le dictionnaire
        for i in range(self.tableau_mines.dimension_rangee):
            for j in range(self.tableau_mines.dimension_colonne):
                case = self.tableau_mines.obtenir_case(i+1, j+1)
                donnees['tableau'][f"({i+1}, {j+1})"] = {
                "minee": case.est_minee,
                "devoilee":case.est_devoilee,
                "nombre_voisins":case.nombre_mines_voisines,
                "drapeau":self.dictionnaire_boutons[(i+1, j+1)].drapeau
                }

        # On crée une fenêtre pour demander le nom du fichier de sauvegarde
        fenetre_sauvegarde = Toplevel()
        fenetre_sauvegarde.geometry("%dx%d%+d%+d" % (300, 100, 0, 0))
        nom_fichier = Label(fenetre_sauvegarde, text="Nom de la sauvegarde")
        nom_fichier.pack()
        entry_nom_fichier = Entry(fenetre_sauvegarde, width = 150)
        entry_nom_fichier.pack()
        sauvegarde_bouton = Button(fenetre_sauvegarde, text="Sauvegarder", 
        command=lambda:[
            self.creer_sauvegarde(entry_nom_fichier.get(),donnees),
            fenetre_sauvegarde.destroy()
            ])
        sauvegarde_bouton.pack()


    def creer_sauvegarde(self,nom,donnees):
        """
        Fonction qui ouvre le fichier de sauvegarde et met les données à 
        l'intérieur

        Args:
            nom (str): Nom du fichier de sauvegarde
            donnees (dict): Dictionnaire contenant les données à sauvegarder
        """
        # On ouvre le fichier de sauvegarde et on écrit les données
        with open(f"{nom}.txt", "w") as fichier_sauvegarde:
            json.dump(donnees, fichier_sauvegarde)


    def charger_partie(self):
        """
        Fonction qui charge une partie à partir d'un fichier texte de
        sauvegarde. On valide aussi que le fichier existe.
        """
        

        # On détruit le cadre qu'on avait au début
        self.cadre.destroy()
        self.cadre = Frame(self)
        self.cadre.grid(padx=10, pady=10)

        # On ouvre le fichier de sauvegarde pour y lire les données
        with open("fichier_sauvegarde.txt", "r") as fichier_sauvegarde:
            donnees = json.load(fichier_sauvegarde)
        
        # On charge les données aux bons attributs
        self.nombre_rangees_partie = donnees['rangees']
        self.nombre_colonnes_partie = donnees['colonnes']
        self.nombre_mines_partie = donnees['mines']
        self.tour = donnees['tours'] - 1
        self.defaite = donnees['defaite']
        self.tableau_mines = Tableau(self.nombre_rangees_partie,
            self.nombre_colonnes_partie,self.nombre_mines_partie)

        self.ajouter_tour()
        self.afficher_chronometre()
        # On recrée le tableau sauvegardé
        for i in range(self.tableau_mines.dimension_rangee):
            for j in range(self.tableau_mines.dimension_colonne):
                bouton = BoutonCase(self.cadre, i+1, j+1)
                bouton.grid(row=i, column=j)
                bouton.bind('<Button-1>', self.trouver_case)
                bouton.bind('<Button-3>', self.mettre_drapeau_rouge)
                #On extrait les données
                self.dictionnaire_boutons[(i+1, j+1)] = bouton
                self.dictionnaire_boutons[(i+1, j+1)].drapeau = \
                    donnees['tableau'][f"({i+1}, {j+1})"]['drapeau']
                case = self.tableau_mines.obtenir_case(i+1, j+1)
                case.est_minee = donnees['tableau'][f"({i+1}, {j+1})"]['minee']
                case.est_devoilee = donnees['tableau'][f"({i+1}, {j+1})"]\
                    ['devoilee']
                case.nombre_mines_voisines = donnees['tableau']\
                    [f"({i+1}, {j+1})"]['nombre_voisins']
                #On reinitialise les photos des case selon leurs statut
                if case.est_devoilee:
                    self.tableau_mines.devoiler_case(i+1, j+1)
                    if case.est_minee:
                        bouton['image'] = self.image_bombe
                    else:
                        bouton['image'] = self.liste_images_nombres\
                            [case.nombre_mines_voisines]
                elif self.dictionnaire_boutons[(i+1, j+1)].drapeau:
                    bouton['image'] = self.image_drapeau
        self.tableau_mines.nombre_cases_sans_mine_a_devoiler = \
            donnees['case_a_devoiler']

    def afficher_createurs(self):
        """
        Fonction qui affiche un message d'information sur les créateurs du jeu.
        """
        print("Aryanne Pommerleau, David Côté, Alex Caissy")

    def mettre_drapeau_rouge(self, event):
        """
        Fonction qui affiche le drapeau rouge quand on fait 
        un clic droit avec la souris.

        Args:
            event (<Button-3>) : Clic sur la souris droite de la case de notre 
                                 choix.
        """

        # On retrouve le bouton sur lequel on a appuyé
        bouton_drapeau = event.widget

        # On retrouve la case du bouton
        case = self.tableau_mines.obtenir_case(
            bouton_drapeau.rangee_x, bouton_drapeau.colonne_y)

        # Si le bouton à déjà un drapeau, on enlève le drapeau
        if bouton_drapeau.drapeau:
            bouton_drapeau.reinitialiser_image()
            bouton_drapeau.drapeau = not bouton_drapeau.drapeau

        # Si le bouton n'a pas de drapeau, on en met un
        elif not bouton_drapeau.drapeau and not case.est_devoilee and \
            not self.defaite:
            bouton_drapeau.drapeau = not bouton_drapeau.drapeau
            bouton_drapeau['image'] = self.image_drapeau
    
class NombreMinesInvalide(Exception):
    """
    Classe créée pour gérer une erreur. Si l'usager entre un nombre de mines
    inférieur aux nombres de cases - 1.

    Args:
        Exception (NombreMinesInvalide): Soulève une erreur.
    """
    pass