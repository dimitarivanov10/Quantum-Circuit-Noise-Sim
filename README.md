# Quantum Engine v1.0: Multi-Qubit Simulator

# ⚛️ Quantum Engine v1.0

**Live Demo:** [https://your-username.github.io/quantum-circuit-noise-sim/](https://your-username.github.io/quantum-circuit-noise-sim/)

_Note: The backend is hosted on a free Render instance. If the app doesn't respond immediately, please wait 30 seconds for the server to "wake up" from sleep mode._

## Project Description

**Quantum Engine v1.0** is a full-stack, modular quantum circuit simulator designed to model 2-qubit systems. The platform implements environmental noise models (Gaussian Decoherence), system fidelity analysis, and partial trace visualizations. It provides an interactive dashboard for users to apply quantum gates, observe entanglement, and witness wavefunction collapse through real-time Bloch Sphere projections.

The project is built with a focus on **Software Architecture**, utilizing a decoupled modular approach to separate mathematical computation from the presentation layer.

---

## Technical Stack

### Backend

- **Language**: Python 3.10+
- **Web Framework**: FastAPI (Asynchronous REST API)
- **Quantum Information**: Qiskit (Statevector management and Partial Trace)
- **Mathematical Logic**: NumPy (Linear Algebra and Kronecker Products)
- **Visualization**: Matplotlib (Agg backend for server-side rendering)
- **Server**: Uvicorn

### Frontend

- **Languages**: HTML5, CSS3, JavaScript (ES6+)
- **Architecture**: Event-driven UI updates with asynchronous API polling
- **Styling**: Responsive dark-themed interface with CSS Grid and Flexbox
- **Data Transport**: Base64 encoding for dynamic, server-generated imagery

---

## Core Logic and Features

### 1. Quantum Gate Operations

The simulator supports a variety of fundamental gates. Single-qubit gates are expanded into 2-qubit Hilbert space using the Kronecker product ($\otimes$):

- **Pauli Gates (X, Y, Z)**: Bit-flip and phase-flip operations.
- **Hadamard (H)**: Creates a balanced superposition state.
- **Phase Rotations (S, T)**: 90-degree and 45-degree rotations around the Z-axis.
- **Entanglement (CNOT)**: A 2-qubit operation where the target qubit is flipped only if the control qubit is in state $|1\rangle$

### 2. Environmental Noise and Fidelity

To simulate real-world quantum hardware limitations, the engine implements a **Gaussian Perturbation Model**. When noise is applied, the ideal state vector is mixed with a normalized random complex vector:
$$\psi_{noisy} = (1 - \eta)\psi_{ideal} + \eta\psi_{random}$$
The **System Fidelity** is calculated as the squared overlap between the ideal and noisy states:
$$F = |\langle \psi_{ideal} | \psi_{noisy} \rangle|^2$$

### 3. Measurement and Wavefunction Collapse

The "Measure" operation triggers a probabilistic collapse based on **Born's Rule**. The state vector instantly collapses into one of the four basis states ($|00\rangle, |01\rangle, |10\rangle, |11\rangle$), and the outcome is logged in the color-coded Measurement History.

---

## Project Structure

The codebase is strictly modularized to ensure maintainability and scalability:

```text
.
├── backend/
│   ├── main.py            # API Controller: Routes and request handling
│   ├── quantum_logic.py   # Math Engine: Matrices, noise, and gates
│   ├── visualizer.py      # Graphics: Bloch sphere rendering
│   └── requirements.txt   # Python dependencies
└── frontend/
    ├── index.html         # Application structure
    ├── style.css          # Responsive design and layout
    └── app.js             # Client-side state and API sync
```

## Installation and Setup

### 1. Backend Configuration

Ensure you have **Python 3.10** or higher installed on your system. It is highly recommended to use a virtual environment to avoid library conflicts.

**Navigate to the backend directory:**

```bash
cd backend
```

### Create and activate a virtual enviroment

- **Windows**:

```bash
python -m venv venv
.\venv\Scripts\activate
```

- **macOS/Linux**:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install required dependencies:

```bash
pip install fastapi uvicorn numpy qiskit matplotlib qiskit-aer
```

### 2. Running the Application

#### 1. Start the Backend Server:

In your activated terminal, run:

```bash
uvicorn main:app --reload
```

The API will be active at **http://127.0.0.1:8000**. Keep this terminal window open.

#### 2. Launch the Frontend

Navigate to the **frontend** folder and open **index.html** in any modern web browser.

## User Tutorial: Step-by-Step Guide

#### Experiment 1: Basic Gate Manipulation

1. Ensure **Target Qubit**: **Qubit 0** is selected.
2. Click **Apply X Gate**. This is a bit-flip. Observe the **Amplitude Vector** change from [1, 0, 0, 0] (State $|00\rangle$) to [0, 1, 0, 0] (State $|01\rangle$).
3. The **Bloch Sphere** for Qubit 0 will rotate 180° to the bottom pole.

#### Experiment 2: Creating Superposition (Quantum Randomness)

1. Click **System Reset**.
2. Apply the **H Gate** (Hadamard) to **Qubit 0**.
3. The state is now $|+\rangle$. The Amplitude Vector will show roughly 0.707 for the first two indices. This means there is a 50/50 chance of measuring 0 or 1.
4. The Bloch Sphere vector will point toward the **X-axis**.

#### Experiment 3: Quantum Entanglement (The Bell State)

1. Click **System Reset**.
2. Apply an **H Gate** to **Qubit 0**.
3. Set the **Target Qubit** to **Qubit 1**.
4. Ensure the **Control Qubit** radio button is set to **Ctrl: Q0**.
5. Click **Apply CNOT**.
6. You have created a Bell State $|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$. The Amplitude Vector now only has values for the first ($|00\rangle$) and last ($|11\rangle$) positions.

#### Experiment 4: Simulating Environmental Noise

1. Apply any gate (e.g., the **H Gate**).
2. Slowly move the **Environmental Noise** slider to **15%**.
3. Watch the **System Fidelity** bar. It will drop from 100%, indicating that the quantum state is losing its "purity" due to simulated decoherence.
4. Click **Measure System**. Because of the noise, the result might differ from the ideal mathematical outcome.

## Troubleshooting

- **"Backend Error" Alert**: This usually means the Python server isn't running. Re-run the uvicorn command in your terminal.
- **Port 8000 Conflict**: If another app is using port 8000, run the server on a different port: uvicorn main:app --port 8080.
- **Dependencies**: If the Bloch spheres do not render, ensure you ran the pip install command inside the activated virtual environment.
