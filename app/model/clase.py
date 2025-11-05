from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, time
from enum import Enum

class Asiste(SQLModel, table=True):
    id_alumno: int = Field(foreign_key="alumno.id_alumno", primary_key=True)
    id_asignatura: int = Field(foreign_key="asignatura.id_asignatura", primary_key=True)
    fecha: date = Field(primary_key=True)
    hora: time = Field(primary_key=True)
    asistio: bool

class Trabaja(SQLModel, table=True):
    id_personal: int = Field(foreign_key="persona.id_persona", primary_key=True)
    fecha: date = Field(primary_key=True)
    hora: time = Field(primary_key=True)

class Asignatura(SQLModel, table=True):
    id_asignatura: int = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    descripcion: str = Field(max_length=200)

class Da(SQLModel, table=True):
    id_profesor: int = Field(foreign_key="profesor.id_profesor", primary_key=True)
    id_asignatura: int = Field(foreign_key="asignatura.id_asignatura", primary_key=True)

class Horario(SQLModel, table = True):
    id_asignatura: int = Field(foreign_key="asignatura.id_asignatura", primary_key=True)
    fecha: date = Field(primary_key=True)
    hora: time = Field(primary_key=True)
    aula: str = Field(max_lenght=20)