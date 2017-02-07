#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# $Id: mmcTools.py,v 2.2 2017/01/23 20:25:42 mmc Exp $
#
# $Log: mmcTools.py,v $
# Revision 2.2  2017/01/23 20:25:42  mmc
# Ajout d'une garde sur print(.. flush=True) dans check_property
# Ajout de sys dans les import pour faire le test
#
# Revision 2.1  2016/11/22 11:27:58  mmc
# Ajout de check_property pour faire des assertions controlées
# Ajout de subtest_readonly pour voir si un attribut est en lecture seule
#
# Revision 1.5  2016/06/16 09:28:51  mmc
# Modification en-tete, déplacement du répertoire source de MetaHeuristique
# vers ASD
#

__author__ = "mmc <marc-michel dot corsini at u-bordeaux dot fr>"
__date__ = "18.02.16"
__usage__ = "Boite à outils"
__version__ = "2.1"
__update__ = "22.11.16"

#------- import --------------
import functools
import inspect
import copy
import sys
#-----------------------------
    
def signature(fonction):
    """
        adaptée de Python in Practice by Mark Summerfield 
        modifiée pour la gestion des instances de classes (et du self)
        utilisation des __annotations__ py3.4+

        Pour savoir si vous pouvez utiliser les annotations faites
        dans le shell:

        import platform
        platform.python_version_tuple() 

        >>> import platform
        >>> platform.python_version_tuple() 
        ('3', '4', '5')

    """
    annotations = fonction.__annotations__
    for k in annotations: # gestion du None à la volée
        if annotations[k] is None: annotations[k] = type(None)
    arg_spec = inspect.getfullargspec(fonction)
    has_return = True
    if "return" not in annotations:
        has_return = False
        print ("Warning: missing type for return value in {} signature".format(fonction.__name__))
    if has_return and annotations['return'] == any: has_return = False

    for arg in arg_spec.args + arg_spec.kwonlyargs:
        if arg == 'self': continue
        assert arg in annotations, "missing type for '{}'".format(arg)
    
    @functools.wraps(fonction)
    def enveloppe(*args,**kargs):
        for name, arg in (list(zip(arg_spec.args,args))+
                            list(kargs.items())):
            if name == 'self': continue # self est non typé
            if annotations[name] == any: continue # any: tout est bon
            assert isinstance(arg,annotations[name]),("expected argument {0} of type {1} got {2} in function '{3}'".format(name,annotations[name],type(arg),fonction.__name__))
        _r = fonction(*args,**kargs)
        if has_return:
            assert isinstance(_r,annotations["return"]), ("{2}: expected return of {0} got {1}".format(annotations["return"],type(_r),fonction.__name__))
        return _r
    return enveloppe

class Controle(object):
    """ 
        permet de faire un getter / setter avec verification
        @property_ : propriete a verifie
    """
    def __init__(self,property_=lambda *args: True,once=False,doc=None):
        self.__propriete = property_
        if doc is None:
            if once:  doc = "\nread-only attribute\n"
            else: doc="\nread-write attribute\n"
        self.__doc = doc
        self.__once = once
        self.__lock = False
    @property
    def propriete(self):
        if not self.lock:
            if self.__once: self.__lock = True
        return self.__propriete
    @property
    def doc(self): return self.__doc
    @property
    def lock(self): return self.__lock
        
def checkMe(cls):
    """ decorateur de classe genere des attributs Controle """
    _pref = '_'+cls.__name__
    def make_property(name,att):
        _prive = _pref+"__"+name
        def getMe(self): return getattr(self,_prive)
        def setMe(self,val):
            if hasattr(self,_prive):
                _old = getattr(self,_prive)
            else: _old = None

            if _old is None or not att.lock:
                if att.propriete(name,val): setattr(self,_prive,val)
                else: raise ValueError("cant set {} to {}".format(name,val))
            #die silently for readonly, uncomment if needed
            #else: raise AttributeError("read-only attribute {}".format(name))
        return property(getMe,setMe,doc=att.doc)
    for nm,at in cls.__dict__.items():
        if isinstance(at,Controle):
            setattr(cls,nm,make_property(nm,at))
    return cls

