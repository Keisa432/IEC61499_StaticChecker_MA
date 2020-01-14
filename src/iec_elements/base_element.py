from dataclasses import dataclass

@dataclass
class BaseElement:
  """ Class representing an IEC61499 element
  """
  source: str
  name: str
  element_type: str
  namespace: str
