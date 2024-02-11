# read version from installed package
from importlib.metadata import version
__version__ = version("pycquant")

from pycquant import QuantStrategies
from pycquant import LoopSTrategies
from datahandling import *