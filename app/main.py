# app/main.py
from fastapi import FastAPI, HTTPException, status
from .schemas import User

app = FastAPI()
users: list[User] = []

@app.get("/hello")
def hello():
    return {"message": "Hello, World!"}

@app.get("/api/users")
def get_users():
    return users

@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    for u in users:
        if u.user_id == user_id:
            return u
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@app.post("/api/users", status_code=status.HTTP_201_CREATED)
def add_user(user: User):
    if any(u.user_id == user.user_id for u in users):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user_id already exists")
    users.append(user)
    return user

@app.put("/api/users/{user_id}", status_code=200)
def update_user(user: User, user_id: int):
    for i, u in enumerate(users):
        if u.user_id==user_id:
            users[i] = user
            return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@app.delete("/api/users/{user_id}", status_code = 204)
def delete_user(user_id: int):
    for u in users:
        if u.user_id == user_id:
            users.remove(u)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")        


@app.get("/health")
def get_health():
    return {"status": "ok"}
# python -m uvicorn app.main:app --reload
# python -m venv venv
# source venv/Scripts/activate