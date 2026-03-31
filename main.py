from fastapi import FastAPI, Depends
import auth
from chatbot import AarogyaChatbot
from schemas import ChatQuery

app = FastAPI(
    title="AarogyaOne Support API",
    description="Medical Chatbot API — secured with API Key (X-API-KEY header)."
)

# Initialize Chatbot
bot = AarogyaChatbot()


# ─── CHAT ENDPOINT (Protected by API Key) ───────────
@app.post("/chat", tags=["Bot"])
def chat_endpoint(
    query: ChatQuery,
    api_key: str = Depends(auth.verify_api_key)
):
    """
    ### Chat with AarogyaOne Bot

    **Authentication**: Pass your API Key in the `X-API-KEY` header.

    **Request Body**:
    ```json
    { "message": "I want ABHA card" }
    ```

    **Response**:
    ```json
    { "response": "...", "status": "success" }
    ```
    """
    response = bot.chat(query.message)
    return {"response": response, "status": "success"}


# ─── HEALTH CHECK ────────────────────────────────────
@app.get("/", tags=["Info"])
def read_root():
    return {
        "status": "AarogyaOne API Running",
        "auth": "API Key (X-API-KEY header)",
        "endpoints": {
            "POST /chat": "Send message to chatbot (requires API Key)"
        }
    }


# ─── JWT ENDPOINTS (COMMENTED OUT — NOT IN USE) ─────
# If you ever need user login with JWT tokens, uncomment below.
#
# from fastapi.security import OAuth2PasswordRequestForm
# from sqlalchemy.orm import Session
# from jose import JWTError, jwt
# import models, database
# from schemas import UserCreate, UserOut, Token
#
# # Initialize database
# # models.Base.metadata.create_all(bind=database.engine)
#
# @app.post("/register", response_model=UserOut, tags=["Auth"])
# def register_user(user: UserCreate, db: Session = Depends(database.get_db)):
#     db_user = db.query(models.User).filter(models.User.username == user.username).first()
#     if db_user:
#         raise HTTPException(status_code=400, detail="Username already registered")
#     hashed_password = auth.get_password_hash(user.password)
#     new_user = models.User(username=user.username, hashed_password=hashed_password)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user
#
# @app.post("/login", response_model=Token, tags=["Auth"])
# async def login(db: Session = Depends(database.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
#     user = db.query(models.User).filter(models.User.username == form_data.username).first()
#     if not user or not auth.verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(status_code=401, detail="Incorrect username or password")
#     access_token = auth.create_access_token(data={"sub": user.username})
#     refresh_token = auth.create_refresh_token(data={"sub": user.username})
#     return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
