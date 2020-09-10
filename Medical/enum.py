from enum import Enum


class Department(Enum):
    General_Physician = "General Physician"
    Dermatology = "Dermatology"
    Paediatrics = "Paediatrics"
    Cardiology = "Cardiology"
    Orthopaedics = "Orthopaedics"
    Psychiatry = "Psychiatry"

    @classmethod
    def choices(cls):
        print(tuple((i.name, i.value) for i in cls))
        return tuple((i.name, i.value) for i in cls)