from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np

from quantum_logic import(  
    apply_noise, serialize_state, prepare_vector, apply_gate, apply_cnot, apply_measure,
    X_GATE, H_GATE, Y_GATE, Z_GATE, S_GATE, T_GATE, I_GATE
)
from visualizer import generate_bloch_sphere

app = FastAPI()

class QubitState(BaseModel):    
    state: list
    noise: float = 0.0
    target: int = 0
    control: int = 0

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Quantum Simulator API is running"}

@app.post("/apply-x")
def apply_x(data: QubitState):
    result = apply_gate(data, X_GATE)
    result["visualization"] = generate_bloch_sphere(prepare_vector(result["new_state"]))
    return result

@app.post("/apply-h")
def apply_h(data: QubitState):
    result = apply_gate(data, H_GATE)
    result["visualization"] = generate_bloch_sphere(prepare_vector(result["new_state"]))
    return result

@app.post("/apply-y")
def apply_y(data: QubitState):
    result = apply_gate(data, Y_GATE)
    result["visualization"] = generate_bloch_sphere(prepare_vector(result["new_state"]))
    return result

@app.post("/apply-z")
def apply_z(data: QubitState):
    result = apply_gate(data, Z_GATE)
    result["visualization"] = generate_bloch_sphere(prepare_vector(result["new_state"]))
    return result

@app.post("/apply-s")
def apply_s(data: QubitState):
    result = apply_gate(data, S_GATE)
    result["visualization"] = generate_bloch_sphere(prepare_vector(result["new_state"]))
    return result

@app.post("/apply-t")
def apply_t(data: QubitState):
    result = apply_gate(data, T_GATE)
    result["visualization"] = generate_bloch_sphere(prepare_vector(result["new_state"]))
    return result

@app.post("/apply-cnot")
def apply_cnot_gate(data: QubitState):
    result = apply_cnot(data)
    result["visualization"] = generate_bloch_sphere(prepare_vector(result["new_state"]))
    return result 

@app.post("/apply-measure") 
def measure(data: QubitState):
    result = apply_measure(data)
    result["visualization"] = generate_bloch_sphere(prepare_vector(result["new_state"]))
    return result 
    