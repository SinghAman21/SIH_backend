from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
import logging
import uvicorn
import models
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from hash_pass import hash_password  # Ensure this function is correctly implemented and imported
from signup import router as signup_router

app = FastAPI()

# Database connection configuration
DATABASE_URL = "mysql+pymysql://your_actual_username:your_actual_password@localhost/my_fastapi_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Model for incoming data
class UserBase(BaseModel):
    name: str
    email: str
    phone_number: Optional[str] = None
    password: str
    gender: Optional[str] = None
    date_of_birth: Optional[str] = None
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

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int

@app.post("/signup", response_model=UserResponse)
async def signup(user: UserCreate):
    db = SessionLocal()
    try:
        # Check if user already exists
        existing_user = db.query(models.User).filter(models.User.email == user.email).first()
        
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already registered")
        
        # Encrypt the user's password
        hashed_password = hash_password(user.password)
        
        # Insert new user with hashed password
        new_user = models.User(
            name=user.name, email=user.email, phone_number=user.phone_number, password=hashed_password,
            gender=user.gender, date_of_birth=user.date_of_birth, address=user.address,
            institute_name=user.institute_name, name_of_degree=user.name_of_degree,
            graduation_year=user.graduation_year, major_field_of_study=user.major_field_of_study,
            achievements=user.achievements, current_employer=user.current_employer,
            work_experience=user.work_experience, professional_field=user.professional_field,
            job_title=user.job_title, skills=user.skills, certificates=user.certificates,
            languages_spoken=user.languages_spoken
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected error occurred.")
    finally:
        db.close()

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

@app.get("/")
def root_route():
    return {"message": "Welcome to the FastAPI app"}

@app.get("/example")
def example_route():
    logging.debug("Processing request")
    try:
        response = {"message": "This is a JSON response"}
        logging.debug(f"Response: {response}")
        return response
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return {"error": "An internal error occurred."}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = Query(None)):
    if item_id < 0:
        raise HTTPException(status_code=422, detail=[
            {"loc": ["path", "item_id"], "msg": "Item ID must be a positive integer", "type": "value_error"}
        ])
    return {"item_id": item_id, "q": q}

# Include the signup router
app.include_router(signup_router)

# Run the server (only necessary if running directly with Python)
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True, debug=True)
