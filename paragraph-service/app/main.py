from fastapi import FastAPI
from .database import engine
from .models import Base
from .routes import router

app = FastAPI()
app.include_router(router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "API is running"}