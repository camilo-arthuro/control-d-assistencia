from sqlmodel import SQLModel, Field
from datetime import date, time

class Horario_T(SQLModel, table=True):
    id_persona: str = Field(foreign_key="trabajador.id_persona", primary_key=True)
    fecha: date = Field(primary_key=True)
    hora: time = Field(primary_key=True)

class Asiste(SQLModel, table=True):
    id_alumno: str = Field(foreign_key="alumno.id_alumno", primary_key=True)
    id_asignatura: str = Field(foreign_key="asignatura.id_asignatura", primary_key=True)
    fecha: date = Field(primary_key=True)
    hora: time = Field(primary_key=True)
    asistio: bool

class Asignatura(SQLModel, table=True):
    id_asignatura: str = Field(default=None, primary_key=True)
    id_profesor: str = Field(foreign_key="profesor.id_profesor")
    id_horario: str = Field(foreign_key="horario_a.id_horario")
    nombre: str = Field(max_length=100)
    descripcion: str = Field(max_length=200)

class Horario_A(SQLModel, table = True):
    id_horario: str = Field(default=None, primary_key=True)
    id_asignatura: str = Field(foreign_key="asignatura.id_asignatura", primary_key=True)
    fecha: date = Field(primary_key=True)
    hora: time = Field(primary_key=True)
    aula: str = Field(max_length=20)