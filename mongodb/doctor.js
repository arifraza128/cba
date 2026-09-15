db.doctors.insertOne({
    doctorId: "D001",
    name: "Dr. Rahul Sharma",
    specialization: "Cardiologist",
    experience: 10,
    phone: "9876543210",
    email: "rahul@example.com",
    department: "Cardiology",
    consultationFee: 800
})
db.doctors.insertMany([
    {
        doctorId: "D002",
        name: "Dr. Priya Singh",
        specialization: "Dermatologist",
        experience: 7,
        phone: "9876543211",
        email: "priya@example.com",
        department: "Dermatology",
        consultationFee: 600
    },
    {
        doctorId: "D003",
        name: "Dr. Amit Kumar",
        specialization: "Neurologist",
        experience: 12,
        phone: "9876543212",
        email: "amit@example.com",
        department: "Neurology",
        consultationFee: 1000
    }
])
db.doctors.insertMany([
    {
        doctorId: "D001",
        name: "Dr. Rahul Sharma",
        specialization: "Cardiologist",
        department: "Cardiology",
        experience: 12,
        phone: "9876543210",
        email: "rahul@hospital.com",
        consultationFee: 1000
    },
    {
        doctorId: "D002",
        name: "Dr. Priya Singh",
        specialization: "Dermatologist",
        department: "Dermatology",
        experience: 8,
        phone: "9876543211",
        email: "priya@hospital.com",
        consultationFee: 700
    },
    {
        doctorId: "D003",
        name: "Dr. Amit Kumar",
        specialization: "Neurologist",
        department: "Neurology",
        experience: 15,
        phone: "9876543212",
        email: "amit@hospital.com",
        consultationFee: 1200
    }
])
