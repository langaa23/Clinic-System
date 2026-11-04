from clinic import AppointmentLog, Clinic
from clock import Clock
from person import Doctor, MedicalLecturer, Nurse, Patient, Pharmacist, Person

def main():
  # Initializing Clock and Clinic
  clock = Clock(current_time=5)
  clinic = Clinic(clock)

  with AppointmentLog() as logger:
    logger.log("--- Clinic Appointment System by Mazviita and Nomalanga Initialized ---")

    #Register Staff & Patients (Unique IDs)
    doc = Doctor("Dr. Muganhu", 101)
    nurse = Nurse("Nurse Beyonce", 102)
    pharmacist = Pharmacist("Mr. Mabayi", 103)

    # Measure constructor count specifically for MedicalLecturer creation
    count_before = Person.get_constructor_count()
    med_lecturer = MedicalLecturer("Dr. Wadi", 104, "Computer Science")
    count_after = Person.get_constructor_count()
    ml_constructor_runs = count_after - count_before

    clinic.register_staff(doc,logger)
    clinic.register_staff(nurse,logger)
    clinic.register_staff(pharmacist,logger)
    clinic.register_staff(med_lecturer,logger)

    pat1 = Patient("Sarudzai", 201)
    pat2 = Patient("Rudo", 202)
    pat3 = Patient("Tino", 203)
    clinic.register_patient(pat1,logger)
    clinic.register_patient(pat2,logger)
    clinic.register_patient(pat3,logger)

    #Polymorphic Fee Loop (No instanceof / type tags anywhere)
    logger.log("--- Staff Roles and Calculated Fees (P = 10) ---\n")
    P_value = 10
    for s in clinic.get_staff_members():
      logger.log(f"Role: {s.role()} \n Name: {s.name} | Fee: ${s.fee(P_value)}\n")

    # Medical Lecturer Constructor Counter (prints cleanly once)
    logger.log(
        "Person constructor run count for MedicalLecturer:"
        f" {ml_constructor_runs}\n"
    )

    #List Bookings (Allows typing/providing information in a list for bookings)
    logger.log("--- Processing Batch Booking List ---")
    booking_requests = [
        {"patient_id": 201, "staff_id": 101, "start_hour": 10},  # Valid Dr booking
        {"patient_id": 202, "staff_id": 102, "start_hour": 10},  # Valid Nurse booking
        {"patient_id": 203, "staff_id": 103, "start_hour": 12},  # Valid Pharmacist booking
    ]

    for req in booking_requests:
      try:
        appt = clinic.book_appointment(
            req["patient_id"], req["staff_id"], req["start_hour"], logger
        )
        appt.confirm()
        logger.log(f"Confirmed appointment No:{appt.appt_id}\n")
      except Exception as e:
        logger.log(f"Booking request failed: {e}\n")

    #Deliberate Failure Demo: Attempting to violate Doctor's 2-hour buffer
    logger.log("--- Deliberate Failure Test: Buffer Violation ---")
    try:
      print("\n[Deliberate Failure Test]: Attempting buffer violation...")
      # Trying to book doctor at hour 11 (violates 2-hour buffer from hour 10)
      clinic.book_appointment(pat2.person_id, doc.person_id, 11, logger)
    except RuntimeError as e:
      print(f"Caught expected error successfully: {e}\n")

    
    print("\n--- Interactive Booking Mode ---")
    while True:
        try:
            p_input = input("Enter Patient ID (or 'q' to quit): ")
            if p_input.lower() == 'q':
                break
            s_input = input("Enter Staff ID: ").strip()
            hour_input = input("Enter Start Hour (0-167): ").strip()

            appt = clinic.book_appointment(int(p_input), int(s_input), int(hour_input), logger)
            appt.confirm()
            print(f"Successfully booked & confirmed appointment #{appt.appt_id}")
        except (ValueError, TypeError, RuntimeError) as err:
            print(f"Interactive booking error: {err}")


if __name__ == "__main__":
  main()