from sqlmodel import SQLModel, Field
from typing import Optional

class PersonalServicio(SQLModel, table=True):
    id_personal: int = Field(foreign_key="persona.id", primary_key=True)