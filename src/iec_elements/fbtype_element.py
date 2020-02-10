from dataclasses import dataclass, field
from lxml import etree
from typing import List, Dict, Any
from .base_element import BaseElement
from .connection_element import parse_connection_elements

def register(parser):
  """Registers parser hook at parser
  
  Arguments:
      parser {IEC parser} -- IEC parser to register hook at
  """
  parser.register_element_hook('FBType', parse_function_block_element)

def parse_function_block_element(doc: etree.ElementTree):
  """Parse FBType elment from doc.

  This function creates a FunctionBlock instance and returns it.
  
  Arguments:
      doc {etree.ElementTree} -- Elementree representing document
      file {str} -- path to source file of element
  
  Returns:
      [FunctionBlock] -- parsed FunctionBlock element
  """
  sub_elems = ('FBNetwork', 'EventConnections', 'DataConnections')
  root = doc.getroot()
  fb_elem = FunctionBlock(root.base, root.attrib['Name'],
      root.tag, root.attrib['Namespace'])

  for elem in doc.getiterator(sub_elems):
    if 'Connection' in elem.tag:
      parse_connection_elements(elem, fb_elem)
    elif elem.tag == 'FBNetwork':
      pass
    else:
      pass
    
  #TODO params, fbnetwork

  return fb_elem

@dataclass
class FunctionBlock(BaseElement):
  """Class representing an FBType element
  
  Arguments:
      BaseElement {[type]} -- [description]
  """
  functionblock_network: List["FunctionBlock"] = field(default_factory=list)
  event_connections: List[Any] = field(default_factory=list)
  data_connections: List[Any] = field(default_factory=list)
  parameters: Dict[str, int] = field(default_factory=dict)