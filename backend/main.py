from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from qiskit.visualization import plot_bloch_multivector
import io
import base64
import matplotlib
matplotlib.use("Agg")
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

def generate_bloch_sphere(vec):
    import matplotlib.pyplot as plt
    
    # 1. Set global dark theme for the text/axes
    plt.rcParams.update({
        "text.color": "#f8fafc",
        "axes.labelcolor": "#f8fafc",
        "xtick.color": "#f8fafc",
        "ytick.color": "#f8fafc",
        "figure.facecolor": "#1e293b",
        "axes.facecolor": "#1e293b"
    })

    # 2. Call the function WITHOUT 'style'
    # We pass the vector color directly using 'color'
    fig = plot_bloch_multivector(vec, font_size=14)
    
    # 3. Manually style the axes and panes
    fig.patch.set_facecolor('#1e293b')
    for ax in fig.axes:
        ax.set_facecolor('#1e293b')
        # Make the 3D grid panes transparent
        ax.xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
        ax.yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
        ax.zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
        # Hide the grid lines for a cleaner "hologram" look
        ax.grid(False)

    buf = io.BytesIO()
    # Save with the dark background
    fig.savefig(buf, format="png", facecolor='#1e293b', bbox_inches='tight')
    buf.seek(0)

    img_str = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig) 
    return img_str
    
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


def apply_gate(data: QubitState, GATE):
    vec = prepare_vector(data.state)
    new_state = np.dot(GATE, vec)
    visual_data = generate_bloch_sphere(new_state)
    return {"new_state": serialize_state(new_state),
            "visualization": visual_data}
    

def prepare_vector(state_list):
    clean_list = [complex(x) if isinstance(x, str) else x for x in state_list]
    return np.array(clean_list, dtype=complex)