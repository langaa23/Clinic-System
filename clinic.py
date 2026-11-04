from appointment import Appointment, AppointmentStatus
from clock import Clock
from person import Patient, Staff

class AppointmentLog:
  """ENCAPSULATION: to encapsulate file opening and closing safely.
  Context manager guaranteeing the log file opens and closes exactly once."""

  def __init__(self, filename="appointment_log.txt"):
    self.filename = filename
    self.file = None

  def __enter__(self):
    self.file = open(self.filename, "a")
    print("[log] opened")
    return self

  def __exit__(self, exc_type, exc_val, exc_tb):
    if self.file:
      self.file.close()
      print("[log] closed")

  def log(self, message: str):
    if self.file:
      self.file.write(message + "\n")
    print(f"LOG -> {message}")

class Clinic:
  """ENCAPSULATION: encapsulates internal records and protects againsts external modifications.
  INVARIANTS:
  - All patient IDs and staff IDs registered in the clinic must be globally unique.
  - No staff member or patient may have two non-cancelled appointments at conflicting hours (respecting staff buffer requirements).
  - All internal dictionaries and lists are protected via defensive copying.
  - Every action is logged through the appointment log context.
  """

  def __init__(self, clock: Clock):
    self.__clock = clock
    self.__patients = {}
    self.__staff_members = {}
    self.__appointments = {}
    self.__next_appt_id = 1

  def register_patient(self, patient: Patient,logger:AppointmentLog):
    if not isinstance(patient,Patient):
      msg = "Expected a Patient object."
      logger.log(f"Failed to register patient: {msg}")
      raise TypeError(msg)
      
    
    person_id = patient.person_id

    if person_id in self.__patients or person_id in self.__staff_members:
        msg = "Person ID must be globally unique."
        logger.log(f"Failed to register patient: {msg}")
        raise ValueError(msg)

    self.__patients[person_id] = patient

  def register_staff(self, staff: Staff,logger: AppointmentLog):
    if not isinstance(staff,Staff):
          msg = "Expected a Staff object."
          logger.log(f"Failed to register staff: {msg}")
          raise TypeError(msg)
    
    person_id = staff.person_id

    if person_id in self.__patients or person_id in self.__staff_members:
        msg = "Person ID must be globally unique."
        logger.log(f"Failed to register staff: {msg}")
        raise ValueError(msg)

    self.__staff_members[person_id] = staff

  def get_patients(self):
    """Returns a copied list to prevent internal list leakage."""
    return list(self.__patients.values())

  def get_staff_members(self):
    """Returns a copied list of staff members."""
    return list(self.__staff_members.values())

  def get_appointments(self):
    """Returns a copied list of appointments."""
    return list(self.__appointments.values())

  def book_appointment(
      self, patient_id: int, staff_id: int, start_hour: int, logger: AppointmentLog
  ) -> Appointment:
    """POLYMORPHISM: calls staff.buffer_hours() without inspecting staff instances treating all uniformly
    Books an appointment enforcing buffer rules using polymorphic staff.buffer_hours()."""
    if isinstance(start_hour, bool) or not isinstance(start_hour, int):
      msg = "Start hour must be an integer."
      logger.log(f"FAILED book: {msg}")
      raise TypeError(msg)

    if not (0 <= start_hour < 168):
      msg = "Start hour must be between 0 and 167."
      logger.log(f"FAILED book: {msg}")
      raise ValueError(msg)
    
    current_time = self.__clock.now()

    if start_hour < current_time:#checking that the time set is greater than or equal to current time
      msg = "Cannot book an appointment in the past."
      logger.log(f"Failed booking attempt: {msg}")
      raise ValueError(msg)

    #validating that the specified id exists in logging
    if patient_id not in self.__patients or staff_id not in self.__staff_members:
      msg = f"FAILED book: Invalid patient or staff ID."
      logger.log(msg)
      raise ValueError(msg)

    patient = self.__patients[patient_id]
    staff = self.__staff_members[staff_id]
    buffer = staff.buffer_hours()

    # Check for schedule conflicts considering buffer requirements
    for appt in self.__appointments.values():
      if appt.status != AppointmentStatus.CANCELLED:
        
        # Check Staff conflict with buffer
        if appt.staff.person_id == staff_id:
          if abs(appt.start_hour - start_hour) <= buffer:
            msg = f"FAILED book staff #{staff_id}: buffer time conflict."
            logger.log(msg)
            raise RuntimeError(msg)

        # Check Patient conflict (patients cannot overlap at the exact same hour)
        if appt.patient.person_id == patient_id:
          if appt.start_hour < start_hour + 1 and start_hour < appt.end_hour:
            msg = f"FAILED book patient #{patient_id}: time slot overlap."
            logger.log(msg)
            raise RuntimeError(msg)
          
    appt_id = self.__next_appt_id
    self.__next_appt_id += 1
    new_appt = Appointment(appt_id, patient, staff, start_hour)
    self.__appointments[appt_id] = new_appt

    logger.log(
        f"SUCCESS book #{appt_id}: Patient {patient.name} with"
        f" {staff.role()} {staff.name} at hour {start_hour}."
    )
    return new_appt

  def cancel_appointment(self, appt_id: int, logger: AppointmentLog):
    """Cancels an appointment safely through its state machine rules."""
    if appt_id not in self.__appointments:
      msg = f"FAILED cancel #{appt_id}: Appointment does not exist."
      logger.log(msg)
      raise KeyError(msg)

    appt = self.__appointments[appt_id]
    try:
      appt.cancel(self.__clock.now())
      logger.log(f"SUCCESS cancel #{appt_id}")
    except RuntimeError as e:
      logger.log(f"FAILED cancel #{appt_id}: {str(e)}")
      raise 