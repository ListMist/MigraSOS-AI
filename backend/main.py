from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="MigraSOS AI API",
    description="AI-assisted migraine triage and care navigation backend",
    version="1.0.0"
)

class SymptomInput(BaseModel):
    age: int
    pain_intensity: int
    duration_hours: float
    nausea: int
    vomiting: int
    light_sensitivity: int
    sound_sensitivity: int
    aura: int
    sudden_worst_headache: int
    weakness_numbness: int
    fever: int
    vision_loss: int
    head_injury: int

def check_red_flags(data):
    red_flags = []

    if data.get("sudden_worst_headache") == 1:
        red_flags.append("Sudden worst headache")

    if data.get("weakness_numbness") == 1:
        red_flags.append("Weakness or numbness")

    if data.get("fever") == 1:
        red_flags.append("Fever with headache")

    if data.get("vision_loss") == 1:
        red_flags.append("Vision loss")

    if data.get("head_injury") == 1:
        red_flags.append("Recent head injury")

    if len(red_flags) > 0:
        return {
            "risk_level": "RED",
            "prediction": "Possible emergency headache",
            "confidence": 1.0,
            "red_flags": red_flags,
            "action": "Seek emergency medical care immediately."
        }

    return None

@app.get("/")
def home():
    return {
        "message": "MigraSOS AI backend is running"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "project": "MigraSOS AI"
    }

@app.post("/predict")
def predict_migraine(data: SymptomInput):
    patient_data = data.dict()

    red_flag_result = check_red_flags(patient_data)

    if red_flag_result:
        return red_flag_result

    if data.pain_intensity >= 8 or data.duration_hours >= 24:
        return {
            "risk_level": "YELLOW",
            "prediction": "Possible severe migraine",
            "confidence": 0.82,
            "action": "Consult a doctor or telemedicine service."
        }

    return {
        "risk_level": "GREEN",
        "prediction": "Possible mild/moderate migraine",
        "confidence": 0.76,
        "action": "Track symptoms and follow doctor-approved care plan."
    }