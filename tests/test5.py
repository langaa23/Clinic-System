import unittest

from person import (
    Staff, Doctor, Nurse, Pharmacist,
    Lecturer, MedicalLecturer, Patient
)


class TestPolymorphism(unittest.TestCase):

    def test_doctor_fee(self):
        doctor = Doctor("Dr Smith", 101)

        self.assertEqual(doctor.fee(2), 50.0)

    def test_nurse_fee(self):
        nurse = Nurse("Nurse Jane", 102)

        self.assertEqual(nurse.fee(2), 12.0)

    def test_pharmacist_fee(self):
        pharmacist = Pharmacist("Mr James", 103)

        self.assertEqual(pharmacist.fee(2), 5.0)

    def test_doctor_buffer_hours(self):
        doctor = Doctor("Dr Smith", 101)

        self.assertEqual(doctor.buffer_hours(), 2)

    def test_nurse_buffer_hours(self):
        nurse = Nurse("Nurse Jane", 102)

        self.assertEqual(nurse.buffer_hours(), 1)

    def test_pharmacist_buffer_hours(self):
        pharmacist = Pharmacist("Mr James", 103)

        self.assertEqual(pharmacist.buffer_hours(), 0)

    def test_staff_polymorphism(self):
        staff_members = [
            Doctor("Dr Smith", 101),
            Nurse("Nurse Jane", 102),
            Pharmacist("Mr James", 103)
        ]

        for staff in staff_members:
            with self.subTest(role=staff.role()):
                self.assertIsInstance(staff, Staff)
                self.assertIsInstance(staff.fee(2), float)
                self.assertIsInstance(staff.buffer_hours(), int)

    def test_staff_is_abstract(self):
        with self.assertRaises(TypeError):
            Staff("Mr Smith", 101)

    def test_medical_lecturer_inherits_from_doctor(self):
        lecturer = MedicalLecturer(
            "Dr Alice", 104, "Computer Science"
        )

        self.assertIsInstance(lecturer, Doctor)

    def test_medical_lecturer_inherits_from_lecturer(self):
        lecturer = MedicalLecturer(
            "Dr Alice", 104, "Computer Science"
        )

        self.assertIsInstance(lecturer, Lecturer)

    def test_medical_lecturer_properties(self):
        lecturer = MedicalLecturer(
            "Dr Alice", 104, "Computer Science"
        )

        self.assertEqual(lecturer.name, "Dr Alice")
        self.assertEqual(lecturer.person_id, 104)
        self.assertEqual(lecturer.module_name, "Computer Science")
        self.assertEqual(lecturer.role(), "Doctor and Lecturer")

    def test_medical_lecturer_uses_doctor_fee(self):
        lecturer = MedicalLecturer(
            "Dr Alice", 104, "Computer Science"
        )

        self.assertEqual(lecturer.fee(2), 50.0)

    def test_medical_lecturer_uses_doctor_buffer(self):
        lecturer = MedicalLecturer(
            "Dr Alice", 104, "Computer Science"
        )

        self.assertEqual(lecturer.buffer_hours(), 2)


if __name__ == "__main__":
    unittest.main()