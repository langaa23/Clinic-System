 
import unittest
from appointment import Appointment, AppointmentStatus
from person import Patient, Doctor


class TestAppointment(unittest.TestCase):

    def setUp(self):
        self.patient = Patient("Alice", 201)
        self.doctor = Doctor("Dr Smith", 101)

    # Construction tests

    def test_valid_appointment_creation(self):
        appt = Appointment(1, self.patient, self.doctor, 10)

        self.assertEqual(appt.appt_id, 1)
        self.assertEqual(appt.patient.name, "Alice")
        self.assertEqual(appt.staff.name, "Dr Smith")
        self.assertEqual(appt.start_hour, 10)
        self.assertEqual(appt.end_hour, 11)
        self.assertEqual(appt.status, AppointmentStatus.PENDING)

    def test_invalid_appointment_id_rejected(self):
        with self.assertRaises(ValueError):
            Appointment(-1, self.patient, self.doctor, 10)

    def test_boolean_appointment_id_rejected(self):
        with self.assertRaises(ValueError):
            Appointment(True, self.patient, self.doctor, 10)

    def test_invalid_patient_rejected(self):
        with self.assertRaises(TypeError):
            Appointment(1, "Alice", self.doctor, 10)

    def test_invalid_staff_rejected(self):
        with self.assertRaises(TypeError):
            Appointment(1, self.patient, "Doctor", 10)

    def test_invalid_start_hour_rejected(self):
        with self.assertRaises(ValueError):
            Appointment(1, self.patient, self.doctor, 168)

    def test_float_start_hour_rejected(self):
        with self.assertRaises(ValueError):
            Appointment(1, self.patient, self.doctor, 10.5)

    def test_boolean_start_hour_rejected(self):
        with self.assertRaises(ValueError):
            Appointment(1, self.patient, self.doctor, True)

    # State transition tests

    def test_initial_status_is_pending(self):
        appt = Appointment(1, self.patient, self.doctor, 10)

        self.assertEqual(appt.status, AppointmentStatus.PENDING)

    def test_pending_appointment_can_be_confirmed(self):
        appt = Appointment(1, self.patient, self.doctor, 10)
        appt.confirm()

        self.assertEqual(appt.status, AppointmentStatus.CONFIRMED)

    def test_confirmed_appointment_cannot_be_confirmed_again(self):
        appt = Appointment(1, self.patient, self.doctor, 10)
        appt.confirm()

        with self.assertRaises(RuntimeError):
            appt.confirm()

    def test_cancelled_appointment_cannot_be_confirmed(self):
        appt = Appointment(1, self.patient, self.doctor, 10)
        appt.cancel(5)

        with self.assertRaises(RuntimeError):
            appt.confirm()

    # Cancellation tests

    def test_pending_appointment_can_be_cancelled(self):
        appt = Appointment(1, self.patient, self.doctor, 10)
        appt.cancel(5)

        self.assertEqual(appt.status, AppointmentStatus.CANCELLED)

    def test_confirmed_appointment_can_be_cancelled_two_hours_before(self):
        appt = Appointment(1, self.patient, self.doctor, 10)
        appt.confirm()
        appt.cancel(8)

        self.assertEqual(appt.status, AppointmentStatus.CANCELLED)

    def test_confirmed_appointment_cannot_be_cancelled_less_than_two_hours_before(self):
        appt = Appointment(1, self.patient, self.doctor, 10)
        appt.confirm()

        with self.assertRaises(RuntimeError):
            appt.cancel(9)

    def test_appointment_cannot_be_cancelled_after_start(self):
        appt = Appointment(1, self.patient, self.doctor, 10)

        with self.assertRaises(RuntimeError):
            appt.cancel(10)

    def test_cancelled_appointment_cannot_be_cancelled_again(self):
        appt = Appointment(1, self.patient, self.doctor, 10)
        appt.cancel(5)

        with self.assertRaises(RuntimeError):
            appt.cancel(6)

    def test_invalid_current_time_type_rejected(self):
        appt = Appointment(1, self.patient, self.doctor, 10)

        with self.assertRaises(ValueError):
            appt.cancel(5.5)

    def test_current_time_out_of_range_rejected(self):
        appt = Appointment(1, self.patient, self.doctor, 10)

        with self.assertRaises(ValueError):
            appt.cancel(169)


if __name__ == "__main__":
    unittest.main()
