#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# $Id: test_tp01.py,v 2.1 2017/02/07 21:01:27 mmc Exp $
#
# $Log: test_tp01.py,v $
# Revision 2.1  2017/02/07 21:01:27  mmc
# Ajout de tests pour Plateau.load
#
# Revision 2.0  2017/02/05 20:21:21  mmc
# jouablesTriees ::DONE:: 984
#
# Revision 1.12  2017/02/05 17:10:18  mmc
# Modification de Plateau___len__ pour gérer les constructeurs douteux
#
# Revision 1.11  2017/02/04 21:59:45  mmc
# Plateau_jouables Plateau_evaluation ::DONE:: 958
#
# Revision 1.10  2017/02/04 21:25:14  mmc
# _Plateau__libres ::DONE:: 945
#
# Revision 1.9  2017/02/04 16:22:39  mmc
# Case_voisins ; Plateau_coord2pos, Plateau_pos2coord
# nbTests = 888
#
# Revision 1.8  2017/02/04 01:01:37  mmc
# Accessible & force ::DONE::
#
# Revision 1.7  2017/02/03 17:32:29  mmc
# Ajout d'un try/except dans test__getitem
# Ajout d'une sortie rapide des tests dans test__getitem
#
# Revision 1.6  2017/02/03 16:16:42  mmc
# Contrôle des variables superflues via subtest_readonly
#
# Revision 1.5  2017/02/03 15:53:34  mmc
# Ajout d'un collecteur pour détecter variable protégée et publique
# A tester sur les property
#
# Revision 1.4  2017/02/02 09:56:45  mmc
# tests Plateau() et p.largeur et p.hauteur
#
# Revision 1.3  2017/01/30 16:25:00  mmc
# Ajout de Case_valeur, Case_estLibre, Case_estBloquee
# En cours Case_voisins
#
# Revision 1.2  2017/01/25 23:06:47  mmc
# Test Case en cours de développement
#
# Revision 1.1  2017/01/24 18:59:40  mmc
# Initial revision
#

__author__ = "mmc <marc-michel dot corsini at u-bordeaux dot fr>"
__date__ = "22.01.17"
__usage__ = "Test pour tp01 virus"
__version__ = "1.01"
__update__ = "07.02.17"


import sys
import os
import random
from numbers import Number
from mmcTools import check_property, has_failure, subtest_readonly

class Data(object):
    """ data collector for success/failure """
    def __init__(self):
        self.yes = 0
        self.no = 0
        self.report = {}
    @property
    def sum(self): return self.yes + self.no


def test_COULEURS(collecteur):
    """ regarde COULEURS VIDE NOIR & BLANC """
    out = ''
    couleur = getattr(tp, 'COULEURS')
    out += check_property(isinstance(couleur, dict))
    prop = set( list(couleur.keys()) ) == set([tp.NOIR, tp.VIDE, tp.BLANC])
    out += check_property(prop)
    out += check_property(tp.VIDE != tp.NOIR)
    out += check_property(tp.VIDE != tp.BLANC)
    out += check_property(tp.BLANC != tp.NOIR)
    collecteur.yes += out.count('.')
    collecteur.no += len(out) - out.count('.')
    return out

def subtest_Case_voisins():
    """ voisins : getter list, setter idx, Case """
    _out =''
    a = tp.Case(0)
    _out += check_property(isinstance(a.voisins, (list, tuple, set)))
    _out += check_property(len(a.voisins) == 0)
    
    vides = tp.Case(0)
    noirs = tp.Case(5,tp.NOIR)
    blancs = tp.Case(10,tp.BLANC)
    vides.voisins = 2, noirs
    _msg = "expect {} found {} voisins"
    _out += check_property(len(vides.voisins) == 1,
                            _msg.format(1,len(vides.voisins)))
    _out += check_property(len(noirs.voisins) == 1,
                            _msg.format(1,len(noirs.voisins)))
    _out += check_property(len(blancs.voisins) == 0, 
                            _msg.format(1,len(blancs.voisins)))
    vides.voisins = 4, blancs
    blancs.voisins = 3, noirs
    _out += check_property(len(vides.voisins) == 2,
                            _msg.format(2,len(vides.voisins)))
    _out += check_property(len(noirs.voisins) == 2,
                            _msg.format(2,len(noirs.voisins)))
    _out += check_property(len(blancs.voisins) == 2,
                            _msg.format(2,len(blancs.voisins)))
    if has_failure(_out, 6):
        print("""
    vide = tp.Case(0)
    noir = tp.Case(5, NOIR)
    blanc = tp.Case(10, BLANC)
    vide.voisins = 2, noir
    vide.voisins = 4, blanc
    blanc.voisins = 3, noir

    chaque Case possède 2 voisins !!!
""")
    return _out

