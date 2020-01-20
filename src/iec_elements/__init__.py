import utils
from .fbtype_element import FunctionBlock

def initialize(parser):
  utils.register_hooks(parser, __path__[0])