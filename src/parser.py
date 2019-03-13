#!/usr/bin/python3
import os
from lxml import etree
from lxml import objectify

#add class functionality to dict
#http://code.activestate.com/recipes/573463-converting-xml-to-dictionary-and-back/
class XmlDictObject(dict):
    """
    Adds object like functionality to the standard dictionary.
    """

    def __init__(self, initdict=None):
        if initdict is None:
            initdict = {}
        dict.__init__(self, initdict)
    
    def __getattr__(self, item):
        return self.__getitem__(item)
    
    def __setattr__(self, item, value):
        self.__setitem__(item, value)
    
    def __str__(self):
        if self.has_key('_text'):
            return self.__getitem__('_text')
        else:
            return ''

    @staticmethod
    def Wrap(x):
        """
        Static method to wrap a dictionary recursively as an XmlDictObject
        """

        if isinstance(x, dict):
            return XmlDictObject((k, XmlDictObject.Wrap(v)) for (k, v) in x.iteritems())
        elif isinstance(x, list):
            return [XmlDictObject.Wrap(v) for v in x]
        else:
            return x

    @staticmethod
    def _UnWrap(x):
        if isinstance(x, dict):
            return dict((k, XmlDictObject._UnWrap(v)) for (k, v) in x.iteritems())
        elif isinstance(x, list):
            return [XmlDictObject._UnWrap(v) for v in x]
        else:
            return x
        
    def UnWrap(self):
        """
        Recursively converts an XmlDictObject to a standard dictionary and returns the result.
        """

        return XmlDictObject._UnWrap(self)

def getDtdFilesFromFolder(folder):
  """Gets dtd files which are located in folder
  
  Arguments:
    folder {String} -- Path to folder containing dtd files
  
  Returns:
    List -- List containing dtd filenames
  """

  return [ os.path.join(folder, file) for file in os.listdir(folder) if file.endswith('.dtd')]

def parseDtdFiles(dtdList):
  for dtd in dtdList:
    with open(dtd) as source:
      tree = etree.DTD(source)
      for elem in tree.elements():
        print(elem)
        for k in elem.content:
          print ('content of' + elem.name + 'is' + k)
  pass

dtd = getDtdFilesFromFolder('./dtd')
parseDtdFiles(dtd)
#dtd as object like dict, maybe not needed -> simple dict with dtd elements as entries? TODO workout parse function
# dict :
#     {
#     [test]: (name of dtd file as key)
#           { 
#             [sub]: dtd elem (first element of test.dtd file)
#           }
#     [nextDtd]:
#     }
#dtd strat, parse xml get right dtd verify then parse known elements to dict and keep simple metric counters
#TODO: work out simple metrics that can be counted during parsing