def subtest_Case_voisinage():
    _out = check_property(tp.Case(42).voisinage == {})
    _ = tp.Case(42)
    _.voisinage['mmc'] = 'is whatching you!'
    _out += check_property( _.voisinage.get('mmc',None) is None,
                            "{} is not read-only: {}".format('Case.voisinage',
                                                         _.voisinage))
    return _out

def subtest_Case___str__():
    """ juste une vérification basique """
    try:
        c = tp.Case(0)
        _out = '.'
    except:
        return 'E'
    _out += check_property(isinstance(str(c),str), 'typage de __str__')
    for x in tp.COULEURS:
        c.valeur = x
        _out += check_property(str(c) == tp.COULEURS[c.valeur],
                               "cas de {}".format(x))
    return _out

def subtest_Case___repr__():
    """ juste une vérification basique """
    _out = check_property(isinstance(repr(getattr(tp, 'Case')(42,tp.NOIR)),
                                     str))
    return _out

def subtest_Case_position():
    """ juste une vérification basique """
    _ = tp.Case(132)
    _out = check_property(_.position == 132, "position fausse")
    return _out

def subtest_Case_valeur():
    """ tests simple sur valeur """
    _out =''
    a = tp.Case(23)
    _out = check_property(a.valeur == tp.VIDE,'couleur par défaut','1')
    try:
        a = tp.Case(42, tp.COULEURS)
        _out += check_property(a.valeur == tp.VIDE,
                               'fausse couleur constructeur', '2')
    except:
        _out += '.'
    a = tp.Case(42, tp.NOIR)
    _out += check_property(a.valeur == tp.NOIR,'couleur constructeur','3')
    a.valeur = tp.VIDE
    _out += check_property(a.valeur == tp.VIDE,'maj vraie couleur','4')
    a.valeur = "mmc is watching you"
    _out += check_property(a.valeur == tp.VIDE,'maj fausse couleur','5')
    return _out

def subtest_Case_estLibre():
    """ estLibre si valeur == VIDE """
    _out =''
    a = tp.Case(42)
    _out = check_property(a.estLibre)
    a = tp.Case(23, tp.VIDE)
    _out += check_property(a.estLibre)
    a.valeur = tp.NOIR
    _out += check_property(not a.estLibre)
    a = tp.Case(231, tp.BLANC)
    _out += check_property(not a.estLibre)
    a = tp.Case(23, tp.NOIR)
    _out += check_property(not a.estLibre)
    a.valeur = tp.VIDE
    _out += check_property(a.estLibre)
    
    return _out

def subtest_Case_estBloquee():
    """ si pas libre et toutes cases du voisinage prise """
    _out =''
    # voisinage vide
    a = tp.Case(42)
    _out = check_property(not a.estBloquee,letter='1')
    a.valeur = tp.NOIR
    _out += check_property(a.estBloquee,letter='2')
    # on modifie le voisinage
    tmp = subtest_Case_voisins()
    sz = len(tmp)
    if sz > 0 and not has_failure(tmp,sz):
        # on peut faire les tests
        voisins = [tp.Case(i) for i in range(3)]
        for i,x in enumerate(voisins): a.voisins = i,x
        # tous libres
        _out += check_property(not a.estBloquee, letter='3')
        voisins[0].valeur = tp.BLANC
        _out += check_property(not a.estBloquee, letter='4')
        voisins[1].valeur = tp.NOIR
        _out += check_property(not a.estBloquee, letter='5')
        voisins[2].valeur = tp.NOIR
        _out += check_property( a.estBloquee, letter='6')
        
    
    
    return _out

