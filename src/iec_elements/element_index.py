from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class ElementReference:
  """ Reference to an element

  """
  id: str
  reference: Any = field(default=None)
  reference_count: int = field(default=0)

class ElementIndex:
  def __init__(self):
    self._elements = dict()

  def add_to_index(self, data: ElementReference):
    self._elements[data.id] = data

  def get_by_id(self, id):
    entry = None
    if id in self._elements:
      entry = self._elements[id]
    return entry
