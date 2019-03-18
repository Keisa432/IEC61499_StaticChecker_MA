class BaseChecker:
  
  name = "base"
  options = ()
  msgs = {}
  priority = 1
  

  def __init__(self, parser):
    self.parser = parser

  def add_stats(self):
    pass
  
  def register_checker(self):
    pass
  