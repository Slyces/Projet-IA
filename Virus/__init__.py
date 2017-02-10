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
from Virus.Structures import Case, Plateau, BLANC, NOIR, VIDE, COULEURS
if sys.version_info > (3, 5):
    from typing import Tuple, Any, NewType
    Color = NewType('Color', Any)
    Coord = NewType('Coord', Tuple[int, int])
# =============================================================================