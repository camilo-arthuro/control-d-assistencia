from sqlmodel import SQLModel, Field
from typing import Optional

class Persona(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    apellidos: str = Field(max_length=100)
    correoelectronico: str = Field(max_length=100, unique=True)