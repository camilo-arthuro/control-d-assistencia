from sqlmodel import SQLModel, Field

class Alumno(SQLModel, table=True):
    id_alumno: int = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    apellidos: str = Field(max_length=100)
    correoelectronico: str = Field(max_length=100, unique=True)

class Persona(SQLModel, table=True):
    id_persona: int = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    apellidos: str = Field(max_length=100)
    correoelectronico: str = Field(max_length=100, unique=True)
    rol = bool # True = Profesor : False = PersonalServicio
class PersonalServicio(SQLModel, table=True):
    id_personal: int = Field(foreign_key="persona.id", primary_key=True)

class Profesor(SQLModel, table=True):
    id_profesor: int = Field(foreign_key="persona.id", primary_key=True)