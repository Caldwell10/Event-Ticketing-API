from fastapi import FastAPI, HTTPException, Depends
from schema import UserCreate, UserOut, ShowCreate, ShowOut, SeatCreateBulk, SeatOut, ReservationCreate, ReservationOut
from models import User, Show, Seat, Reservation
from database import get_db
from services import hash_password, normalize_seat_labels

import uvicorn


# Create the FastAPI app
app = FastAPI()

# Evaluating root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Event Ticketing System API"}

# create user endpoint
@app.post("/users/", response_model=UserOut)
def create_user(user: UserCreate, db=Depends(get_db)):
    # check for existing user with same email
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # If no existing user, create a new one
    new_user = User(
        name = user.name,
        phone_number = user.phone_number,
        email = user.email,
        password = hash_password(user.password)
    )

    # Save to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# create show endpoint
@app.post("/shows/", response_model=ShowOut)
def create_show(show: ShowCreate, db=Depends(get_db)):
    # Check for existing show with same title and start time
    existing_show = db.query(Show).filter(Show.title == show.title, Show.starts_at == show.starts_at).first()
    if existing_show:
        raise HTTPException(status_code=400, detail="Show with the same title and start time already exists")
    
    # unpack show data and create Show instance
    new_show = Show(**show.dict())

    # Save to database
    db.add(new_show)
    db.commit()
    db.flush(new_show)

    return new_show

# bulk create seats endpoint
app.post("/shows/{show_id}/seats", response_model=list[SeatOut])
def create_seats_bulk(show_id, seats: SeatCreateBulk, db=Depends(get_db)):
     # Check if show exists
    show = db.query(Show).filter(Show.id == show_id).first()
    if not show:
        raise HTTPException(status_code=404, detail="Show not found")
    

    # Create seat objects via list comprehension
    new_seats = [Seat(seat_number=normalize_seat_labels(seat_number)) for seat_number in seats.seat_numbers]

    # Bulk save seats into database
    db.add_all(new_seats)
    db.commit()
    db.refresh(new_seats)  

    return list(new_seats)



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)