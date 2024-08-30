from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
#routers
from .routers import items

app = FastAPI()
origins = ["http://localhost:300",]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

trialDB=[]

app.include_router(items.router)
@app.get("/home")
async def home(limit=20,sort: Optional[str]=None):
    return {"message": f"this is the home page, these many posts are seen {limit}"}