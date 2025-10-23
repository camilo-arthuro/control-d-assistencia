from sqlmodel import SQLModel, Field

class UserTic(SQLModel, table = True):
    id: int = Field(default=None, primary_key=True)
    level: int
    name: str
    last_name: str
    rol: str