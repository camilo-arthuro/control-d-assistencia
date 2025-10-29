from fastapi import FastAPI, Depends
import threading
from mqtt_service import start_mqtt
from .test_classes.UserTest import AlumneTest
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session, select
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.on_event("startup")
def startup_event():
    thread = threading.Thread(target=start_mqtt)
    thread.daemon = True
    thread.start()

@app.post("/api/assistencia", response_model=dict, tags=["CREATE USER"])
async def create_user(new_user: AlumneTest, db: Session = Depends(get_db)):
    user_data = AlumneTest.model_validate(new_user)
    db.add(user_data)
    db.commit()
    return {"msg":"User added to the DDBB"}