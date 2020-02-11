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

def parse_function_block_element(doc: etree.ElementTree) -> "FunctionBlock":
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
        parse_fb_network_block(elem, fb_elem)
    #TODO: ECC
  return fb_elem

def parse_fb_network_block(network_elem: etree.ElementTree, 
  parent: "FunctionBlock"
) -> None:
  """Parse FBNetwork elements

  This function parses the FB elements and its Parameters of the FBNetwork. And adds
  them to the functionblock_network list of the parent. 
  
  Arguments:
      fb {etree.ElementTree} -- element to be parsed
      parent {FunctionBlock} -- parent element
  """
  for fb in network_elem.getiterator('FB'):
    sub_block = FbNetworkBlock(fb.base, fb.attrib['Name'],
        fb.tag, fb.attrib['Namespace'])

    for param in fb.getiterator('Parameter'):
      sub_block.parameters[param.attrib['Name']] = param.attrib['Value']

    parent.functionblock_network.append(sub_block)

@dataclass
class FunctionBlock(BaseElement):
  """Class representing an FBType element
  
  Arguments:
      functionblock_network {List[FbNetworkBlock]} -- List of sub function blocks
      event_connections {List[Connection]} -- List of event connections
      data_connections {List[Connection]} -- List of data connections
  """
  functionblock_network: List["FbNetworkBlock"] = field(default_factory=list)
  event_connections: List[Any] = field(default_factory=list)
  data_connections: List[Any] = field(default_factory=list)

@dataclass
class FbNetworkBlock(BaseElement):
  """FBNetwork Element of a Functionblock
  
  Arguments:
      fb_ref {[type]} -- Reference to FBType
      parameters {Dict[str, any]} -- Dictionary of parameters for FB element
  """
  fb_ref: "ElementRefercence" = field(default=None)
  parameters: Dict[str, Any] = field(default_factory=dict)

