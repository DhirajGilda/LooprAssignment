from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
import json

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Load user data from JSON file
def load_users():
  with open("data/users.json", "r") as file:
    return json.load(file)


# Load product data from JSON file
def load_products():
  with open("data/products.json", "r") as file:
    return json.load(file)


# Save user data to JSON file
def save_users(users):
  with open("data/users.json", "w") as file:
    json.dump(users, file, indent=4)


# Save cart data to JSON file
def save_cart(username, cart):
  with open(f"data/cart_{username}.json", "w") as file:
    json.dump(cart, file, indent=4)


# Verify user credentials
def verify_user(username, password):
  users = load_users()
  user = users.get(username)
  if user and user["password"] == password:
    return user


# Create password context for hashing and verifying passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Generate JWT token
def create_access_token(username):
  secret_key = "ThisIsASecretKey123"  # Replace with your own secret key
  expires_delta = timedelta(minutes=30)
  expire = datetime.utcnow() + expires_delta
  to_encode = {"sub": username, "exp": expire}
  encoded_jwt = jwt.encode(to_encode, secret_key, algorithm="HS256")
  return encoded_jwt


# Verify JWT token
def decode_token(token):
  secret_key = "ThisIsASecretKey123"  # Replace with your own secret key
  try:
    payload = jwt.decode(token, secret_key, algorithms=["HS256"])
    return payload["sub"]
  except jwt.ExpiredSignatureError:
    raise HTTPException(status_code=401, detail="Token has expired.")
  except jwt.InvalidTokenError:
    raise HTTPException(status_code=401, detail="Invalid token.")


# Models
class UserCreate(BaseModel):
  username: str
  password: str


class UserLogin(BaseModel):
  username: str
  password: str


class Product(BaseModel):
  productId: int
  image: str
  name: str
  price: float
  quantity: int


class Cart(BaseModel):
  products: List[Product]


@app.post("/users/register")
def register_user(user: UserCreate):
  users = load_users()
  if user.username in users:
    raise HTTPException(status_code=400, detail="Username already exists.")
  hashed_password = pwd_context.hash(user.password)
  users[user.username] = {
    "username": user.username,
    "password": hashed_password
  }
  save_users(users)
  return {"message": "User registered successfully."}


@app.post("/users/login")
def login_user(user: UserLogin):
  verified_user = verify_user(user.username, user.password)
  if not verified_user:
    raise HTTPException(status_code=401,
                        detail="Invalid username or password.")
  access_token = create_access_token(user.username)
  return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me")
def get_current_user(token: str = Depends(oauth2_scheme)):
  username = decode_token(token)
  return {"username": username}


@app.post("/cart/add")
def add_product_to_cart(product: Product, token: str = Depends(oauth2_scheme)):
  username = decode_token(token)
  cart = load_cart(username)
  cart["products"].append(product)
  save_cart(username, cart)
  return {"message": "Product added to cart successfully."}


# Implement other cart management endpoints (update, delete, read) based on your requirements.

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)
