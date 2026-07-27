class Patient:
    def __init__(self, patient_id, name, age, appointment_time):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.appointment_time = appointment_time

    def patient_category(self):
        if self.age >= 60:
            return "Senior Citizen"
        elif self.age >= 18:
            return "Adult"
        else:
            return "Child"

    def appointment_session(self):
        if 6 <= self.appointment_time < 12:
            return "Morning"
        elif 12 <= self.appointment_time < 17:
            return "Afternoon"
        elif 17 <= self.appointment_time <= 23:
            return "Evening"
        else:
            return "Invalid Appointment Time"

    def display(self):
        print("\n----- Appointment Details -----")
        print("Patient ID:", self.patient_id)
        print("Patient Name:", self.name)
        print("Age:", self.age)
        print("Category:", self.patient_category())
        print("Appointment Time:", self.appointment_time, ":00")
        print("Session:", self.appointment_session())


patient_id = input("Enter Patient ID: ")
name = input("Enter Patient Name: ")
age = int(input("Enter Age: "))
time = int(input("Enter Appointment Hour (24-hour format): "))

patient = Patient(patient_id, name, age, time)
patient.display()