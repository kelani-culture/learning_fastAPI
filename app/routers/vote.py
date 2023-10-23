from fastapi import status, HTTPException, Depends, APIRouter
from .. import schema, models, oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/votes',
    tags=['vote']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schema.Vote, db: Session = Depends(get_db),
         current_user: int = Depends(oauth2.get_current_user)):
    
    find_post = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id).first()
    if not find_post:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post of id {vote.post_id} does not exist")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id ==\
        vote.post_id,models.Vote.user_id == current_user.id)

    found_vote = vote_query.first()
    if (vote.dire == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"""current user id {current_user.id} already voted on post id {vote.post_id}""")
        new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Vote not found')
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "vote deleted successfully"}
    return {"message": "vote added successfully"}