from sqlmodel import SQLModel, Field
from typing import Optional

class Clase(SQLModel, table=True):
    id_alumno: int = Field(foreign_key="alumno.id_alumno", primary_key=True)
    id_asignatura: int = Field(foreign_key="asignatura.id_asignatura", primary_key=True)
    hora: int = Field(primary_key=True)
    dia: int = Field(primary_key=True)
    mes: int = Field(primary_key=True)
    año: int = Field(primary_key=True)
    asistio: bool = Field(default=False)

class Fecha(SQLModel, table=True):
    hora: int = Field(primary_key=True)
    dia: int = Field(primary_key=True)
    mes: int = Field(primary_key=True)
    año: int = Field(primary_key=True)

class Asignatura(SQLModel, table=True):
    id_asignatura: int = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    descripcion: Optional[str] = Field(default=None)

class DarAsignatura(SQLModel, table=True):
    id_profesor: int = Field(foreign_key="profesor.id_profesor", primary_key=True)
    id_asignatura: int = Field(foreign_key="asignatura.id_asignatura", primary_key=True)