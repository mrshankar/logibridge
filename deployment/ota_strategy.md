# E3: OTA Strategy Selection

Inputs: model 280 KB (INT8 TFLite), 85 trucks, M2M SIM at ₹0.10/MB, update every 6 weeks (about 8.7 cycles/year). 280 KB = 0.28 MB.

| Strategy | Data sent per cycle | Cost per cycle | Cost per year | If the new model is bad |
|---|---|---|---|---|
| Full replacement | 85 × 0.28 = 23.8 MB | **₹2.38** | ₹20.6 | All 85 trucks affected until rollback |
| Canary (10 trucks, then 75) | 2.8 MB, then 21.0 MB = 23.8 MB | **₹2.38** (₹0.28 if aborted after canary) | ₹20.6 | Only 10 trucks affected |
| Shadow mode (new model runs silently beside the old one) | 23.8 MB model + about 11.9 MB comparison logs = 35.7 MB | **₹3.57** | ₹31.0 | No truck affected, but a week or more of delay |

The shadow log size is my assumption (7 days × 20 KB/day × 85 trucks), not given in the brief.

**Recommendation: canary (10 trucks first).**

Bandwidth cost is trivial for every option (under ₹4 per cycle), so the decision rests on safety. One undetected refrigeration failure cost ₹28 lakh, which dwarfs any data cost.

- **Against full replacement:** a regression (for example, missing Critical states) would hit all 85 trucks at once with no early warning, and pushing a corrective model costs another cycle over rural links with 35–90 minute gaps.
- **Against shadow mode:** it is the safest for the cargo, but it runs two models on the Pi at once (extra power against the 10 W budget), needs comparison logs uploaded over unreliable rural links, and has no ground truth to judge disagreements, so it delays rollout for little extra assurance. It also costs about 50% more data.
- **Why canary:** the same total bytes as full replacement, but a faulty model is caught on 10 trucks (12%), and an aborted rollout costs only ₹0.28. Choose canary trucks across urban and rural routes so connectivity-gap behaviour is exercised, watch Class 2 recall and PSI drift for a set period, then roll out to the remaining 75 with the same Ansible playbook. Trucks that miss the push during an outage catch up when coverage returns.
