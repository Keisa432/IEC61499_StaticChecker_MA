#!/usr/bin/python3
from file_index import FileIndex
from elementparser import ElementParser
import iec_elements

def main():
  index = FileIndex(r"C:\Users\Dominik\Documents\LStudioProjects\ma_test", ['.sys', '.fbt', '.res'])
  parser = ElementParser(r"D:\LOYTEC\L-STUDIO 3.0\Studio\data\Schemas")
  linx = index.get_file_by_name('LINX.fbt')
  system = index.get_file_by_name('System.sys')
  iec_elements.initialize(parser)
  parser.parse(str(system))
  parser.parse(str(linx))
  
if __name__ == "__main__":
  main()