def subtest_Case_estAccessible():
    """ tests accessibilité """
    _out = ''
    a = tp.Case(23)
    _out += check_property(not a.estAccessible(tp.BLANC),
                           "case VIDE sans voisins")
    _out += check_property(not a.estAccessible(tp.NOIR),
                           "case VIDE sans voisins")
    a.valeur = tp.BLANC
    _out += check_property(not a.estAccessible(tp.BLANC),
                           "case non VIDE sans voisins")
    _out += check_property(not a.estAccessible(tp.NOIR),
                           "case non VIDE sans voisins")
    _test_voisins = subtest_Case_voisins()
    if has_failure(_test_voisins, len(_test_voisins)): return _out
    vides = tp.Case(0)
    noirs = tp.Case(5,tp.NOIR)
    blancs = tp.Case(10,tp.BLANC)
    vides.voisins = 2, noirs
    _out += check_property(not vides.estAccessible(tp.BLANC),
                           "case VIDE sans voisins BLANC")
    
    _out += check_property(vides.estAccessible(tp.NOIR),
                           "case VIDE avec voisin NOIR")
    vides.voisins = 4, blancs
    blancs.voisins = 3, noirs
    _msg = "{0.valeur} {0.estLibre} {0.voisins}".format(vides)
    _msg += " devrait être accessible à {}"
    _out += check_property(vides.estAccessible(tp.BLANC),
                               _msg.format(tp.BLANC))
    _out += check_property(vides.estAccessible(tp.NOIR),
                               _msg.format(tp.NOIR))
    for x in (blancs, noirs):
        _out += check_property(not x.estAccessible(tp.BLANC), "non vide")
        _out += check_property(not x.estAccessible(tp.NOIR), "non vide")

    
    return _out

def subtest_Case_force():
    _out = ''
    a = tp.Case(23)
    _out += check_property(a.force(tp.BLANC) == 0,"case VIDE force 0")
    _out += check_property(a.force(tp.NOIR) == 0,"case VIDE force 0")
    for couleur in (tp.BLANC, tp.NOIR):
        a.valeur = couleur
        _out += check_property(a.force(tp.BLANC) == 0,
                                   "case {} force 0".format(couleur))
        _out += check_property(a.force(tp.NOIR) == 0,
                                   "case {} force 0".format(couleur))

    vide = tp.Case(0)
    blanc = [tp.Case(i, tp.BLANC) for i in range(10,15)]
    noir = [tp.Case(i, tp.NOIR) for i in range(2,7) ]
    _out += check_property(vide.valeur == tp.VIDE,
                           "failed default constructeur")
    _out += check_property(blanc[0].valeur == tp.BLANC,
                            "failed initialisation")
    _out += check_property(noir[0].valeur == tp.NOIR,
                            "failed initialisation")
    
    if has_failure(_out,3): return _out
    for i,x in enumerate(range(2,7,2)):
        vide.voisins = x, noir[i]
        noir[i].voisins = x, blanc[i]
    for i,x in enumerate(range(1,8,2)):
        vide.voisins = x, blanc[i]
    _out += check_property(len(vide.voisinage) == 7,
                        "voisinage found {} expected 7"
                        "".format(len(vide.voisinage)))
    _out += check_property(vide.force(tp.BLANC) == 3,
                        "found {} expected 3".format(vide.force(tp.BLANC)))
    _out += check_property(vide.force(tp.NOIR) == 4,
                        "found {} expected 4".format(vide.force(tp.NOIR)))
    for x in (noir, blanc):
        for y in x:
            _out += check_property(y.force(tp.BLANC) == 0,
                                "non vide force 0 found {}"
                                "".format(y.force(tp.BLANC)))
            _out += check_property(y.force(tp.NOIR) == 0,
                                "non vide force 0 found {}"
                                "".format(y.force(tp.NOIR)))
            if has_failure(_out):
                print("{0} libre? {0.estLibre} accessible Noir? {1}"
                      " accessible Blanc? {2}"
                      "".format(y,y.estAccessible(tp.NOIR),
                                y.estAccessible(tp.BLANC)))

    return _out


def test_Case_init(klass, coll):
    """ vérification du constructeur """
    try:
        vide = getattr(tp, 'VIDE')
        out = '.'
        coll.yes += 1
    except:
        out = 'E'
        coll.no += 1
        return out

    try:
        x = klass(3,vide)
        out += '.'
        coll.yes += 1
    except:
        out += 'E'
        coll.no += 1
        return out

    try:
        x = klass(3)
        out += '.'
        coll.yes += 1
    except:
        out += 'E'
        coll.no += 1

    return out
            
