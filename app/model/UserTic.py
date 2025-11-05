from sqlmodel import SQLModel, Field
from enum import Enum
from .clase import ClaseEnum

class RolEnum(str, Enum):
    alumno = "alumno"
    profesor = "profesor"
    personal_servicio = "personal_servicio"

class Persona(SQLModel, table=True):
    id_persona: int = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    apellidos: str = Field(max_length=100)
    correoelectronico: str = Field(max_length=100, unique=True)
    rol: RolEnum

class Alumno(SQLModel, table=True):
    id_alumno: int = Field(foreign_key="persona.id_persona", primary_key=True)

class PersonalServicio(SQLModel, table=True):
    id_personal: int = Field(foreign_key="persona.id_persona", primary_key=True)

class Profesor(SQLModel, table=True):
    id_profesor: int = Field(foreign_key="persona.id_persona", primary_key=True)