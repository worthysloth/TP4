# -*- coding: utf-8 -*-
"""
Module contenant la description de la classe Tableau. Un tableau est utilisé 
pour jouer une partie du jeu Démineur.

Auteurs: Aryanne Pomerleau, David Côté, Alexandre Caissy
"""

from case import Case
from random import randint


class Tableau():
    """
    Tableau du jeu de démineur, implémenté avec un dictionnaire de cases.
    
    Warning:
        Si vous ajoutez des attributs à la classe Tableau, n'oubliez pas de les 
        documenter ici.

    Attributes:
        dimension_rangee (int): Nombre de rangées du tableau
        dimension_colonne (int): Nombre de colonnes du tableau
        nombre_mines (int): Nombre de mines cachées dans le tableau

        nombre_cases_sans_mine_a_devoiler (int) : Nombre de cases sans mine qui 
        n'ont pas encore été dévoilées
        Initialement, ce nombre est égal à dimension_rangee * dimension_colonne 
        - nombre_mines

        dictionnaire_cases (dict): Un dictionnaire de case en suivant le format 
        suivant:
            Les clés sont les positions du tableau sous la forme d'un tuple 
            (x, y), x étant le numéro de la rangée, y étant le numéro de la 
            colonne. Les éléments sont des objets de la classe Case.
    """
    def __init__(self,dimension_rangee=5, dimension_colonne=5, nombre_mines=2):
        """ Initialisation d'un objet tableau.
        
        Attributes:
            dimension_rangee (int): Nombre de rangées du tableau 
                                    (valeur par défaut: 5)
            dimension_colonne (int): Nombre de colonnes du tableau 
                                    (valeur par défaut: 5)
            nombre_mines (int): Nombre de mines cachées dans le tableau 
                                    (valeur par défaut: 5)
        """ 
        # On initialise le tableau de départ
        self.dimension_rangee = dimension_rangee
        self.dimension_colonne = dimension_colonne
        self.nombre_mines = nombre_mines

        # Le dictionnaire de case, vide au départ, qui est rempli par la 
        # fonction initialiser_tableau().

        # On initialise le dictionnaire de cases
        self.dictionnaire_cases = {}
    
        # On remplit le tableau
        self.initialiser_tableau()

        # On calculce le nombre de cases sans mine
        self.nombre_cases_sans_mine_a_devoiler = self.dimension_rangee * \
        self.dimension_colonne - self.nombre_mines

    def valider_coordonnees(self, rangee_x, colonne_y):
        """
        Valide les coordonnées reçues en argument. Les coordonnées sont 
        considérées valides si elles se trouvent bien dans les dimensions du
        tableau.
        
        Args:
            rangee_x (int) : Numéro de la rangée de la case dont on veut valider
                            les coordonnées
            colonne_y (int): Numéro de la colonne de la case dont on veut 
                            valider les coordonnées
        
        Returns:
            bool: True si les coordonnées (x, y) sont valides, False autrement
        """

        # On crée deux variables booléennes pour valider la rangée et la 
        # colonne
        rangee_valide = rangee_x >= 1 and rangee_x <= self.dimension_rangee
        colonne_valide = colonne_y >= 1 and colonne_y <= self.dimension_colonne

        return rangee_valide and colonne_valide
    
    def obtenir_case(self, rangee_x, colonne_y):
        """
        Récupère une case à partir de ses numéros de ligne et de colonne
        
        Args:
            rangee_x (int) : Numéro de la rangée de la case
            colonne_y (int): Numéro de la colonne de la case
        Returns:
            Case: Une référence vers la case obtenue
            (ou None si les coordonnées ne sont pas valides)
        """

        # On vérifie que les coordonnées entrées sont valide
        # Si non, on retourne None
        if not self.valider_coordonnees(rangee_x, colonne_y):
            return None
        
        # Si les coordonnées sont valides, on retourne la case correspondante
        return self.dictionnaire_cases[(rangee_x, colonne_y)]

    def obtenir_voisins(self, rangee_x, colonne_y):
        """
        Retourne une liste de coordonnées correspondant aux cases voisines d'une
        case. Toutes les coordonnées retournées doivent être valides 
        (c'est-à-dire se trouver à l'intérieur des dimensions du tableau).

        Args:
            rangee_x (int) : Numéro de la rangée de la case dont on veut 
                            connaître les cases voisines
            colonne_y (int): Numéro de la colonne de la case dont on veut 
                            connaître les cases voisines

        Returns:
            list : Liste des coordonnées (tuple x, y) valides des cases voisines
            de la case dont les coordonnées sont reçues en argument
        """
        # On initialise une liste vide
        liste_coordonnees_cases_voisines = []

        # On parcours les voisins potentiels 
        for rangee in range(-1,2):
            for colonne in range(-1,2):
            
                # Si on se trouve sur les limites on ne passe pas le tuple
                if rangee_x+rangee == 0 or colonne_y+colonne == 0:
                    pass
                elif rangee_x+rangee > self.dimension_rangee or colonne_y+\
                    colonne > self.dimension_colonne:
                    pass
                else: # Si on est dans le tableau, on passe le tuple
                    liste_coordonnees_cases_voisines.append((rangee_x+rangee,\
                        colonne_y+colonne))

        return liste_coordonnees_cases_voisines

    def initialiser_tableau(self):
        """
        Initialise le tableau à son contenu initial en suivant les étapes 
        suivantes:
            1) On crée chacune des cases du tableau 
                (cette étape est programmée pour vous).
            2) On y ajoute ensuite les mines dans certaines cases qui sont 
                choisies au hasard
                (attention de ne pas choisir deux fois la même case!).
                - À chaque fois qu'on ajoute une mine dans une case, on obtient 
                    la liste de ses voisins 
                    (pour se faire, utilisez la méthode obtenir_voisins)
                - Pour chaque voisin, on appelle la méthode 
                    ajouter_une_mine_voisine de la case correspondante.
        """
        # On parcours les rangées et les colonnes pour y ajouter une case
        for rangee_x in range(1, self.dimension_rangee+1):
            for colonne_y in range(1, self.dimension_colonne+1):
                self.dictionnaire_cases[(rangee_x, colonne_y)] = Case()
        
        # On crée une liste de tuple aléatoire NON-répétitive
        # On initie la liste
        liste_tuple_random = []

        # On initie le compteur
        compteur = 0
        while compteur < self.nombre_mines:
    
                # On crée le tuple aléatoire
            random_x = randint(1, self.dimension_rangee)
            random_y = randint(1, self.dimension_colonne)

            # On s'assure que le tuple ne soit pas dans la liste
            if (random_x, random_y) not in liste_tuple_random:
                liste_tuple_random.append((random_x, random_y))
                compteur += 1

        # On parcours les clés de 'self.dictionnaire_cases' pour y placer les 
        # mines
        for cle in liste_tuple_random:

            # On ajoute la mine
            self.dictionnaire_cases[cle].ajouter_mine()

            # On crée un tuple avec la clé
            x, y = cle

            # On parcrous la liste_voisins pour ajouter_une_mine_voisine
            liste_voisins = self.obtenir_voisins(x, y)
            for voisin in liste_voisins:
                self.dictionnaire_cases[voisin].ajouter_une_mine_voisine()


    def coordonnees_dans_limite(self, rangee_x, colonne_y):
        """
        Valide que les coordonées entrées sont à l'intérieur des limites du 
        tableaux créé.
        Args:
            rangee_x (int) : Numéro de la rangée de la case dont on veut valider
            la position
            colonne_y (int): Numéro de la colonne de la case dont on veut 
            valider la position
        Returns:
            bool : True si et seulement si les 2 coordonnées sont à l'intérieur
            du tableau
        """
        
        return 1 <= rangee_x <= self.dimension_rangee and 1 <= colonne_y <= \
            self.dimension_colonne


    def valider_coordonnees_a_devoiler(self, rangee_x, colonne_y):
        """
        Valide que les coordonnées reçues en argument sont celles d'une case que
        l'on peut dévoiler 
        (donc que les coordonnées sont valides et que la case correspondante n'a
        pas encore été dévoilée).
        
        Args:
            rangee_x (int) : Numéro de la rangée de la case dont on veut valider
            les coordonnées
            colonne_y (int): Numéro de la colonne de la case dont on veut
            valider les coordonnées
        
        Returns
            bool: True si la case à ces coordonnées (x, y) peut être dévoilée,
            False autrement (donc si la case a déjà été dévoilée ou que les 
            coordonnées ne dont pas valides).
        """  
        # On valide que les coordonnées recues sont dans le tableau et que la
        # case n'a toujours pas été dévoilée
        if self.valider_coordonnees(rangee_x, colonne_y) \
        and not self.obtenir_case(rangee_x, colonne_y).est_devoilee:
            return True
        else:
            return False
        
    def afficher_solution(self):
        """
        Méthode qui affiche le tableau de la solution à l'écran. La solution
        montre les mines pour les cases qui en contiennent et la valeur du
        nombre de mines voisines pour les autres cases.
        
        Important: Vous n'avez pas à modifier cette méthode, mais vous pouvez 
        vous en inspirer pour écrire la méthode afficher_tableau().
        """
        print() # Retour de ligne
        
        for rangee_x in range(0, self.dimension_rangee+1):
            
            # Affichage d'une ligne, caractère par caractère
            for colonne_y in range(0, self.dimension_colonne+1):
                if rangee_x == 0 and colonne_y == 0: 
                    # Premiers caractères de l'en-tête (coin supérieur gauche)
                    car = '  |' 
                elif rangee_x == 0:
                    # En-tête: numéro de la colonne 
                    # (si y > 10, on affiche seulement l'unité pour éviter les 
                    # décalages)
                    car = f'{colonne_y%10}' 
                elif colonne_y == 0:
                    # Début de ligne: numéro de la ligne sur deux caractères,
                    # suivi d'une ligne verticale.
                    car = f'{rangee_x:<2}|' 
                else:
                    # Contenu d'une case
                    case_xy = self.obtenir_case(rangee_x, colonne_y)  
                    if case_xy.est_minee:
                        car = 'M'
                    else:
                        car = str(case_xy.nombre_mines_voisines)
                
                # Afficher le caractère suivit d'un espace (sans retour de 
                # ligne)
                print(car, end=" ")
            
            # À la fin de chaque ligne
            print() # Retour de ligne
            if rangee_x == 0: # Ligne horizontale de l'en-tête
                print('--+-' + '--'*self.dimension_colonne) 
         
    def afficher_tableau(self):
        """
        Méthode qui affiche le tableau à l'écran. Le tableau montre le contenu 
        des cases dévoilées (mine ou nombre de mines voisines) ou un carré pour
        les cases non dévoilées.
        """
        print() # Retour de ligne
        
        for rangee_x in range(0, self.dimension_rangee+1):
            
            # Affichage d'une ligne, caractère par caractère
            for colonne_y in range(0, self.dimension_colonne+1):
                if rangee_x == 0 and colonne_y == 0: 
                    # Premiers caractères de l'en-tête (coin supérieur gauche)
                    car = '  |' 
                elif rangee_x == 0:
                    # En-tête: numéro de la colonne 
                    # (si y > 10, on affiche seulement l'unité pour éviter les 
                    # décalages)
                    car = f'{colonne_y%10}' 
                elif colonne_y == 0:
                    # Début de ligne: numéro de la ligne sur deux caractères,
                    # suivi d'une ligne verticale.
                    car = f'{rangee_x:<2}|' 
                else:
                    # Contenu d'une case
                    case_xy = self.obtenir_case(rangee_x, colonne_y)

                    # Si la case est devoilee  
                    if case_xy.est_devoilee:
                        if case_xy.est_minee:
                            car = 'M'
                        else:
                            car = str(case_xy.nombre_mines_voisines)

                    #Si la case n'est pas dévoilee         
                    else:
                        car = '◼'
                                        
                # Afficher le caractère suivit d'un espace (sans retour de 
                # ligne)
                print(car, end=" ")
            
            # À la fin de chaque ligne
            print() # Retour de ligne
            if rangee_x == 0: # Ligne horizontale de l'en-tête
                print('--+-' + '--'*self.dimension_colonne) 


    def contient_cases_a_devoiler(self):
        """
        Méthode qui indique si le tableau contient des cases à dévoiler.
        
        Returns:
            bool: True s'il reste des cases à dévoiler, False autrement.
        """

        return self.nombre_cases_sans_mine_a_devoiler != 0

    def devoiler_case(self, rangee_x, colonne_y):
        """
        Méthode qui dévoile le contenu de la case dont les coordonnées sont
        reçues en argument. Si la case ne contient pas de mine, on décrémente
        l'attribut qui représente le nombre de cases sans mine à dévoiler. Aussi
        si cette case n'est voisine d'aucune mine, on dévoile ses voisins. 
       
        Args:
            rangee_x (int) : Numéro de la rangée de la case à dévoiler
            colonne_y (int): Numéro de la colonne de la case à dévoiler
        """
        # On met la propriété est_devoilee à true
        self.obtenir_case(rangee_x, colonne_y).est_devoilee = True
        
        # Si la case n'a pas de mine, on décrémente le nombre de cases sans
        # mines
        if not self.obtenir_case(rangee_x, colonne_y).est_minee and \
            self.valider_coordonnees(rangee_x, colonne_y):
                self.nombre_cases_sans_mine_a_devoiler -= 1
        
        # On crée la liste des voisins
        voisins = self.obtenir_voisins(rangee_x, colonne_y)
        
        # On initialie une variable bool
        devoiler = True
        
        # On parcours la liste voisins pour voir si la case est minée. 
        for x,y in voisins:
            if self.obtenir_case(x,y).est_minee == True:
                devoiler = False

        # Si la case n'a pas de mine, on met sa propriété est_devoilee à true
        # et on décrémente le nombre de cases sans mine à dévoiler
        if devoiler == True:
            for x,y in voisins:
                self.obtenir_case(x,y).est_devoilee = True
                self.nombre_cases_sans_mine_a_devoiler -= 1
            
        
    def contient_mine(self, rangee_x, colonne_y):
        """
        Méthode qui vérifie si la case dont les coordonnées sont reçues en 
        argument contient une mine.
        
        Args:
            rangee_x (int) : Numéro de la rangée de la case dont on veut 
                            vérifier si elle contient une mine
            colonne_y (int): Numéro de la colonne de la case dont on veut 
                            vérifier si elle contient une mine
        
        Returns:
            bool: True si la case à ces coordonnées (x, y) contient une mine, 
            False autrement.
        """
        return self.obtenir_case(rangee_x, colonne_y).est_minee



