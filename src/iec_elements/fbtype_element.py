from dataclasses import dataclass, field
from typing import List, Dict, Any
from .base_element import BaseElement

@dataclass
class FbType(BaseElement):
  """Class representing an FBType element
  
  Arguments:
      BaseElement {[type]} -- [description]
  """
  sub_fb: List["FbType"] = field(default_factory=list)
  event_connections: List[Any] = field(default_factory=list)
  data_connections: List[Any] = field(default_factory=list)
  parameters: Dict[str, int] = field(default_factory=dict)