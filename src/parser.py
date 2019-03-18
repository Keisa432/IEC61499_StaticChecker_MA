#!/usr/bin/python3
import os
from lxml import etree
from lxml import objectify
from xml_elems import DtdXmlObj

iec_xml_elements = dict() #used for xml parsing an metric processing?
dtd_xml_trees = dict() # used for validation after parsing

def get_dtd_files_from_folder(folder):
  """Gets dtd files which are located in folder
  
  Arguments:
    folder {String} -- Path to folder containing dtd files
  
  Returns:
    List -- List containing dtd filenames
  """
  return [ os.path.join(folder, file) for file in os.listdir(folder) if file.endswith('.dtd')]

def element_index_from_dtd_list(dtdList):
  """ Tries to parse the files in dtdList and extracts the XML element
  and adds them to the global element dictionary.
  
  Arguments:
    dtdList {List} -- List containing DTD file paths
  """

  for dtd in dtdList:
    with open(dtd) as source:
      try:
        content = parse_dtd_file(source)
      except Exception as error:
        print(error)
        continue
      add_dtd_content(source.name, content)
      del content

def parse_dtd_file(file):
  return etree.DTD(file)

def add_dtd_content(source=None, dtd_content=None):
  """adds content of dtd file to element repository. A subscope
  for the dtd file is created
  
  Keyword Arguments:
    source {String} -- path to dtd file (default: {None})
    dtd_content {etree.DtdObject} -- parsed dtd file (default: {None})
  
  Raises:
    NameError -- raised if no source path is specified
  """

  if source is None:
    raise NameError('DTD name not defined. Cannot create subscope')
  sub_scope = iec_xml_elements[extract_filename_from_path(source)] = dict()
  dtd_xml_trees[extract_filename_from_path(source)] = dtd_content
  
  if dtd_content is not None:
    for elem in dtd_content.elements():
      obj = DtdXmlObj(elem)
      sub_scope.update({obj.name :obj})


def extract_filename_from_path(path):
  """Gets filename with out extension from path
  
  Arguments:
    path {String} -- Path to file
  
  Returns:
    String -- filename
  """

  return os.path.splitext(os.path.basename(path))[0]


if __name__ == '__main__':
  dtd = get_dtd_files_from_folder('./src/dtd')
  element_index_from_dtd_list(dtd)
#TODO: work out simple metrics that can be counted during parsing
#TODO parse FB xml and match with iec_elements plus verify with dtd
#TODO init routine for parser, create parser class ?
#TODO define metric modules
#TODO toplevel class provides add_stats -> sub module references stats
#TODO open/close functions for reset/finish checking 
#TODO raw metrics: nummber of fbs, fbtypes, ecc states, events, inputs, outputs, ecc vertrices
#TODO further metrics: undefined datatypes, cycles in ecc, not reacheable ecc states, locks in ecc,...
#TODO define how checkers know which elements to check -> list dereived from dtds?
#TODO draw graph, what types are there!!!
#TODO main program searches for sys file -> tries to find referenced fb/types  -> hash files to recognize if something changed? (Would need background timer/thread that checks files and makrs them as "dirty")
#TODO each checker has a check function -> sorted list by prio -> do_check iterates over all checkers
#TODO define output format of msg, write list to file , maybe GUI output?? (super extra) would be useful for graphs
#TODO output would be filename, elment name, type (err/warn), message