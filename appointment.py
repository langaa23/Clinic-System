from enum import Enum
from person import Patient, Staff

class AppointmentStatus(Enum):
  PENDING = 1
  CONFIRMED = 2
  CANCELLED = 3

class Appointment:
  """ENCAPSULATION:
  -Encapsulation appointment details rather than allowing direct field modification.
  INVARIANTS:
  - Every appointment has a valid patient and staff member.
  - The appointment lasts exactly one hour.
  - Status must be PENDING, CONFIRMED or CANCELLED.
  - A CANCELLED appointment can never be reactivated.
  - Only a PENDING appointment can be confirmed
  - An appointment cannot be cancelled once it has started.
  - A CONFIRMED appointment cannot be cancelled less than two hours before its start time.
  - Start hour must be between 0 and 167 
  """

  def __init__(
      self, appt_id: int, patient: Patient, staff: Staff, start_hour: int
  ):
    if isinstance(appt_id, bool) or not isinstance(appt_id, int) or appt_id <= 0:
        raise ValueError("Appointment ID must be a positive integer.")

    if not isinstance(patient, Patient):
        raise TypeError("Expected a Patient object.")

    if not isinstance(staff, Staff):
        raise TypeError("Expected a Staff object.")

    if isinstance(start_hour, bool) or not isinstance(start_hour, int):
        raise ValueError("Start hour must be an integer.")

    if not (0 <= start_hour < 168):
        raise ValueError("Start hour must be between 0 and 167.")

    self.__appt_id = appt_id
    self.__patient = patient
    self.__staff = staff
    self.__start_hour = start_hour#encapsulated
    self.__status = AppointmentStatus.PENDING
    
  @property
  def appt_id(self) -> int:
    return self.__appt_id

  @property
  def patient(self) -> Patient:
    return self.__patient

  @property
  def staff(self) -> Staff:
    return self.__staff

  @property
  def start_hour(self) -> int:
    return self.__start_hour

  @property
  def status(self) -> AppointmentStatus:
    return self.__status

  @property
  def end_hour(self) -> int:
    return self.__start_hour + 1

  def confirm(self):
      #controlled state transition method.
      if self.__status != AppointmentStatus.PENDING:
        raise RuntimeError(
            "Only pending appointments can be confirmed."
        )

      self.__status = AppointmentStatus.CONFIRMED
    

  def cancel(self, current_time: int):
    """Enforces cancellation rules:
    - Cancelled appointments can never return.
    - Confirmed appointments cannot be cancelled less than 2 hours before start.
    - No appointment can be cancelled once it has started.
    """
    if isinstance(current_time, bool) or not isinstance(current_time, int):
      raise ValueError("Current time must be an integer.")

    if not (0 <= current_time <= 168):
      raise ValueError("Current time must be between 0 and 168.")
    if self.__status == AppointmentStatus.CANCELLED:
      raise RuntimeError("Appointment is already cancelled.")

    if current_time >= self.__start_hour:
      raise RuntimeError("Cannot cancel an appointment once it has started.")

    if (
        self.__status == AppointmentStatus.CONFIRMED
        and (self.__start_hour - current_time) < 2
    ):
      raise RuntimeError(
          "Confirmed appointments cannot be cancelled less than 2 hours before start."
      )

    self.__status = AppointmentStatus.CANCELLED