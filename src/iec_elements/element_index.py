from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class ElementReference:
  """ Reference to an element

  """
  id: str
  reference: Any = field(default=None)

class ElementIndex:
  def __init__(self):
    pass

  def add_to_index(self):
    pass

  def get_by_id(self, id):
    pass