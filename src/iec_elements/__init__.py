import utils

def initialize(parser):
  utils.register_hooks(parser, __path__[0])