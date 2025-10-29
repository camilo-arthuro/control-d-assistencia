from sqlmodel import SQLModel, Field

class Clase(SQLModel, table=True):
    id_alumno: int = Field(foreign_key="alumno.id_alumno", primary_key=True)
    id_asignatura: int = Field(foreign_key="asignatura.id_asignatura", primary_key=True)
    hora: int = Field(primary_key=True)
    dia: int = Field(primary_key=True)
    mes: int = Field(primary_key=True)
    año: int = Field(primary_key=True)
    asistio: bool = Field(default=False)