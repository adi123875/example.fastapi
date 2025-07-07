from fastapi import FastAPI, Response, status, HTTPException,Depends,APIRouter
from typing import List,Optional
from sqlalchemy.orm import session
from sqlalchemy import func
from .. import models,schemas,oauth2
from ..database import get_db
router=APIRouter(
    prefix="/posts",
    tags=['posts']
)

@router.get("/",response_model=List[schemas.postout])
async def get_posts(db:session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search:Optional[str]=""):
    # cursor.execute(""" SELECT * FROM posts""") 
    # posts=cursor.fetchall()
    # print(search)
    # posts=db.query(models.post).filter(models.post.title.contains(search)).limit(limit).offset(skip).all()

    posts=db.query(models.post,func.count(models.vote.post_id).label("votes")).join(models.vote,models.vote.post_id==models.post.id,isouter=True).group_by(models.post.id).filter(models.post.title.contains(search)).limit(limit).offset(skip).all()
    return posts
    

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.post)
async def create_posts(post:schemas.postcreate,db:session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES(%s, %s, %s) RETURNING *  """,(post.title,post.content,post.published))
    # new_post=cursor.fetchone()
    # conn.commit()
    print(current_user.email)
    new_post=models.post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post




@router.get("/{id}",response_model=schemas.postout)
async def get_post(id:int,db:session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id=%s """,(str(id),))
    # post=cursor.fetchone()
    # post=db.query(models.post).filter(models.post.id==id).first()
    post=db.query(models.post,func.count(models.vote.post_id).label("votes")).join(models.vote,models.vote.post_id==models.post.id,isouter=True).group_by(models.post.id).filter(models.post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not exists")
   
    return post

@router.delete("/{id}")
async def delete_post(id:int,db:session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id=%s returning * """,(str(id),))
    # deleted_post=cursor.fetchone()
    # conn.commit()
   post_query=db.query(models.post).filter(models.post.id==id)
   post=post_query.first()
   if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not exists")
   if post.owner_id != current_user.id:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="not authorized to delete")
   post_query.delete(synchronize_session=False)
   db.commit()
   return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.post)
async def update_post(id:int,post:schemas.postcreate,db:session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title=%s,content=%s,published=%s WHERE id =%s returning * """,(post.title,post.content,post.published,(str(id),)))
    # updated_post=cursor.fetchone()
    # conn.commit()
    post_query=db.query(models.post).filter(models.post.id==id)
    updated_post=post_query.first()
    if updated_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not exists")
    if updated_post.owner_id != current_user.id:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="not authorized to update")
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()