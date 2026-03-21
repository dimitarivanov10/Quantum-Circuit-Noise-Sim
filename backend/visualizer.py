import io
import base64
import matplotlib
matplotlib.use("Agg") 
import matplotlib.pyplot as plt
from qiskit.visualization import plot_bloch_multivector
from qiskit.quantum_info import partial_trace, Statevector

def generate_bloch_sphere(vec):
    import matplotlib.pyplot as plt
    
    plt.rcParams.update({
        "text.color": "#f8fafc",
        "axes.labelcolor": "#f8fafc",
        "xtick.color": "#f8fafc",
        "ytick.color": "#f8fafc",
    })

    full_state = Statevector(vec)
    images = []

    for i in [1, 0]:
        q_state = partial_trace(full_state, [1 - i])
        fig = plot_bloch_multivector(q_state, font_size=14, figsize=(5,5));
        fig.patch.set_alpha(0.0)

        for ax in fig.axes:
            ax.set_facecolor((0, 0, 0, 0))
            ax.xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
            ax.yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
            ax.zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
            ax.grid(False)

        buf = io.BytesIO()
        fig.savefig(buf, format="png", transparent=True , bbox_inches='tight', pad_inches=0.1, dpi=100)
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode("utf-8")
        images.append(img_str)
        plt.close(fig) 

  
    return images
    
