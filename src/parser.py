#!/usr/bin/python3
import os
from lxml import etree
from lxml import objectify
from xml_elems import DtdXmlObj

iec_xml_elements = dict()

def get_dtd_files_from_folder(folder):
  """Gets dtd files which are located in folder
  
  Arguments:
    folder {String} -- Path to folder containing dtd files
  
  Returns:
    List -- List containing dtd filenames
  """
  return [ os.path.join(folder, file) for file in os.listdir(folder) if file.endswith('.dtd')]

def element_repo_from_dtd_list(dtdList):
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
  if source is None:
    raise NameError('DTD name not defined. Cannot create subscope')
  sub_scope = iec_xml_elements[extract_filename_from_path(source)] = dict()

  if dtd_content is not None:
    for elem in dtd_content.elements():
      obj = DtdXmlObj(elem)
      sub_scope.update({obj.name :obj})


def extract_filename_from_path(path):
  return os.path.splitext(os.path.basename(path))[0]


if __name__ == '__main__':
  dtd = get_dtd_files_from_folder('./src/dtd')
  element_repo_from_dtd_list(dtd)
  print(iec_xml_elements)
  elem = iec_xml_elements['DataType']['DataType']
#TODO: work out simple metrics that can be counted during parsing
#TODO parse FB xml and match with iec_elements plus verify with dtd