def test_Case(collecteur):
    case = getattr(tp, "Case")
    out = test_Case_init(case, collecteur)
    test_it = []
    lattr = "voisins voisinage __str__ __repr__ position valeur"
    lattr += " estLibre estBloquee estAccessible force"
    lattr = lattr.split()
    badQte, badValues = check_validity('Case', case(0), lattr)
    if badQte > 0:
        _msg = "*** Classe Case ***\n"
        _msg += ("Warning: Votre code contient {} variables interdites\n"
                "".format(badQte))
        _msg += "{}\n".format(badValues)
        _msg += "="*17+"\n"
        collecteur.report['Case'] = _msg
        
    for att in lattr:
        msg = check_property(hasattr(case, att),
                              "Missing {}".format(att))
        if has_failure(msg): collecteur.no += 1
        else:
            collecteur.yes += 1
            test_it.append( att )
        out += msg
    print("Existence Case:",out)
    _ro = [ _ for _ in "voisinage position estLibre estBloquee".split()
            if _ in test_it ]
    b = case(42)
    out = subtest_readonly(b, _ro)
    collecteur.yes += out.count('.')
    collecteur.no += out.count('E')
    print(out) ; out =''
    for meth in test_it:
        sub = 'subtest_Case_'+meth
        tmp = eval(sub)()
        bad = len(tmp) - tmp.count('.')
        collecteur.no += bad
        collecteur.yes += len(tmp) - bad
        if bad > 0:
            print("failure {} : {}".format(sub,tmp))
            return out+tmp
        out += tmp
    return out

def subtest_Plateau___str__():
    """ juste une vérification basique """
    _out = check_property(isinstance(str(getattr(tp, 'Plateau')(3, 5)),
                                     str))
    return _out

def subtest_Plateau___repr__():
    """ juste une vérification basique """
    _out = check_property(isinstance(repr(getattr(tp, 'Plateau')(3, 5)),
                                     str))
    return _out

