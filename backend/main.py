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

#Pauli's Z-Gate
Z_GATE = np.array([[1, 0], [0, -1]])

# S-Gate (90 degree rotation)
S_GATE = np.array([[1, 0], [0, 1j]])

# T-Gate (45 degree rotation)
T_GATE = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]])

@app.get("/")
def home():
    return {"message": "Quantum Simulator API is running"}

def serialize_state(vec):
    return [str(x) if x.imag != 0 else float(x.real) for x in vec]

@app.post("/apply-x")
def apply_x(data: QubitState):
    vec = prepare_vector(data.state)
    new_state = np.dot(X_GATE, vec)
    return {"new_state": serialize_state(new_state)}

@app.post("/apply-h")
def apply_h(data: QubitState):
    vec = prepare_vector(data.state)
    new_state = np.dot(H_GATE, vec)
    return {"new_state": serialize_state(new_state)}

@app.post("/apply-y")
def apply_y(data: QubitState):
    vec = prepare_vector(data.state)
    res = np.dot(Y_GATE, vec)
    return {"new_state": serialize_state(res)}

@app.post("/apply-z")
def apply_z(data: QubitState):
    vec = prepare_vector(data.state)
    new_state = np.dot(Z_GATE, vec)
    return {"new_state": serialize_state(new_state)}

@app.post("/apply-s")
def apply_s(data: QubitState):
    vec = prepare_vector(data.state)
    new_state = np.dot(S_GATE, vec)
    return {"new_state": serialize_state(new_state)}

@app.post("/apply-t")
def apply_t(data: QubitState):
    vec = prepare_vector(data.state)
    new_state = np.dot(T_GATE, vec)
    return {"new_state": serialize_state(new_state)}

def prepare_vector(state_list):
    clean_list = [complex(x) if isinstance(x, str) else x for x in state_list]
    return np.array(clean_list, dtype=complex)