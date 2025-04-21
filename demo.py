import numpy as np
import matplotlib.pyplot as plt

def parametric_curve(t: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    # Example: a circle
    x = np.cos(t)
    y = np.sin(t)
    return x, y

def draw_tick_marks_on_curve(t: np.ndarray, tick_interval: float, tick_length: float):
    x, y = parametric_curve(t)

    # Compute tangent vectors
    dx = np.gradient(x, t)
    dy = np.gradient(y, t)
    tangent_length = np.hypot(dx, dy)
    dx /= tangent_length
    dy /= tangent_length

    # Compute normals (perpendicular to tangents)
    nx = -dy
    ny = dx

    # Approximate arc length and select tick mark indices
    arc_length = np.cumsum(np.hypot(np.diff(x), np.diff(y)))
    arc_length = np.insert(arc_length, 0, 0)
    tick_indices = [0]
    last_tick_pos = 0.0

    for i, s in enumerate(arc_length):
        if s - last_tick_pos >= tick_interval:
            tick_indices.append(i)
            last_tick_pos = s

    # Plot the parametric curve
    plt.plot(x, y, label="Parametric Curve")

    # Plot tick marks and labels
    for i in tick_indices:
        x0 = x[i]
        y0 = y[i]
        tx = nx[i] * tick_length / 2
        ty = ny[i] * tick_length / 2
        plt.plot([x0 - tx, x0 + tx], [y0 - ty, y0 + ty], color="red")

        # Add label slightly offset along normal
        label_x = x0 + nx[i] * tick_length
        label_y = y0 + ny[i] * tick_length
        plt.text(label_x, label_y, f"t={t[i]:.2f}", fontsize=8,
                 ha='center', va='center')

    plt.axis("equal")
    plt.title("Parametric Curve with Tick Marks and Labels")
    plt.legend()
    plt.show()

# Example usage
t_values = np.linspace(0, 2 * np.pi, 1000)
draw_tick_marks_on_curve(t_values, tick_interval=0.5, tick_length=0.1)

