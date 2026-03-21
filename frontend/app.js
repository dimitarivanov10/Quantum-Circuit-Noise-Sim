let currentState = [1, 0, 0, 0];
const noiseSlider = document.getElementById("noise-slider");
const noiseDisplay = document.getElementById("noise-display");
const fidelityVal = document.getElementById("fidelity-val");
const fidelityBar = document.getElementById("fidelity-bar");
const stateDisplay = document.getElementById("state-display");
const visualPlaceholder = document.getElementById("visual-placeholder");
const sphere0 = document.getElementById("bloch-sphere-0");
const sphere1 = document.getElementById("bloch-sphere-1");
const logList = document.getElementById("log-list");

noiseSlider.oninput = function () {
  noiseDisplay.innerText = this.value;
};

async function applyGate(gateType) {
  console.log(`Executing ${gateType} transformation...`);

  const noiseLevel = noiseSlider.value / 100;
  const target = parseInt(
    document.querySelector('input[name="target-qubit"]:checked').value,
  );
  let control = 0;

  if (gateType === "cnot") {
    control = parseInt(
      document.querySelector('input[name="control-qubit"]:checked').value,
    );
    if (control === target) {
      alert("Error: Control and target qubits must be different!");
      return;
    }
  }

  try {
    const response = await fetch(`http://127.0.0.1:8000/apply-${gateType}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        state: currentState,
        noise: noiseLevel,
        target: target,
        control: control,
      }),
    });

    if (!response.ok) throw new Error("Server communication failed.");

    const data = await response.json();

    currentState = data.new_state;
    updateUI();

    if (data.visualization) {
      sphere0.src = `data:image/png;base64,${data.visualization[0]}`;
      sphere1.src = `data:image/png;base64,${data.visualization[1]}`;
      sphere0.style.display = "block";
      sphere1.style.display = "block";
      visualPlaceholder.style.display = "none";
    }

    if (data.fidelity !== undefined) {
      const percentage = (data.fidelity * 100).toFixed(1);
      fidelityVal.innerText = percentage;
      fidelityBar.style.width = percentage + "%";
    }

    if (gateType === "measure") {
      stateDisplay.classList.add("measuring");
      addToLog(data.result);
      setTimeout(() => stateDisplay.classList.remove("measuring"), 500);
    }
  } catch (error) {
    console.error("Quantum Engine Error:", error);
    alert("Connection Error: Is the Python backend running?");
  }
}

function updateUI() {
  const formatted = currentState.map((num) => {
    if (typeof num === "string") {
      return num.replace(/(\d+\.\d{3})\d+/g, "$1");
    }
    return num.toFixed(3);
  });

  stateDisplay.innerHTML = `
    [${formatted[0]}, ${formatted[1]}]<br>
    [${formatted[2]}, ${formatted[3]}]
  `;
}

function addToLog(result) {
  if (!logList) return;
  const entry = document.createElement("div");
  entry.className = "log-entry";
  entry.innerHTML = `Measured: <span class="log-${result}">|${result}⟩</span>`;
  logList.prepend(entry);
}

function resetCircuit() {
  sphere0.style.display = "none";
  sphere1.style.display = "none";
  visualPlaceholder.style.display = "block";
  logList.innerHTML = "";

  currentState = [1, 0, 0, 0];
  updateUI();

  fidelityVal.innerText = "100";
  fidelityBar.style.width = "100%";

  console.log("System Status: Reset to Ground State |00>");
}

updateUI();
console.log("Quantum Engine Interface v1.0 Loaded.");
