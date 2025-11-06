from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, create_engine, Session, select
from .mqtt.mqtt_service import start_mqtt
from dotenv import load_dotenv
from .model.UserTic import Persona, Alumno, Profesor, PersonalServicio
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

@app.post("/api/asistencia/persona", response_model=dict, tags=["CREAR USUARIO"])
async def crear_usuario(usuario_nuevo: Persona, db: Session = Depends(get_db)):
    datos_usuario = Persona.model_validate(usuario_nuevo)
    db.add(datos_usuario)
    db.commit()
    if datos_usuario.rol == "alumno":
        nuevo_alumno=Alumno.model_validate({"id_alumno" : datos_usuario.id_persona})
        db.add(nuevo_alumno)
    elif datos_usuario.rol == "profesor":
        nuevo_profesor=Profesor.model_validate({"id_profesor" : datos_usuario.id_persona})
        db.add(nuevo_profesor)
    elif datos_usuario.rol == "personal_servicio":
        nuevo_personal=PersonalServicio.model_validate({"id_personal" : datos_usuario.id_persona})
        db.add(nuevo_personal)
    db.commit()
    return {"msg":"Usuario creado y añadido a la DDBB"}

@app.post("/api/asistencia/asignatura", response_model=dict, tags=["CREAR ASIGNATURA"])
async def crear_asignatura(asignatura_nueva: Asignatura, db: Session = Depends(get_db)):
    datos_asignatura = Asignatura.model_validate(asignatura_nueva)
    db.add(datos_asignatura)
    db.commit()
    return {"msg":"Asignatura creada y añadida a la DDBB"}

@app.get("/api/asistencia/personas", response_model=list[Persona], tags=["VER USUARIOS"])
async def ver_personas(db: Session = Depends(get_db)):
    query = select(Persona)
    datos_personas = db.exec(query).all()
    return [Persona.model_validate(persona) for persona in datos_personas]

@app.get("/api/asistencia/asignaturas", response_model=list[Asignatura], tags=["VER ASIGNATURAS"])
async def ver_asignaturas(db: Session = Depends(get_db)):
    query=select(Asignatura)
    datos_asignaturas=db.exec(query).all()
    return [Asignatura.model_validate(asignatura) for asignatura in datos_asignaturas]

@app.delete("/api/asistencia/persona", response_model=dict, tags=["ELIMINAR USUARIO"])
async def eliminar_usuario(id: int, db: Session = Depends(get_db)):
    query=select(Persona).where(Persona.id_persona == id)
    eliminar_usuario= db.exec(query).first()
    if eliminar_usuario:
        if eliminar_usuario.rol == "alumno":
            query_alumno=select(Alumno).where(Alumno.id_alumno == id)
            eliminar_alumno=db.exec(query_alumno).first()
            db.delete(eliminar_alumno)
        elif eliminar_usuario.rol == "profesor":
            query_profesor=select(Profesor).where(Profesor.id_profesor == id)
            eliminar_profesor=db.exec(query_profesor).first()
            db.delete(eliminar_profesor)
        elif eliminar_usuario.rol == "personal_servicio":
            query_personal=select(PersonalServicio).where(PersonalServicio.id_personal == id)
            eliminar_personal=db.exec(query_personal).first()
            db.delete(eliminar_personal)
        db.commit()
    db.delete(eliminar_usuario)
    db.commit()
    return {"msg":"Usuario eliminado"}