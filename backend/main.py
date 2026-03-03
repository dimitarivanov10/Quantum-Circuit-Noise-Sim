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

# Pauli's X-Gate
X_GATE = np.array([[0, 1], [1, 0]])

# Hadamaard-Gate
H_GATE = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]])

#Pauli's Y-Gate
Y_GATE = np.array([[0, -1j], [1j, 0]])

@app.get("/")
def home():
    return {"message": "Quantum Simulator API is running"}

@app.post("/apply-x")
def apply_x(data: QubitState):
    vec = np.array(data.state)
    new_state = np.dot(X_GATE, vec)
    return {"new_state": new_state.tolist()}

@app.post("/apply-h")
def apply_h(data: QubitState):
    vec = np.array(data.state)
    new_state = np.dot(H_GATE, vec)
    return{"new_state": new_state.tolist()}

@app.post("/apply-y")
def apply_y(data: QubitState):
    vec = np.array(data.state, dtype=complex)
    res = np.dot(Y_GATE, vec)
    serialized_state = [str(x) if x.imag != 0 else x.real for x in res]
    return{"new_state": serialized_state}

def prepare_vector(state_list):
    clean_list = [complex(x) if isinstance(x, str) else x for x in state_list]
    return np.array(clean_list, dtype=complex)