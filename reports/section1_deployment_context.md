# 1. FreightBridge Deployment Context

FreightBridge runs 85 refrigerated trucks for the pilot (265 vehicles at full scale). A refrigeration failure warms cargo by about 1 °C/min, and one undetected failure already cost ₹28 lakh in spoiled vaccines. LogiEdge therefore classifies cargo state (Normal / Warning / Critical) on the truck itself. Four constraints force this edge-first design.

**Latency.** The SLA is 90 s from fault signature to alert. On-device, a 30 s window sliding every 10 s exposes a fault within 40 s and inference takes about 3 ms, leaving roughly 50 s of margin. A rural 4G round trip (100–500 ms, more under congestion) would fit the budget in isolation, but only when coverage exists.

**Bandwidth.** Raw sensing (1 Hz temperature, 500 Hz × 3-axis vibration, 4-byte samples) is about 518.7 MB per truck per day, which at ₹0.10/MB is ₹51.9 per truck per day, or about ₹16.1 lakh per year for 85 trucks. Edge processing sends only heartbeats and alerts, about 0.15 MB/day (₹0.015), roughly 3,500 times less.

**Connectivity.** The Nashik–Aurangabad route has seven blackout zones of 35–90 minutes. A cloud-only system is blind during each; LogiEdge keeps classifying, alerts in the cab, logs locally, and syncs when coverage returns.

**Privacy.** Raw sensor streams never leave the truck, so pharmaceutical clients can be assured that cargo data is processed on hardware FreightBridge controls, with only small encrypted result messages sent upstream.

**Hardware selection.** Applying the Constraint Triangle (performance, power, cost), the model is tiny, so performance is not limiting and the dominant vertices are power (10 W AI budget on the 12 V supply) and fleet-scale cost. The Jetson Orin Nano Super draws 15 W, breaching the budget, and costs ₹45,000 per truck (₹119 lakh at 265 trucks). The STM32H7 is cheapest (₹3,500) and lowest power (0.4 W) but cannot run Linux, Mosquitto, Docker or Ansible, so the MQTT, container OTA and local log design would not be possible. We select the **Raspberry Pi 5 + AI HAT+**: 7.5 W, ₹15,000 per truck (₹12.75 lakh pilot, ₹39.75 lakh at scale), and the full software stack.

**System architecture.** Figure 1 shows the design: sensors publish to a local Mosquitto broker on the truck; preprocessing builds a 6-feature vector; the Dockerised INT8 MLP classifies it; alerts go to the cab and to a local append-only log; a store-and-forward cellular uplink delivers alerts and log batches to the operations centre, which also pushes OTA models.

*[Insert figure: scenario_architecture/system_architecture.png]*

**Arithmetic Intensity and Roofline.** With about 45 MFLOPs and 18 MB moved per inference, Arithmetic Intensity is 45/18 = 2.5 FLOP/byte. The Pi 5 CPU ridge point is 16 GFLOP/s ÷ 12 GB/s = 1.33 FLOP/byte. Since 2.5 exceeds 1.33 the model is **compute-bound**, attaining the 16 GFLOP/s peak with about 2.8 ms of compute versus 1.5 ms of memory time. Latency is therefore improved by reducing FLOPs or raising compute throughput (structured pruning and INT8 quantisation), not by adding memory bandwidth.
