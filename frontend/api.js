export async function postGateRequest(gateType, payload) {
  const url = `https://quantum-circuit-noise-sim.onrender.com/apply-${gateType}`;
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
  return await response.json();
}
