"""
Genera PNG didattici per cap.01 Ponte Matematico (vettori, coseno, distanza, normalizzazione).
Esecuzione: dalla root del repo
  py -3 ponte_matematico_m2_m3/genera_infografiche_png.py
Output: ponte_matematico_m2_m3/figures/*.png

Ogni figura racconta UNA sola idea, con numeri visibili e layout a pannelli affiancati.
"""

from __future__ import annotations

import os

import matplotlib.pyplot as plt
import numpy as np


HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "figures")


def _arrow(ax, x0, y0, dx, dy, color, label=None, label_offset=(0.1, 0.15)):
    ax.annotate(
        "",
        xy=(x0 + dx, y0 + dy),
        xytext=(x0, y0),
        arrowprops=dict(arrowstyle="-|>", lw=2.5, color=color),
    )
    if label:
        ax.text(
            x0 + dx + label_offset[0],
            y0 + dy + label_offset[1],
            label,
            fontsize=11,
            color=color,
            fontweight="bold",
        )


def _setup_axes(ax, xlim, ylim, title=None):
    ax.set_aspect("equal")
    ax.axhline(0, color="#bbb", lw=1)
    ax.axvline(0, color="#bbb", lw=1)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xticks([])
    ax.set_yticks([])
    if title:
        ax.set_title(title, fontsize=12)


def _cosine(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


# ============================================================
# Fig 1 — Coseno: stesso vettore, angoli diversi (3 casi)
# ============================================================

def fig_coseno_spettro():
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.5))
    fig.suptitle("Coseno tra due vettori = quanto puntano nella stessa direzione", fontsize=13)

    casi = [
        ("Direzione simile", np.array([3.0, 0.5]), np.array([2.8, 1.2]), "#1f77b4", "#ff7f0e"),
        ("Quasi perpendicolari", np.array([3.0, 0.2]), np.array([0.5, 2.8]), "#1f77b4", "#ff7f0e"),
        ("Direzioni opposte", np.array([3.0, 0.5]), np.array([-2.8, -0.6]), "#1f77b4", "#ff7f0e"),
    ]

    for ax, (titolo, a, b, ca, cb) in zip(axes, casi):
        cos = _cosine(a, b)
        _setup_axes(ax, (-3.5, 3.5), (-3.5, 3.5), titolo)
        _arrow(ax, 0, 0, a[0], a[1], ca, "a")
        _arrow(ax, 0, 0, b[0], b[1], cb, "b")
        ax.text(
            0.5,
            -3.1,
            f"cos(a, b) = {cos:+.2f}",
            fontsize=12,
            fontweight="bold",
            ha="center",
            transform=ax.transData,
            bbox=dict(boxstyle="round", fc="#fff8d6", ec="#aaaaaa"),
        )

    fig.tight_layout(rect=(0, 0, 1, 0.94))
    path = os.path.join(OUT_DIR, "01_coseno_allineamento.png")
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


# ============================================================
# Fig 2 — Perpendicolari (focus su 90°)
# ============================================================

def fig_perpendicolari():
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    _setup_axes(ax, (-0.5, 3.5), (-0.5, 3.5), "Vettori perpendicolari → coseno = 0")

    a = np.array([2.5, 0.0])
    b = np.array([0.0, 2.5])
    _arrow(ax, 0, 0, a[0], a[1], "#1f77b4", "a = [2.5, 0]")
    _arrow(ax, 0, 0, b[0], b[1], "#ff7f0e", "b = [0, 2.5]")

    arc_theta = np.linspace(0, np.pi / 2, 50)
    r = 0.4
    ax.plot(r * np.cos(arc_theta), r * np.sin(arc_theta), color="#444", lw=1.5)
    ax.text(0.55, 0.55, "90°", fontsize=11, color="#444")

    ax.text(
        1.8,
        -0.35,
        f"cos(a, b) = {_cosine(a, b):+.2f}",
        fontsize=12,
        fontweight="bold",
        ha="center",
        bbox=dict(boxstyle="round", fc="#fff8d6", ec="#aaaaaa"),
    )

    fig.tight_layout()
    path = os.path.join(OUT_DIR, "02_coseno_perpendicolare.png")
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


# ============================================================
# Fig 3 — Distanza euclidea: due punti vicini vs due punti lontani
# ============================================================

def fig_distanza_euclidea():
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Distanza euclidea = lunghezza del segmento tra due punti", fontsize=13)

    coppie = [
        ("Punti vicini (distanza piccola)", np.array([1.0, 1.5]), np.array([1.6, 2.0])),
        ("Punti lontani (distanza grande)", np.array([0.5, 0.5]), np.array([3.5, 3.2])),
    ]

    for ax, (titolo, p, q) in zip(axes, coppie):
        _setup_axes(ax, (0, 4), (0, 4), titolo)
        d = float(np.linalg.norm(p - q))
        ax.plot([p[0], q[0]], [p[1], q[1]], "o-", color="#2ca02c", lw=2.5, markersize=8)
        ax.text(p[0] + 0.05, p[1] - 0.25, f"P = ({p[0]}, {p[1]})", fontsize=10)
        ax.text(q[0] - 1.0, q[1] + 0.15, f"Q = ({q[0]}, {q[1]})", fontsize=10)
        ax.text(
            2.0,
            0.25,
            f"distanza = {d:.2f}",
            fontsize=12,
            fontweight="bold",
            ha="center",
            bbox=dict(boxstyle="round", fc="#fff8d6", ec="#aaaaaa"),
        )

    fig.tight_layout(rect=(0, 0, 1, 0.94))
    path = os.path.join(OUT_DIR, "03_distanza_euclidea.png")
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


