# =============================================================================
'''
Quick description of the file
'''
# =============================================================================
__author__ = 'Simon Lassourreuille & Antoine Loizel'
__version__ = ''
__date__ = '08/02/2017'
__email__ = 'simon.lassourreuille@etu.u-bordeaux.fr'
__email__ += ' & ' + 'antoine.loizel@etu.u-bordeaux.fr'
__status__ = 'Prototype'
# =============================================================================
import sys
if sys.version_info > (3.5):
    from typing import Tuple, Any, NewType

    Color = NewType('Color', Any)
    Coord = NewType('Coord', Tuple[int, int])
# =============================================================================
# Constantes
BLANC = 0
NOIR = 1
VIDE = None
COULEURS = {BLANC: "O", NOIR: "X", VIDE:"_"}
# =============================================================================