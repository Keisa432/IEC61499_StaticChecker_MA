#!/usr/bin/python3
from checkers import ValidationErrorReporter
from file_index import FileIndex
from elementparser import ElementParser

def main():
  index = FileIndex(r"C:\Users\Dominik\Documents\LStudioProjects\ma_test", ['.sys', '.fbt', '.res'])
  parser = ElementParser(r"D:\LOYTEC\L-STUDIO 3.0\Studio\data\Schemas")
  error_reporter = ValidationErrorReporter()
  parser.attach('validationError', error_reporter)
  linx = index.get_file_by_name('LINX.fbt')
  system = index.get_file_by_name('System.sys')
  parser.register_element_hook('test', None)
  parser.register_element_hook('test1', None, 'test')
  parser.parse(str(system))
  parser.parse(str(linx))
  error_reporter.print_error_list()
  
if __name__ == "__main__":
  main()
