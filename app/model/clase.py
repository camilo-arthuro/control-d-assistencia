from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, time
from enum import Enum

class AsistenciaAlumno(SQLModel, table=True):
    id_alumno: int = Field(foreign_key="alumno.id_alumno", primary_key=True)
    id_clase: int = Field(foreign_key="clase.id_clase", primary_key=True)
    id_asignatura: int = Field(foreign_key="asignatura.id_asignatura", primary_key=True)
    total_asistencia: int
    total_faltas: int
    total_justificadas: int
    porcentaje_fallas: int

class PrimeraAsistencia(SQLModel):
    id_alumno: int
    id_clase: int
    id_asignatura: int

class ClaseEnum(str,Enum):
    daw="DAW"
    dam="DAM"
    asix="ASIX"
class Clase(SQLModel, table=True):
    id_clase: int = Field(default=None, primary_key=True)
    nombre: ClaseEnum = Field(max_length=100)
    anyo_estudio: int

class AsistenciaClases(SQLModel, table=True):
    id_alumno: int = Field(foreign_key="alumno.id_alumno", primary_key=True)
    id_clase: int = Field(foreign_key="clase.id_clase", primary_key=True)
    id_asignatura: int = Field(foreign_key="asignatura.id_asignatura", primary_key=True)
    fecha: date
    hora: time
    asistio: bool

class Trabaja(SQLModel, table=True):
    id_personal: int = Field(foreign_key="persona.id_persona", primary_key=True)
    fecha: date
    hora: time
    zona: str
    asistio: bool

class DescripcionEnum(str, Enum):
    mañana= "mañana"
    tarde="tarde"
class Asignatura(SQLModel, table=True):
    id_asignatura: int = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    descripcion: DescripcionEnum

class DarAsignatura(SQLModel, table=True):
    id_profesor: int = Field(foreign_key="profesor.id_profesor", primary_key=True)
    id_asignatura: int = Field(foreign_key="asignatura.id_asignatura", primary_key=True)
'''    
class Fecha(SQLModel, table=True):
    hora: int = Field(primary_key=True)
    dia: int = Field(primary_key=True)
    mes: int = Field(primary_key=True)
    anyo: int = Field(primary_key=True)
'''