def test_initialisation():
    tableau_test = Tableau()

    assert tableau_test.contient_cases_a_devoiler()
    assert tableau_test.nombre_cases_sans_mine_a_devoiler == \
        tableau_test.dimension_colonne * tableau_test.dimension_rangee - \
            tableau_test.nombre_mines

def test_valider_coordonnees():

    tableau_test = Tableau()
    dimension_x, dimension_y = tableau_test.dimension_rangee, \
        tableau_test.dimension_colonne

    assert tableau_test.valider_coordonnees(dimension_x, dimension_y)
    assert not tableau_test.valider_coordonnees(dimension_x+1, dimension_y)
    assert not tableau_test.valider_coordonnees(dimension_x, dimension_y+1)
    assert not tableau_test.valider_coordonnees(-dimension_x, dimension_y)
    assert not tableau_test.valider_coordonnees(0, 0)
    
def test_obtenir_voisins():
    tableau_test = Tableau()
    assert tableau_test.obtenir_voisins(3,3) == [(2,2),(2,3),(2,4),(3,2),(3,3),\
        (3,4),(4,2),(4,3),(4,4)]
    assert tableau_test.obtenir_voisins(1,1) == [(1,1),(1,2),(2,1),(2,2)]
    assert tableau_test.obtenir_voisins(4,5) == [(3,4),(3,5),(4,4),(4,5),(5,4),\
        (5,5)]
    
