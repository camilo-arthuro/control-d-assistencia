from sqlmodel import SQLModel, Field
from typing import Optional

class Asignatura(SQLModel, table=True):
    id_asignatura: int = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    descripcion: Optional[str] = Field(default=None)