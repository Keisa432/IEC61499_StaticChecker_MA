from dataclasses import dataclass
from lxml import etree

def register(parser):
  """Registers parser hook at parser
  
  Arguments:
      parser {IEC parser} -- IEC parser to register hook at
  """
  parser.register_element_hook('Connection', parse_connection_element, 'FBType')

  def parse_connection_element(doc: etree.ElementTree, fb:['FunctionBlock']):
    """Parse connection elements.

    This function parses all connection elements if present and adds them to the
    passed FunctionBlock fb. This includes Event and DataConnections.

    Arguments:
        doc {etree.ElementTree} -- Elementree representing document
        fb {FunctionBlock} -- Parent FunctionBlock of connection

    Returns:
      [FunctionBlock] -- parsed FunctionBlock element
    """
    pass

@dataclass
class Connection:
  connection_type: str
  conn_from: str
  conn_to: str
  pass
