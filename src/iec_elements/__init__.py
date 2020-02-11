import utils
from .fbtype_element import FunctionBlock
from .element_index import ElementReference

def initialize(parser):
  utils.register_hooks(parser, __path__[0])