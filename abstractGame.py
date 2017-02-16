#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Définition de classes abstraites
- Game : la structure du jeu
- Player : ce que doit faire un joueur
"""

__author__ = "mmc <marc-michel dot corsini at u-bordeaux dot fr>"
__date__ = "Avr 2013"
__update__ = "5.12.16"
__usage__ = "Classes abstraites pour jeux de plateau"

from mmcTools import signature
from numbers import Number
import copy

class Game(object):
    """
    La classe generique pour des jeux a deux joueurs
    """
    def __init__(self,*args,**kwargs):
        """
        constructeur de classe, joue le role de l'initialisation
        Il va falloir créer la configuration initiale
        *args : parametres necessaires à l'initialisation
        **kwargs : parametres nommés necessaires à l'initialisation
        """
        self.reset(*args, **kwargs)
        
    def reset(self, *args, **kwargs):
        """ initialisation du jeu """
        raise NotImplementedError("initialisation: non definie")

    @property
    def configuration(self):
        """
        renvoie la configuration courante du jeu
        une configuration c'est une paire: etat_jeu, joueur
        """
        raise NotImplementedError("configuration: non definie")

    @configuration.setter
    def configuration(self, newcfg):
        """
        On fait ici les controles pour s'assurer que tout ce passe
        pour le mieux, on peut a ce niveau sauvegarder l'ancienne
        configuration (par exemple pour gerer un historique)

        utilisation
        jeu = Game()
        jeu.configuration = nouvelle_configuration
        """
        raise NotImplementedError("configuration: non definie")

    @property
    def etat_jeu(self):
        """ renvoie une copie du jeu pour éviter des ennuis """
        return copy.deepcopy(self.configuration[0])

    @property
    def trait(self):
        """ renvoie le joueur à qui c'est le tour """
        return copy.deepcopy(self.configuration[1])
        
    def __str__(self):
        """
        renvoie la chaine à afficher lors d'un print
        """
        raise NotImplementedError("affichage: non definie")

    @classmethod
    def regles(cls):
        """ affiche les regles du jeux """
        _msg = """
        ICI ON MET LES REGLES DU JEU
        """
        return _msg

    def adversaire(self, joueur):
        """ renvoie l'autre joueur """
        raise NotImplementedError("adversaire: non définie")

    def gagnant(self, joueur):
        """ 
        @return True si la configuration est une victoire pour le joueur 
        @return False sinon
        """
        raise NotImplementedError("gagnant: non definie")

    def perdant(self, joueur):
        """ 
        @return True si la configuration est une defaite pour le joueur
        @return False sinon
        """
        raise NotImplementedError("perdant: non definie")

    def finPartie(self, joueur):
        """ renvoie True si la partie est terminee """
        raise NotImplementedError("finPartie: non definie")

    def listeCoups(self, joueur):
        """ renvoie la liste des coups autorises pour le joueur """
        raise NotImplementedError("listeCoups: non definie")

    def joue(self, coup, joueur):
        """
        renvoie une nouvelle configuration
        apres que le joueur a effectue son coup
        ATTENTION: on ne modifie pas la configuration courante
        """
        raise NotImplementedError("joue: non definie")

    def evaluation(self, joueur):
        """
        evalue numeriquement la situation dans laquelle 
        se trouve le joueur
        """
        raise NotImplementedError("evaluation: non definie")

class Player(object):
    """
    classe specifique pour la definition d'un joueur
    """
    def __init__(self,*args,**kwargs):
        self.nom = 'default player'

    def __str__(self): return self.nom

    def __call__(self,*args,**kwargs):
        """
        Simule un joueur comme une fonction
        A = Player(...)
        A(....) est equivalent a A.choixCoup(....)
        """
        return self.choixCoup(*args,**kwargs)

    def choixCoup(self, unJeu, joueur):
        """ renvoie le coup choisi par le joueur
        le coup est obligatoirement un coup appartenant a
        listeCoups(joueur)
        """
        assert (isinstance(unJeu, Game))
        raise NotImplementedError("choixCoup: undef")

    @property
    def nom(self): return self.__name

    @nom.setter
    def nom(self,val):
        if not isinstance(val,str): self.__name = str(val)[:30]
        else: self.__name = val[:30]


@signature            
def partie(jeu: Game, funA: Player, funB: Player,
           nbManches: int=1) -> tuple:
    """
    funA et funB sont des fonctions pour les joueurs A et B
    elles recoivent en entree un etat/configuration et un joueur,
    elles renvoient un coup
    
    par defaut on fera jouer  humain contre humain

    Une partie est constituée de plusieurs manches
    partie doit
    1. afficher les regles du jeu & initialiser une partie
    2. faire autant de manches que nécessaires
    3. afficher les informations à la fin de chaque manche
    4. s'arreter quand la partie est terminee
    5. afficher qui a gagné
    """
    raise NotImplementedError("partie: non definie")

@signature
def manche(jeu: Game, funA: Player,funB: Player) -> tuple:
    """
    funA et funB sont des fonctions pour les joueurs A et B
    elles recoivent en entree un etat/configuration et un joueur,
    elles renvoient un coup
    
    par defaut on fait jouer  humain contre humain

    manche doit
    1. initialiser une manche
    2. faire jouer alternativement le joueur A et le joueur B
    3. afficher les informations
    4. s'arreter quand la manche est terminee
    """
    raise NotImplementedError("manche: non definie")
