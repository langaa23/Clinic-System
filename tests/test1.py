import unittest
from person import Patient, Doctor
from clock import Clock


class TestPerson(unittest.TestCase):

    def test_valid_patient_creation(self):
        patient = Patient("Alice", 101)

        self.assertEqual(patient.name, "Alice")
        self.assertEqual(patient.person_id, 101)
        self.assertEqual(patient.role(), "Patient")

    def test_valid_doctor_creation(self):
        doctor = Doctor("Dr Smith", 102)

        self.assertEqual(doctor.name, "Dr Smith")
        self.assertEqual(doctor.person_id, 102)
        self.assertEqual(doctor.role(), "Doctor")

    def test_empty_name_rejected(self):
        with self.assertRaises(ValueError):
            Patient("   ", 103)

    def test_invalid_name_type_rejected(self):
        with self.assertRaises(TypeError):
            Patient(123, 104)

    def test_invalid_person_id_rejected(self):
        with self.assertRaises(ValueError):
            Patient("Alice", -1)

    def test_float_id_rejected(self):
        with self.assertRaises(TypeError):
            Patient("Alice", 10.5)

    def test_boolean_id_rejected(self):
        with self.assertRaises(TypeError):
            Patient("Alice", True)       

class TestClock(unittest.TestCase):

    def test_valid_clock_creation(self):
        clock = Clock(50)
        self.assertEqual(clock.now(), 50)

    def test_negative_start_time_rejected(self):
        with self.assertRaises(ValueError):
            Clock(-1)

    def test_time_above_limit_rejected(self):
        with self.assertRaises(ValueError):
            Clock(169)

    def test_float_time_rejected(self):
        with self.assertRaises(TypeError):
            Clock(5.5)

    def test_boolean_time_rejected(self):
        with self.assertRaises(TypeError):
            Clock(True)

    def test_advance_clock(self):
        clock = Clock(10)
        clock.advance(5)

        self.assertEqual(clock.now(), 15)

    def test_negative_advance_rejected(self):
        clock = Clock(10)

        with self.assertRaises(ValueError):
            clock.advance(-5)

    def test_float_advance_rejected(self):
        clock = Clock(10)

        with self.assertRaises(TypeError):
            clock.advance(2.5)

    def test_boolean_advance_rejected(self):
        clock = Clock(10)

        with self.assertRaises(TypeError):
            clock.advance(True)

    def test_clock_cannot_exceed_168(self):
        clock = Clock(165)
        clock.advance(10)

        self.assertEqual(clock.now(), 168)
if __name__ == "__main__":
    unittest.main()