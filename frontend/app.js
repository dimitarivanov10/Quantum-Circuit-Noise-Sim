let currentState = [1, 0];

async function applyGate(gateType) {
  console.log(`Sending request to apply ${gateType} gate...`);

  const url = `http://127.0.0.1:8000/apply-${gateType}`;

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ state: currentState }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    currentState = data.new_state;
    if (data.visualization) {
      document.getElementById("bloch-sphere").src =
        `data:image/png;base64,${data.visualization}`;
    }

    updateUI();
  } catch (error) {
    console.error("Could not connect to the backend:", error);
    alert("Backend error! Make sure your Python terminal is running!");
  }
}

function resetCircuit() {
  currentState = [1, 0];
  updateUI();
  console.log("Amplitude vector reset to [1.000, 0.000]");
}

function updateUI() {
  const formatted = currentState.map((num) => {
    return typeof num === "number" ? num.toFixed(3) : num;
  });
  document.getElementById("state-display").innerText =
    `[${formatted.join(", ")}]`;
}
console.log("Quantum App.js loaded successfully!");
