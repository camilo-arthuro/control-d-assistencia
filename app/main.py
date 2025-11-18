from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, create_engine, Session, select
from .mqtt.mqtt_service import start_mqtt
from dotenv import load_dotenv
from .model.UserTic import Trabajador, Alumno, Profesor, PersonalServicio
from .model.clase import Asignatura
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

# CREATE
@app.post("/api/asistencia/trabajador", response_model=dict, tags=["CREAR TRABAJADOR"])
async def crear_trabajador(trabajador_nuevo: Trabajador, db: Session = Depends(get_db)):
    datos_trabajador = Trabajador.model_validate(trabajador_nuevo)
    db.add(datos_trabajador)
    db.commit()
    if datos_trabajador.rol == "profesor":
        nuevo_profesor=Profesor.model_validate({"id_profesor" : datos_trabajador.id_trabajador})
        db.add(nuevo_profesor)
    elif datos_trabajador.rol == "personal_servicio":
        nuevo_personal=PersonalServicio.model_validate({"id_personal" : datos_trabajador.id_trabajador})
        db.add(nuevo_personal)
    db.commit()
    return {"msg":"Trabajdor creado y añadido a la DDBB"}

@app.post("/api/asistencia/alumno", response_model=dict, tags=["CREAR ALUMNO"])
async def crear_alumno(alumno_nuevo: Alumno, db:Session = Depends(get_db)):
    datos_alumno = Alumno.model_validate(alumno_nuevo)
    db.add(datos_alumno)
    db.commit()
    return {"msg":"Alumno creado y añadido a la DDBB"}

@app.post("/api/asistencia/asignatura", response_model=dict, tags=["CREAR ASIGNATURA"])
async def crear_asignatura(asignatura_nueva: Asignatura, db: Session = Depends(get_db)):
    datos_asignatura = Asignatura.model_validate(asignatura_nueva)
    db.add(datos_asignatura)
    db.commit()
    return {"msg":"Asignatura creada y añadida a la DDBB"}

# READ
@app.get("/api/asistencia/trabajadores", response_model=list[Trabajador], tags=["VER TRABAJADORES"])
async def ver_personas(db: Session = Depends(get_db)):
    query = select(Trabajador)
    datos_personas = db.exec(query).all()
    return [Trabajador.model_validate(persona) for persona in datos_personas]

@app.get("/api/asistencia/alumnos", response_model=list[Alumno], tags=["VER ALUMNOS"])
async def ver_personas(db: Session = Depends(get_db)):
    query = select(Alumno)
    datos_alumnos = db.exec(query).all()
    return [Alumno.model_validate(alumno) for alumno in datos_alumnos]

@app.get("/api/asistencia/asignaturas", response_model=list[Asignatura], tags=["VER ASIGNATURAS"])
async def ver_asignaturas(db: Session = Depends(get_db)):
    query=select(Asignatura)
    datos_asignaturas=db.exec(query).all()
    return [Asignatura.model_validate(asignatura) for asignatura in datos_asignaturas]

# DELETE
@app.delete("/api/asistencia/persona", response_model=dict, tags=["ELIMINAR USUARIO"])
async def eliminar_usuario(id: str, db: Session = Depends(get_db)):
    query=select(Alumno).where(Alumno.id_alumno == id)
    eliminar_usuario= db.exec(query).first()
    if eliminar_usuario:
        db.delete(eliminar_usuario)
        db.commit()
    else:
        query_trabajador=select(Trabajador).where(Trabajador.id_trabajador == id)
        eliminar_trabajador=db.exec(query_trabajador).first()
        if eliminar_trabajador.rol == "profesor":
            query_profesor=select(Profesor).where(Profesor.id_profesor == id)
            eliminar_profesor=db.exec(query_profesor).first()
            db.delete(eliminar_profesor)
            db.commit()
        elif eliminar_trabajador.rol == "personal_servicio":
            query_personal=select(PersonalServicio).where(PersonalServicio.id_personal == id)
            eliminar_personal=db.exec(query_personal).first()
            db.delete(eliminar_personal)
            db.commit()
        db.commit()
    return {"msg":"Usuario eliminado"}
