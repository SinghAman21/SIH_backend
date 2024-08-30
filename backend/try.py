from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models
from database import engine, SessionLocal
from auth import bcrypt_context

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class SignUp(BaseModel):
    email: EmailStr  
    name: str
    phone_number: Optional[str] = None
    password: str
    gender: str
    date_of_birth: Optional[date] = None
    address: Optional[str] = None
    institute_name: Optional[str] = None
    name_of_degree: Optional[str] = None
    graduation_year: Optional[int] = None
    major_field_of_study: Optional[str] = None
    achievements: Optional[str] = None
    current_employer: Optional[str] = None
    work_experience: Optional[str] = None
    professional_field: Optional[str] = None
    job_title: Optional[str] = None
    skills: Optional[str] = None
    certificates: Optional[str] = None
    languages_spoken: Optional[str] = None

class Login(BaseModel):
    email: EmailStr
    password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", status_code=status.HTTP_200_OK)
async def read_firstpg(request: Request):
    return templates.TemplateResponse("parallax.html", {"request": request})

@app.get("/login/", status_code=status.HTTP_200_OK)
async def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/signup", status_code=status.HTTP_200_OK)
async def read_signup(request: Request):
    return templates.TemplateResponse("sign-up.html", {"request": request})


@app.post("/signup/", status_code=status.HTTP_201_CREATED)
async def create_user(user: SignUp, db: Session = Depends(get_db)):
    try:
        # Hash the password before storing it
        hashed_password = bcrypt_context.hash(user.password)
        user_data = user.dict()
        user_data['password'] = hashed_password
        
        db_user = models.User(**user_data)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        db.rollback()
        if "Duplicate entry" in str(e.orig):
            raise HTTPException(status_code=400, detail="Email already registered")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/login/", status_code=status.HTTP_200_OK)
async def login_user(user: Login, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    
    if not db_user or not bcrypt_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    return {"msg": "Login successful", "user_id": db_user.id}

@app.get("/signup/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
