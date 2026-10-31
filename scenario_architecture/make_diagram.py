"""Draws system_architecture.png (Task A2). Run: python make_diagram.py"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(15, 7.5))
ax.set_xlim(0, 15)
ax.set_ylim(0, 7.5)
ax.axis("off")


def box(x, y, w, h, text, fc="#e8f1fb", ec="#2b5c8a", fs=9, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                                fc=fc, ec=ec, lw=1.5))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            fontweight="bold" if bold else "normal")


def arrow(x1, y1, x2, y2, label="", dashed=False, dy=0.12):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", lw=1.5, color="#333",
                                linestyle="--" if dashed else "-"))
    if label:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + dy, label, ha="center",
                fontsize=7.5, color="#333")


# Truck edge node boundary
ax.add_patch(FancyBboxPatch((0.2, 0.4), 9.1, 6.6, boxstyle="round,pad=0.05",
                            fc="#fafafa", ec="#555", lw=2, ls="--"))
ax.text(0.4, 6.7, "TRUCK: Edge node (Raspberry Pi 5 + AI HAT+, 7.5 W, 12 V via DC-DC)",
        fontsize=10, fontweight="bold")

# Sensors
box(0.5, 5.0, 1.9, 0.8, "Temperature\n1 Hz", fc="#fff3d6", ec="#b07a00")
box(0.5, 3.8, 1.9, 0.8, "Vibration (3-axis)\n500 Hz raw, RMS 0.5 Hz", fc="#fff3d6", ec="#b07a00")
box(0.5, 2.6, 1.9, 0.8, "Door sensor\nOPEN / CLOSE events", fc="#fff3d6", ec="#b07a00")
ax.text(1.45, 5.95, "Sensors", ha="center", fontsize=9, fontweight="bold")

# Broker
box(3.2, 3.5, 1.9, 1.6, "Local MQTT broker\n(Mosquitto, localhost)\nlogibridge/trucks/\n{truck_id}/...", fc="#e3f5e1", ec="#2e7d32")
for y in (5.4, 4.2, 3.0):
    arrow(2.4, y, 3.2, 4.3 if y != 3.0 else 3.7)

# Pipeline
box(5.9, 4.9, 3.1, 1.1, "Preprocessing\n5-sample moving avg, 30 s / 10 s windows,\n6-feature vector, normalise (training_stats.npy)", fs=7)
box(5.9, 3.5, 3.1, 1.0, "Inference service (Docker)\nMLP TFLite INT8: Normal / Warning / Critical", fs=8, bold=True)
box(5.9, 2.2, 3.1, 0.9, "Alert engine\nin-cab alert + publish to\n.../inference topic", fs=8)
arrow(5.1, 4.6, 5.9, 5.4)
arrow(7.45, 4.9, 7.45, 4.5)
arrow(7.45, 3.5, 7.45, 3.1)

# Local log + monitoring
box(3.2, 1.0, 2.2, 1.0, "Local alert log\n(append-only, offline store)", fc="#f3e5f5", ec="#6a1b9a", fs=8)
box(6.2, 0.5, 2.7, 0.8, "Drift monitor (PSI) +\nAnsible-managed OTA agent", fc="#f3e5f5", ec="#6a1b9a", fs=8)
arrow(5.9, 2.5, 5.4, 1.7)
arrow(7.55, 1.3, 7.55, 2.2, dashed=True)

# Uplink
box(10.3, 2.4, 1.6, 1.2, "Cellular uplink\nM2M SIM\n(store-and-forward,\nTLS)", fc="#ffe0e0", ec="#b71c1c", fs=8)
arrow(5.4, 1.5, 10.3, 2.5, label="", dashed=True)
ax.text(9.6, 1.45, "log sync when\ncoverage returns", fontsize=7.5, ha="center")
arrow(9.0, 2.65, 10.3, 3.0)

# Ops centre
box(13.0, 1.6, 1.8, 3.4, "Operations\ncentre backend\n\nAlert dashboard\nChain-of-custody\nlogs\nOTA / model\nregistry", fc="#e1e8f5", ec="#1a237e", fs=8.5, bold=True)
arrow(11.9, 3.3, 13.0, 3.3)
ax.text(12.45, 3.45, "alerts +\nlog batch", fontsize=7.5, ha="center")
arrow(13.0, 2.4, 11.9, 2.4)
ax.text(12.45, 2.0, "OTA model", fontsize=7.5, ha="center")

ax.text(7.5, 0.1, "LogiEdge: all inference runs on the truck and works offline; the uplink carries only alerts, "
        "heartbeats and log batches (about 0.15 MB/day vs about 519 MB/day raw).",
        ha="center", fontsize=8.5, style="italic")
plt.savefig("system_architecture.png", dpi=150, bbox_inches="tight")
