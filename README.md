# Quantum Engine v1.0: Multi-Qubit Simulator

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
