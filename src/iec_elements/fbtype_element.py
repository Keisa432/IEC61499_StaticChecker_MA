from dataclasses import dataclass, field
from typing import List, Any
from .base_element import BaseElement

@dataclass
class FbTypeElement(BaseElement):
  """Class representing an FBType element
  
  Arguments:
      BaseElement {[type]} -- [description]
  """
  sub_fb: List["FbTypeElement"] = field(default_factory=list)
  event_connections: List[Any] = field(default_factory=list)
  data_connections: List[Any] = field(default_factory=list)