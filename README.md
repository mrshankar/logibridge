# LogiEdge: Intelligent Edge AI Platform for Cold-Chain Logistics

AIML ZG535 (Machine Learning on Edge) mini-project, BITS Pilani WILP. Edge AI pipeline that classifies truck cargo state (Normal / Warning / Critical) on-device, offline-capable.

## Folder map and owners

| Folder | Content | Owner |
|---|---|---|
| `scenario_architecture/` | A1 constraint analysis, A2 architecture diagram | P1 |
| `hardware/` | B1 Constraint Triangle, B2 Roofline | P1 |
| `data_pipeline/` | simulator, preprocessing, training_stats.npy, MQTT design | P2 |
| `training/` | dataset generation, training, PTQ, pruning, `models/` | P3 (D1), P4 (F1) |
| `inference/` | Dockerfile, inference_service.py, model.tflite | P3 |
| `monitoring/` | drift_monitor.py, reference_dist.json | P4 |
| `deployment/` | logibridge_deploy.yml (Ansible) | P3 |
| `optimisation/` | benchmark.py, results/ | P4 |
| `reports/` | phase reports, final report | P1 assembles |
| `demo/` | `demo_video_link.txt` | P1 |

## Team

| Person | Role | GitHub |
|---|---|---|
| P1 | Architecture, hardware, report lead | TODO |
| P2 | Sensor pipeline and MQTT | TODO |
| P3 | Model training, Docker, Ansible | TODO |
| P4 | Optimisation and drift monitoring | TODO |

## Git workflow

- `main` is always runnable. Work on a branch (`p2/simulator`, `p3/train-model`), open a PR, get one review.
- Only touch your own folders; ask the owner before editing someone else's.
- Do not commit videos or large datasets. Models (.tflite, .npy) are small and are committed.
- Commit messages: short imperative, e.g. `Add simulator --anomaly flag`.

## Key deadlines

Internal deadline Sun 9 Nov 2026; LMS due Mon 10 Nov. Handoffs: P2 `training_stats.npy` Sat 25 Oct, P3 FP32 model Wed 29 Oct.
