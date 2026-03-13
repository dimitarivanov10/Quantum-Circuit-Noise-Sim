# Quantum Circuit Simulator

## Project Description
The Quantum Circuit Simulator is a full-stack web application designed to simulate basic quantum computing operations on a single qubit. The project provides a visual and interactive environment for understanding quantum state manipulation through various quantum gates.

A key feature of the application is the real-time visualization of the qubit's state on a Bloch Sphere. Users can apply fundamental quantum gates to observe how the state vector rotates in 3D space and perform measurements to witness wavefunction collapse based on quantum probability.

## Tech Stack

### Backend
* **Language**: Python 3.10+
* **Framework**: FastAPI
* **Quantum Computation**: Qiskit
* **Mathematics and Logic**: NumPy
* **Visualization Engine**: Matplotlib
* **Server**: Uvicorn

### Frontend
* **Languages**: HTML5, CSS3, JavaScript (ES6+)
* **Styling**: Custom CSS with a dark-themed, glassmorphism-inspired UI
* **Image Handling**: Base64 encoding for dynamic image rendering

## Project Structure
The project is organized into two main directories:
* **backend/**: Contains `main.py`, which handles the API endpoints for gate applications and Bloch Sphere generation.
* **frontend/**: Contains `index.html`, `style.css`, and `app.js` for the user interface and client-side logic.

## Installation and Setup

### 1. Prerequisites
Ensure Python is installed on your system. You will also need to have `pip` available to install dependencies.

### 2. Virtual Environment Setup
It is recommended to use a virtual environment to manage dependencies.

**Windows**
```powershell
# Create the environment
python -m venv venv

# Activate the environment
.\venv\Scripts\Activate.ps1
