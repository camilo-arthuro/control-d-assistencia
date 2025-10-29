from sqlmodel import SQLModel, Field

class Fecha(SQLModel, table=True):
    hora: int = Field(primary_key=True)
    dia: int = Field(primary_key=True)
    mes: int = Field(primary_key=True)
    año: int = Field(primary_key=True)