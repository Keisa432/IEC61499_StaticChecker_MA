from typing import Any
from pathlib import Path
from lxml import etree

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

  def _get_element_hooks(self) -> None:
    pass

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

  def parse(self, file) -> None:
    dtd = self._get_dtd_from_doctype(file)
    for event, element in etree.iterparse(file, events=('start', 'end')):
      if event == 'start':
        try:
          self._validate_xml_element(element, dtd)
        except ValidationError as error:
          self._notify('validationError', error)
        #TODO call parser hook to create element
        #TODO parent stack for context, only add interesting elements to stack e.g. only elements with parser hooks
        print(f'start {element}')
      if event == 'end':
        print(f'end {element}')

  def _get_dtd_from_doctype(self, file_name: str) -> etree.DTD:
    """Gets DTD specified by DOCTYPE of file. Returns None if
    no match is found.
    
    Arguments:
        file_name {str} -- Name of the file that is currently parsed
    
    Returns:
        etree.DTD -- DTD object
    """
    doc_type = self._get_doctype_line(file_name)
    result = [ self._dtds[dtd] for dtd in self._dtds.keys() if dtd in doc_type]
    return result[0] if len(result) > 0 else None

  def _get_doctype_line(self, file_name: str) -> str:
    """Fetches the DOCTYPE line of the file
    
    Arguments:
        file_name {str} -- Name of the file that is currently parsed
    
    Returns:
        str -- DOCTYPE line
    """
    with open(file_name) as file:
      for line in file.readlines():
        if '!DOCTYPE' in line:
          return line
      return None

  def _validate_xml_element(
      self, element: etree._Element,dtd: etree.DTD
  ) -> None:
    """Verifies that element is valid.
    
    Arguments:
        element {etree._Element} -- element to verify
        dtd {etree.DTD} -- DTD used for validation
    
    Raises:
        ValidationError: If element is invalid
    """
    if dtd.validate(element) is False:
      raise ValidationError(str(dtd.error_log.filter_from_errors()[0]))


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