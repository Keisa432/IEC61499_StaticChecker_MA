from typing import Any
from pathlib import Path
from lxml import etree
from iec_elements import FunctionBlock

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
    self._parse_elems_from_file(doc)

  def _parse_elems_from_file(self, doc: etree.ElementTree) -> None:
    """Prase Elments from given document
    
    Arguments:
        doc {etree.ElementTree} -- document to parse
        file {str} -- path to document thats currently processed
    
    Raises:
        NameError: Raised if an unknown root element is encountered
    """
    elem: FunctionBlock = None
    if doc.docinfo.root_name in self._element_hooks:
      self._element_hooks[doc.docinfo.root_name](doc)
    else:
      pass
    self._notify('element', elem)

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
#TODO define metric modules
#TODO toplevel class provides add_stats -> sub module references stats
#TODO open/close functions for reset/finish checking 
#TODO raw metrics: nummber of fbs, fbtypes, ecc states, events, inputs, outputs, ecc vertrices
#TODO further metrics: undefined datatypes, cycles in ecc, not reacheable ecc states, locks in ecc,...
#TODO each checker has a check function -> sorted list by prio -> do_check iterates over all checkers
#TODO define output format of msg, write list to file , maybe GUI output?? (super extra) would be useful for graphs
#TODO output would be filename, elment name, type (err/warn), message
#TODO how to handle incomplete types