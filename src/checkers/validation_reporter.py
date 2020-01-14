class ValidationErrorReporter:
  """Class collecting DTD validation errors

    This class stores the validation errors of the parsed XML IEC files.
  """
  def __init__(self):
    self._error_list = []

  def __call__(self, event, error):
    if event == 'validationError':
      self._error_list.append(error)

  def print_error_list(self):
    """ Print all collected errors
    """
    for error in self._error_list:
      print(error)