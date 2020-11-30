# -*- coding: utf-8 -*-
"""
Module contenant la description de la classe Partie qui permet de jouer une
partie du jeu démineur. Dois être démarré en appelant la méthode jouer(). Cette
classe contient les informations sur une partie et utilise un objet
tableau_mines (une instance de la classe Tableau).

Auteurs: Aryanne Pomerleau, David Côté, Alexandre Caissy
"""

from tableau import Tableau


class Partie():
    """
    Contient les informations sur une partie du jeu Démineur, qui se jouera avec
    un tableau de mines. Des méthodes sont disponibles pour faire avancer la
    partie et interagir avec l'utilisateur.

    Attributes:
        tableau_mines (Tableau): Le tableau de cases où les mines sont cachées
        avec lequel se déroule la partie.
        partie_terminee (bool): True lorsque l'utilisateur a terminé de jouer la
        partie (victoire ou défaite)
    """

    def __init__(self):
        """
        Initialisation de la Partie.

        Note: L'instance de la classe Tableau, qui sera manipulée par les
        méthodes de la classe, sera initialisée lors de l'appel de la méthode
        Partie.jouer().
        """
        self.tableau_mines = None
        self.partie_terminee = False

    def jouer(self):
        """
        Auteur: David
        Tant que la partie n'est pas terminée, on joue un tour de la partie.
        Une fois la partie terminée, on affiche le tableau de cases complètement
        dévoilée et on indique un message sur l'issue de la partie (victoire ou
        défaite).
        """
           # On demande à l'usager le nombre de rangee, colonnes et mines
           # et on valide les entrées (entiers positifs, si entrée vide on met 
           # le tableau de défault 5x5)
        try:
            rangee_x = int(input("Entrez le nombre de lignes:"))
            colonne_y = int(input("Entrez le nombre de colonnes:"))
            nombre_mines = int(input("Entrez le nombre de mines:"))
            while rangee_x <= 0 or colonne_y <= 0 or nombre_mines <= 0:
                print("Entrez des entiers positifs!")
                rangee_x = int(input("Entrez le nombre de lignes:"))
                colonne_y = int(input("Entrez le nombre de colonnes:"))
                nombre_mines = int(input("Entrez le nombre de mines:"))
            self.tableau_mines = Tableau(rangee_x, colonne_y, nombre_mines)
        except ValueError:
            print("\nAucune dimensions sélectionnées.")
            print("Tableau 5x5 avec 5 mines:")
            self.tableau_mines = Tableau()


        # On initialise un compteur de tours
        compteur_tours = 0
        # On joue un tour tans que la partie n'est pas terminée
        while not self.partie_terminee:
            compteur_tours += 1
            print(f'\n===> Tour #{compteur_tours} <===')
            if compteur_tours % 5 == 0:
                print(f"\nLâchez pas! Vous avez fait {compteur_tours} tours!")
            self.tableau_mines.afficher_tableau()
            self.tour()

        # Si la partie est termninée, on affiche la solution
        print(f"\nVoici la solution:")
        self.tableau_mines.afficher_solution()

        # On vérifie si on a une victoire ou une défaite
        # Victoire s'il ne reste plus de case à dévoiler
        # Défaite sinon.
        if self.tableau_mines.nombre_cases_sans_mine_a_devoiler <= 0:
            print("\nVictoire!")
        else:
            print("\nDéfaite!")

    def tour(self):
        """ 
        Jouer un tour, c'est-à-dire:
        
        À chaque tour:
            - On demande à l'utilisateur les coordonnées d'une case à dévoiler
            - On dévoile la case
            - On détecte si une mine a été actionnée, 
              auquel cas affecte True à l'attribut self.partie_terminee.
            - On détecte si toutes les cases ont été dévoilées, 
              auquel cas affecte True à l'attribut self.partie_terminee.
        """

        # On demande à l'utilisateur les coordonnées d'une case à dévoiler
        rangee_x, colonne_y = self.demander_coordonnees_case_a_devoiler()

        # On dévoile la case
        self.tableau_mines.devoiler_case(rangee_x, colonne_y)

        # On détecte si une mine a été actionnée
        if self.tableau_mines.obtenir_case(rangee_x, colonne_y).est_minee:
            self.partie_terminee = True

        # On détecte si toutes les cases ont été dévoilées
        elif self.tableau_mines.nombre_cases_sans_mine_a_devoiler == 0:
            self.partie_terminee = True

    def valider_coordonnees(self, rangee_x, colonne_y):
        """
        Méthode qui valide les coordonnées reçues en paramètres.
        Les coordonnées doivent:
            1) être des caractères numériques;
            2) être à l'intérieur des valeurs possibles des rangées et des 
            colonnes du tableau;
            3) correspondre à une case qui n'a pas encore été dévoilée.

        Args:
            rangee_x (str):     Chaîne de caractères contenant la rangée
            colonne_y (str):    Chaîne de caractères contenant  la colonne

        Returns:
            bool : True si les coordonnées sont valides, False autrement.
        """

        # On valide les coordonnées en vérifiant qu'elles sont numériques, ainsi
        # qu'avec la fonction valider_coordonnees_a_devoiler
        return rangee_x.isnumeric() and colonne_y.isnumeric() and \
            self.tableau_mines.valider_coordonnees_a_devoiler(
                int(rangee_x), int(colonne_y))

    def demander_coordonnees_case_a_devoiler(self):
        """
        Auteur: David
        Méthode qui demande à l'utilisateur d'entrer la coordonnée de la case 
        qu'il veut dévoiler. Cette coordonnée comporte un numéro de rangée et un
        numéro de colonne. Tant que les coordonnées ne sont pas valides, on 
        redemande de nouvelles coordonnées. Une fois les coordonnées validées,
        on retourne les deux numéros sous forme d'entiers.

        Returns:
            int: Numéro de la rangée
            int: Numéro de la colonne

        """
        # On demande à l'usager d'entrer le numéro de la ligne à dévoiler
        rangee_x = input("Entrez le numéro de ligne:")

        # On crée une espace vide
        print()

        # On demande à l'usager d'entrer le numéro de la colonne à dévoiler
        colonne_y = input("Entrez le numéro de colonne:")

        # Tant que les coordonnées entrées par l'usager sont non valide, on
        # demande de nouvelles coordonnées.
        while not self.valider_coordonnees(rangee_x, colonne_y):
            print("\nCoordonnées non valides. Recommencez!\n")
            rangee_x = input("Entrez le numéro de ligne:")
            colonne_y = input("\nEntrez le numéro de colonne:")

        return int(rangee_x), int(colonne_y)
