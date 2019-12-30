#!/usr/bin/python3
from file_index import FileIndex
from elementparser import ElementParser

def main():
  index = FileIndex(r"C:\Users\Dominik\Documents\LStudioProjects\ma_test", ['.sys', '.fbt', '.res'])
  parser = ElementParser(r"C:\Users\Dominik\python\ma\IEC61499_StaticChecker_MA\data\dtd")
  system = index.get_file_by_name('System.sys')
  parser.parse(str(system))

if __name__ == "__main__":
  main()