def test_valider_coordonnees_a_devoiler():
    tableau_test = Tableau(dimension_rangee=5, dimension_colonne=5, \
        nombre_mines=5)
    tableau_test.devoiler_case(3,3)
    assert tableau_test.valider_coordonnees_a_devoiler(3,3) == False
    assert tableau_test.valider_coordonnees_a_devoiler(10,10) == False
    
def test_devoiler_case():
    tableau_test = Tableau()
    tableau_test.devoiler_case(3,3)
    assert tableau_test.obtenir_case(3,3).est_devoilee
    assert tableau_test.obtenir_case(3,5).est_devoilee == False

def test_case_contient_mine():
    tableau_test = Tableau(dimension_rangee=5, dimension_colonne=5, \
        nombre_mines=0)
    case = tableau_test.obtenir_case(3,3)
    case.ajouter_mine()
    assert tableau_test.contient_mine(3,3) == True
    assert tableau_test.contient_mine(2,3) == False


if __name__ == '__main__':
    tableau_test = Tableau()
    print('\nTABLEAU:')
    tableau_test.afficher_tableau()
    print('\nSOLUTION:')   
    tableau_test.afficher_solution()
    print('Tests unitaires...')
    test_initialisation()
    test_valider_coordonnees()
    test_obtenir_voisins()
    test_valider_coordonnees_a_devoiler()
    test_devoiler_case()
    test_case_contient_mine()
    print('Tests réussis!')
    
    
    