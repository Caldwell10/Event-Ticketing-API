from fastapi import FastAPI, HTTPException, Depends
from schema import UserCreate, UserOut, ShowCreate, ShowOut, SeatCreateBulk, SeatOut, ReservationCreate, ReservationOut
from models import User, Show, Seat, Reservation
from database import get_db
from services import hash_password


# Create the FastAPI app
app = FastAPI()


# create user endpoint
@app.post("/users/", response_model=UserOut)
def create_user(user: UserCreate, db=Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    new_user = User(
        name = user.name,
        phone_number = user.phone_number,
        email = user.email,
        password = hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user