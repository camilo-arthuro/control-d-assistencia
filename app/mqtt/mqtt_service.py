from sqlalchemy.exc import IntegrityError
from sqlmodel import SQLModel, create_engine, Session, select
from dotenv import load_dotenv
from datetime import datetime, date, time
from app.model.users import Alumno, Trabajador
from app.model.academics import RegistroHorario_T, Asiste, Horario_T
import paho.mqtt.client as mqtt
import os
import json

load_dotenv()

# AWS IoT MQTT
AWS_IOT_ENDPOINT = os.getenv("AWS_IOT_ENDPOINT")
AWS_IOT_PORT = int(os.getenv("AWS_IOT_PORT", 8883))
#AWS_IOT_TOPIC = os.getenv("AWS_IOT_TOPIC")
AWS_IOT_SUB_TOPIC = os.getenv("AWS_IOT_SUB_TOPIC", "rfid/tag")
AWS_IOT_PUB_TOPIC = os.getenv("AWS_IOT_PUB_TOPIC", "rfid/led")
AWS_IOT_CLIENT_ID = os.getenv("AWS_IOT_CLIENT_ID")
AWS_IOT_CERT = os.getenv("AWS_IOT_CERT")
AWS_IOT_KEY = os.getenv("AWS_IOT_KEY")
AWS_IOT_ROOT_CA = os.getenv("AWS_IOT_ROOT_CA")

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
    print("Conectado a AWS IoT con codigo:", rc)
    client.subscribe(AWS_IOT_SUB_TOPIC)

def publish_led(client, value: int):
    message = json.dumps({"Led": str(value)})
    client.publish(AWS_IOT_PUB_TOPIC, message)
    print(f"Publicado a {AWS_IOT_PUB_TOPIC}: {message}")

def on_message(client, userdata, msg):
    print(f"Mensaje recibido en {msg.topic}: {msg.payload}")

    try:
        payload = str(msg.payload.decode())
        print("Payload decodificado: ", payload)
    except Exception as e:
        print("Formato inesperado, no se pudo convertir: ", e)
        payload = "Formato inesperado"
    id_tarjeta = payload
    info_fecha = datetime.now()
    fecha_actual = info_fecha.date()
    hh = info_fecha.hour
    mm = info_fecha.minute
    hora_actual=time(hh,mm)

    with (Session(engine) as db):
        query = select(Alumno).where(Alumno.id_tarjeta == id_tarjeta)
        ddbb_alumno = db.exec(query).first()
        if not ddbb_alumno:
            query_trabajador=select(Trabajador).where(Trabajador.id_tarjeta == id_tarjeta)
            ddbb_trabajador=db.exec(query_trabajador).first()
            if not ddbb_trabajador:
                publish_led(client, 0)
                return print(f"Tarjeta sin asignar: {id_tarjeta}")
            else:
                registro_trabajador=RegistroHorario_T(
                    id_trabajador=ddbb_trabajador.id_trabajador,
                    fecha=fecha_actual,
                    hora=hora_actual
                )
                try:
                    guardar_registro=Horario_T.model_validate(registro_trabajador)
                    db.add(guardar_registro)
                    db.commit()
                    publish_led(client, 1)
                    return print(f"Asistencia registrada. ID: {guardar_registro.id_trabajador} - Tarjeta: {id_tarjeta}")
                except IntegrityError:
                    db.rollback()
                    publish_led(client, 0)
                    print(f"Registro duplicado: {registro_trabajador.id_horario_t} - {registro_trabajador.id_trabajador} ya existe un horario para este trabajador en ese instante.")
        else:
            registro_alumno=Asiste(
                id_alumno = ddbb_alumno.id_alumno,
                id_asignatura= "P1",
                fecha= fecha_actual,
                hora= hora_actual,
                asistio= True
            )
            try:
                db.add(registro_alumno)
                db.commit()
                publish_led(client, 1)
                return print(f"Asistencia registrada {id_tarjeta}")
            except IntegrityError:
                db.rollback()
                publish_led(client, 0)
                print("Registro duplicado: ya existe un registro para este alumno en ese instante")

def start_mqtt():
    client = mqtt.Client(client_id=AWS_IOT_CLIENT_ID)
    client.tls_set(ca_certs=AWS_IOT_ROOT_CA,
                   certfile=AWS_IOT_CERT,
                   keyfile=AWS_IOT_KEY)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(AWS_IOT_ENDPOINT, AWS_IOT_PORT, keepalive=60)
    client.loop_forever()
