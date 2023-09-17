from fastapi import FastAPI
import models
from database import engine
from routers import auth, todos

app = FastAPI()

# create all tables in the database
models.Base.metadata.create_all(bind=engine)

# include the auth router
app.include_router(auth.router)
app.include_router(todos.router)
