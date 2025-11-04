from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, create_engine, Session, select
from .mqtt.mqtt_service import start_mqtt
from dotenv import load_dotenv
from .model.UserTic import Alumno, Persona
from .model.clase import Asignatura, DarAsignatura, Clase, AsistenciaAlumno, PrimeraAsistencia
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

@app.post("/api/asistencia/primer-registro", response_model=dict, tags=["PREIMER REGISTRO"])
async def primer_registro(datos_registro: PrimeraAsistencia, db: Session=Depends(get_db)):
    id_asignatura=datos_registro.id_asignatura
    msg= f"Alumno/a añadido/a a la asignatura {id_asignatura}"
    registro=AsistenciaAlumno(
        id_alumno=datos_registro.id_alumno,
        id_clase=datos_registro.id_clase,
        id_asignatura=id_asignatura,
        total_asistencia=0,
        total_faltas=0,
        total_justificadas=0,
        porcentaje_fallas=0
    )
    db.add(registro)
    db.commit()
    return {"msg":msg}

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

@app.post("/api/asistencia/clase", response_model=dict, tags=["CREAR CLASE"])
async def crear_asignatura(clase_nueva: Clase, db: Session = Depends(get_db)):
    datos_clase = Clase.model_validate(clase_nueva)
    db.add(datos_clase)
    db.commit()
    return {"msg":"Clase añadida a la DDBB"}

@app.post("/api/asistencia/dar-asignatura", response_model=dict, tags=["ASIGNAR PROFESOR"])
async def crear_asignatura(profesor_asignado: DarAsignatura, db: Session = Depends(get_db)):
    datos_profesor_asignatura = DarAsignatura.model_validate(profesor_asignado)
    db.add(datos_profesor_asignatura)
    db.commit()
    return {"msg":"Profesor/a asignado/a y añadido/a a la DDBB"}

@app.get("/api/asistencia/alumno/{id}", response_model=Alumno, tags=["READ Alumno by ID"])
async def get_alumno_by_id(id: int, db: Session = Depends(get_db)):
    query=select(Alumno).where(Alumno.id_alumno == id)
    alumno_by_id=db.exec(query).first()
    return Alumno.model_validate(alumno_by_id)

@app.get("/api/asistencia/alumnos", response_model=list[Alumno], tags=["READ All Alumnos"])
async def get_all_alumnos(db: Session = Depends(get_db)):
    query=select(Alumno)
    alumnos=db.exec(query).all()
    return [Alumno.model_validate(alumno) for alumno in alumnos]

@app.get("/api/asistencia/persona/{id}", response_model=Persona, tags=["READ Personal by ID"])
async def get_persona_by_id(id: int, db: Session = Depends(get_db)):
    query=select(Persona).where(Persona.id_persona == id)
    persona_by_id=db.exec(query).first()
    return Persona.model_validate(persona_by_id)

@app.get("/api/asistencia/personal", response_model=list[Persona], tags=["READ All Personal"])
async def get_all_personal(db: Session = Depends(get_db)):
    query=select(Persona)
    personal=db.exec(query).all()
    return [Persona.model_validate(persona) for persona in personal]

