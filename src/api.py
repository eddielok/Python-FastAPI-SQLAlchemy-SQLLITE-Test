from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from lib import crud, models, schemas
from lib.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)


app = FastAPI(description="""Coding Monkey test Python""")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User, tags=["users"])
def create_new_users(user: schemas.UserBase, db: Session = Depends(get_db)):
    """create_new_users"""
    return crud.create_user(db=db, user=user)

@app.get("/users", response_model=List[schemas.User], tags=["users"])
def Get_Users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get users"""
    users = crud.get_users(db, skip=skip, limit=limit)
    return users
    
@app.get("/users/{email}", response_model=schemas.User, tags=["users"])
def Get_User_by_Email(email: str, db: Session = Depends(get_db)):
    """Get User by Email"""
    db_user = crud.get_user_by_email(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
    
@app.delete("/users/{email}")
def Delete_User_by_Email(email: str, db: Session = Depends(get_db)):
    """create_new_users"""
    db_user = crud.get_user_by_email(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if crud.delete_user(db=db, user=db_user):
        return {"detail": "User Deleted"}
    
@app.put("/users/{id}", response_model=schemas.User, tags=["users"])
def Update_User_by_UserID(id:int, user: schemas.UserBase, db: Session = Depends(get_db)):
    """Update_Users"""
    db_user = crud.get_user_by_id(db, id=id)
    #db_user.email = user.email
    #db_user.name = user.name
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_user(db=db,id=id, user=user)
    
@app.get("/")
async def Check_DB_Connection():
    """DB Connected"""
    return {"message": "DB Connected Successfully"}