def check_property(p,msg='default',letter='E'):
    """ permet de tester une propriété
    @input p: propriété à tester (vraie ou fausse)
    @input msg: message spécifique en cas d'erreur [defaut=default]
    @input letter: code d'erreur [defaut=E]
    @return letter (echec) . (succes)
    """
    try:
        assert( p ), 'failure %s' % msg
        _ = '.'
    except Exception as _e:
        if sys.version_info >= (3,3): print(_e, flush=True)
        else: print(_e)
        _ = letter
        
    return _

def has_failure(string,sz=1):
    """ vérifie si les sz derniers tests ont échoué """
    sz = min(len(string), sz)
    return string[-sz:] != '.'*sz
    

def subtest_readonly(obj,lattr):
    """ vérification de chaque attribut de obj en lecture seule 
    
    Principe: on sauvegarde dans oldv la valeur courante
    on cherche à affecter un entier, un float, une liste, une chaine
    si ça marche -> erreur + remise en place de l'ancienne valeur

    """
    _s = '' ; _msg =''
    lattr = lattr.split() if isinstance(lattr,str) else lattr
    for att in lattr:
        _msg += "test attribut {}".format(att)
        oldv = copy.deepcopy(getattr(obj,att))
        try:
            _s += '.'
            setattr(obj,att,421)
            if oldv != getattr(obj,att): _s += 'E'
        except Exception:
            _s += '.'
        if has_failure(_s,2):
            _msg += '\n\tavant %s apres %s\n' % (oldv,getattr(obj,att))
            setattr(obj,att,oldv)

        try:
            _s += '.'
            setattr(obj,att,42.24)
            if oldv != getattr(obj,att): _s += 'E'
        except Exception:
            _s += '.'
        if has_failure(_s,2):
            _msg += '\n\tavant %s apres %s\n' % (oldv,getattr(obj,att))
            setattr(obj,att,oldv)
            
        try:
            _s += '.'
            setattr(obj,att,[-1, 0, 1, 'a'])
            if oldv != getattr(obj,att): _s += 'E'
        except Exception:
            _s += '.'
        if has_failure(_s,2):
            _msg += '\n\tavant %s apres %s\n' % (oldv,getattr(obj,att))
            setattr(obj,att,oldv)
            
        try:
            _s += '.'
            setattr(obj,att,"gasp")
            if oldv != getattr(obj,att): _s += 'E'
        except Exception:
            _s += '.'
        if has_failure(_s,2):
            _msg += '\n\tavant %s apres %s\n' % (oldv,getattr(obj,att))
            setattr(obj,att,oldv)
            
        _msg += _s+'\n'
        _s = ''
    return _msg

if __name__ == "__main__":
    print("="*3,"petits tests sur l'utilisation de @signature","="*3)
    @signature
    def fun(x: int,y: int) -> any : return x+y
    try:
        print('fun(3,4) =',end=' ')
        print(fun(3,4))
        print('fun(3.,4) =',end=' ')
        print(fun(3.,4))
    except Exception as _e:
        print("failure\n",_e)
    @signature
    def gun(x: int,y: float = 1.2) -> int: y**x # genere une erreur 
    try:
        print('gun(3)',gun(3))
        print('gun(3.,4)',gun(3.,4))
    except Exception as _e:
        print(_e)

    @checkMe
    class XX:
        a = Controle(lambda _,x: isinstance(x,int))
        b = Controle(lambda _,x: isinstance(x,int),True)
        def __init__(self,v):
            self.a = v
            self.b = v
            
        def __str__(self): return "a = {0.a}, b = {0.b}".format(self)
    

    print("\n\n")
    print("="*3,"petit test sur attribut de la classe",XX.__name__,"="*3)
    u = XX(42)
    print("a",XX.a.__doc__)
    print("b",XX.b.__doc__)    
    print(u)
    print('u.__dict__',u.__dict__)
    print('modification de u.a = 124',end=' ')
    u.a = 124
    print('reussite',u)
    print('modification de u.b = 24',end=' ')
    u.b = 24
    print('echec',u)

    print("\n\n")
    print("="*3,"petit test avec check_property","="*3)
    print(check_property(1 == 1//3, "test idiot //", "X"))
    print(check_property(1 == 1%3, "test idiot modulo", "X"))

    print("\n\n")
    print("="*3,"les attributs sont-ils readonly","="*3)
    print(subtest_readonly(u,'a b a'))
