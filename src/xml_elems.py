#!/usr/bin/python3
from lxml import etree

class DtdXmlObj(dict):
  """
  Storage class for DTD element
  """

  def __init__(self, dtd_elem=None):
    dict.__init__(self)
    self.name = None
    self.type = None
    self.contains = []
    self.attributes = set()

    if dtd_elem is not None:
      self.name = dtd_elem.name
      self.type = dtd_elem.type
      self.__set_obj_data(dtd_elem)

  
  def __set_obj_data(self, dtd_elem):
    if self.type == 'element' and dtd_elem.content is not None:
      self.__get_element_content(dtd_elem.content)
      self.__get_element_attributes(dtd_elem)
    pass
  
  def __get_element_content(self, content):
    """Extracts the sub elements form content. Content is organized as binary tree
    
    Arguments:
      content {Binary Tree} -- Binary tree representing element content
    """
    if content.left:
      self.__get_element_content(content.left)
      if content.left.name is not None and content.left.type == 'element':
        self.contains.append(content.left)

    if content.right:
      self.__get_element_content(content.right)
      if content.right.name is not None and content.right.type == 'element':
        self.contains.append(content.right)

  def __get_element_attributes(self, dtd_elem):
    self.attributes = dtd_elem.attributes()

  def get_content_element(self):
    for elem in self.contains:
      yield elem
  
  def get_attribute(self):
    for att in self.attributes:
      yield att
    
