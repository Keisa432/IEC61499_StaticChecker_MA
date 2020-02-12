#!/usr/bin/python3
import iec_elements
from checkers import ValidationErrorReporter
from file_index import FileIndex
from elementparser import ElementParser
from iec_elements import ElementReference, ElementIndex

element_index = ElementIndex()

def add_to_element_index(event, data) -> None:
  ref = ElementReference('.'.join([data.namespace,data.name]), data, 1)
  element_index.add_to_index(ref)

def main():
  index = FileIndex(r"C:\Users\Dominik\Documents\LStudioProjects\ma_test", ['.sys', '.fbt', '.res'])
  parser = ElementParser(r"D:\LOYTEC\L-STUDIO 3.0\Studio\data\Schemas")
  error_reporter = ValidationErrorReporter()
  parser.attach('validationError', error_reporter)
  parser.attach('element', add_to_element_index)
  iec_elements.initialize(parser)
  for file in index:
     parser.parse(str(file))
  error_reporter.print_error_list()
  
if __name__ == "__main__":
  main()
