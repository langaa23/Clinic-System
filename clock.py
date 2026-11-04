class Clock:
  """Custom Clock object to track time as an integer from 0 to 168 (one week).
  ENCAPSULATION:
  Bundles time data and controls access through public methods with validation checks
  """

  def __init__(self, current_time: int = 0):
    if isinstance(current_time,bool) or not isinstance(current_time,int):
      raise TypeError("Time must be an integer.")
    if not (0<= current_time <= 168):
      raise ValueError("Time must be between 0 and 168 hours")
    self._current_time = current_time  #encapsulation state

  def now(self) -> int:
    """Returns the current simulation hour."""
    return self._current_time

  def advance(self, hours: int):
    #encapsulation state modifier with boundary validation.
      if isinstance(hours, bool) or not isinstance(hours, int):
        raise TypeError("Hours must be an integer.")

      if hours < 0:
        raise ValueError("Cannot move time backwards.")

      new_time = self._current_time + hours
      self._current_time = min(new_time, 168)
    