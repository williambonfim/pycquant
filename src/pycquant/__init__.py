# read version from installed package
from importlib.metadata import version
__version__ = version("pycquant")

from pycquant import QuantStrategies
from pycquant import LoopStrategies
from datahandling import *
from pycquant import MP_LoopStrategies