#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# $Id: test_tp01.py,v 1.2 2017/01/25 23:06:47 mmc Exp $
#
# $Log: test_tp01.py,v $
# Revision 1.2  2017/01/25 23:06:47  mmc
# Test Case en cours de développement
#
# Revision 1.1  2017/01/24 18:59:40  mmc
# Initial revision
#

__author__ = "mmc <marc-michel dot corsini at u-bordeaux dot fr>"
__date__ = "22.01.17"
__usage__ = "Test pour tp01 virus"
__version__ = "0.1"
__update__ = "22.01.17"

import os
import sys

from mmcTools import check_property, has_failure, subtest_readonly


class Data(object):
    """ data collector for success/failure """
    def __init__(self):
        self.yes = 0
        self.no = 0
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
    _out = check_property(isinstance(str(getattr(tp, 'Case')(42,tp.NOIR)),
                                     str))
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
    _out = check_property(a.valeur == tp.VIDE)
    a = tp.Case(42, tp.NOIR)
    _out += check_property(a.valeur == tp.NOIR)
    try:
        a = tp.Case(42, tp.COULEURS)
        _out += check_property(a.valeur == tp.VIDE)
    except:
        _out += '.'
    a = tp.Case(42, tp.NOIR)
    _out += check_property(a.valeur == tp.NOIR)
    a.valeur = tp.VIDE
    _out += check_property(a.valeur == tp.VIDE)
    a.valeur = "mmc is watching you"
    _out += check_property(a.valeur == tp.VIDE)
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
    lattr += " estLibre estBloquee"
    lattr = lattr.split()
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
            p = getattr(tp, 'Plateau')(i, j)
            prop = len(p) == p.largeur*p.hauteur + (p.hauteur//2)**2
            _out += check_property(prop)
    return _out

def subtest_Plateau___getitem__():
    _out =''
    return _out

def subtest_Plateau_largeur():
    _out =''
    return _out

def subtest_Plateau_hauteur():
    _out =''
    return _out

def subtest_Plateau_pos2coord():
    _out =''
    return _out

def subtest_Plateau_coord2pos():
    _out =''
    return _out

def subtest_Plateau_configuration():
    _out =''
    return _out

def subtest_Plateau_libres():
    _out =''
    return _out

def subtest_Plateau_jouables():
    _out =''
    return _out

def subtest_Plateau_jouablesTriees():
    _out =''
    return _out

def subtest_Plateau_evaluation():
    _out =''
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
                
    return out


def test_Plateau(collecteur):
    plateau = getattr(tp, "Plateau")
    out = test_Plateau_init(plateau, collecteur)
    test_it = []
    lattr = "__str__ __repr__ __len__ __getitem__ largeur hauteur"
    lattr += " pos2coord coord2pos configuration libres jouables"
    lattr += " jouablesTriees evaluation"
    lattr = lattr.split()
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
        elif not hasattr(tp, nom) : c.no += 1
        else: c.yes += 1
    print(out)

    for test_it in _todo:
        name_test = 'test_'+test_it
        print("{} : {}".format(name_test,eval(name_test)(c)))
    
    
    print("global {res.sum} success {res.yes} fault {res.no}".format(res=c),end=' ')
    if c.sum != 0 : print("rate: {}%".format(round(100*c.yes/c.sum,2)))
    print("optimum: 189")
