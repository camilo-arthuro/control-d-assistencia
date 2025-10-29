from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, create_engine, Session, select
from mqtt_service import start_mqtt
from dotenv import load_dotenv
from .model.UserTic import Alumno, Persona, PersonalServicio, Profesor
from .model.clase import Clase, Fecha, Asignatura, DarAsignatura
import threading
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.on_event("startup")
def startup_event():
    thread = threading.Thread(target=start_mqtt)
    thread.daemon = True
    thread.start()

@app.post("/api/asistencia/alumno", response_model=dict, tags=["CREAR ALUMNO"])
async def crear_alumno(alumno_nuevo: Alumno, db: Session = Depends(get_db)):
    datos_alumno = Alumno.model_validate(alumno_nuevo)
    db.add(datos_alumno)
    db.commit()
    return {"msg":"Alumno/a añadido/a a la DDBB"}

@app.post("/api/asistencia/personal", response_model=dict, tags=["CREAR PERSONAL"])
async def crear_personal(personal_nuevo: Persona, db: Session = Depends(get_db)):
    datos_personal = Persona.model_validate(personal_nuevo)
    db.add(datos_personal)
    db.commit()
    return {"msg":"Personal añadido a la DDBB"}

@app.post("/api/asistencia/asignatura", response_model=dict, tags=["CREAR ASIGNATURA"])
async def crear_asignatura(asignatura_nueva: Asignatura, db: Session = Depends(get_db)):
    datos_asignatura = Asignatura.model_validate(asignatura_nueva)
    db.add(datos_asignatura)
    db.commit()
    return {"msg":"Asignatura añadida a la DDBB"}

@app.post("/api/asistencia/dar-asignatura", response_model=dict, tags=["CREAR ASIGNATURA"])
async def crear_asignatura(profesor_asignado: DarAsignatura, db: Session = Depends(get_db)):
    datos_profesor_asignatura = DarAsignatura.model_validate(profesor_asignado)
    db.add(datos_profesor_asignatura)
    db.commit()
    return {"msg":"Profesor/a asignado/a y añadido/a a la DDBB"}