from sqlmodel import SQLModel, Field
from datetime import date, time

class Horario_T(SQLModel, table=True):
    id_horario_t: int = Field (default=None, primary_key=True)
    id_trabajador: int = Field(foreign_key="trabajador.id_trabajador")
    fecha: date
    hora: time

class RegistroHorario_T(SQLModel):
    id_trabajador: int
    fecha: date
    hora: time

class Asiste(SQLModel, table=True):
    id_alumno: int = Field(foreign_key="alumno.id_alumno", primary_key=True)
    id_asignatura: str = Field(foreign_key="asignatura.id_asignatura", primary_key=True)
    fecha: date = Field(primary_key=True)
    hora: time = Field(primary_key=True)
    asistio: bool

class Asignatura(SQLModel, table=True):
    id_asignatura: str = Field(default=None, primary_key=True)
    id_profesor: int = Field(foreign_key="profesor.id_profesor")
    nombre: str = Field(max_length=100)
    descripcion: str = Field(max_length=200)

class Horario_A(SQLModel, table = True):
    id_horario_a: int = Field(default=None, primary_key=True)
    id_asignatura: str = Field(foreign_key="asignatura.id_asignatura", primary_key=True)
    fecha: date
    hora: time
    aula: str = Field(max_length=20)