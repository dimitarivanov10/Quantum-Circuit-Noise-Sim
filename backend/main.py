from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import random

from quantum_logic import(
    prepare_vector, apply_noise, serialize_state, prepare_vector, apply_gate, apply_cnot,
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
    return apply_gate(data, X_GATE)

@app.post("/apply-h")
def apply_h(data: QubitState):
    return apply_gate(data, H_GATE)

@app.post("/apply-y")
def apply_y(data: QubitState):
    return apply_gate(data, Y_GATE)

@app.post("/apply-z")
def apply_z(data: QubitState):
    return apply_gate(data, Z_GATE)

@app.post("/apply-s")
def apply_s(data: QubitState):
    return apply_gate(data, S_GATE)

@app.post("/apply-t")
def apply_t(data: QubitState):
    return apply_gate(data, T_GATE)

@app.post("/apply-cnot")


@app.post("/apply-measure")
    