#!/usr/bin/python3
from file_index import FileIndex
from elementparser import ElementParser

def main():
  index = FileIndex(r"C:\Users\Dominik\Documents\LStudioProjects\ma_test", ['.sys', '.fbt', '.res'])
  parser = ElementParser(r"D:\LOYTEC\L-STUDIO 3.0\Studio\data\Schemas")
  system = index.get_file_by_name('LINX.fbt')
  parser.parse(str(system))

if __name__ == "__main__":
  main()
