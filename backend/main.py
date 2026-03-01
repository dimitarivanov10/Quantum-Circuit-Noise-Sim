from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

X-GATE = np.array([[0, 1], [1, 0]])

@app.get("/")
def home():
    return {"message": "Quantum Simulator API is running"}

@app.post("/apply-x")
def apply_x(state: list):
    vec = np.array(state)
    new_state = np.dot(X_GATE, vec)
    return {"new_state": new_state.tolist()}
