from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from qiskit.visualization import plot_bloch_multivector
import io
import base64
import matplotlib
matplotlib.use("Agg")
import numpy as np
import random
from qiskit.quantum_info import partial_trace, Statevector

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

I_GATE = np.eye(2)

def generate_bloch_sphere(vec):
    import matplotlib.pyplot as plt
    
    plt.rcParams.update({
        "text.color": "#f8fafc",
        "axes.labelcolor": "#f8fafc",
        "xtick.color": "#f8fafc",
        "ytick.color": "#f8fafc",
    })

    full_state = Statevector(vec)
    images = []

    for i in [1, 0]:
        q_state = partial_trace(full_state, [1 - i])
        fig = plot_bloch_multivector(q_state, font_size=14, figsize=(5,5));
        fig.patch.set_alpha(0.0)

        for ax in fig.axes:
            ax.set_facecolor((0, 0, 0, 0))
            ax.xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
            ax.yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
            ax.zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
            ax.grid(False)

        buf = io.BytesIO()
        fig.savefig(buf, format="png", transparent=True , bbox_inches='tight', pad_inches=0.1, dpi=100)
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode("utf-8")
        images.append(img_str)
        plt.close(fig) 

  
    return images
    
@app.get("/")
def home():
    return {"message": "Quantum Simulator API is running"}

def serialize_state(vec):
    return [str(x) if x.imag != 0 else float(x.real) for x in vec]

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
def apply_cnot(data: QubitState):
    if data.control == 1 and data.target == 0:
        GATE = np.array([[1, 0, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, 0, 1],
                         [0, 0, 1, 0]])
    else:
        GATE = np.array([[1, 0, 0, 0],
                         [0, 0, 0, 1],
                         [0, 0, 1, 0],
                         [0, 1, 0, 0]])
    return apply_gate(data, GATE)

@app.post("/apply-measure")
def apply_measure(data: QubitState):
    vec = prepare_vector(data.state)
    
    ideal_state = vec.copy() 
    noisy_state = apply_noise(vec.copy(), data.noise)
    fidelity = np.abs(np.vdot(ideal_state, noisy_state))**2

    probs = np.abs(noisy_state)**2
    probs /= np.sum(probs)

    outcomes = list(range(len(noisy_state)))
    outcome = random.choices(outcomes, weights=probs)[0]

    new_state = np.zeros_like(noisy_state, dtype=complex)
    new_state[outcome] = 1.0

    visual_data = generate_bloch_sphere(new_state)
    outcome_str = format(outcome, f"0{int(np.log2(len(noisy_state)))}b")
    
    return {
        "new_state": serialize_state(new_state),
        "visualization": visual_data,
        "result": outcome_str,
        "fidelity": float(fidelity) 
    }

def apply_gate(data: QubitState, GATE):
    vec = prepare_vector(data.state)
    
    if GATE.shape == (2, 2):
        if data.target == 0:
            final_gate = np.kron(I_GATE, GATE)
        else:
            final_gate = np.kron(GATE, I_GATE)
    else:
        final_gate = GATE
        
    ideal_state = np.dot(final_gate, vec)
    noisy_state = apply_noise(ideal_state.copy(), data.noise)
    
    fidelity = np.abs(np.vdot(ideal_state, noisy_state))**2

    visual_data = generate_bloch_sphere(noisy_state)

    return {"new_state": serialize_state(noisy_state),
            "visualization": visual_data,
            "fidelity": float(fidelity)
            }
    

def prepare_vector(state_list):
    clean_list = [complex(x) if isinstance(x, str) else x for x in state_list]
    return np.array(clean_list, dtype=complex)

def apply_noise(state, noise_level):
    if noise_level > 0:
        perturbation = np.array([random.gauss(0, 1) + 1j*random.gauss(0, 1) for _ in range(len(state))], dtype=complex)
        perturbation /= np.linalg.norm(perturbation)
        
        state = (1 - noise_level) * state + noise_level * perturbation
        state /= np.linalg.norm(state)
    return state