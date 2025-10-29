from sqlmodel import SQLModel, Field

class DarAsignatura(SQLModel, table=True):
    id_profesor: int = Field(foreign_key="profesor.id_profesor", primary_key=True)
    id_asignatura: int = Field(foreign_key="asignatura.id_asignatura", primary_key=True)