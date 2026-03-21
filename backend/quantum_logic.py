import numpy as np
import random

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

def serialize_state(vec):
    return [str(x) if x.imag != 0 else float(x.real) for x in vec]

def apply_noise(state, noise_level):
    if noise_level > 0:
        perturbation = np.array([random.gauss(0, 1) + 1j*random.gauss(0, 1) for _ in range(len(state))], dtype=complex)
        perturbation /= np.linalg.norm(perturbation)
        
        state = (1 - noise_level) * state + noise_level * perturbation
        state /= np.linalg.norm(state)
    return state

def prepare_vector(state_list):
    clean_list = [complex(x) if isinstance(x, str) else x for x in state_list]
    return np.array(clean_list, dtype=complex)

def apply_measure(data):
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

    outcome_str = format(outcome, f"0{int(np.log2(len(noisy_state)))}b")
    
    return {
        "new_state": serialize_state(new_state),
        "result": outcome_str,
        "fidelity": float(fidelity) 
    }

def apply_cnot(data):
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

def apply_gate(data, GATE):
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


    return {"new_state": serialize_state(noisy_state),
            "fidelity": float(fidelity)
            }

