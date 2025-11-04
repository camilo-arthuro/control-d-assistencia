from sqlmodel import SQLModel, create_engine, Session, select
from dotenv import load_dotenv
from datetime import datetime, date, time
from app.model.UserTic import Alumno, Persona
from app.model.clase import AsistenciaAlumno, Asignatura, Trabaja, Clase, AsistenciaClases
import paho.mqtt.client as mqtt
import os

load_dotenv()

MQTT_HOST = os.getenv("MQTT_HOST")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC")
MQTT_CLIENT_ID = os.getenv("MQTT_CLIENT_ID")

#DDBB
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

def on_connect(client, userdata, flags, rc):
    print("Conectado a HiveMQ broker con codigo:", rc)
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    print(f"Mensaje recibido en {msg.topic}: {msg.payload.decode()}")

    id_usuario = int(msg.payload.decode())
    info_fecha = datetime.now()
    fecha_actual = info_fecha.date()
    hh = info_fecha.hour
    mm = info_fecha.minute
    hora_actual=time(hh,mm)
    jornada = "mañana" if hh < 14 else "tarde"

    with (Session(engine) as db):
        query = select(Alumno).where(Alumno.id_alumno == id_usuario)
        ddbb_alumno = db.exec(query).first()

        if ddbb_alumno:
            query_asignatura = select(Asignatura).where(Asignatura.descripcion == jornada)
            ddbb_asignatura = db.exec(query_asignatura).first()
            if not ddbb_asignatura:
                return print(f"No se encontró asignatura para jornada {jornada}")
            else:
                existe_registro = select(AsistenciaAlumno).where(
                    AsistenciaAlumno.id_alumno == id_usuario
                ).where(AsistenciaAlumno.id_clase == ddbb_asignatura.id_asignatura)
                ddbb_registro= db.exec(existe_registro).first()
                num_asistencia = ddbb_registro.asistio
                num_falta = ddbb_registro.falto
                num_justificantes = ddbb_registro.justificante
                existe_en_clase = select(Clase).where(Clase.nombre == ddbb_alumno.clase)
                ddbb_clase = db.exec(existe_en_clase).first()
                
                registro_alumno = asistencia_alumno(
                    ddbb_alumno.id_alumno,ddbb_clase.id_clase,ddbb_asignatura.id_asignatura,num_asistencia,
                    num_falta,num_justificantes
                )
                ddbb_registro.sqlmodel_update(registro_alumno)
                db.add(registro_alumno)
                db.commit()
                registro_clase= asistencia_clase(
                    ddbb_alumno.id_alumno, ddbb_clase.id_clase, ddbb_asignatura.id_asignatura,
                    fecha_actual,hora_actual
                )
                db.add(registro_clase)
                db.commit()
                return print(f"Asistencia registrada")
        else:
            query = select(Persona).where(Persona.id == id_usuario)
            ddbb_personal = db.exec(query).first()
            if not ddbb_personal:
                return print(f"Tarjeta sin asignar {id_usuario}")
            else:
                registro_personal =asistencia_trabaja(ddbb_personal.id_persona,fecha_actual,hora_actual)
                db.add(registro_personal)
                db.commit()
                return print(f"Asistencia registrada")

def start_mqtt():
    client = mqtt.Client(client_id=MQTT_CLIENT_ID)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_HOST, MQTT_PORT)
    client.loop_forever()

def asistencia_alumno(id_alumno, id_clase, id_asignatura, total_asistencia, total_faltas, total_justificadas):
    registro = AsistenciaAlumno(
        id_alumno=id_alumno,
        id_clase= id_clase,
        id_asignatura=id_asignatura,
        asistio=total_asistencia + 1,
        falto=total_faltas,
        justificante=total_justificadas,
        porcentaje_fallas=(total_faltas * 100) / (total_asistencia + 1 + total_faltas)
    )
    return registro

def asistencia_clase(id_alumno, id_clase, id_asignatura, fecha, hora):
    registro=AsistenciaClases(
        id_alumno=id_alumno,
        id_clase=id_clase,
        id_asignatura=id_asignatura,
        fecha=fecha,
        hora=hora,
        asistio= True
    )
    return registro

def asistencia_trabaja(id_persona, fecha, hora):
    registro=Trabaja(
        id_persona=id_persona,
        fecha=fecha,
        hora=hora,
        zona="itic bcn",
        asistio=True
    )
    return registro