def subtest_Plateau___len__():
    """ juste une vérification basique """
    _out = ''
    for i in range(1,10):
        for j in range(2,7):
            try:
                p = getattr(tp, 'Plateau')(i, j)
            except Exception as _e:
                print("Erreur création de Plateau({},{}), {}".format(i,j,_e))
                _out += 'E'
                return _out
            prop = len(p) == p.largeur*p.hauteur + (p.hauteur//2)**2
            _out += check_property(prop,"longueur fausse")
    return _out

def subtest_Plateau___getitem__():
    _out =''
    mmc = "0123456789abcdefghijklmnopqrstuvwxyz"
    mmc += "abcdefghijklmnopqrstuvwxyz".upper()
    mmc_sz = len(mmc)
    p = tp.Plateau(5,5)
    _out += check_property( isinstance(p[3], tp.Case), "wrong type", '1')
    _out += check_property( isinstance(p[3,2], tp.Case), "wrong type", '2')
    k = 3
    for i in range(len(p)):
        _out += check_property( p[i].position == i, "wrong pos",mmc[k])
        k = (k+1) % mmc_sz
        if has_failure(_out): break
    if has_failure(_out): return _out
    largeur = [ p.largeur + _ for _ in range(p.hauteur // 2 + 1) ]
    largeur += [p.largeur + _ for _ in range(p.hauteur // 2 - 1, -1, -1)]
    pos = 0
    for i in range(p.hauteur):
        if has_failure(_out): return _out
        for j in range(largeur[i]):
            try:
                _out += check_property(p[i,j].position == pos,
                                    "expected {} for p[{},{}]".format(pos,i,j),
                                    mmc[k])
            except Exception as _e:
                print(_e)
                print("expected {} for p[{},{}]".format(pos,i,j))
                _out += 'E'
                break
            pos += 1
            k = (k+1) % mmc_sz
            
    return _out

def subtest_Plateau_largeur():
    """ largeur c'est le premier paramètre du constructeur """
    _out =''
    klass = tp.Plateau
    for i in range(2,7):
        for j in range(2,13):
            try:
                p = klass(i,j)
            except:
                print("Constructeur Plateau({},{}) failed".format(i,j))
                _out += 'E'
                return _out
            _out += check_property(p.largeur == i,
                                   "largeur expected {} got {}"
                                   "".format(i,p.largeur))
    return _out

def subtest_Plateau_hauteur():
    """ hauteur = 5 si pair, h sinon """
    _out =''
    klass = tp.Plateau
    for i in range(2,7):
        for j in range(2,13):
            try:
                p = klass(i,j)
            except:
                print("Constructeur Plateau({},{}) failed".format(i,j))
                _out += 'E'
                return _out
            prop = p.hauteur == j if j%2 == 1 else p.hauteur == 5
            v = 5 if j%2 == 0 else j
            _out += check_property(prop,
                                   "largeur expected {} got {}"
                                   "".format(v,p.hauteur))
    return _out

def subtest_Plateau_pos2coord():
    """ une position impossible est ignorée """
    _out =''
    louches = [ 'a', '1', .3, (1,2), [3] ]
    p = tp.Plateau(3, 7)
    mmc = 0
    for x in louches:
        mmc += 1
        try:
            _ = p.pos2coord(x)
        except:
            print("pos2coord({}) doit être autorisé".format(repr(x)))
            _out += 'E'
            return _out
        _out += check_property(_ is None, "expect None got {}".format(_),
                               str(mmc))
        if has_failure(_out): return _out
    # maintenant on vérifie le bon calcul
    taille = [p.largeur + _ for _ in range(p.hauteur//2)]
    taille += [p.largeur + _ for _ in range(p.hauteur//2,-1,-1)]
    len_p = len(p)
    total = 0 ;     lig = 0
    for i in range(len_p):
        if total >= taille[lig]:
            total -= taille[lig] ; lig+=1
        val2test = p.pos2coord(i)
        _out += check_property(isinstance(val2test,(tuple,list)),
                               "position {} bad type found {}"
                               "".format(i,type(val2test)))
        if has_failure(_out): return _out
        _out += check_property(len(val2test) == 2,
                               "position {} bad length, expected 2".format(i))
        if has_failure(_out): return _out
        _out += check_property(tuple(val2test) == (lig,total),
                               "position {}: expected {}, found {}"
                               "".format(i, repr((lig,total)), repr(val2test)))
        if has_failure(_out): return _out
        total += 1
    return _out

def subtest_Plateau_coord2pos():
    """ version feignante """
    _out =''
    _essai = subtest_Plateau_pos2coord()
    if not has_failure(_essai, len(_essai)):
        for i in range(3,7):
            for j in range(2,5):
                p = tp.Plateau(i,j)
                for k in range(len(p)):
                    _ = p.coord2pos(* p.pos2coord(k))
                    _out += check_property(k == _,
                                        "expect {} got {} for Plateau({}{})"
                                        "".format(k, _, i, j)
                                           )
                    if has_failure(_out): return _out
                
    #peut-être que c'est fait
    for i in range(3,7):
        for j in range(2,5):
            p = tp.Plateau(i,j)
            for k in range(p.largeur):
                _ = p.coord2pos(0,k)
                _out += check_property(k == _,
                                        "expect {} got {} for Plateau({}{})"
                                        "".format(k, _, i, j)
                                           )
                _ = p.coord2pos(p.hauteur-1, k)
                n = len(p) - p.largeur
                _out += check_property(n+k == _,
                                        "expect {} got {} for Plateau({}{})"
                                        "".format(n+k, _, i, j)
                                           )
                if has_failure(_out,2): return _out
    return _out

def subtest_Plateau_configuration():
    _out =''
    p = tp.Plateau(3,5)
    _out += check_property(len(p) == len(p.configuration),
                            "controle taille",'1')
    _out += check_property(isinstance(p.configuration, (list, tuple)),
                            "controle typage",'2')
    try:
        p.configuration[7].valeur = tp.NOIR
        if p.configuration[7].valeur == tp.VIDE: _out += '.'
        else: _out += '3'
    except:
        _out += '.'

    p[7].valeur = tp.NOIR
    _out += check_property(p[7].valeur == tp.NOIR, "valeur incorrecte", '4')
    _out += check_property(p.configuration[7].valeur == tp.NOIR,
                           "valeur incorrecte", '5')
    return _out

def subtest_Plateau_libres():
    _out =''
    p = tp.Plateau(3,3)
    lattr = "__len__ __iter__ __getitem__ __setitem__".split()
    for att in lattr:
        _out += check_property(hasattr(p.libres, att),
                                   "something missing {}".format(att))
    for i in range(1,5):
        for j in range(3,7):
            p = getattr(tp,'Plateau')(i,j)
            _msg = "all is free expected {0} found {1}  "
            _msg += "Plateau({2.largeur},{2.hauteur})"
            _out += check_property(len(p.libres) == len(p),
                                    _msg.format(len(p.libres), len(p), p))

            w = min(len(p),7)
            _ = random.sample(range(len(p)),w)
            for x in _ :
                if x%2 : p[x].valeur = tp.BLANC
                else: p[x].valeur = tp.NOIR
                    
            _msg2 = "all but {3} are free expected {0} found {1}  "
            _msg2 += "Plateau({2.largeur},{2.hauteur})"
            _out += check_property(len(p.libres) == len(p) -w,
                                    _msg2.format(len(p.libres), len(p)-w, p, w))

            # on remet certaines case vide
            _a = 0
            for k in range(0,w,2): p[_[k]].valeur = tp.VIDE ; _a += 1
            w -=  _a
            _out += check_property(len(p.libres) == len(p) -w,
                                    _msg2.format(len(p.libres), len(p)-w, p, w))
                
    return _out

def subtest_Plateau_jouables():
    _out =''
    _accessibles = subtest_Case_estAccessible()
    if has_failure(_accessibles, len(_accessibles)): return 'E'
    p = tp.Plateau(5,3)
    lattr = "__len__ __iter__ __getitem__ __setitem__".split()
    for att in lattr:
        for pion in (tp.BLANC, tp.NOIR):
            _out += check_property(hasattr(p.jouables(pion), att),
                                   "something missing {} jouables({})"
                                   "".format(att, pion))

            if has_failure(_out): return _out

    for pion in (tp.BLANC, tp.NOIR):
        _out += check_property(len(p.jouables(pion)) == 0, "Plateau vide")
    _msg = """
     B . N . .
    B . N . . .
     . . . . .
    """
    p[0].valeur = tp.BLANC
    p[2].valeur = tp.NOIR
    p[5].valeur = tp.BLANC
    p[7].valeur = tp.NOIR
    for coul in (tp.NOIR, tp.BLANC):
        l = p.jouables(coul)
        for x in l:
            _out += check_property(isinstance(x, tp.Case),
                                    "wrong value Case expected found {}"
                                    "".format(type(x)))
    _pblancs = len(p.jouables(tp.BLANC))
    _pnoirs = len(p.jouables(tp.NOIR))
    _out += check_property(_pblancs == 3,
                               _msg+"\nfound {} expected 3 pour BLANC"
                               "".format(_pblancs) )
    _out += check_property(_pnoirs == 6,
                               _msg+"\nfound {} expected 6 pour NOIR"
                               "".format(_pnoirs) )
    return _out

def subtest_Plateau_jouablesTriees():
    _out =''
    _jouables = subtest_Plateau_jouables()
    _forces = subtest_Case_force()
    if has_failure(_jouables+_forces, len(_jouables+_forces)):
        print("cant test until Plateau_jouables and Case_force"
              "arent bug free")
        return 'E'
    p = tp.Plateau(5,3)
    _msg = """
                 *** Plateau de test ***
     B . N . .
    B . N . . .
     . . . . .
    """
    p[0].valeur = tp.BLANC
    p[2].valeur = tp.NOIR
    p[5].valeur = tp.BLANC
    p[7].valeur = tp.NOIR
    soluce = {tp.NOIR : [2, 1, 0, 0, 0, 0],
              tp.BLANC : [2, 1, 0]}
    for coul in (tp.NOIR, tp.BLANC):
        l = p.jouables(coul)
        m = p.jouablesTriees(coul)
        for x in m:
            _out += check_property(isinstance(x, tp.Case),
                                    "wrong value Case expected found {}"
                                    "".format(type(x)))
        if has_failure(_out, len(p)): return _out
        # test sur la taille
        _out += check_property(len(l) == len(m),
                            "Joueur {}: length of jouables and jouablesTriees"
                            " are different".format(tp.COULEURS[coul]))
        if has_failure(_out):
            print(_msg)
            return _out
        # test sur le contenu
        ls = set([x.position for x in l])
        try:
            ms = set([x.position for x in m])
            _out += '.'
        except Exception as _e:
            print(_e)
            print(_msg)
            return _out+'E'
        _out += check_property(ls == ms,
                            "Joueur {}: jouables and jouablesTriees"
                            " are different {}"
                            "".format(tp.COULEURS[coul],
                                      ls.symmetric_difference(ms)))
        if has_failure(_out):
            print(_msg)
            return _out
        # test sur le résultat attendu "calcul à la main"
        _out += check_property( soluce[coul] == [x.force(coul) for x in m])
        if has_failure(_out):
            print(_msg)
    return _out

def subtest_Plateau_evaluation():
    """ test uniquement le type de retour pour une couleur """
    _out =''
    p = tp.Plateau()
    for pion in (tp.BLANC, tp.NOIR):
        _out = check_property(isinstance(p.evaluation(pion), Number),
                              "bad type {} not a number"
                              "".format(p.evaluation(pion)))
    return _out

def subtest_Plateau_load():
    """ load permet de modifier le plateau dans sa globalité """
    import random
    def check_eq(a,b): return all([x.valeur == y for x,y in zip(a,b)])

    _out = ''
    p = tp.Plateau()
    _out = subtest_Plateau_configuration()
    if has_failure(_out,len(_out)): return _out
    _fake = [tp.VIDE, tp.NOIR, tp.BLANC]*(len(p)//3)
    h = len(p) - len(_fake)
    _fake.extend([tp.NOIR,tp.BLANC][:h])
    _out += check_property(len(p) == len(_fake))
    try:
        r = p.load(_fake)
        _out += check_property(r is None,
                               "None expected found {}".format(type(r)))
    except Exception as _e:
        print(_e)
        _out += 'E'
        return _out
    _out += check_property(check_eq(p.configuration, _fake),
                            "load({})".format(type(_fake)), '1')
    random.shuffle(_fake)
    try:
        r = p.load(tuple(_fake))
        _out += check_property(r is None,
                               "None expected found {}".format(type(r)))
    except Exception as _e:
        print(_e)
        _out += 'E'
        return _out
    _out += check_property(check_eq(p.configuration, _fake),
                            "load({})".format(tuple), '2')
    random.shuffle(_fake)
    try:
        _dico = {i: x for i,x in enumerate(_fake)}
        r = p.load(_dico.values())
        _out += check_property(r is None,
                               "None expected found {}".format(type(r)))
    except Exception as _e:
        print(_e)
        _out += 'E'
        return _out
    _out += check_property(check_eq(p.configuration, _fake),
                            "load({})".format(type(_dico.values())), '3')

    random.shuffle(_fake)
    try:
        _str = ' '.join([str(x) for x in _fake])
        _old = [x.valeur for x in p.configuration]
        r = p.load(_str)
        _out += check_property(r is None,
                               "None expected found {}".format(type(r)))
    except Exception as _e:
        print(_e)
        _out += 'E'
        return _out
    _out += check_property(check_eq(p.configuration, _old),
                            "load({})".format(type(_str)), '4')

    
    _str = [tp.COULEURS[x] for x in _fake]
    try:
        _old = [x.valeur for x in p.configuration]
        r = p.load(_str)
        _out += check_property(r is None,
                               "None expected found {}".format(type(r)))
    except Exception as _e:
        print(_e)
        _out += 'E'
        return _out
    _out += check_property(check_eq(p.configuration, _old),
                            "load({})".format(type(_str)), '5')

    return _out

def test_Plateau_init(klass, coll):
    """ vérification du constructeur """
    out =''
    for i in range(2,5):
        for j in range(2,7):
            try:
                x = klass(i, j)
                out += '.'
                coll.yes += 1
            except:
                out += 'E'
                coll.no += 1

            
        try:
            x = klass(i)
            out += '.'
            coll.yes += 1
        except:
            out += 'E'
            coll.no += 1
    try:
        x = klass()
        out += '.'
        coll.yes += 1
    except:
        print("Failure constructeur Plateau()")
        out += 'E'
        coll.no += 1
    return out


def test_Plateau(collecteur):
    plateau = getattr(tp, "Plateau")
    out = test_Plateau_init(plateau, collecteur)
    test_it = []
    lattr = "__str__ __repr__ __len__ __getitem__ largeur hauteur"
    lattr += " pos2coord coord2pos configuration libres jouables"
    lattr += " jouablesTriees evaluation load"
    lattr = lattr.split()
    badQte, badValues = check_validity('Plateau', plateau(3,5), lattr)
    if badQte > 0:
        _msg = "*** Classe Plateau ***\n"
        _msg += ("Warning: Votre code contient {} variables interdites\n"
                "".format(badQte))
        _msg += "{}\n".format(badValues)
        _msg += "="*17+"\n"
        collecteur.report['Plateau'] = _msg

    for att in lattr:
        msg = check_property(hasattr(plateau, att),
                             "Missing {}".format(att))
        if has_failure(msg): collecteur.no += 1
        else:
            collecteur.yes += 1
            test_it.append( att )
        out += msg
    print("Existence Plateau:", out)
    roAtt = "largeur hauteur configuration libres"
    _ro = [ _ for _ in roAtt.split() if _ in test_it ]
    p = plateau(5)
    out = subtest_readonly(p, _ro)
    collecteur.yes += out.count('.')
    collecteur.no += out.count('E')
    print(out) ; out = ''
    for meth in test_it:
        sub = 'subtest_Plateau_'+meth
        tmp = eval(sub)()
        bad = len(tmp) - tmp.count('.')
        collecteur.no += bad
        collecteur.yes += len(tmp) - bad
        if bad > 0:
            print("failure {} : {}".format(sub,tmp))
            return out+tmp
        out += tmp
    return out

def check_validity(klassname, obj, lattr=[]):
    """ en entrée une classe et les atributs demandés
    en sortie le nombre d'attributs protégés (interdits)
    + le nombre d'attributs publiques (interdits)
    renvoie les interdits
    """
    public = set([])
    protected = set([])
    private = set([])
    klass = getattr(tp,klassname)
    prefix = '_'+klassname+'__'
    forget = len(prefix)
    for x in dir(obj):
        if x.startswith('__'): continue
        if x.startswith(prefix): private.add(x[forget:])
        elif x in lattr: continue
        elif x[0] == '_' and x[1].isalpha() : protected.add(x)
        else: public.add(x)

    for x in public.copy() :
        if callable(getattr(obj,x)): public.discard(x)
    for x in protected.copy() :
        if callable(getattr(obj,x)): public.discard(x)

    badV = set([])
    badV.update(protected, public)

    for val in badV.copy():
        sz = len("test attribut {}".format(val))
        _diagnostic = subtest_readonly(obj,val)
        if _diagnostic.count('E') - val.count('E') == 0: badV.discard(val)
    return len(badV), badV
            
if __name__ == '__main__' :
    if len(sys.argv) == 1:
        param = input("quel est le fichier à traiter ? ")
        if not os.path.isfile(param): ValueError("need a python file")
    else: param = sys.argv[1]

    etudiant = param.split('.')[0]
    c = Data()

    out = check_property(etudiant != '','acces au fichier')
    print("tentative de lecture de {}".format(etudiant))
    tp = __import__(etudiant) # revient à faire import XXX as tp
    _todo = [] # les tests à réaliser

    print("pré-requis")
    cte = "BLANC NOIR VIDE".split()
    tocheck = "COULEURS Case Plateau".split()
    for nom in  cte+tocheck:
        out += check_property(hasattr(tp, nom), "No {} found".format(nom))
        if hasattr(tp, nom) and nom in tocheck:
            _todo.append( nom ) ; c.yes += 1
        elif not hasattr(tp, nom) :
            print("Missing: {}".format(nom))
            c.no += 1
        else: c.yes += 1
    print(out)

    for test_it in _todo:
        name_test = 'test_'+test_it
        print("{} : {}".format(name_test,eval(name_test)(c)))
    
    
    print("global {res.sum} success {res.yes} fault {res.no}"
          "".format(res=c),end=' ')
    if c.sum != 0 : print("rate: {}%".format(round(100*c.yes/c.sum,2)))
    print("optimum: 1001")
    
    for k in c.report: print(c.report[k])
