from .. import models, oauth2
from ..schema import PostCreate, Post, PostOut
from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import Optional
from sqlalchemy import func, select
from ..database import get_db
from sqlalchemy.orm import Session
import json
from typing import List


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)



@router.get("/")
def get_posts(db: Session = Depends(get_db),
              user_id: int= Depends(oauth2.get_current_user ),
              limit: int = 10, skip: int=0, search: Optional[str]=""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).\
        limit(limit).\
            offset(skip).all()
    return posts

@router.post("/", status_code=201, response_model=Post)
def create_posts(post: PostCreate, db: Session = Depends(get_db),
                 user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, contents, published)
    #                VALUES (%s, %s, %s) RETURNING *""", (req.title, req.content, req.published))
    # new_post = cursor.fetchone()
    # if not new_post:
    #     return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
    #                          detail="Unsuccessfully create posts")
    # conn.commit()
    new_post = models.Post(owner_id=user_id.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/{id}', response_model=Post)
def get_post(id: int, db: Session = Depends(get_db),
             user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",
    #                (id,))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Id Not found")
    return post


@router.delete("/{id}", status_code=204)
def delete_post(id: int, db: Session = Depends(get_db),
                user_id: int = Depends(oauth2.get_current_user)):
    # find the index in the array that has required ID
    # cursor.execute(""" DELETE  FROM posts where id = %s RETURNING * """,
    #                (id,))
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Id not found")
    

    if post.owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorizeed to perform action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=List[Post])
def update_post(id:int, post: PostCreate, db: Session = Depends(get_db), 
                user_id: int = Depends(oauth2.get_current_user)):
    post_q = db.query(models.Post).filter(models.Post.id == id)
    pos = post_q.first()
    if pos == None:
        return HTTPException(status.HTTP_404_NOT_FOUND,
                             detail="could not update post wrong id")
    if pos.owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorizeed to perform action")
    post_q.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_q.first() 