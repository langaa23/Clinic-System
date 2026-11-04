import unittest
import tempfile
import os

from clinic import AppointmentLog


class TestAppointmentLog(unittest.TestCase):

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.filename = self.temp_file.name
        self.temp_file.close()

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_log_file_opens(self):
        with AppointmentLog(self.filename) as logger:
            self.assertFalse(logger.file.closed)

    def test_message_is_written_to_file(self):
        with AppointmentLog(self.filename) as logger:
            logger.log("Appointment booked successfully.")

        with open(self.filename, "r") as file:
            content = file.read()

        self.assertIn("Appointment booked successfully.", content)

    def test_new_messages_are_appended(self):
        with AppointmentLog(self.filename) as logger:
            logger.log("First appointment.")

        with AppointmentLog(self.filename) as logger:
            logger.log("Second appointment.")

        with open(self.filename, "r") as file:
            content = file.read()

        self.assertIn("First appointment.", content)
        self.assertIn("Second appointment.", content)

    def test_log_file_closes_after_context(self):
        with AppointmentLog(self.filename) as logger:
            log_file = logger.file

        self.assertTrue(log_file.closed)

    def test_log_file_closes_when_exception_occurs(self):
        log_file = None

        with self.assertRaises(RuntimeError):
            with AppointmentLog(self.filename) as logger:
                log_file = logger.file
                raise RuntimeError("Simulated error")

        self.assertTrue(log_file.closed)


if __name__ == "__main__":
    unittest.main()