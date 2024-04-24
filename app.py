# Fichier app.py
from fastapi import FastAPI, HTTPException, status
from patient import Patient
from typing import List
from pymongo import MongoClient
from pymongo.collection import Collection

app = FastAPI()
client = MongoClient('mongodb://mongodb:27017/')
db = client.patient_db
patients: Collection = db.patients

def extract_ssn_details(ssn: str):
    details = {
        'gender': 'Male' if ssn[0] == '1' else 'Female',
        'year_of_birth': ssn[1:3],
        'month_of_birth': ssn[3:5],
        'department_of_birth': ssn[5:7],
        'country_code': ssn[7:10],
        'birth_index': ssn[10:13]
    }
    return details


@app.get('/patients', response_model=List[Patient])
async def get_patients():
    return list(patients.find({}, {'_id': 0}))

@app.post('/patients', response_model=Patient, status_code=status.HTTP_201_CREATED)
async def create_patient(patient: Patient):
    ssn_details = extract_ssn_details(patient.ssn)
    if ssn_details['department_of_birth'] != '91':
        raise HTTPException(status_code=400, detail="Patients must be born in Essonne (91)")

    if patients.find_one({'ssn': patient.ssn}):
        raise HTTPException(status_code=400, detail="Patient with the same SSN already exists")
    patients.insert_one(patient.dict())
    return patient

@app.get('/patients/{ssn}')
async def get_patient_by_ssn(ssn: str):
    patient = patients.find_one({'ssn': ssn}, {'_id': 0})
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    patient_details = extract_ssn_details(ssn)
    patient.update(patient_details)
    return patient

@app.put('/patients/{ssn}', response_model=Patient)
async def update_patient_by_ssn(ssn: str, patient: Patient):
    result = patients.replace_one({'ssn': ssn}, patient.dict())
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient