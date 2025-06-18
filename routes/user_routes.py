from fastapi import status , Depends , APIRouter
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from src.models import User 
from src.schemas import SignUpUser , SignInUser , Updated_User
from src.database import get_db
from src.utils import send_welcome_mail 
from passlib.context import CryptContext

router = APIRouter()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/sign-up" , status_code = status.HTTP_201_CREATED)
async def signup(user : SignUpUser , db : Session = Depends(get_db)):
    User_check = db.query(User).filter(User.email == user.email).first()
    if User_check:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail= "User with this id already exists")
    hashed_password = pwd_context.hash(user.password)
    new_user = User(email = user.email , firstname = user.firstname , lastname = user.lastname , password = hashed_password )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    user_name = user.firstname + " " + user.lastname
    send_welcome_mail(user.email , user_name)
    return {"message": "User created successfully", "user_id": new_user.user_id}


@router.post("/sign-in")
async def signin (user : SignInUser , db : Session = Depends(get_db)) -> dict :
    User_check = db.query(User).filter(User.email == user.email).first()
    if not User_check :
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail= "User not found")
    if not pwd_context.verify(user.password, User_check.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong password")
    return { "id" : User_check.user_id}


@router.patch("/update-user/{id}")
async def UpdatedUser (id : int , user : Updated_User , db : Session = Depends(get_db)) -> dict :
    User_check = db.query(User).filter(User.user_id == id).first()
    hashed_password = pwd_context.hash(user.password)
    if User_check:
        if user.email is not None:
            User_check.email = user.email
        if user.firstname is not None:
            User_check.firstname = user.firstname
        if user.lastname is not None:
            User_check.lastname = user.lastname
        if user.password is not None: 
            User_check.password = pwd_context.hash(user.password)
        db.commit()
        db.refresh(User_check)
        return{
            "email" : User_check.email ,
            "first name" : User_check.firstname ,
            "last name" : User_check.lastname ,
            "password" : User_check.password 
        }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    

@router.delete("/delete-user/{id}")
async def delete_user (id : int ,db : Session = Depends(get_db)):
    User_check = db.query(User).filter(User.user_id == id).first()
    if User_check :
        db.delete(User_check)
        db.commit()
        return {}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.get("/get-user/{id}")
async def get_user(id : int , db: Session = Depends(get_db)) -> dict :
    user = db.query(User).filter(User.user_id == id).first()
    if user :
        return{
            "email" : user.email ,
            "first name" : user.firstname ,
            "last name" : user.lastname ,
            "password" : user.password ,
            "created_at" : user.created_at ,
            "updated_at" : user.updated_at
        }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")