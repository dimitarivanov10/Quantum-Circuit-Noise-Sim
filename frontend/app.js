let currentState = [1, 0, 0, 0];
const noiseSliderDivEl = document.getElementById("noise-slider");
const noiseDisplayDivEl = document.getElementById("noise-display");

noiseSliderDivEl.oninput = function () {
  noiseDisplayDivEl.innerText = this.value;
};

async function applyGate(gateType) {
  console.log(`Sending request to apply ${gateType} gate...`);

  const url = `http://127.0.0.1:8000/apply-${gateType}`;
  const noiseLevel = noiseSliderDivEl.value / 100;

  let target = 0;
  const targetEl = document.querySelector('input[name="target-qubit"]:checked');
  if (targetEl) target = parseInt(targetEl.value);

  let control = 0;
  if (gateType === 'cnot') {
    const controlEl = document.querySelector('input[name="control-qubit"]:checked');
    if (controlEl) {
      control = parseInt(controlEl.value);
      if (control === target) {
        alert("Control and target qubits must be different for CNOT!");
        return;
      }
    }
  }

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ state: currentState, noise: noiseLevel, target: target, control: control }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    currentState = data.new_state;
    updateUI();
    if (data.visualization && Array.isArray(data.visualization)) {
      const sphere0ImgEl = document.getElementById("bloch-sphere-0");
      const sphere1ImgEl = document.getElementById("bloch-sphere-1");
      const visualPlaceholderEl = document.getElementById("visual-placeholder");

      sphere0ImgEl.src = `data:image/png;base64,${data.visualization[0]}`;
      sphere1ImgEl.src = `data:image/png;base64,${data.visualization[1]}`;
      visualPlaceholderEl.style.display = "none";
    }

    if (gateType === "measure") {
      const stateDisplayDivEl = document.getElementById("state-display");
      stateDisplayDivEl.classList.add("measuring");

      addToLog(data.result);
      setTimeout(() => stateDisplayDivEl.classList.remove("measuring"), 500);
    }
  } catch (error) {
    console.error("Could not connect to the backend:", error);
    alert("Backend error! Make sure your Python terminal is running!");
  }
}

function addToLog(result) {
  const logListEl = document.getElementById("log-list");
  if (!logListEl) return;

  const entryDivEl = document.createElement("div");
  entryDivEl.className = "log-entry";
  entryDivEl.innerHTML = `Measured: <span class="log-${result}">|${result}⟩</span>`;
  logListEl.prepend(entryDivEl);
}

function resetCircuit() {
  const sphereImgEl = document.getElementById("bloch-sphere");
  const visualPlaceholderEl = document.getElementById("visual-placeholder");
  const logListEl = document.getElementById("log-list");

  sphereImgEl.style.display = "none";
  visualPlaceholderEl.style.display = "block";
  currentState = [1, 0, 0, 0];
  updateUI();
  if (logListEl) {
    logListEl.innerHTML = "";
  }
  console.log("System reboot: Vector and logs cleared");
}

function updateUI() {
  const formatted = currentState.map((num) => {
    return typeof num === "number" ? num.toFixed(3) : num;
  });
  document.getElementById("state-display").innerHTML =
    `[${formatted[0]}, ${formatted[1]}]<br>[${formatted[2]}, ${formatted[3]}]`;
}
console.log("Quantum App.js loaded successfully!");
