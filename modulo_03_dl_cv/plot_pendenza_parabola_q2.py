"""
Grafico didattico — Quiz d'ingresso Q2 (cap.03 M3)
f(x) = x^2: pendenza positiva in x=3, negativa in x=-3.

Esecuzione (dalla root del repo):
    py -3 modulo_03_dl_cv/plot_pendenza_parabola_q2.py

Output:
    modulo_03_dl_cv/figures/03_02_pendenza_parabola_q2.png
"""

from __future__ import annotations

import os

import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "figures", "03_02_pendenza_parabola_q2.png")


def f(x: np.ndarray) -> np.ndarray:
    return x**2


def pendenza_locale(x0: float, dx: float = 1.0) -> float:
    """Pendenza approssimata: (f(x0+dx) - f(x0)) / dx (passo verso destra)."""
    return (f(x0 + dx) - f(x0)) / dx


def plot_pendenza_parabola_q2(out_path: str = OUT_PATH, show: bool = False) -> str:
    x = np.linspace(-4.2, 4.2, 400)
    y = f(x)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle(
        "f(x) = x² — La «curva» è la parabola. La pendenza = sali o scendi andando verso destra",
        fontsize=13,
        fontweight="bold",
        y=1.02,
    )

    casi = [
        (-3.0, axes[0], "#1f77b4", "x = −3", "pendenza NEGATIVA (−)"),
        (3.0, axes[1], "#d62728", "x = 3", "pendenza POSITIVA (+)"),
    ]

    for x0, ax, color, titolo_pannello, etichetta_pendenza in casi:
        ax.plot(x, y, color="#333", lw=2.5, label="curva f(x) = x²")
        ax.axhline(0, color="#aaa", lw=0.8)
        ax.axvline(0, color="#aaa", lw=0.8)

        y0 = float(f(x0))
        x1 = x0 + 1.0
        y1 = float(f(x1))

        # Punto sulla curva
        ax.scatter([x0], [y0], s=120, c=color, zorder=5, edgecolors="white", linewidths=1.5)
        ax.annotate(
            f"({x0:g}, {y0:g})",
            (x0, y0),
            textcoords="offset points",
            xytext=(12, 10),
            fontsize=11,
            color=color,
            fontweight="bold",
        )

        # Passo di 1 verso destra (idea geometrica senza derivate)
        ax.annotate(
            "",
            xy=(x1, y1),
            xytext=(x0, y0),
            arrowprops=dict(arrowstyle="-|>", lw=2.5, color=color),
        )
        ax.scatter([x1], [y1], s=70, c=color, alpha=0.5, zorder=4)
        ax.text(
            (x0 + x1) / 2,
            (y0 + y1) / 2,
            "un passo\nverso destra →",
            ha="center",
            va="center",
            fontsize=10,
            color=color,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.85),
        )

        delta_y = y1 - y0
        verso = "SALI" if delta_y > 0 else "SCENDI"
        ax.text(
            0.03,
            0.97,
            f"{titolo_pannello}\n"
            f"f({x0:g})={y0:g}  →  f({x1:g})={y1:g}\n"
            f"Δy = {delta_y:+.0f}  →  {verso}\n"
            f"{etichetta_pendenza}",
            transform=ax.transAxes,
            va="top",
            fontsize=11,
            bbox=dict(boxstyle="round", facecolor="#fff8e1" if delta_y > 0 else "#e3f2fd", alpha=0.95),
        )

        # Tangente (pendenza esatta f'(x)=2x) — solo come riferimento visivo
        pendenza_esatta = 2 * x0
        x_tan = np.linspace(x0 - 1.2, x0 + 1.2, 2)
        y_tan = pendenza_esatta * (x_tan - x0) + y0
        ax.plot(
            x_tan,
            y_tan,
            "--",
            color=color,
            lw=1.8,
            alpha=0.85,
            label=f"tangente (pendenza = {pendenza_esatta:+.0f})",
        )

        ax.set_xlim(-4.2, 4.2)
        ax.set_ylim(-1, 14)
        ax.set_xlabel("x (orizzontale)")
        ax.set_ylabel("f(x) = y (altezza sulla curva)")
        ax.set_title(titolo_pannello, fontsize=12, fontweight="bold")
        ax.legend(loc="lower right", fontsize=9)
        ax.grid(True, alpha=0.25)

    fig.text(
        0.5,
        0.02,
        "In entrambi i punti f(x)=9 (stessa altezza). La pendenza cambia perché "
        "a sinistra la U scende verso destra, a destra sale.",
        ha="center",
        fontsize=10,
        style="italic",
    )

    plt.tight_layout()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fig.savefig(out_path, dpi=130, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)
    return out_path


if __name__ == "__main__":
    path = plot_pendenza_parabola_q2(show=False)
    print(f"Salvato: {path}")
