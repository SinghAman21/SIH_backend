from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
@app.get("/")
async def root():
    return {"message": "Hello World"}