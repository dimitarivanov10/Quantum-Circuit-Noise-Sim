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
    updateUI();
  } catch (error) {
    console.error("Could not connect to the backend:", error);
    alert("Backend error! Make sure your Python terminal is running!");
  }
}
