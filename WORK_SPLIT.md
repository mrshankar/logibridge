# LogiEdge: Work Split (5 people, revised 31 Oct 2026)

Person 5 joined after the original 4-way split. Person 3 was the heaviest and on the critical path, so Docker and Ansible moved to Person 5. Person 3 also takes the 3σ experiment, since it needs P3's own model. Anything not listed here is unchanged. Internal deadline Sun 9 Nov; LMS due Mon 10 Nov (late penalty 2 marks per day).

## Person 1: Architecture, hardware, report lead
| Task | Status / deadline |
|---|---|
| Repo, A1, A2, B1, B2, E3, report Section 1 draft | **Done** |
| D3: map all 10 pipeline stages (inputs from P2, P3, P4, P5) | Tue 4 Nov |
| Merge all sections into `GROUPNO_LogiEdge_Final.pdf`, check 2,500–3,000 words | Sat 8 Nov |
| Edit demo video (15–20 min) from everyone's segments, upload, link in `demo/demo_video_link.txt` | Sat 8 Nov |

## Person 2: Sensor pipeline and MQTT
| Task | Deadline |
|---|---|
| Mosquitto broker, topic tree, C1 `simulator.py`, C2 `preprocessing.py`, `training_stats.npy`, C3 fusion (original deadlines 20–25 Oct, hand off to P3 as soon as ready) | **Overdue, finish first** |
| `mqtt_architecture.md`: topic tree figure and QoS justification | Sun 2 Nov |
| Report Section 2 (500–600 words, includes fusion justification and the 3σ results table from P3) | Wed 5 Nov |

## Person 3: Model training and inference service
| Task | Deadline |
|---|---|
| D1 `generate_dataset.py`, `train_model.py` (MLP 32-16, validation accuracy above 88%), share FP32 model with P4 and P5 | Wed 29 Oct (**overdue if not done**) |
| D2 `inference_service.py` (preprocess, infer, publish to `logibridge/trucks/{truck_id}/inference`, `MODEL_PATH` env var) | Sat 1 Nov |
| **Moved from P2:** 3σ shifted-stats normalisation experiment and results table, send table to P2 | Fri 31 Oct |
| Report Section 3, model training part (accuracy, dataset); P5 adds Docker and Ansible, P1 adds D3 and E3 | Wed 5 Nov |

## Person 4: Optimisation and drift monitoring (unchanged)
| Task | Deadline |
|---|---|
| `benchmark.py`, `drift_monitor.py` on a dummy model | Mon 27 Oct |
| F1: M2 PTQ INT8 (`convert_ptq.py`), M3 pruning + INT8 (`prune_quantise.py`) | Fri 31 Oct / Sun 2 Nov |
| F2 benchmark (15 cells, `pareto_chart.png`) | Mon 3 Nov |
| F3 deployment recommendation (Class 2 recall above 95%) | Tue 4 Nov |
| E1 `reference_dist.json`, PSI monitoring and drift injection | Wed 5 Nov |
| Report Sections 4 and 5 (P5 provides the Ansible paragraph) | Wed 5 Nov |

## Person 5: Docker, OTA demo and Ansible (new)
| Task | Deadline |
|---|---|
| **Moved from P3:** D2 Dockerfile (`python:3.11-slim`, pip layers before `COPY model.tflite`, `MODEL_PATH` env var), start with a dummy model, then use P3's service | Sun 2 Nov |
| **Moved from P3:** OTA layer-cache demo: change only the model, rebuild, record it, calculate the 85-truck bandwidth saving | Mon 3 Nov |
| **Moved from P3:** E2 `logibridge_deploy.yml` with exactly 7 tasks and a local Docker registry | Tue 4 Nov |
| **Moved from P3:** run the playbook twice, confirm second run shows `changed=0`, record both runs | Tue 4 Nov |
| Report Section 3 Docker and bandwidth-saving text, plus the Ansible paragraph for Section 5 | Wed 5 Nov |

## Roughly equal load
P1 about 4 marks left (most already done), P2 about 7, P3 about 4, P4 about 6.5, P5 about 3.5, plus everyone's own demo segment and report text. P1 and P5 have the most spare capacity, so they cover integration help and reviews.

## Shared milestones
- **Handoffs:** P2 to P3 (`training_stats.npy`, `preprocessing.py`); P3 to P4 and P5 (FP32 model, then `inference_service.py` by 1 Nov).
- **6 Nov:** about 30 minutes each walking the team through your code; the viva can ask anyone about any component.
- **9 Nov checklist:** add the instructor as a collaborator, test the video link in an incognito window, put the link in `demo/demo_video_link.txt`.
