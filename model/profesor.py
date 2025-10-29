from sqlmodel import SQLModel, Field
from typing import Optional

class Profesor(SQLModel, table=True):
    id_profesor: int = Field(foreign_key="persona.id", primary_key=True)