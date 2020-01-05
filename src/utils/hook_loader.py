from typing import List
from pathlib import Path
from astroid import modutils
import sys

def register_hooks(parser: "elementparser.ElementParser", path: str) -> None:
  """ Load all modules in the given directory and look for modules
  with a 'register' function. This is used to register parser hooks
  
  Arguments:
      parser {elementparser.ElementParser} -- parser to register hooks
      path {str} -- Path of the directory
  """
  directory = Path(path)
  file_name_list =  _get_module_list(directory)
  for f in file_name_list:
    try:
      module = modutils.load_module_from_file(directory / f)
    except ValueError:
        # empty module name
        continue
    except ImportError as e:
        print(f'Problem importing module {f}: {e}', file=sys.stderr)
    else:
        if hasattr(module, 'register'):
          module.register(parser)



def _get_module_list(directory: Path) -> List[str]:

  if directory.is_dir() is False:
    return []

  modules = [ f.stem
              for f in directory.iterdir()
              if not f.stem.startswith('__') and f.suffix == '.py']

  return modules
