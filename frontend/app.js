let currentState = [1, 0];
const noiseSliderDivEl = document.getElementById("noise-slider");
const noiseDisplayDivEl = document.getElementById("noise-display");

noiseSlider.oninput = function () {
  noiseDisplay.innerText = this.value;
};

async function applyGate(gateType) {
  console.log(`Sending request to apply ${gateType} gate...`);
  
  const url = `http://127.0.0.1:8000/apply-${gateType}`;
  const noiseLevel = noiseSlider.value / 100;

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ state: currentState, noise: noiseLevel }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    currentState = data.new_state;
    updateUI();
    if (data.visualization) {
      const sphereImgEl = document.getElementById("bloch-sphere");
      const visualPlaceholderEl = document.getElementById("visual-placeholder");

      sphereImgEl.src = `data:image/png;base64,${data.visualization}`;
      sphereImgEl.style.display = "block";
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
  currentState = [1, 0];
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
  document.getElementById("state-display").innerText =
    `[${formatted.join(", ")}]`;
}
console.log("Quantum App.js loaded successfully!");
