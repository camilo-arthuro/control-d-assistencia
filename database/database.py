from sqlmodel import SQLModel, create_engine, Session
import os

class DatabaseManager:
    def __init__(self, database_url=None):
        if database_url is None:
            database_url = ""
        
        self.engine = create_engine(database_url, echo=True)
    
    def create_tables(self):
        SQLModel.metadata.create_all(self.engine)
    
    def get_session(self):
        return Session(self.engine)