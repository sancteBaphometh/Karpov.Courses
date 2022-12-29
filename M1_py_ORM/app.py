from typing import List

from sqlalchemy import func, desc
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
from database import SessionLocal
from schema import UserGet, PostGet, FeedGet
from table_feed import Feed
from table_post import Post
from table_user import User

app = FastAPI()


def get_db():
    with SessionLocal() as db:
        return db


@app.get("/user/{id}", response_model=UserGet)
def find_user(id, db: Session = Depends(get_db)):
    result = db.query(User)\
        .filter(User.id == id).one_or_none()

    if result:
        return result
    else:
        raise HTTPException(404, "User not found")


@app.get("/post/{id}", response_model=PostGet)
def find_post(id, db: Session = Depends(get_db)):
    result = db.query(Post)\
        .filter(Post.id == id).one_or_none()

    if result:
        return result
    else:
        raise HTTPException(404, "Post not found")


@app.get("/user/{id}/feed", response_model=List[FeedGet])
def user_feed(id, limit: int = 10, db: Session = Depends(get_db)):
    result = db.query(Feed) \
        .filter(Feed.user_id == id)\
        .order_by(Feed.time.desc())\
        .limit(limit).all()

    if result:
        return result
    else:
        raise HTTPException(404, "User not found")


@app.get("/post/{id}/feed", response_model=List[FeedGet])
def post_feed(id, limit: int = 10, db: Session = Depends(get_db)):
    result = db.query(Feed) \
        .filter(Feed.post_id == id) \
        .order_by(Feed.time.desc()) \
        .limit(limit).all()

    if result:
        return result
    else:
        raise HTTPException(404, "Post not found")


@app.get("/post/recommendations/", response_model=List[PostGet])
def get_recommended_feed(limit: int = 10, db: Session = Depends(get_db)):
    result = db.query(Post)\
        .select_from(Feed)\
        .filter(Feed.action == "like")\
        .join(Post)\
        .group_by(Post.id)\
        .order_by(desc(func.count(Post.id)))\
        .limit(limit).all()

    return result