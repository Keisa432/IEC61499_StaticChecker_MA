from typing import Any
from pathlib import Path
from lxml import etree
from iec_elements import FbTypeElement

class ValidationError(Exception):
  """Thrown by the ElementParser

     This error is raised by the ElementParser if
     it encounters an invalid XML element
  """
  def __init__(self, message):
    super().__init__(message)


class ElementParser:
  """ Parser class for IEC61499 XML files

    Parses XML files containing IEC61499 elements and validates
    them using DTD files.
  """
  def __init__(self, dtd_path: str) -> None:
    self._dtds = {}
    self._element_hooks = {}
    self._current_elem_index = None
    self._observers = {}
    self._parse_dtd_files(dtd_path)

  def _parse_dtd_files(self, dtd_path: str) -> None:
    """Parse all DTD files found under dtd_path
    
    Arguments:
        dtd_path {str} -- path to DTD files
    """
    for file in Path(dtd_path).rglob('**/*.dtd'):
      try:
        self._dtds[file.name] = etree.DTD(str(file))
      except Exception as e:
        print(e)

  def register_element_hook(self, hook_type: str, hook: Any) -> None:
    self._element_hooks[hook_type] = hook

  def attach(self, event: str ,observer: Any) -> None:
    """Attach observer

    Attached observers will be notified if an element is parsed
    successfully or if a invalid element was found
    
    Arguments:
        event {str} -- Event for which the observer will be registered
        observer {Any} -- obsever 
    """
    if event in self._observers:
      self._observers[event].append(observer)
    else:
      self._observers[event] = []
      self._observers[event].append(observer)

  def _notify(self, event:str, data: Any) -> None:
    """Notify all attached observers of event
    
    Arguments:
        event {str} -- Event that occured
        data {Any} -- Data of the event
    """
    if event in self._observers:
      for observer in self._observers[event]:
        observer(event, data)

  def parse(self, file: str) -> None:
    """Parses and validates content of file

    Parses the given file. The content is validated against
    the DTD specified by the !DOCTYPE of the given file. If this
    function encounters invalid elements it emits an 'validationError'
    event. If an element is  parsed it emits a 'parsedElement' event
    
    Arguments:
        file {str} -- file to parse
    """
    doc = etree.parse(file)
    dtd = self._get_dtd_from_doctype(doc.docinfo.doctype)
    try:
      self._validate_xml_tree(doc, dtd)
    except ValidationError as error:
      self._notify('validationError', error)
    self._parse_elems_from_file(doc, file)

  def _parse_elems_from_file(self, doc: etree.ElementTree, file:str) -> None:
    """Prase Elments from given document
    
    Arguments:
        doc {etree.ElementTree} -- document to parse
        file {str} -- path to document thats currently processed
    
    Raises:
        NameError: Raised if an unknown root element is encountered
    """
    if doc.docinfo.root_name == 'System':
      print('parsing system')
    elif doc.docinfo.root_name == 'FBType':
      print('parsing FBType')
      self._create_new_fbtype_element(doc, file)
    else:
      # should not happen but cover anyway
      raise NameError(f'Unknown root element: {doc.docinfo.root}')

  def _create_new_fbtype_element(self, doc: etree.ElementTree, file:str) -> None:
    root = doc.getroot()
    fb_elem = FbTypeElement(file,
        root.attrib['Name'], root.tag, root.attrib['Namespace'])

    for elem in doc.getiterator(('FB', 'Connection')):
      if elem.tag == 'FB':
        fb_elem.sub_fb.append('test')
      elif elem.tag == 'EventConnections':
        fb_elem.event_connections.append('event_conn')
      elif elem.tag == 'DataConnections':
        fb_elem.data_connections.append('data_conn')
      else:
        pass
    self._notify('element', fb_elem)

  def _get_dtd_from_doctype(self, doc_type: str) -> etree.DTD:
    """Gets DTD specified by DOCTYPE of file. Returns None if
       no match is found.
    
    Arguments:
        doc_type {str} -- DOCTYPE line of file
    
    Returns:
        etree.DTD -- DTD object
    """
    result = [ self._dtds[dtd] for dtd in self._dtds.keys() if dtd in doc_type]
    return result[0] if len(result) > 0 else None

  def _validate_xml_tree(
      self, tree: etree._ElementTree, dtd: etree.DTD
  ) -> None:
    """Verifies that element is valid.
    
    Arguments:
        tree {etree._ElementTree} -- tree to verify
        dtd {etree.DTD} -- DTD used for validation
    
    Raises:
        ValidationError: If element is invalid
    """
    if dtd and dtd.validate(tree) is False:
      #TODO convert list to text and rais for each entry
      raise ValidationError(str(dtd.error_log.filter_from_errors()))


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