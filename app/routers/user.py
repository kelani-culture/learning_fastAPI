# create user
from .. import utils, models
from ..schema import User, UserResponse
from fastapi import status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=['users']
)


@router.post('/', status_code=status.HTTP_201_CREATED,
          response_model=UserResponse)
def create_user(user:User, db: Session=Depends(get_db)):
    # hash password = user.password
    check_email = db.query(models.User).filter(models.User.email == user.email).first()
    if check_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='email already exists')
    hashed_password =utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}', response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user id {id} not found")
    return user