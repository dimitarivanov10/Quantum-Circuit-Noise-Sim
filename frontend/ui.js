export function updateFidelityUI(fidelity) {
  if (fidelity === undefined) return;
  const percentage = (fidelity * 100).toFixed(1);
  document.getElementById("fidelity-val").innerText = percentage;
  document.getElementById("fidelity-bar").style.width = percentage + "%";
}

export function updateVisualizer(visualization) {
  const sphere0ImgEl = document.getElementById("bloch-sphere-0");
  const sphere1ImgEl = document.getElementById("bloch-sphere-1");
  const placeholder = document.getElementById("visual-placeholder");

  if (visualization && visualization.length === 2) {
    sphere0ImgEl.src = `data:image/png;base64,${visualization[0]}`;
    sphere1ImgEl.src = `data:image/png;base64,${visualization[1]}`;
    sphere0ImgEl.style.display = "block";
    sphere1ImgEl.style.display = "block";
    placeholder.style.display = "none";
  }
}

export function formatVector(state) {
  return state.map((num) => {
    if (typeof num === "string") return num.replace(/(\d+\.\d{3})\d+/g, "$1");
    return num.toFixed(3);
  });
}
