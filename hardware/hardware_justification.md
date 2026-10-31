# B: Hardware Selection and Justification

## B1: Constraint Triangle

The three vertices are **Performance (accuracy and latency)**, **Power/thermal**, and **Cost**. The workload is a tiny 6-feature MLP (INT8 model about 280 KB) that must answer within 90 s, so performance is easy for every option. The dominant vertex is therefore **Power and Cost at fleet scale**, subject to the node being able to run the software stack (Linux, Mosquitto, Docker, Ansible) that the architecture depends on.

| | Option 1: Pi 5 + AI HAT+ | Option 2: Jetson Orin Nano Super | Option 3: STM32H7 MCU |
|---|---|---|---|
| Compute | CPU about 16 GFLOP/s, plus 13 TOPS NPU | 67 TOPS GPU | Cortex-M7, no NPU |
| Power vs 10 W AI budget | 7.5 W, **within** | 15 W, **exceeds by 50%** | 0.4 W, within |
| Unit cost | ₹15,000 | ₹45,000 | ₹3,500 |
| 85-truck pilot | ₹12.75 lakh | ₹38.25 lakh | ₹2.98 lakh |
| 265-truck scale-out | ₹39.75 lakh | ₹119.25 lakh | ₹9.28 lakh |
| Runs Linux, Docker, Mosquitto, Ansible | Yes | Yes | No |
| 90 s latency | Met with large margin | Met | Met for the model alone |

**Recommendation: Option 1 (Raspberry Pi 5 + AI HAT+).**

- **For:** 7.5 W fits the 10 W budget on the 12 V supply via DC-DC converter, with headroom. It runs the full stack the project specifies: a local Mosquitto broker, a Docker inference container, a local alert log with store-and-forward, and Ansible-managed OTA. The Roofline analysis (B2) shows inference takes about 2.8 ms against a 90 s SLA. It costs ₹39.75 lakh at 265 trucks, about a third of the Jetson.
- **Against Option 2 (Jetson):** 15 W breaks the 10 W AI power budget and needs a bigger DC-DC converter and thermal design in a truck cab. It costs 3× more (₹119 lakh at scale) and its 67 TOPS are unusable by a 280 KB MLP, so the money buys nothing.
- **Against Option 3 (STM32H7):** It is cheapest and lowest power, and could run the bare model, but it cannot run Linux, a Mosquitto broker, Docker containers or Ansible, so the MQTT, container-based OTA and idempotent deployment design would have to be rewritten as bare-metal firmware. It also has little memory for the local log, buffering 30 s windows and store-and-forward across 90-minute outages. The saving (about ₹30 lakh at scale) does not justify losing manageability for pharmaceutical-grade monitoring.

The AI HAT+ is optional for this model; the Pi 5 CPU alone suffices, so it could be dropped to cut unit cost if the benchmarks confirm it.

## B2: Arithmetic Intensity and Roofline

Given: 45 MFLOPs and 18 MB moved per inference; Pi 5 CPU peak 16 GFLOP/s, memory bandwidth 12 GB/s.

- **Arithmetic Intensity** = 45 × 10⁶ FLOP / 18 × 10⁶ B = **2.5 FLOP/byte**
- **Ridge point** = 16 × 10⁹ / 12 × 10⁹ = **1.33 FLOP/byte**
- Attainable performance = min(16 GFLOP/s, 12 GB/s × 2.5 = 30 GFLOP/s) = **16 GFLOP/s**
- Since 2.5 > 1.33, the model sits to the right of the ridge: **compute-bound**.
- Cross-check: compute time = 45 MFLOP / 16 GFLOP/s = 2.81 ms; memory time = 18 MB / 12 GB/s = 1.5 ms. Compute dominates, so inference takes about 2.8 ms.

**Optimisation implied:** because the model is compute-bound, raising memory bandwidth alone will not help. Latency improves by cutting FLOPs (structured pruning, variant M3) and by raising effective compute throughput (INT8 quantisation uses NEON integer SIMD with more operations per instruction, or offload to the Hailo NPU). Quantisation also cuts bytes 4×. Either way, 2.8 ms is about four orders of magnitude below the 90 s SLA.
