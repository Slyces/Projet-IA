# =============================================================================
'''
Quick description of the file
'''
# =============================================================================
__author__ = 'Simon Lassourreuille & Loizel Antoine'
__version__ = ''
__date__ = '16/02/2017'
__email__ = 'simon.lassourreuille@etu.u-bordeaux.fr'\
            '& antoine.loizel@etu.u-bordeaux.fr'
__status__ = 'TD'
# =============================================================================
from main import *
from abstractGame import *
from random import choice
# =============================================================================
class HexVirus(Game):
    def __init__(self, largeur: int, hauteur: int):
        self.__p = Plateau(largeur, hauteur)
        self.reset()

    # -------------------------------------------------------------------------
    @classmethod
    def regles(cls):
        """ affiche les regles du jeux """
        _msg = """
        Cliquer au hasard.
        """
        return _msg

    # -------------------------------------------------------------------------
    def reset(self):
        hauteur, largeur = self.__p.hauteur, self.__p.largeur
        self.__p = Plateau(largeur, hauteur)
        self.__p[0].valeur = BLANC
        self.__p[hauteur - 1, largeur - 1].valeur = BLANC
        self.__p[0, largeur - 1].valeur = NOIR
        self.__p[hauteur-1,0].valeur = NOIR
        self.__trait = BLANC

    # -------------------------------------------------------------------------
    @property
    def configuration(self):
        return self.__p.configuration, self.__trait

    # -------------------------------------------------------------------------
    @configuration.setter
    def configuration(self, args):
        """ args : configuration, trait """
        # print("    conf entry :", args)
        self.__p.load([x.valeur for x in args[0]])
        self.__trait = args[1]

    # -------------------------------------------------------------------------
    @property
    def etat_jeu(self):
        """ renvoie une copie du jeu pour éviter des ennuis """
        return copy.deepcopy(self.configuration[0])

    # -------------------------------------------------------------------------
    @property
    def trait(self):
        """ renvoie le joueur à qui c'est le tour """
        return copy.deepcopy(self.configuration[1])

    # -------------------------------------------------------------------------
    def scores(self):
        """ Dict of scores if game is ended, else None """
        for couleur in (BLANC, NOIR):
            if not self.listeCoups(couleur):
                scores = {couleur: len(list(filter(lambda x: x.valeur == couleur,
                                                   self.configuration[0])))}
                scores[self.adversaire(couleur)] = len(self.__p) - scores[couleur]
                return scores

    # -------------------------------------------------------------------------
    def adversaire(self, joueur):
        """ renvoie l'autre joueur """
        return BLANC if joueur == NOIR else NOIR

    # -------------------------------------------------------------------------
    def gagnant(self, joueur):
        """
        @return True si la configuration est une victoire pour le joueur
        @return False sinon
        """
        scores = self.scores()
        if scores:
            return scores[joueur] >= scores[self.adversaire(joueur)]
        return False

    # -------------------------------------------------------------------------
    def perdant(self, joueur):
        """
        @return True si la configuration est une defaite pour le joueur
        @return False sinon
        """
        return self.gagnant(self.adversaire(joueur))

    # -------------------------------------------------------------------------
    def finPartie(self, joueur= None):
        """ renvoie True si la partie est terminee """
        return bool(self.scores())

    # -------------------------------------------------------------------------
    def listeCoups(self, joueur):
        """ renvoie la liste des coups autorises pour le joueur """
        return self.__p.jouables(joueur)

    # -------------------------------------------------------------------------
    def joue(self, coup, joueur):
        """
        renvoie une nouvelle configuration
        apres que le joueur a effectue son coup
        ATTENTION: on ne modifie pas la configuration courante
        """
        newcfg, trait = self.configuration
        newcfg[coup.position].valeur = joueur
        for voisin in newcfg[coup.position].voisins:
            if voisin.valeur == self.adversaire(joueur):
                # ("trouvé :", repr(voisin))
                newcfg[voisin.position].valeur = joueur
                # print('Changé ? :', repr(newcfg[voisin.position]))
        # print('newconfig :', newcfg)
        return newcfg, self.adversaire(trait)

    # -------------------------------------------------------------------------
    def evaluation(self, joueur):
        """
        evalue numeriquement la situation dans laquelle
        se trouve le joueur
        """
        return self.__p.evaluation(joueur)

    # -------------------------------------------------------------------------
    def __str__(self):
        return str(self.__p) + '\nLe joueur {} a le trait.'.format(
            {NOIR:'Noir',BLANC:'Blanc'}[self.__trait])

# =============================================================================
class Humain(Player):
    # -------------------------------------------------------------------------
    def __init__(self, nom: str= None):
        self.nom = input("Rosa Rosa Rosam Rosae Rosae Rosā votre identité.\n")

    # -------------------------------------------------------------------------
    def choixCoup(self, unJeu: 'HexVirus', joueur):
        print(unJeu)
        coups = unJeu.listeCoups(joueur)
        str_coups = ' '.join([str(x.position) for x in coups])
        print("Coups jouables : {}".format(str_coups))
        entry = input('Choisissez votre coup\n')
        while entry.strip() not in str_coups.split():
            entry = input('Choisissez votre coup\n')
        print('=' * 35)
        # print('CHoix :', repr(list(filter(lambda x: x.position == int(entry), coups))[0]))
        return unJeu.joue(list(filter(lambda x: x.position == int(entry),coups))[0],joueur)

# =============================================================================
class Aleatoire(Player):
    # -------------------------------------------------------------------------
    def __init__(self):
        self.nom = choice(('MMC le DIEU', 'MMC the God', "AL", "SL", "TLesAmis",
                          "O(n^34)"))

    # -------------------------------------------------------------------------
    def choixCoup(self, unJeu, joueur):
        return unJeu.joue(choice(unJeu.listeCoups(joueur)), joueur)

# =============================================================================
@signature
def partie(jeu: Game, playerA: Player, playerB: Player,
           nbManches: int = 2) -> tuple:
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
    # 1. Print des règles
    jeu.regles()
    #    Initialisation de la Partie

    scoreA, scoreB = 0, 0
    for n in range(nbManches*3):
        scores = manche(jeu, playerA, playerB)
        print("Fin de la manche ! Résultats ? COMPTEZ VOUS MÊME."\
              "\nNon, j'déconne : {} {} - {} {}".format(
            playerA.nom, scores[BLANC], scores[NOIR], playerB.nom
        ))
        if jeu.gagnant(BLANC): scoreA += 1
        else: scoreB += 1
        print('=' * 70)
    print("="*35)
    print("Score de la partiiiiiiiiiie :")
    from time import sleep
    sleep(1)
    print('Suspense !!!')
    sleep(1)
    print('Alors, on attends ?')
    sleep(3)
    print("\n\n{} {} - {} {}".format(playerA.nom, scoreA, scoreB, playerB.nom))
    return (0,0)

# =============================================================================
@signature
def manche(jeu: Game, playerA: Player, playerB: Player) -> tuple:
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
    # 1. Initialiser
    jeu.reset()
    trait = BLANC

    players = {BLANC: playerA, NOIR: playerB}

    # 4. S'arrêter quand la manche est terminée
    while not jeu.finPartie():
        # 2. Faire jouer alternativement
        jeu.configuration = players[jeu.trait](jeu, jeu.trait)
    # 3. Afficher les informations
    scores = jeu.scores()
    return (scores[BLANC], scores[NOIR])

if __name__ == '__main__':
    Antoine = Humain()
    Simon = Aleatoire()
    print('Simon.nom :', Simon.nom)
    p = partie(HexVirus(3,3), Antoine, Simon)