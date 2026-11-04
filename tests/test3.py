import unittest
import tempfile
import os

from clinic import Clinic, AppointmentLog
from clock import Clock
from person import Patient, Doctor, Nurse, Pharmacist


class TestClinic(unittest.TestCase):

    def setUp(self):
        self.clock = Clock(5)
        self.clinic = Clinic(self.clock)

        # Create a temporary log file for each test
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.log_filename = self.temp_file.name
        self.temp_file.close()

        self.logger = AppointmentLog(self.log_filename)
        self.logger.__enter__()

        self.patient = Patient("Alice", 201)
        self.patient2 = Patient("Bob", 202)
        self.doctor = Doctor("Dr Smith", 101)

        self.clinic.register_patient(self.patient, self.logger)
        self.clinic.register_patient(self.patient2, self.logger)
        self.clinic.register_staff(self.doctor, self.logger)

    def tearDown(self):
        self.logger.__exit__(None, None, None)

        if os.path.exists(self.log_filename):
            os.remove(self.log_filename)

    # Registration tests

    def test_patient_registration(self):
        patients = self.clinic.get_patients()

        self.assertIn(self.patient, patients)

    def test_staff_registration(self):
        staff = self.clinic.get_staff_members()

        self.assertIn(self.doctor, staff)

    def test_duplicate_patient_id_rejected(self):
        duplicate = Patient("Charlie", 201)

        with self.assertRaises(ValueError):
            self.clinic.register_patient(duplicate, self.logger)

    def test_duplicate_id_across_patient_and_staff_rejected(self):
        duplicate = Doctor("Dr Jones", 201)

        with self.assertRaises(ValueError):
            self.clinic.register_staff(duplicate, self.logger)

    def test_invalid_patient_type_rejected(self):
        with self.assertRaises(TypeError):
            self.clinic.register_patient("Alice", self.logger)

    def test_invalid_staff_type_rejected(self):
        with self.assertRaises(TypeError):
            self.clinic.register_staff("Dr Smith", self.logger)

    # Appointment booking tests

    def test_successful_appointment_booking(self):
        appointment = self.clinic.book_appointment(
            201, 101, 10, self.logger
        )

        self.assertEqual(appointment.appt_id, 1)
        self.assertEqual(appointment.patient, self.patient)
        self.assertEqual(appointment.staff, self.doctor)
        self.assertEqual(appointment.start_hour, 10)

    def test_appointment_ids_increment(self):
        first = self.clinic.book_appointment(201, 101, 10, self.logger)

        # Use another staff member to avoid a staff scheduling conflict
        nurse = Nurse("Nurse Jane", 102)
        self.clinic.register_staff(nurse, self.logger)

        second = self.clinic.book_appointment(202, 102, 10, self.logger)

        self.assertEqual(first.appt_id, 1)
        self.assertEqual(second.appt_id, 2)

    def test_unknown_patient_rejected(self):
        with self.assertRaises(ValueError):
            self.clinic.book_appointment(999, 101, 10, self.logger)

    def test_unknown_staff_rejected(self):
        with self.assertRaises(ValueError):
            self.clinic.book_appointment(201, 999, 10, self.logger)

    def test_past_appointment_rejected(self):
        with self.assertRaises(ValueError):
            self.clinic.book_appointment(201, 101, 4, self.logger)

    def test_float_start_hour_rejected(self):
        with self.assertRaises((TypeError, ValueError)):
            self.clinic.book_appointment(201, 101, 10.5, self.logger)

    def test_boolean_start_hour_rejected(self):
        with self.assertRaises((TypeError, ValueError)):
            self.clinic.book_appointment(201, 101, True, self.logger)

    def test_start_hour_out_of_range_rejected(self):
        with self.assertRaises(ValueError):
            self.clinic.book_appointment(201, 101, 168, self.logger)

    # Scheduling conflict tests

    def test_patient_cannot_have_overlapping_appointments(self):
        self.clinic.book_appointment(201, 101, 10, self.logger)

        nurse = Nurse("Nurse Jane", 102)
        self.clinic.register_staff(nurse, self.logger)

        with self.assertRaises(RuntimeError):
            self.clinic.book_appointment(201, 102, 10, self.logger)

    def test_patient_can_have_adjacent_appointments(self):
        self.clinic.book_appointment(201, 101, 10, self.logger)

        nurse = Nurse("Nurse Jane", 102)
        self.clinic.register_staff(nurse, self.logger)

        appointment = self.clinic.book_appointment(
            201, 102, 11, self.logger
        )

        self.assertEqual(appointment.start_hour, 11)

    def test_doctor_buffer_blocks_appointments_before_and_after(self):
        self.clinic.book_appointment(201, 101, 10, self.logger)

        nurse = Nurse("Nurse Jane", 102)
        self.clinic.register_staff(nurse, self.logger)

        # The doctor has a 2-hour buffer.
        for hour in (8, 9, 11, 12):
            with self.subTest(hour=hour):
                with self.assertRaises(RuntimeError):
                    self.clinic.book_appointment(
                        202, 101, hour, self.logger
                    )

    def test_doctor_can_be_booked_outside_buffer(self):
        self.clinic.book_appointment(201, 101, 10, self.logger)

        # Three hours after the existing appointment is outside the buffer.
        appointment = self.clinic.book_appointment(
            202, 101, 13, self.logger
        )

        self.assertEqual(appointment.start_hour, 13)

    # Getter tests

    def test_get_patients_returns_a_copy(self):
        patients = self.clinic.get_patients()
        patients.clear()

        self.assertEqual(len(self.clinic.get_patients()), 2)

    def test_get_staff_returns_a_copy(self):
        staff = self.clinic.get_staff_members()
        staff.clear()

        self.assertEqual(len(self.clinic.get_staff_members()), 1)

    def test_get_appointments_returns_a_copy(self):
        self.clinic.book_appointment(201, 101, 10, self.logger)

        appointments = self.clinic.get_appointments()
        appointments.clear()

        self.assertEqual(len(self.clinic.get_appointments()), 1)


if __name__ == "__main__":
    unittest.main()