# ============================================================
# Fig 4 — Normalizzazione: prima vs dopo, sul cerchio unitario
# ============================================================

def fig_normalizzazione():
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))
    fig.suptitle(
        "Normalizzare = portare QUALSIASI vettore a lunghezza 1 (mantiene la direzione, scarta la lunghezza)",
        fontsize=13,
    )

    theta = np.linspace(0, 2 * np.pi, 200)

    v = np.array([3.0, 4.0])
    w = np.array([6.0, 8.0])
    nv = float(np.linalg.norm(v))
    nw = float(np.linalg.norm(w))
    uv = v / nv
    uw = w / nw

    ax_l, ax_c, ax_r = axes

    _setup_axes(ax_l, (-1.5, 10), (-1.5, 10), "PRIMA — v=(3,4) e w=(6,8): w è 2·v")
    ax_l.plot(np.cos(theta), np.sin(theta), color="#cccccc", lw=1)
    _arrow(ax_l, 0, 0, v[0], v[1], "#1f77b4", f"v\n||v||={nv:.0f}")
    _arrow(ax_l, 0, 0, w[0], w[1], "#ff7f0e", f"w\n||w||={nw:.0f}")
    ax_l.text(
        4.5,
        -1.2,
        "Stessa direzione, lunghezze diverse",
        fontsize=10,
        ha="center",
        color="#444",
    )

    _setup_axes(ax_c, (-1.5, 1.5), (-1.5, 1.5), "DOPO (v e w) — coincidono sullo STESSO punto")
    ax_c.plot(np.cos(theta), np.sin(theta), color="#888", lw=1.2)
    _arrow(ax_c, 0, 0, uv[0], uv[1], "#1f77b4", f"v/||v|| = ({uv[0]:.1f}, {uv[1]:.1f})", label_offset=(-0.6, 0.1))
    ax_c.plot(uw[0], uw[1], "o", color="#ff7f0e", markersize=12, mfc="none", mew=2)
    ax_c.text(
        uw[0] - 0.05,
        uw[1] - 0.35,
        "w/||w|| (cerchio arancione)\n→ stesso punto di v/||v||",
        fontsize=9,
        color="#ff7f0e",
        ha="left",
    )
    ax_c.text(
        0.0,
        -1.4,
        "Direzione uguale ⇒ vettore unitario UGUALE",
        fontsize=10,
        ha="center",
        color="#444",
    )

    a = np.array([3.0, 0.5])
    b = np.array([0.5, 2.5])
    ua = a / np.linalg.norm(a)
    ub = b / np.linalg.norm(b)

    _setup_axes(ax_r, (-1.5, 1.5), (-1.5, 1.5), "DOPO (a e b) — direzioni diverse, punti diversi")
    ax_r.plot(np.cos(theta), np.sin(theta), color="#888", lw=1.2)
    _arrow(ax_r, 0, 0, ua[0], ua[1], "#2ca02c", f"a/||a|| = ({ua[0]:.2f}, {ua[1]:.2f})", label_offset=(-0.55, -0.25))
    _arrow(ax_r, 0, 0, ub[0], ub[1], "#9467bd", f"b/||b|| = ({ub[0]:.2f}, {ub[1]:.2f})", label_offset=(-0.5, 0.05))
    ax_r.text(
        0.0,
        -1.4,
        "Entrambi sul cerchio, ma in punti diversi\n(la normalizzazione funziona comunque)",
        fontsize=10,
        ha="center",
        color="#444",
    )

    fig.tight_layout(rect=(0, 0, 1, 0.93))
    path = os.path.join(OUT_DIR, "04_normalizza_norma1.png")
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


# ============================================================
# Fig 5 — Coseno vs distanza: stessa direzione, distanze molto diverse
# ============================================================

def fig_coseno_vs_distanza():
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle(
        "Stessa direzione (coseno alto) ≠ stessa posizione (distanza piccola)",
        fontsize=13,
    )

    a = np.array([1.0, 0.5])
    b_corto = np.array([1.2, 0.6])
    b_lungo = np.array([4.5, 2.25])

    for ax, b, titolo in [
        (axes[0], b_corto, "Stessa direzione, vicini"),
        (axes[1], b_lungo, "Stessa direzione, lontani"),
    ]:
        _setup_axes(ax, (-0.5, 5.5), (-0.5, 3.5), titolo)
        _arrow(ax, 0, 0, a[0], a[1], "#1f77b4", "a")
        _arrow(ax, 0, 0, b[0], b[1], "#ff7f0e", "b")
        cos = _cosine(a, b)
        dist = float(np.linalg.norm(a - b))
        ax.text(
            2.5,
            -0.35,
            f"cos = {cos:+.2f}    distanza = {dist:.2f}",
            fontsize=11,
            fontweight="bold",
            ha="center",
            bbox=dict(boxstyle="round", fc="#fff8d6", ec="#aaaaaa"),
        )

    fig.tight_layout(rect=(0, 0, 1, 0.94))
    path = os.path.join(OUT_DIR, "05_coseno_vs_distanza.png")
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    paths = [
        fig_coseno_spettro(),
        fig_perpendicolari(),
        fig_distanza_euclidea(),
        fig_normalizzazione(),
        fig_coseno_vs_distanza(),
    ]
    print("Creati:")
    for p in paths:
        print(" ", p)


if __name__ == "__main__":
    main()
