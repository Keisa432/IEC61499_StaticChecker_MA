from typing import List, Tuple, Dict
from pathlib import Path
import glob

class FileIndex:
  """Creates a index of all files with file_extions found in
     search path
  """
  def __init__(self, search_path: str, file_extensions: List[str]) -> None:
    self._search_path = Path(search_path)
    self._file_extensions = file_extensions
    self._file_index = { ext: {} for ext in file_extensions }
    self._collect_files()

  def _collect_files(self) -> None:
    """Collects all files in search_path and stores them in hash tables. Each
       file extension has its own hash table
    """
    for ext in self._file_extensions:
      file_hash = self._file_index[ext]
      for file in self._search_path.rglob(('*' + ext)):
        file_hash[file.stem] = file

  def get_file_by_name(self, file_name: str) -> Path:
    """Get a file by name.

    Arguments:
        file_name {str} -- string representing a file name

    Returns:
        Path -- Path class representing the requeste file
    """
    file_obj = Path(file_name)
    return_obj = None
    try:
        if file_obj.suffix:
          return_obj = self._file_index[file_obj.suffix][file_obj.stem]
        else:
          for _, index in self._file_index.items():
            if file_obj.stem in index:
              return_obj = index[file_obj.stem]
    except KeyError as e:
      print(e)

    return return_obj

  def get_files_with_ext(self, extension: str) -> Dict[str, Path]:
    """Get all files with a specified extension

    Arguments:
        extension {str} -- string representing a file extions to look for e.g. .fbt

    Raises:
        KeyError: if file with this extension could not be found

    Returns:
        Dict[str, Path] -- dictonary containing all files with given extension
    """
    try:
      return self._file_index[extension]
    except KeyError as error:
      raise error
