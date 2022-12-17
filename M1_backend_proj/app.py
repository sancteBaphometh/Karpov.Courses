import datetime
from fastapi.responses import JSONResponse
import psycopg2
from fastapi import FastAPI, Depends
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    name: str
    surname: str
    age: int
    registration_date: datetime.date


class PostResponse(BaseModel):
    id: int
    text: str
    topic: str

    class Config:
        orm_mode = True


def get_db():
    conn = psycopg2.connect(
        "postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml",
        cursor_factory=RealDictCursor
    )

    return conn


@app.get("/hello")
def say_hello() -> str:
    return "hello, world"


@app.get("/")
def sum_num(a: int, b: int) -> int:
    return a + b


@app.get("/sum_date")
def sum_date(current_date: datetime.date, offset: int) -> datetime.date:
    return current_date + datetime.timedelta(offset)


@app.post("/user/validate")
def validate(json_file: User) -> str:
    return f"Will add user: {json_file.name} {json_file.surname} with age {json_file.age}"


@app.get("/user/{id}")
def find_user(id: int, db = Depends(get_db)):
    with db.cursor() as cursor:
        cursor.execute(
            f"""
            SELECT gender, age, city
            FROM "user"
            WHERE id = {id}
            """
        )

        result = cursor.fetchone()

        if not result:
            return JSONResponse(
                status_code=404,
                content={"detail": "user not found"},
            )
        else:
            return result


@app.get("/post/{id}", response_model = PostResponse)
def find_post(id: int, db = Depends(get_db)):
    with db.cursor() as cursor:
        cursor.execute(
            f"""
            SELECT id, text, topic
            FROM post
            WHERE id = {id}
            """
        )

        result = cursor.fetchone()

        if not result:
            return JSONResponse(
                status_code=404,
                content={"detail": "post not found"},
            )
        else:
            return result