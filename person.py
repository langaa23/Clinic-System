from abc import ABC, abstractmethod
class Person(ABC):
  """Abstract base class for everyone in the clinic.
  - Uses ABC to define an abstract that cannot be instantiated directly.
  _ Encapsulates private attributes (__name, __id) accessed through properties.
  INVARIANTS:
  - Name cannot be empty or whitespace.
  - ID must be a positive integer (> 0).
  """

  _constructor_counter = 0

  def __init__(self, name: str, person_id: int, **kwargs):
    if not isinstance(name,str):
      raise TypeError("Name must be a string")
    if not name.strip():
      raise ValueError("Name cannot be empty.")
    name = name.strip()
    if isinstance(person_id,bool) or not isinstance(person_id,int):
       raise TypeError("ID must be an integer")
    if person_id <= 0:
      raise ValueError("ID must be a positive integer.")

    self.__name = name #encapsulated
    self.__id = person_id #encapsulated
    Person._constructor_counter += 1
    super().__init__(**kwargs)

  @property  #to validate data
  def name(self) -> str:
    return self.__name

  @property
  def person_id(self) -> int:
    return self.__id

  @abstractmethod
  def role(self) -> str:
    pass

  @classmethod
  def get_constructor_count(cls) -> int:
    return cls._constructor_counter


class Patient(Person):
  """Represents a clinic patient.
  INHERITANCE and POLYMORPHISM
  Inherits from Person and implements the abstract role() method.
  """
  def role(self) -> str:
    return "Patient"

class Staff(Person):
  """Abstract staff member defining polymorphic fees and buffer hours.
  ABSTRACTION and INHERITANCE
  abstracts class extending Person for specific behaviors.
  """

  @abstractmethod
  def fee(self, p_value: int) -> float:
    pass

  @abstractmethod
  def buffer_hours(self) -> int:
    pass


class Doctor(Staff):
  """Doctor staff member: fee = 40 + 5 * (P mod 5), buffer = 2 hours.
  INHERITANCE and POLYMORPHISM:
  Inherits from staff and provides polymorphic implementations for fee calculation and buffer hours.
  """
  def role(self) -> str:
    return "Doctor"

  def fee(self, p_value: int) -> float:
    return float(40 + 5 * (p_value % 5))

  def buffer_hours(self) -> int:
    return 2


class Nurse(Staff):
  """Nurse staff member: fee = 10 + (P mod 3), buffer = 1 hour.
  Implements polymorphic fee and buffer rules specific to nurses.
  """
  def role(self) -> str:
    return "Nurse"

  def fee(self, p_value: int) -> float:
    return float(10 + (p_value % 3))

  def buffer_hours(self) -> int:
    return 1


class Pharmacist(Staff):
  """Pharmacist staff member: fee = 5, buffer = 0 hours.
  implements polymorphic fee and buffer rules specific to pharmacists.
  """

  def role(self) -> str:
    return "Pharmacist"

  def fee(self, p_value: int) -> float:
    return 5.0

  def buffer_hours(self) -> int:
    return 0


class Lecturer:
  """Mix-in class representing a lecturer."""
  def __init__(self, module_name: str, **kwargs):
    if not module_name or not module_name.strip():
      raise ValueError("Module name cannot be empty.")
    self.__module_name = module_name
    super().__init__(**kwargs)
    
  @property
  def module_name(self) -> str:
    return self.__module_name


class MedicalLecturer(Doctor, Lecturer):
  """Multiple inheritance class combining Doctor and Lecturer.
  Using super() calls to prevent duplicate base initialization.
  """
  def __init__(self, name: str, person_id: int, module_name: str):
    super().__init__(name=name, person_id=person_id, module_name=module_name)

  def role(self) -> str:
    return "Doctor and Lecturer"