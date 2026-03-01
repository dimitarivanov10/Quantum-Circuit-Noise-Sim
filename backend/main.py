from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np

app = FastAPI()

class QubitState(BaseModel):
    state: list

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

X_GATE = np.array([[0, 1], [1, 0]])

@app.get("/")
def home():
    return {"message": "Quantum Simulator API is running"}

@app.post("/apply-x")
def apply_x(data: QubitState):
    vec = np.array(data.state)
    new_state = np.dot(X_GATE, vec)
    return {"new_state": new_state.tolist()}
