from fastapi import FastAPI
from nysmix.db import DatabasePostgres, File, Snapshot
from sqlmodel import Session, select, DATE, cast, func
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "https://gautsi.static.observableusercontent.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


db = DatabasePostgres()


@app.on_event("startup")
def on_startup():
    db.create()


@app.get("/")
async def root():
    return {"message": "Hello World test again"}


@app.get("/files/")
def read_files():
    with Session(db.engine) as session:
        files = session.exec(select(File)).all()
    return files


@app.get("/summary/")
def get_daily_summary():
    with Session(db.engine) as session:
        statement = select(
            cast(Snapshot.timestamp, DATE), Snapshot.fuel, func.sum(Snapshot.gen_mw)
        ).group_by(cast(Snapshot.timestamp, DATE), Snapshot.fuel)
        result = session.exec(statement).all()
    return result
