from dataclasses import dataclass, field
from lxml import etree
from typing import List, Dict, Any
from .base_element import BaseElement

def register(parser):
  """Registers parser hook at parser
  
  Arguments:
      parser {IEC parser} -- IEC parser to register hook at
  """
  parser.register_element_hook('FBType', parse_function_block_element)

def parse_function_block_element(doc: etree.ElementTree, file:str):
  """Parse FBType elment from doc.

  This function creates a FunctionBlock instance and returns it.
  
  Arguments:
      doc {etree.ElementTree} -- Elementree representing document
      file {str} -- path to source file of element
  
  Returns:
      [FunctionBlock] -- parsed FunctionBlock element
  """
  root = doc.getroot()
  fb_elem = FunctionBlock(file, root.attrib['Name'],
      root.tag, root.attrib['Namespace'])
  return fb_elem

@dataclass
class FunctionBlock(BaseElement):
  """Class representing an FBType element
  
  Arguments:
      BaseElement {[type]} -- [description]
  """
  sub_fb: List["FunctionBlock"] = field(default_factory=list)
  event_connections: List[Any] = field(default_factory=list)
  data_connections: List[Any] = field(default_factory=list)
  parameters: Dict[str, int] = field(default_factory=dict)