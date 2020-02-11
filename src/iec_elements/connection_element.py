from typing import List
from dataclasses import dataclass
from lxml import etree

def parse_connection_elements(elem: etree.ElementTree, fb:['FunctionBlock']) -> 'FunctionBlock':
  """Parse connection elements.

  This function parses all connection elements if present and adds them to the
  passed FunctionBlock fb. This includes Event and DataConnections.

  Arguments:
      elem {etree.ElementTree} -- Elementree representing document
      fb {FunctionBlock} -- Parent FunctionBlock of connection

  Returns:
    [FunctionBlock] -- parsed FunctionBlock element
  """
  if elem.tag == 'DataConnections':
    add_connection(fb.data_connections, 'Data', elem)
  elif elem.tag == 'EventConnections':
    add_connection(fb.event_connections, 'Event', elem)
  return fb

def add_connection(conn_list: List['Connection'], type: str, 
  elem: etree.ElementTree
) -> 'FunctionBlock':
  for con in elem:
    conn_list.append(Connection(type, con.attrib['Source'], 
        con.attrib['Destination']))

@dataclass
class Connection:
  connection_type: str
  source: str
  dest: str
  pass
