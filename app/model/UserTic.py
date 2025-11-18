from sqlmodel import SQLModel, Field
from enum import Enum

class RolEnum(str, Enum):
    profesor = "profesor"
    personal_servicio = "personal_servicio"

class Trabajador(SQLModel, table=True):
    id_trabajador: str = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    apellidos: str = Field(max_length=100)
    correoelectronico: str = Field(max_length=100, unique=True)
    rol: RolEnum

class PersonalServicio(SQLModel, table=True):
    id_personal: str = Field(foreign_key="trabajador.id_trabajador", primary_key=True)

class Profesor(SQLModel, table=True):
    id_profesor: str = Field(foreign_key="trabajador.id_trabajador", primary_key=True)
    
class Alumno(SQLModel, table=True):
    id_alumno: str = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    apellidos: str = Field(max_length=100)
    correoelectronico: str = Field(max_length=100, unique=True)