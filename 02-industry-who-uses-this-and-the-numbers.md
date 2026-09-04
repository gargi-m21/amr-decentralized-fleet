# Industry Reality: Decentralized Multi-Robot Warehouses

**Report type:** Industry / market / research brief for a NeurIPS-style and hackathon robotics problem statement (PS) on *decentralized / edge multi-robot warehouse coordination*.  
**As-of date:** 4 September 2026.  
**Method:** Primary sources preferred (company blogs, IR filings, BLS, Interact Analysis, McKinsey, Ocado/Amazon/Geek+ official pages, academic papers). Vendor marketing is labeled as such. Market-research houses other than Interact Analysis / LogisticsIQ / McKinsey / IDC / Mordor are treated as lower-confidence.  
**Honest headline:** The *problem* (labor, congestion, Wi-Fi, latency, single-point-of-failure) is genuine and large. The *industry solution* is **hybrid**, not fully peer-to-peer. Almost nobody at Amazon/Ocado scale runs a Raspberry Pi swarm with no central planner. Edge and onboard autonomy are real and growing; global traffic still sits in a fleet manager.

---

## 0. How to read this document

Three confidence tags appear throughout:

| Tag | Meaning |
|---|---|
| **PRIMARY** | Company IR, government statistical agency, named analyst firm press release, peer-reviewed / arXiv paper, official product docs |
| **VENDOR** | Throughput, ROI, or “2–3×” claims from the vendor or a customer case study the vendor published |
| **SECONDARY** | Aggregator blogs, unaudited market-size PDFs, unsourced “340 AGV incidents” claims — use with caution |

When two reputable sources disagree on market size (they often do, because “AMR,” “AGV,” “mobile robot,” and “warehouse automation” are different baskets), both are shown and the definition is stated.

---

## 1. Why the problem is genuine (the numbers)

### 1.1 Warehouse labor is still the dominant cost — and still short

Labor is not a side issue. It is the economic reason AMRs exist.

- **Labor share of warehouse opex: ~50–70%.** Repeated across operator surveys and practitioner guides (Hueman RPO, 2026, citing industry workforce research: [https://www.huemanrpo.com/resources/blog/transportation-logistics-job-market-report](https://www.huemanrpo.com/resources/blog/transportation-logistics-job-market-report); Stealth Agents 2026 warehouse staffing guide: [https://stealthagents.com/research/warehouse-and-fulfillment-staffing-costs-2026](https://stealthagents.com/research/warehouse-and-fulfillment-staffing-costs-2026)). This is an industry rule of thumb, not a BLS series. Treat as **SECONDARY** on the exact band, **strong** on the qualitative fact that labor dominates.
- **U.S. warehousing wages are still rising.** BLS Current Employment Statistics, series *Average hourly earnings of all employees, warehousing and storage (NAICS 493)*, not seasonally adjusted: **$24.69 in January 2024 → $24.74 in December 2024 → $26.00 in December 2025 → $26.85 (preliminary) in June 2026** (**PRIMARY**, U.S. Bureau of Labor Statistics, 2026: [https://data.bls.gov/timeseries/CEU4349300003](https://data.bls.gov/timeseries/CEU4349300003); industry snapshot [https://www.bls.gov/iag/tgs/iag493.htm](https://www.bls.gov/iag/tgs/iag493.htm)). That is roughly **+8.7% from Jan 2024 to Jun 2026**, and **+5.1% calendar 2025** (Dec-to-Dec).
- **Shortages are structural, not a 2021 hangover.** Descartes + SAPIO Research surveyed **1,000** supply-chain/logistics decision-makers in late 2023: **76%** reported notable workforce shortages; **37%** rated them high-to-extreme; **56%** of warehouse operations were affected; **58%** said service levels suffered (**PRIMARY**, Descartes, 30 Jan 2024: [https://www.descartes.com/resources/news/descartes-study-reveals-76-supply-chain-and-logistics-operations-are-experiencing](https://www.descartes.com/resources/news/descartes-study-reveals-76-supply-chain-and-logistics-operations-are-experiencing)).
- **Turnover remains brutal.** Practitioner sources put warehouse turnover in the **~36–49%** range (Hueman 2026; Cahoot 2025 citing industry surveys: [https://www.cahoot.ai/warehouse-shortage/](https://www.cahoot.ai/warehouse-shortage/)). **SECONDARY** on the exact percentage; directionally consistent with a decade of MHI / logistics-manager surveys.
- **Automation penetration is still low.** McKinsey (27 Sep 2024): *“only about 20 percent of warehouses in North America have adopted any form of automation”* despite mature technology (**PRIMARY**, McKinsey: [https://www.mckinsey.com/industries/industrials-and-electronics/our-insights/distribution-blog/navigating-warehouse-automation-strategy-for-the-distributor-market](https://www.mckinsey.com/industries/industrials-and-electronics/our-insights/distribution-blog/navigating-warehouse-automation-strategy-for-the-distributor-market)). Interact Analysis (15 Jan 2025) is even more specific for *this* PS: **by 2030, only 13% of warehouses will have deployed at least one fulfillment AMR**, and **only 3% of forklifts shipped globally will be automated** (**PRIMARY**, Interact Analysis: [https://interactanalysis.com/macro-economic-factors-cause-slowdown-in-global-mobile-robot-market/](https://interactanalysis.com/macro-economic-factors-cause-slowdown-in-global-mobile-robot-market/)).
- **YC-company claim, flagged:** Manifold (YC S2026) states *“The US Warehouse industry spends $75bn on labor each year. Yet, only 10% of US warehouses have any form of automation.”* (**VENDOR**, YC company page: [https://www.ycombinator.com/companies/manifold-2](https://www.ycombinator.com/companies/manifold-2)). The 10% figure is in the same neighborhood as McKinsey’s 20% “any automation” if you tighten the definition to robotics; do not treat $75bn as audited.

**Why this matters for the PS:** every extra minute a robot spends stopped at a choke point, waiting on Wi-Fi, or idling because a central planner died, is a minute of the most expensive line item in the building.

### 1.2 AMR / AGV market size, CAGR, installed base

**Gold-standard source for mobile robots is Interact Analysis**, not generic “market research” PDFs that disagree by 3×.

| Metric | Figure | Year / horizon | Source | Tag |
|---|---|---|---|---|
| Mobile robot revenue (AGV+AMR, material handling) | **just under $5 billion** | 2024 | Interact Analysis, 9 Jan 2026 | PRIMARY |
| Forecast revenue | **$14 billion** | 2030 | Same | PRIMARY |
| CAGR | **19%** average annual, 2024–2030 | 2026 forecast | Same | PRIMARY |
| Prior forecast (installed base) | **>4.2 million units** by 2030 | Jan 2025 forecast | Interact Analysis, 15 Jan 2025 | PRIMARY |
| AGV share of mobile-robot revenue | **~33% (2024) → ~20% (2030)** — AMRs taking share | 2026 | Interact Analysis Jan 2026 | PRIMARY |
| China’s shipment share | **~58% (2024) → ~46% (2030)** | 2026 | Same | PRIMARY |
| Fulfillment AMRs in warehouses | **13% of warehouses by 2030** will have ≥1 | 2025 forecast | Interact Analysis Jan 2025 | PRIMARY |
| Broader *warehouse automation* (AS/RS, conveyors, software, robots) | **~$30B (2025) → ~$66B (2031)**, CAGR **~14%** | 2025–2031 | Mordor Intelligence | PRIMARY-ish (paid analyst, public abstract) |
| Warehouse automation (LogisticsIQ) | **~$64B by 2032**, CAGR **12.3% (2026–2032)**; earlier public note **~$55B by 2030** | 2025–2026 | LogisticsIQ / PR Newswire | PRIMARY |
| AMR-only (narrower basket) | **$2.77B (2025) → $3.20B (2026) → $10.36B (2034)**, CAGR **15.8%** | 2026 | Fortune Business Insights | SECONDARY (definition narrower than Interact) |

Sources:

- Interact Analysis, 9 Jan 2026, *Mobile robots market outpaces fixed automation*: [https://interactanalysis.com/mobile-robots-market-outpaces-fixed-automation/](https://interactanalysis.com/mobile-robots-market-outpaces-fixed-automation/)
- Interact Analysis, 15 Jan 2025, *Macro-economic factors cause slowdown*: [https://interactanalysis.com/macro-economic-factors-cause-slowdown-in-global-mobile-robot-market/](https://interactanalysis.com/macro-economic-factors-cause-slowdown-in-global-mobile-robot-market/)
- Mordor Intelligence warehouse automation abstract: [https://www.mordorintelligence.com/industry-reports/warehouse-automation-market](https://www.mordorintelligence.com/industry-reports/warehouse-automation-market)
- LogisticsIQ: [https://www.thelogisticsiq.com/research/warehouse-automation-market](https://www.thelogisticsiq.com/research/warehouse-automation-market) and PR Newswire, 2024/25: [https://www.prnewswire.co.uk/news-releases/warehouse-automation-market-to-reach-55-billion-by-2030-driven-by-e-commerce-and-supply-chain-transformation---logisticsiq-302252722.html](https://www.prnewswire.co.uk/news-releases/warehouse-automation-market-to-reach-55-billion-by-2030-driven-by-e-commerce-and-supply-chain-transformation---logisticsiq-302252722.html)
- Fortune Business Insights AMR: [https://www.fortunebusinessinsights.com/autonomous-mobile-robots-market-105055](https://www.fortunebusinessinsights.com/autonomous-mobile-robots-market-105055)

**Reconciliation:** Interact’s *mobile robot* ~$5B (2024) is the right number for “AMRs and AGVs that move in warehouses and factories.” Mordor/LogisticsIQ ~$30B is the *entire warehouse automation stack* (racks, shuttles, WMS, conveyors, AS/RS). Do not mix them.

**Skepticism:** Interact cut its 2027 forecast by **18%** in January 2025 and cut the 2030 revenue path another **12%** in January 2026 because of tariffs and delayed capex. The market is real and growing double-digits; it is not a straight line.

### 1.3 Cost of downtime / Wi-Fi / cloud outages in warehouses

This is the PS’s strongest *business* argument, and it is documented — with the caveat that the best recent numbers come from a **WMS vendor** with a product to sell (hybrid/edge WMS).

- **$5,000–$100,000 per hour** warehouse downtime, depending on scale and SLA exposure. Synergy Logistics (SnapFulfil) report *Warehouse Resilience & Downtime*, as covered by FreightWaves / Produce Wire, 26 Mar 2026: [https://theproducewire.com/warehouses-face-100k-hour-downtime-risk-as-cloud-outages-mount/](https://theproducewire.com/warehouses-face-100k-hour-downtime-risk-as-cloud-outages-mount/). **VENDOR** (the dollar band), **PRIMARY** as a named survey: **84%** of organizations had at least one significant disruption in 24 months; **nearly half** reported **idling automation assets** because of software or connectivity interruptions. The report explicitly argues for **on-site edge appliances** so picking continues when AWS/Azure/Cloudflare/Verizon blip.
- **Marks & Spencer (UK) ransomware, 2025:** cited in the same coverage as “tens, hundreds of thousands of dollars a day” while not shipping. Directionally confirms that a fulfillment IT outage is a P&L event, not an IT ticket.
- **Generic “cost of downtime $15,000/minute”** (Gatling, Xurrent, 2026) is **enterprise-IT folklore**, not warehouse-specific. Do not use it for this PS. Warehouse-hour figures are the right unit.
- **Wi-Fi is a first-class failure mode for AMRs**, independently of cloud SaaS:
  - Performance Networks (UK wireless integrator, 2025/26): warehouse Wi-Fi was designed for handheld scanners that tolerate dropouts; AMRs need continuous telemetry, navigation updates, and safety signalling. Conservative robot roaming leaves the robot stuck on a dying AP; symptoms are hesitation, retries, and unreproducible stalls. [https://www.performancenetworks.co.uk/blog/amr-robot-wifi/](https://www.performancenetworks.co.uk/blog/amr-robot-wifi/)
  - Cisco industrial reference design for AGV/AMR wireless: factories/warehouses need **ultra-reliable wireless backhaul**, not office Wi-Fi, precisely because mobile robots fail closed when the radio dies. **PRIMARY**, Cisco: [https://www.cisco.com/c/en/us/td/docs/solutions/Verticals/Industrial_Automation/IA_Verticals/Factory/IA-Factory-CRD1/IA-Factory-CRD1.html](https://www.cisco.com/c/en/us/td/docs/solutions/Verticals/Industrial_Automation/IA_Verticals/Factory/IA-Factory-CRD1/IA-Factory-CRD1.html)
  - Private 5G vs Wi-Fi 6 decision guides (2025–2026) document **50–200 ms “make-and-break” AP handoff** on Wi-Fi, during which an AMR that requires a live control channel **stops for safety**, then cascades a queue behind it. Private 5G is sold as seamless handover. Example: [https://ifactoryapp.com/greenfield-consulting/private-5g-vs-wifi-6-greenfield-factories](https://ifactoryapp.com/greenfield-consulting/private-5g-vs-wifi-6-greenfield-factories) (**SECONDARY** on the exact ms band; the *mechanism* is standard 802.11 roaming physics).
  - Metal racking, forklifts, and moving inventory create **RF dead zones**. This is textbook indoor wireless, not a research hypothesis. Integrators redesign AP density specifically for robot fleets.

**What we could not find (honesty):** a single public post-mortem of the form “Warehouse X lost $Y because AMR Wi-Fi dead zone Z.” Operators do not publish those. The evidence is: (a) an entire Cisco CRD exists to prevent it; (b) WMS vendors are pitching hybrid/edge because cloud+Wi-Fi outages idle robots; (c) private 5G RFPs for AMR fleets are now a category. That is **medium-strong** industrial evidence, not a courtroom exhibit.

### 1.4 Latency: cloud vs edge vs onboard for robot control loops

There is a clean, widely agreed **tiering**. The exact milliseconds vary by paper; the *order of magnitude* does not.

| Function | Typical latency budget | Where it must run | Notes |
|---|---|---|---|
| E-stop / safety scanner | **<1–10 ms** | **Onboard**, safety-rated PLC / MCU | Never cloud. ISO 3691-4 / ANSI B56.5. |
| Joint / base velocity loop | **<5–20 ms** | **Onboard** | Hard real-time. |
| Local obstacle avoidance / DWA / TEB | **10–50 ms** | **Onboard** (or on-prem GPU) | Must survive Wi-Fi loss. |
| Fleet traffic / intersection reservation | **tens of ms to a few hundred ms** | **On-prem fleet manager** or local V2V | Cloud round-trip is too jittery. |
| Task assignment / MAPF replan | **100 ms – a few seconds** | On-prem or cloud GPU (cuOpt, DeepFleet) | Latency-tolerant *if* robots can keep a prior plan. |
| Model training, dashboards, predictive maintenance | **seconds to hours** | **Cloud** | Ocado streams bot health to cloud; Amazon trains DeepFleet on SageMaker. |

Sources (architecture, not a single lab measurement):

- NVIDIA Isaac ROS *Cloud Control* — missions go to an on-robot **Mission Client** over **VDA5050/MQTT**; the robot executes locally: [https://nvidia-isaac-ros.github.io/concepts/cloud_control/index.html](https://nvidia-isaac-ros.github.io/concepts/cloud_control/index.html) (**PRIMARY**)
- NVIDIA Isaac Mission Control — central cuOpt + occupancy graph; robot-side client: [https://github.com/nvidia-isaac/isaac_mission_control](https://github.com/nvidia-isaac/isaac_mission_control) (**PRIMARY**)
- Practitioner latency tables (edge 3–45 ms vs cloud 50–200 ms typical, 800 ms+ under congestion): ModulEdge 2026 [https://moduledge.com/blog/edge-data-center-robots](https://moduledge.com/blog/edge-data-center-robots); CXTMS 2026 warehouse edge post [https://cxtms.com/blog/industrial-edge-computing-warehouse-robotics-on-premise-ai-decision-latency-2026](https://cxtms.com/blog/industrial-edge-computing-warehouse-robotics-on-premise-ai-decision-latency-2026). Treat millisecond point estimates as **SECONDARY**; the architectural split is **PRIMARY** from NVIDIA/VDA/ISO.

**Implication for the PS:** “Cloud path planning has high latency” is **true for the control loop**, **overstated for task assignment**. Industry already split the stack. A student system that does *global A\** in the cloud every 50 ms is fighting physics. A student system that does *local CA on-device* and *replans when the link drops* is copying 2025 production architecture.

### 1.5 Collision / incident statistics

Public, warehouse-specific AMR-vs-AMR crash rates are **almost nonexistent**. Safety vendors and OSHA talk about **human–robot** harm, which is a different (and more important) problem.

- **OSHA Severe Injury Reports, 2015–2022:** academic analysis identified **77 robot-related accidents** (federal OSHA only, so incomplete): **54 stationary robots** (66 injuries, mostly finger amputations) and **23 mobile-robot accidents** (27 injuries, mostly leg/foot fractures). **PRIMARY** paper: *Robot-related injuries in the workplace: An analysis of OSHA Severe Injury Reports*, Applied Ergonomics, 2024: [https://www.sciencedirect.com/science/article/abs/pii/S0003687024001017](https://www.sciencedirect.com/science/article/abs/pii/S0003687024001017). This is **not** an AMR-choke-point congestion statistic; it is workplace injury.
- **Walmart DC / Swisslog trolley, 18 Oct 2016:** employee struck by an automated trolley at Walmart DC 7019; OSHA citations later vacated on LOTO technicalities. **PRIMARY** OSHRC decision: [https://www.oshrc.gov/wp-content/uploads/17-0777__17-0784_Decision_and_Order_-DATED-_pub.pdf](https://www.oshrc.gov/wp-content/uploads/17-0777__17-0784_Decision_and_Order_-DATED-_pub.pdf). Shows that “automated vehicle hits person in a DC” is a documented class of event.
- **GEODIS + Locus (powered industrial equipment, not robot-robot):** incidents involving powered industrial equipment dropped from **7 in 2022 to 2 over the following 24 months** after AMR conversion (**VENDOR** customer story, Modern Materials Handling: [https://www.mmh.com/article/system_report_geodis_doubles_picking_throughput_with_amrs](https://www.mmh.com/article/system_report_geodis_doubles_picking_throughput_with_amrs)). Useful as “AMRs can *reduce* forklift-class collisions,” not as “robots never deadlock.”
- **ISO 3691-4:2023** (driverless industrial trucks) and **ANSI/ITSDF B56.5** exist because collisions with people, racks, and other vehicles are a recognized hazard class. Compliance is a purchase requirement, not a research paper.
- **Do not use** unsourced blog claims such as “OSHA recorded 340 AGV incidents, 11 fatalities, 2019–2025” unless you can open the OSHA database yourself. We could not verify that count from a primary OSHA table for this report.

**For the PS:** robot–robot *deadlock at a narrow aisle* is an **efficiency** problem (throughput), documented heavily in MAPF literature and by Amazon DeepFleet (“congestion and deadlocks”). Robot–human collision is a **safety** problem, documented in OSHA SIRs. Keep them separate.

### 1.6 Fleet-size growth (the installed-base proof)

| Operator / vendor | Fleet / footprint | Date | Coordination style (see §2) | Source |
|---|---|---|---|---|
| **Amazon Robotics** | **1,000,000th robot deployed**; **300+ facilities**; world’s largest industrial mobile-robot fleet (Amazon’s claim) | Jun 2025 | Central traffic + onboard Proteus autonomy; DeepFleet for congestion | Amazon, 2025: [https://www.aboutamazon.com/news/operations/amazon-million-robots-ai-foundation-model](https://www.aboutamazon.com/news/operations/amazon-million-robots-ai-foundation-model) |
| Amazon (growth path) | ~750k (2023/24) → 1,000,000 (2025); **+250,000 in ~one year** | 2025 | Same | Amazon + secondary charts (Visual Capitalist / Ark via Yahoo); treat 750k as **SECONDARY** unless in a 10-K |
| Amazon DeepFleet | **10%** improvement in robotic fleet **travel time**; trained on **billions of hours** of nav data; **thousands of robots per floor** | 2025 | Learned central traffic prediction | Amazon Science, 11 Aug 2025: [https://www.amazon.science/blog/amazon-builds-first-foundation-model-for-multirobot-coordination](https://www.amazon.science/blog/amazon-builds-first-foundation-model-for-multirobot-coordination); arXiv: [https://arxiv.org/html/2508.08574v2](https://arxiv.org/html/2508.08574v2) |
| **Ocado** (grid bots) | **>17,000 bots**; **153 million km/year**; up to **1,200 totes/hour per station**; control loop **10 Hz** | Aug 2026 | **Extremely centralized** “air traffic control” | Ocado Group: [https://www.ocadogroup.com/newsroom/stories/meet-the-bots-that-power-ocado-groups-online-grocery-fulfilment-across-the-globe](https://www.ocadogroup.com/newsroom/stories/meet-the-bots-that-power-ocado-groups-online-grocery-fulfilment-across-the-globe); [https://www.ocadogroup.com/about-us/our-technology](https://www.ocadogroup.com/about-us/our-technology) |
| **Geek+** | **~56,000** AMRs delivered by 31 Dec 2024; **>72,000** by 31 Dec 2025; **>81,000** by 30 Jun 2026; **1,000+** end customers; Interact Analysis: **#1 global AMR share, 7 consecutive years** | 2024–2026 | Hybrid: central RCS + onboard NAV | Geek+ 2025 annual results PDF; PR Newswire 1 Sep 2026: [https://www.prnewswire.com/news-releases/subscription-based-services-boom-geek-reports-2026-interim-results-orders-up-35-5-breakthroughs-across-the-business-spectrum-302867104.html](https://www.prnewswire.com/news-releases/subscription-based-services-boom-geek-reports-2026-interim-results-orders-up-35-5-breakthroughs-across-the-business-spectrum-302867104.html); IR: [https://ir.geekplus.com/](https://ir.geekplus.com/) |
| **Locus Robotics** | **17,000+** AMRs, **360+** sites, **150+** customers; **6 billion** cumulative picks; some sites **350+** bots | 2025–2026 | Cloud-native **LocusONE** orchestration + onboard AMR NAV | Sacra; Automated Warehouse 2025/26: [https://www.automatedwarehouseonline.com/locus-robotics-reaches-6b-picks-revenue-sets-records/](https://www.automatedwarehouseonline.com/locus-robotics-reaches-6b-picks-revenue-sets-records/); [https://locusrobotics.com/](https://locusrobotics.com/) |
| **AutoStore** | **~1,900 systems in 65 countries**; FY2025 revenue **$538.6M** (down 10.4% YoY) | YE 2025 | Central cube/grid software, not free-roam AMR | AutoStore Q4 2025: [https://news.cision.com/autostore-as/r/autostore--q4-2025-financial-results,c4306434](https://news.cision.com/autostore-as/r/autostore--q4-2025-financial-results,c4306434) |
| **Hai Robotics** | Example: **948 robots** (278 ACR + 670 AMRs) at LPP Romania, **>9,400 totes/hour**; Maersk Singapore: **49 A42T + 110 AMRs**, **>1,000 totes/hour** | 2025–2026 | Hierarchical: ACR in racks + AMR transit + WMS | Hai / trade press: [https://www.hairobotics.com/news/hai-robotics-and-maersk-redefine-fashion-fulfilment-high-density-robotics-10-metre-scale-singapore](https://www.hairobotics.com/news/hai-robotics-and-maersk-redefine-fashion-fulfilment-high-density-robotics-10-metre-scale-singapore) |
| **Quicktron** | Official: **>35,000** operational units, **1,000+** clients; secondary profiles cite **42,000+** | 2025 | Central RCS + AMR | Quicktron About: [https://www.quicktron.com/about-us](https://www.quicktron.com/about-us) |
| **Boston Dynamics Stretch @ DHL** | **10 units** live as of Jun 2025; unloading **up to 700 cases/hour**; MOU for **1,000+ additional** by 2030 | 2025 | Mostly single-robot cell + WMS; not a 1,000-AMR traffic problem *yet* | Boston Dynamics, 13 May 2025: [https://bostondynamics.com/news/dhl-signs-mou-for-additional-1000-robot-deployment/](https://bostondynamics.com/news/dhl-signs-mou-for-additional-1000-robot-deployment/) |

Amazon’s own product pages also list **Sequoia** (inventory sortation), **Proteus** (first fully autonomous Amazon AMR in open areas with people), **Hercules** (1,250 lb payload drive unit), **Pegasus**, **Vulcan** (tactile arm), and **DeepFleet / Project Eluna** as the software layer ([https://www.aboutamazon.com/news/operations/amazon-robotics-robots-fulfillment-center](https://www.aboutamazon.com/news/operations/amazon-robotics-robots-fulfillment-center)).

### 1.7 Throughput gains: AMR vs manual (mostly vendor-claimed)

| Claim | Number | Baseline | Tag | Source |
|---|---|---|---|---|
| Locus typical | **2–3× picker productivity** vs manual cart picking | Manual walk-and-pick | VENDOR | Locus ROI blog: [https://locusrobotics.com/blog/true-roi-autonomous-mobile-robots](https://locusrobotics.com/blog/true-roi-autonomous-mobile-robots) |
| Locus / nGroup | **124 → 285 LPH** (**+129%**) | Manual | VENDOR customer | [https://locusrobotics.com/blog/warehouse-amrs-beyond-picking](https://locusrobotics.com/blog/warehouse-amrs-beyond-picking) |
| Locus / GEODIS Dallas | **65 → 98 UPH** (**+51%**) with 12 Vector AMRs | Manual carts | VENDOR case study | [https://locusrobotics.com/wp-content/uploads/2024/03/GEODIS-Dallas-TX-Vector-Case-Study.pdf](https://locusrobotics.com/wp-content/uploads/2024/03/GEODIS-Dallas-TX-Vector-Case-Study.pdf) |
| Locus / GEODIS Plainfield | **~85% average**, up to **150%** some days; “picking twice as much” | Electric pallet jack | VENDOR / MMH | [https://www.mmh.com/article/system_report_geodis_doubles_picking_throughput_with_amrs](https://www.mmh.com/article/system_report_geodis_doubles_picking_throughput_with_amrs) |
| Exotec Skypod | **up to 5×** vs manual; any SKU **<2 minutes** | Manual | VENDOR | [https://www.exotec.com/blog/the-impact-of-robotics-on-labor/](https://www.exotec.com/blog/the-impact-of-robotics-on-labor/) |
| Ocado bots | **1,200 totes/h/station**; 50-item order in **~5 minutes** (older Ingenia profile of Erith) | N/A (grid, not vs cart) | PRIMARY / journalism | Ocado 2026 blog; Ingenia: [https://www.ingenia.org.uk/articles/hives-of-activity/](https://www.ingenia.org.uk/articles/hives-of-activity/) |
| Amazon DeepFleet | **+10% fleet travel-time efficiency** | Amazon’s own prior traffic stack | PRIMARY (Amazon-claimed, internally measured) | Amazon 2025 |
| McKinsey distributor case | **4× productivity**, **15–20% faster response**, **20%** less space, **20%** run-rate savings | That client’s pre-automation DC | PRIMARY (consulting case; not AMR-specific) | McKinsey 2024 |
| Academic lifelong MAPF | **~25% higher throughput** vs rolling-horizon prioritized planning with *random* priorities | Random-priority RH-PP, not stop-and-wait | PRIMARY (sim) | Yan et al., JAIR / arXiv 2026: [https://arxiv.org/html/2603.23838](https://arxiv.org/html/2603.23838) |

**Read this correctly for the PS:** 2–3× vs *walking pickers* is **not** the same as 20% vs *stop-and-wait robots*. The first is “buy AMRs.” The second is “write a better coordinator.” Both are real; they answer different questions. Amazon’s **10%** on an already-optimized million-robot fleet is the most important number in this table: **coordination quality still has double-digit juice after a decade of Kiva-style central planning.**

### 1.8 Single-point-of-failure and Wi-Fi dead zones — documented industry response

Industry has voted with architecture, not with a tell-all blog post:

1. **VDA 5050** (VDA, v2.1.0, Jan 2025) *defines* a **master control** that assigns orders, computes routes, and does traffic control — and simultaneously assumes vehicles have **onboard** navigation and safety. The standard exists because mixed-vendor fleets cannot all depend on one proprietary brick. PDF: [https://www.vda.de/dam/jcr:f0c9c019-1506-4dee-998a-e92723fbf025/EN-VDA5050-V2_0_0.pdf](https://www.vda.de/dam/jcr:f0c9c019-1506-4dee-998a-e92723fbf025/EN-VDA5050-V2_0_0.pdf) (**PRIMARY**; note the URL slug still says V2_0_0).
2. **Hybrid WMS / edge appliance** pitch (Synergy 2026, §1.3) is an explicit reaction to **cloud SPOF**.
3. **OTTO Fleet Manager** advertises AMRs that **“automatically exchange information… to predict approaching intersections and proactively avoid blockages”** — local negotiation *in addition to* a central manager: [https://ottomotors.com/fleet-manager/](https://ottomotors.com/fleet-manager/) (**VENDOR**, but the product exists).
4. **ROS 2 + Zenoh:** DDS multicast discovery collapses on lossy warehouse Wi-Fi and multi-subnet fleets; Eclipse Zenoh / `rmw_zenoh` is the industrial answer to “the middleware *is* the SPOF.” Eclipse: [https://github.com/eclipse-zenoh/zenoh-plugin-ros2dds](https://github.com/eclipse-zenoh/zenoh-plugin-ros2dds); deployment model: [https://zenoh.io/docs/getting-started/deployment/](https://zenoh.io/docs/getting-started/deployment/).
5. **Open-RMF** (Open Robotics) + **Free Fleet** over Zenoh: heterogeneous robots, task dispatch, *and* a path that does not require one vendor’s cloud. [https://osrf.github.io/ros2multirobotbook/integration_free_fleet_adapter.html](https://osrf.github.io/ros2multirobotbook/integration_free_fleet_adapter.html)

### 1.9 Edge computing market in robotics / logistics

Edge numbers are **definitionally mushy**. Prefer IDC for “edge computing as a whole,” and treat robotics-specific TAM PDFs as directional.

- **IDC Worldwide Edge Spending Guide (17 Mar 2025):** global edge spending **~$261 billion in 2025**, CAGR **13.8%**, **~$380 billion by 2028**. Taxonomy explicitly includes **robotics** as one of six enterprise domains (with AI, IoT, AR, VR, drones). **PRIMARY**, IDC: [https://my.idc.com/getdoc.jsp?containerId=prUS53261225](https://my.idc.com/getdoc.jsp?containerId=prUS53261225)
- **Edge AI for robotics** (MarketIntelo, 2025): **$4.2B (2025) → $36.8B (2034)**, CAGR **28.5%**. Same firm’s **onboard edge AI for mobile robots**: **$4.2B (2025) → $20.8B (2034)**, CAGR **22.8%**. **SECONDARY** (boutique TAM; two reports colliding at $4.2B is a yellow flag). [https://marketintelo.com/report/edge-ai-for-robotics-market](https://marketintelo.com/report/edge-ai-for-robotics-market)
- **Industrial edge computing for logistics** (DataIntelo): **$3.7B (2025) → $12.44B (2034)**. **SECONDARY**.
- NVIDIA’s commercial gravity is the real signal: **Jetson Orin / Thor** on AMRs, **Isaac ROS** on-robot, **cuOpt** in the facility, **Mission Control** as the fleet brain. That product split *is* the market.

---

## 2. How industry actually does it today (architecture patterns)

If you remember one diagram, remember this:

```
WMS / ERP / OMS
        │  (orders, SKUs, SLAs)
        ▼
Fleet manager / WES / “master control”     ← task allocation, traffic, MAPF, VDA5050
        │
        │  MQTT / DDS / Zenoh / proprietary
        ▼
On-robot stack: localization, local planner, safety PLC     ← survives radio loss
        │
        ▼
Optional cloud: training, dashboards, predictive maintenance, RaaS billing
```

**Fully decentralized P2P warehouses are research and a few intersection-negotiation features. They are not the production default.**

### 2.1 Pattern A — Centralized fleet manager / traffic control (traditional, still dominant at density)

**What it is:** One process owns the map, assigns goals, reserves cells/aisles, and prevents two robots from claiming the same resource. Robots are smart actuators.

**Who uses it:**

| System | Why it is centralized | Density / constraint |
|---|---|---|
| **Amazon Kiva / Hercules / Pegasus grid** | Drive units on a marked floor; pods are chess pieces. DeepFleet still predicts *central* traffic. Amazon Science is explicit: simulating thousands of robots faster than real time is too expensive, so they learned a model — still a **floor-level** model, not gossip. | Thousands of robots per FC floor |
| **Ocado Hive / OSP bots** | “There is no way we could achieve the required throughput if the robots were autonomous, moving around the grid dodging one another.” (Paul Clarke-era Ingenia interview.) Control software talks to each bot **10 times per second**, can **change the mission mid-journey**. | 1,700+ bots per hive historically; 17,000+ globally |
| **AutoStore** | Robots on a cube; ports and grid occupancy are globally scheduled. | 1,900 sites |
| **Classic AGV (Dematic, Daifuku, JBT, SSI)** | Magnetic tape / QR / contour; zone controllers and a traffic PLC. | Factories, beverage, auto |

**Products:** Amazon Robotics; Ocado Smart Platform; AutoStore; most AS/RS; VDA 5050 “master control”; NVIDIA **cuOpt** + Mission Dispatch; **OTTO Fleet Manager**; **MiR Fleet**; Geek+ **RCS**; GreyOrange **GreyMatter**; Locus **LocusONE**.

**Failure mode the PS cares about:** if the master dies or the radio to the master dies, robots **stop or limp on the last assigned path**. Safety requires fail-safe stop; throughput requires a fallback planner — which is the PS.

### 2.2 Pattern B — Hybrid: central task allocation + local collision avoidance (**the industry default for AMRs**)

**What it is:** WMS/WES says *what* to do. A fleet manager says *which robot* and *which route*. The robot’s onboard stack does SLAM, dynamic obstacle avoidance (people, pallets, other robots at close range), and ISO-rated safety stop. If the fleet manager is slow, the robot can still not hit a person.

**Who uses it:**

- **Locus Origin / Vector / Array + LocusONE:** cloud (or VPC) orchestration of work; robots navigate existing aisles among humans. Locus is explicit that LocusONE “does not just control robots, it manages dynamic warehouse workflows” and rebalances as robots join (**VENDOR** interview, 2025: [https://roboticsandautomationnews.com/2025/07/30/exclusive-interview-with-locus-robotics-born-in-the-digital-age/93405/](https://roboticsandautomationnews.com/2025/07/30/exclusive-interview-with-locus-robotics-born-in-the-digital-age/93405/)).
- **Geek+ P40 / M100 / PopPick, etc.:** central RCS for traffic in goods-to-person maps; onboard LiDAR/vision for local CA. Scale (81k units) is impossible without this split.
- **Hai Robotics ACR + companion AMRs:** vertical retrieval is a different robot type than floor transit; WMS integration + virtual commissioning. Hierarchical *and* hybrid.
- **MiR (Teradyne) + MiR Fleet;** **OTTO (Rockwell)**; **Seegrid**; **Vecna**; **Quicktron**; **GreyOrange Ranger + GreyMatter**.
- **Amazon Proteus:** the interesting exception *inside* Amazon — “fully autonomous” in *open, unrestricted* areas with people, i.e. local perception, while the fulfillment *grid* remains centrally choreographed.
- **Boston Dynamics Stretch:** onboard manipulation and navigation; DHL WMS assigns jobs. Fleet-of-1,000 is a 2030 problem, not a 2025 traffic-control problem.
- **NVIDIA Isaac AMR / Isaac ROS:** textbook hybrid. **Mission Client on robot**, **Mission Control + cuOpt + SWAGGER graph in the facility/cloud**, **VDA5050**. SAP EWM optional. This is what “industrial ROS 2” looks like in 2026.

**Local CA algorithms in the wild:** Nav2 DWB/MPPI, vendor proprietary, safety LiDAR fields (SICK, Pepperl+Fuchs, PILS). These are **not** MAPF. They will deadlock two robots in a narrow aisle if nobody has a global reservation. That gap *is* the PS.

### 2.3 Pattern C — Fully decentralized / P2P / V2V-style

**What it is:** robots broadcast pose/intent, negotiate intersections, maybe run distributed MAPF or priority rules, no (or optional) central brain.

**Who actually ships this:**

- **Almost no large warehouse.** Ocado’s own engineers said autonomy-on-the-grid would kill throughput.
- **Pieces of it, yes:**
  - OTTO’s intersection prediction via **AMR-to-AMR info exchange** (still under Fleet Manager).
  - Academic **virtual traffic lights**: decentralized planning + a thin central conflict node (arXiv 2511.07811, 2025: [https://arxiv.org/pdf/2511.07811](https://arxiv.org/pdf/2511.07811)).
  - **V2X / ETSI** robot awareness messages — outdoor/CCAM, not tote-to-person (arXiv 2605.06662).
  - **Zenoh peer/router** topologies and ROS 2 multi-robot namespacing — *comms* decentralization, not *planning* decentralization.
  - Research swarms, CRDTs, blockchain orchestration (RoboMesh, etc.) — **not** in Amazon FCs.

**Honest status:** decentralized coordination is an **active research and standards** area (MAPF, VDA 5050 extensions, MassRobotics interoperability, Open-RMF) and a **resilience feature**, not the thing that runs 17,000 Ocado bots.

### 2.4 Pattern D — Hierarchical / zone controllers

**What it is:** a site-level WES, then **zone** or **hive** or **floor** controllers, then robots. Congestion is isolated. Used wherever the map is too big for one MIP/MAPF.

**Who uses it:**

- Amazon: **per-floor** models in DeepFleet (robot-centric, robot-floor, graph-floor). A million robots are **not** one planning problem; they are hundreds of buildings × multiple floors.
- Ocado: **ambient hive vs chilled hive**; each is its own chessboard.
- Hai / Geek+ **MFC (micro-fulfillment)** vs campus DC: different controllers.
- Auto OEM plants: AGV **block zones** and traffic lights at aisle crossings — 1990s technology that still works.
- Open-RMF: **fleets + maps + traffic negotiation** as separate layers.

This is the realistic way a student team “scales”: **don’t build a 1,000-agent global optimum; build zones + a protocol at the boundary.**

### 2.5 Pattern E — Cloud vs on-prem vs onboard edge

| Layer | Typical 2026 placement | Examples |
|---|---|---|
| Safety | Onboard, certified | ISO 3691-4 scanners, e-stop |
| Local NAV / CA | Onboard (x86, Jetson, vendor ARM) | Nav2, vendor stack, Proteus |
| Fleet traffic | **On-prem server or private cloud in the DC** | RCS, Fleet Manager, Mission Control, Ocado CFC software |
| Task / labor orchestration | Cloud *or* on-prem WES | LocusONE (cloud-native RaaS), GreyMatter, WMS |
| Learning | Cloud | DeepFleet on SageMaker; Ocado predictive maintenance streamed to cloud |
| Teleop / incident | Cloud + edge video | Formant, InOrbit |

**Locus is the existence proof that “cloud fleet manager” can work** — for **collaborative picking AMRs** at walking speeds, with humans as the safety backup, and with enough radio engineering. **Ocado is the existence proof that 10 Hz centralized control works** — on a **private, structured, no-pedestrian grid** with industrial networking, not public AWS from a Pi on Wi-Fi 4.

**RaaS billing** (Locus, Geek+ subscriptions, AutoStore ASaaS) lives in the cloud even when control does not. Do not confuse “the dashboard is in AWS” with “the motion planner is in us-east-1.”

### 2.6 Named product map (quick reference)

| Product | Company | Role in coordination |
|---|---|---|
| Proteus, Sequoia, Hercules, Pegasus, Vulcan, DeepFleet | Amazon Robotics | Mixed: grid-central + open-area AMR + learned traffic |
| OSP bots, OMRS Chuck/Porter, Ocado IQ | Ocado | Grid: 10 Hz central; AMR: software-assigned tasks |
| LocusONE, Origin, Vector, Array | Locus | Cloud orchestration + collaborative AMRs |
| RCS + PopPick / RoboShuttle | Geek+ | Central RCS, #1 AMR vendor by Interact share |
| HaiPick ACR + AMRs | Hai Robotics | Hierarchical G2P |
| AutoStore R5/R5+ / software | AutoStore | Cube AS/RS |
| Ranger + GreyMatter | GreyOrange | AI WES, hardware-agnostic claims |
| QuickMix / RCS | Quicktron | Central + AMR |
| Fetch / Symmetry → Skild Brain | Zebra → Skild AI (2026) | Was hybrid AMR; now foundation-model play |
| MiR Fleet, MiR250/1350 | MiR / Teradyne | Hybrid manufacturing AMRs |
| OTTO Fleet Manager, OTTO 600/1500 | OTTO / Rockwell | Hybrid + intersection exchange |
| Stretch | Boston Dynamics / Hyundai | Cell autonomy + WMS |
| Isaac ROS, Mission Control, cuOpt | NVIDIA | Reference hybrid stack, VDA5050 |
| Nav2, Open-RMF, rmw_zenoh | Open Robotics / Eclipse | Open industrial stack |
| VDA 5050 | VDA | Standard master↔AGV API |

---

## 3. Who actually uses distributed / edge approaches

### 3.1 Amazon Robotics

- **What they do:** Design, manufacture, and operate the world’s largest industrial mobile-robot fleet (Amazon’s wording) inside Amazon’s own network. Kiva acquisition (2012) took goods-to-person pods off the merchant market and created the startup wave (Locus, 6 River, Geek+, GreyOrange).
- **Centralized or distributed?** **Both, stacked.** Drive-unit floors are a **centralized multi-agent traffic problem** (DeepFleet: assign tasks, route around congestion, +10% travel time). Proteus is **onboard autonomy** among humans. Safety is onboard. Training is cloud (SageMaker). Amazon Science says they cannot simulate a couple thousand robots faster than real time with the compute already used by the live planner — that is a **central compute bottleneck**, which is exactly why learned models and (for others) edge decomposition exist.
- **Public technical details:** DeepFleet paper, four architectures (robot-centric won most metrics; 13M–840M parameters): [https://arxiv.org/html/2508.08574v2](https://arxiv.org/html/2508.08574v2). Shreveport, LA (2024) as the multi-system showcase site.
- **PS relevance:** Amazon is *not* decentralized. Amazon *is* proof that **congestion, re-routing, and task assignment** are still open at planetary scale — they built a foundation model for it.

### 3.2 Ocado

- **What they do:** License **Ocado Smart Platform** (grocery CFCs) and, via the 6 River acquisition, **OMRS** (Chuck/Porter AMRs + Ocado IQ) for brownfield.
- **Centralized or distributed?** Grid bots: **maximally centralized**, 10 Hz, mid-mission replan, digital twin for “how many bots on this grid.” OMRS: **hybrid** like Locus (AMRs + associates). Predictive maintenance telemetry **to the cloud**; motion **on the grid controller**.
- **Public details:** Ocado technology page and Aug 2026 bot story (17,000+ bots, 10 Hz, 1,200 totes/h). Ingenia Erith profile: autonomy-on-grid rejected as throughput-infeasible.
- **PS relevance:** Mid-journey re-allocation is **production**, not a paper. The communication rate (10 Hz) is a **hard real-time LAN**, not Wi-Fi-to-cloud.

### 3.3 Locus Robotics

- **What they do:** Collaborative AMRs as RaaS for 3PLs and retailers (DHL, GEODIS, Ryder, CEVA, Cardinal Health, etc.).
- **Centralized or distributed?** **Cloud-central orchestration (LocusONE) + onboard NAV.** Elastic fleet sizing (vendor: 30%+ peak swell, some customers 3× for peak). That only works if task allocation is global and CA is local.
- **Public details:** 6B picks; 2–3× vs manual (vendor); GEODIS +50–100% UPH. Series G **$41.6M** reported Sep 2026 ([https://www.finsmes.com/2026/09/locus-robotics-raises-41-6m-in-series-g-funding.html](https://www.finsmes.com/2026/09/locus-robotics-raises-41-6m-in-series-g-funding.html)) — **SECONDARY** on round size until Locus IR confirms.
- **PS relevance:** Closest commercial cousin to “many robots in aisles, humans present, dynamic work.” Still not P2P.

### 3.4 Geek+

- **What they do:** Broadest commercial AMR catalog (shelf-to-person, tote-to-person, sorting, forklift AMRs, now embodied/humanoid experiments). HK-listed (2590.HK). Interact Analysis: #1 AMR share seven years running (company cites Interact in 1H2026 results).
- **Centralized or distributed?** **Hybrid RCS.** 81k robots cannot each solve global MAPF on a Pi; they also cannot freeze when a Shanghai cloud POP dies — so local NAV + site RCS is the only design that fits the installed base.
- **Public details:** 2025 profit inflection; 75%+ of revenue overseas in 1H2026; RoboShuttle Hyper **6,000 totes/h** (**VENDOR**). Annual results PDF: [https://ir.geekplus.com/](https://ir.geekplus.com/).
- **PS relevance:** The company that *won* AMRs still sells a **robot control system**, not a blockchain swarm.

### 3.5 NVIDIA Isaac AMR / Isaac ROS / cuOpt

- **What they do:** The default **open-ish industrial reference architecture** for anyone not Amazon/Ocado.
- **Centralized or distributed?** **Hybrid, documented.** Mission Control = fleet manager + cuOpt routes + VDA5050 dispatch. Mission Client = on-robot ROS 2. Jetson = onboard inference. Cloud = optional.
- **Public details:** GitHub `nvidia-isaac/isaac_mission_control`; Isaac ROS cloud-control docs; NGC containers. Known limitation (older notes): early Mission Control optimized **single-robot** global plans more than full VRP — the stack is evolving, not magic.
- **PS relevance:** If a student team says “we did it the NVIDIA way,” they mean **onboard client + on-prem dispatcher**, not ChatGPT-in-the-cloud driving PWM.

### 3.6 ROS 2 + DDS / Zenoh as the open industrial stack

- **DDS (Fast DDS, Cyclone, etc.):** excellent on a **wired LAN**, painful on **warehouse Wi-Fi** (discovery storms, multicast, NAT). Fine for a 5-robot lab; a 50-robot, multi-subnet, cloud-dashboard deployment is where people switch.
- **Zenoh (`rmw_zenoh`, `zenoh-bridge-ros2dds`):** router/peer architecture, topic filtering, namespacing per robot, WAN-friendly. Used by **Open-RMF Free Fleet** to talk to Nav2 robots without melting the RF.
- **Open-RMF:** task dispatch, traffic negotiation, lifts/doors, **heterogeneous fleets** — the open-source cousin of VDA 5050 + a WES.
- **InOrbit OpenRobOps:** sits “between ROS 2 and Open-RMF” so vendors stop writing a bespoke fleet manager ([https://www.inorbit.ai/blog/announcing-the-evolution-of-inorbits-product-suite](https://www.inorbit.ai/blog/announcing-the-evolution-of-inorbits-product-suite)).
- **PS relevance:** The open stack is **already** “edge-first comms + optional central tasker.” A hackathon that reinvented MQTT topic names is theater; a hackathon that implements **link-down local policy + choke-point protocol on Zenoh** is on-trend.

### 3.7 Other notable production users (short)

| Player | Coordination | Notes |
|---|---|---|
| **GreyOrange** (US/India/Singapore roots) | GreyMatter WES, “thousands of decisions/s,” hardware-agnostic CRN | Software-centric; Ranger robots |
| **Hai Robotics** (Shenzhen) | ACR + AMR hierarchy | Large fashion 3PL installs |
| **Quicktron** (Shanghai; KION/Dematic partnership) | RCS | 35k+ units official |
| **AutoStore** (Norway) | Central cube | Not AMR traffic; still multi-robot |
| **Exotec** (France) | Skypod 3D AMR-AS/RS | Vendor 5× throughput |
| **Symbotic** (US; Walmart) | High-density AHS, central software | Public company; MAPF papers use “Symbotic maps” |
| **MiR / Teradyne** | MiR Fleet | ISO 3691-4; factories more than e-com |
| **OTTO / Rockwell** | Fleet Manager + V2V-ish intersections | Manufacturing material flow |
| **Seegrid, Vecna, Fox, Balyo** | Hybrid | Pallet / tugger AMRs |
| **Formant, InOrbit** | Cloud ops / mixed-fleet orchestration | Meta-layer above vendor RCS |
| **Rapyuta Robotics** (Tokyo; ETH RoboEarth lineage) | Cloud robotics + ASRS | Academic-to-industry cloud/edge story |

### 3.8 Academic → industry spinouts (the ones that matter)

| Lineage | Company | What transferred |
|---|---|---|
| Kiva (Wurman, D’Andrea, Mountz) | Amazon Robotics | Centralized pod MAPF at scale; D’Andrea later Verity (drones) |
| Willow Garage / Fetch (Melonee Wise) | Fetch → Zebra → **Skild AI (2026)** | AMR NAV in unstructured DCs; now foundation-model warehouse brain |
| University of Waterloo / Clearpath | **OTTO Motors → Rockwell (2023)** | Heavy AMRs + fleet manager |
| ETH / RoboEarth “Rapyuta” cloud engine | **Rapyuta Robotics** | Cloud robotics → warehouse ASRS |
| MIT / Berkeley / Covariant (Abbeel et al.) | Covariant → **Amazon reverse-acquihire 2024** | Dexterous picking, not traffic |
| 6 River (ex-Kiva founders) | Shopify **$450M (2019)** → **Ocado (2023)** | Collaborative AMR “Chuck” |
| CMU / Skild (Pathak) | Skild + Fetch assets | Generalist robot brain on warehouse hardware |
| Open Robotics | Open-RMF, Nav2 | The open WES/fleet layer |

**Multi-Robot Systems labs** (Prorok/Cambridge, Rus/MIT, Pavone/Stanford, Koenig/USC MAPF, Ma/CMU, Stern et al. MAPF zoo) mostly transfer **algorithms** (CBS, PBS, PIBT, LNS2, lifelong MAPF) into Amazon/NVIDIA/Geek+ planners rather than shipping a branded “decentralized warehouse OS.” The **Lifelong Multi-Agent Path Finding** literature *is* the scientific home of this PS.

---

## 4. Y Combinator and the startup landscape

YC is **not** where million-robot traffic control is built. YC is where **brownfield labor replacement** (pick, unload, pack) and **robot ops tooling** get funded. That still maps to the PS: those robots will collide in aisles unless *someone* coordinates them.

### 4.1 YC companies directly in the PS neighborhood

| Company | Batch | One-line | Public $ | PS relevance |
|---|---|---|---|---|
| **Manifold** | S2026 | Per-pick robotic labor; no retrofit; claims **$75bn** US warehouse labor, **10%** automation | Undisclosed (YC) | States the labor TAM; will need multi-robot coordination as soon as >1 cell is live. [https://www.ycombinator.com/companies/manifold-2](https://www.ycombinator.com/companies/manifold-2) |
| **InLoop Robotics** | Spring 2026 | Rental robot arms for pack/kit; human-in-loop teleop; **300+ picks/h** claimed | Undisclosed | Stationary cells; orchestration with AMRs is the next integration. [https://www.ycombinator.com/companies/inloop-robotics](https://www.ycombinator.com/companies/inloop-robotics) |
| **Yondu** | W24 (YC page; $500k seed reported) | Drop-in humanoid/bin-pick for 3PLs; WMS routing + teleop→autonomy | ~$0.5M reported | Explicitly positions AMR as “low automation” and themselves as the missing pick. Coordination software mentioned. [https://www.ycombinator.com/companies/yondu](https://www.ycombinator.com/companies/yondu) |
| **Remy AI** | W2026 | Manipulation robots for e-com 3PLs | Undisclosed | Same: arms + future mobile base = traffic PS |
| **Servo7** | W2026 (Amsterdam) | Loose-loaded container unloading; CEVA, DHL, PostNL named | Undisclosed | Dock congestion; not aisle MAPF, but multi-robot dock scheduling is cousin |
| **DeepReach** | S2026 | Warehouse human-demo data flywheel | Undisclosed | Data, not coordination |
| **Agency Tool Company** | S2026 | OTA deploy to **Jetson and Raspberry Pi**; logistics robotics among launch partners | Undisclosed | Admits **field networks drop**; resume-able deploy. Directly about edge ops. |
| **Formant** (often listed in robotics ops, YC-adjacent / alumni ecosystem; founded 2017) | — | Cloud+edge robot ops, teleop, mixed-fleet orchestration | **$21M** (2023, BMW i Ventures / Intel Capital) | The “single pane of glass” when you have four AMR vendors. [https://www.intelcapital.com/formants-explosive-enterprise-growth-attracts-new-investment-led-by-bmw-i-ventures-joined-by-intel-capital-and-gs-futures/](https://www.intelcapital.com/formants-explosive-enterprise-growth-attracts-new-investment-led-by-bmw-i-ventures-joined-by-intel-capital-and-gs-futures/) |
| **InOrbit** | **W18** (widely cited YC alumnus) | Mixed-fleet orchestration, OpenRobOps, Open-RMF alignment | Not recently public | Closest YC-lineage company to *this exact PS* (vendor-agnostic coordination). [https://www.inorbit.ai/orchestration](https://www.inorbit.ai/orchestration) |

YC robotics directory (127 companies as of Sep 2026): [https://www.ycombinator.com/companies/industry/robotics](https://www.ycombinator.com/companies/industry/robotics). Most are humanoids, defense, data, welding — **not** warehouse MAPF. The 2026 warehouse cluster (Manifold, InLoop, Remy, Servo7, Yondu) is **manipulation-heavy**, which is the current VC fashion. **Fleet coordination is treated as infrastructure** (InOrbit, Formant, Open-RMF, VDA 5050), which is why a student PS can still be novel at the *algorithm* layer.

### 4.2 Notable non-YC startups and vendors worldwide

**China**

- **Geek+** (Beijing, HK-listed) — §3.4.
- **Hai Robotics** (Shenzhen) — ACR leader.
- **Quicktron / Flashhold** (Shanghai) — KION/Dematic channel.
- **Hikrobot** (Hikvision group) — huge domestic AGV/AMR.
- **Standard Robots, ForwardX, Kenhwin** — AMR / vision.

**Europe**

- **Ocado** (UK, LSE:OCDO) — grid + OMRS.
- **AutoStore** (Norway, OSE:AUTO).
- **Exotec** (France, Skypod).
- **Magazino → Jungheinrich**; **Arculus → Jungheinrich**.
- **ASTI / Sevensense → ABB**.
- **Servo7** (NL, YC) — trailer unload.
- **MiR** (Denmark, Teradyne).

**India**

- **GreyOrange** (founded India, HQ now US) — GreyMatter.
- **Addverb** (Reliance-backed) — AMRs, sortation, WES.
- **Tata, TVS** automation arms; various WMS+AMR integrators.

**Israel**

- **Foretellix-style** validation is auto; warehouse-adjacent: **DriveNets** is networking. Historically **Warehouse Robotics** activity via **inVia** (US with Israeli tech ties) and computer-vision pickers. Israel’s 2025–26 robotics energy is more **defense / autonomy** than tote AMRs — do not overclaim.

**Japan**

- **Rapyuta Robotics** — cloud/ASRS.
- **Mujin** (intelligence for industrial robots).
- **Hakobot, Preferred Robotics**, and the **Daifuku / Murata / Toyota** (Vanderlande) incumbent stack — Japan still wins **fixed automation** more than free-roam AMR share.

**United States (non-YC)**

- **Locus, Symbotic, Berkshire Grey, RightHand, Boston Dynamics, Skild, Covariant-alumni-at-Amazon, Fox Robotics, Seegrid, Vecna, Formant.**

### 4.3 How this maps to the PS

Investors are paying for **picks per hour** and **unloads per hour**. They assume **someone else’s software** will keep robots from gridlocking. That software market (fleet management / WES / VDA 5050 / Open-RMF) is real — MarkWide’s **$2.8B (2026) robot fleet-management software** TAM is **SECONDARY**, but the *category* (InOrbit, Formant, vendor RCS, NVIDIA Mission Control) is not imaginary. A student decentralized coordinator is a **thin, edge-native slice** of that category.

---

## 5. Business state 2025–2026

### 5.1 Consolidation and acquisitions

| Year | Deal | Signal |
|---|---|---|
| 2012 | Amazon ← **Kiva ~$775M** | Incumbent takes G2P off the market |
| 2018–19 | Teradyne ← **MiR**; Shopify ← **6 River $450M** | Collaborative AMR gold rush |
| 2021 | Zebra ← **Fetch ~$290–300M** | Scanner giant tries AMR |
| 2023 | Rockwell ← **Clearpath / OTTO**; Ocado ← **6 River** (from Shopify); ABB ← **Sevensense** | Automation conglomerates want AMR |
| 2023 | Jungheinrich ← **Magazino**, **Arculus**; SSI Schäfer ← **DS Automotion** | European MH incumbents fill AMR holes |
| 2024 | Amazon ← **Covariant** talent (reverse acquihire) | Picking intelligence goes in-house |
| 2025 | Zebra **winds down** Fetch AMR group | Scale was not there for Zebra |
| 2026 | **Skild AI ← Zebra robotics / Fetch assets** | Foundation-model companies buying *hardware + data + installed base* |
| 2026 | Locus reported **Nexera** tuck-in; Comau ← Invent (trade press) | Orchestration + intra-logistics tuck-ins |
| 2025–26 | Geek+ **IPO (HK)** then embodied-intelligence spend | Public AMR pure-play exists; still not easy money (1H2026 still loss-making after R&D) |
| 2025 | AutoStore **revenue −10.4%** YoY | Cube AS/RS cyclical; not “AMRs won forever” |

Sources: LogisticsIQ M&A list in the $55B-by-2030 release; Robot Report on Zebra wind-down and Skild (Apr 2026): [https://www.therobotreport.com/skild-acquires-fetch-robotics-assets-from-zebra-automation/](https://www.therobotreport.com/skild-acquires-fetch-robotics-assets-from-zebra-automation/); Supply Chain Dive on Shopify/6 River: [https://www.supplychaindive.com/news/shopify-acquire-robotics-startup-6-river-systems-450m-fulfillment/562587/](https://www.supplychaindive.com/news/shopify-acquire-robotics-startup-6-river-systems-450m-fulfillment/562587/); AutoStore Q4 2025; Geek+ 1H2026 PR.

**Read the Zebra/Fetch story carefully:** a Fortune-500 with a $300M AMR bet **exited**. That is evidence the **business** is hard (integration, RF, safety, sales cycles), not that the **problem** is fake. Skild buying the ashes is evidence that **software brains + existing robots** is the 2026 thesis.

### 5.2 Who is winning (2026, unromantic)

| Segment | Incumbent winner | Challenger |
|---|---|---|
| Captive e-com scale | **Amazon** (1M robots, DeepFleet) | Nobody; they don’t sell it |
| Grocery grid | **Ocado** (software) vs **AutoStore** (hardware cube) vs **Exotec** | Kroger pullback in US (2026) shows **deployment risk**, not algorithm risk |
| Merchant AMR (sell to 3PLs) | **Geek+** on units/share (Interact); **Locus** on Western 3PL RaaS mindshare | Quicktron, Hai, GreyOrange |
| Heavy manufacturing AMR | **MiR**, **OTTO/Rockwell**, **Seegrid** | Chinese pallet AMRs on price |
| Cube/ASRS | **AutoStore**, **Exotec**, **Symbotic**, **Hai** | — |
| Mixed-fleet software | Vendor RCS + **VDA 5050** + **InOrbit/Formant** | Open-RMF (open, slower sales) |
| Trailer unload / case | **Boston Dynamics Stretch** (DHL MOU), **Servo7**-class startups | Still early unit counts |

**China still ships the most mobile robots**; Interact says that *share* is peaking as US/EU/RoAPAC catch up and as Chinese unit prices stay lower (so revenue share falls faster than shipment share).

### 5.3 Open problems that are *exactly* the PS gaps

These remain unsolved as *products*, not as PowerPoint:

1. **Graceful degradation when the master or the radio dies.** Safety stop is solved (ISO). **Continuing the mission with local policies** without creating a deadlock storm is not a shipped, vendor-neutral feature.
2. **Choke points** (narrow aisles, single-cell doors, elevator vestibules, pack-station queues). Amazon needed DeepFleet *after* a decade of Kiva. MAPF papers still burn pages on this.
3. **Dynamic re-tasking** when orders change, a robot is delayed, or a human blocks an aisle. Ocado does it at 10 Hz on a private grid. Free-roam AMRs among people do it more slowly and centrally.
4. **Heterogeneous fleets.** VDA 5050 and Open-RMF exist because DHL does not want five traffic managers. Interoperability is **incomplete** in 2026.
5. **Wi-Fi / roaming.** Integrators still treat RF as a custom professional-services project.
6. **Compute placement.** Jetson-class onboard inference is winning for vision; **global MAPF still wants a GPU in the IT closet**, not a Pi. The PS’s Raspberry Pi is a **stand-in for “onboard/edge,”** not for Amazon’s planner.
7. **Lifelong MAPF at 100–1,000 agents with incomplete comms.** Academic (CBS, PBS, PIBT, LNS, RL-priority) and Amazon (DeepFleet) are the two frontiers. Neither is “solved.”

### 5.4 Why “decentralized on Raspberry Pi” is a real slice — and where it is theater

**Real (mimic this):**

- Onboard **local CA** that does not require the cloud.
- A **protocol** when two robots meet at a choke point (priority, reservation, virtual traffic light).
- **Replan / re-allocate** when a path is blocked or a robot drops off the network.
- **Edge-first comms** (Zenoh/DDS/MQTT LAN), cloud optional.
- Measuring **makespan / extra wait** vs stop-and-wait — Amazon’s 10% and MAPF’s ~25% say **20% is a plausible research target** on a naive baseline.

**Theater (do not pretend this is Amazon):**

- Raspberry Pi as a **safety-rated** controller (it is not).
- “Fully decentralized, no leader” at **thousands** of agents on a grid — Ocado tried the thought experiment and rejected it.
- Claiming **2–3× throughput** (that is vs humans, from Locus) for a coordination algorithm.
- Ignoring **ISO 3691-4** scanners, **e-stop**, and **pedestrians**.
- Cloud REST calls inside the **50 ms** obstacle loop.
- One global A\* for 200 agents every tick on a Pi.

**The industrial trend the PS rides:** compute and *reactive* intelligence move **out to the robot and the site**; *learning* and *analytics* stay in the cloud; *traffic* stays **mostly central but must fail soft**. A student decentralized coordinator is a **fail-soft / choke-point / comms-loss** module that vendors still handle poorly in brownfield Wi-Fi warehouses.

---

## 6. Scorecard: evidence the PS is a real problem

| Claim in PS | Supporting evidence | Source | Strength |
|---|---|---|---|
| **Cloud path planning has high latency** | Control loops need tens of ms; public-cloud RTT is typically **50–200 ms** and worse under congestion. NVIDIA/Isaac and ISO put safety and local NAV **onboard**. Task assignment *can* live at 100 ms–seconds. The claim is **true for the inner loop**, overstated if the PS meant “all planning.” | NVIDIA Isaac ROS Cloud Control (2025–26); Cisco AGV CRD; practitioner edge-vs-cloud tables (ModulEdge, CXTMS 2026) | **Strong** (inner loop); **medium** (if applied to WMS-level tasking) |
| **Wi-Fi dead zones are a real warehouse risk** | Entire integrator category (Cisco URWB, private 5G RFPs, AMR Wi-Fi redesigns). Synergy: ~**50%** of surveyed ops **idled automation** on connectivity/software interrupts; **84%** had a significant disruption in 24 months. Metal racks + roaming gaps of **50–200 ms** cause safety stops. No single public $Y dead-zone postmortem. | Cisco CRD; Performance Networks; Synergy/FreightWaves 2026; Descartes-adjacent outage coverage | **Strong** as engineering risk; **medium** as quantified $ loss |
| **Central server is a SPOF** | VDA 5050 *assumes* a master control — and therefore a failure domain. Hybrid WMS/edge appliances are sold specifically because **cloud WMS outages idle robots** ($5k–$100k/h). Ocado/Amazon mitigate with on-prem CFC/FC software HA, not by deleting the master. Fetch/Zebra scale failure is commercial, not SPOF, but shows operational brittleness. | VDA 5050:2025; Synergy 2026; Ocado 10 Hz controller (implied HA) | **Strong** that SPOF is a design driver; **weak** that production sites run a single un-paired VM |
| **Edge / decentralized is the industry shift** | **Edge: yes.** Jetson, Isaac ROS, onboard CA, IDC edge spend **$261B (2025)**. **Fully decentralized planning: no.** Ocado rejected it; Amazon DeepFleet is central; VDA 5050 is master+vehicle; Geek+/Locus/OTTO are hybrid. Shift is **hybrid / edge-for-reactivity**, not gossip MAPF. | IDC 2025; Ocado Ingenia; Amazon Science 2025; NVIDIA Mission Control | **Strong** for edge; **weak** for fully decentralized |
| **Collision avoidance at choke points matters** | DeepFleet’s *raison d’être* is congestion and deadlock on FC/sortation floors; +**10%** travel time. Lifelong MAPF literature exists because naive CA deadlocks. OTTO markets intersection prediction. Hai/Geek+ G2P maps are bottlenecked at stations and aisles. OSHA data is mostly **human** injury, not robot-robot. | Amazon Science / DeepFleet arXiv 2025; OTTO Fleet Manager; MAPF (Stern et al.; Yan et al. 2026) | **Strong** for throughput; **medium** for safety-incident stats |
| **Dynamic re-routing / re-allocation matters** | Ocado: missions **changed mid-journey** at 10 Hz as new orders arrive. LocusONE: real-time task interleaving and peak fleet swell. Amazon DeepFleet: longer-term goal is **assignments + target locations**, not just prediction. Academic lifelong MAPF is literally this. | Ocado 2026 bot blog; Locus interviews; DeepFleet blog | **Strong** |
| **20% time improvement vs stop-and-wait is a plausible target** | Amazon got **10%** vs an *already sophisticated* central planner. RL-guided prioritized planning got **~25% throughput** vs random-priority RH-PP in warehouse MAPF sims. Locus **2–3×** is vs **humans**, wrong baseline. Stop-and-wait is a *worse* baseline than Amazon’s old stack, so **20% vs stop-and-wait is conservative**, not ambitious — **if** the sim is congested. Empty map: you will not see 20%. | Amazon 2025; Yan et al. JAIR/arXiv 2026; Locus (wrong baseline) | **Strong** as a *congested-sim* target; **weak** as a universal KPI |

---

## 7. Implications for a student team

### 7.1 Realistic to mimic in simulation (do these)

1. **Hybrid stack in miniature:** global task queue + local reactive CA + a **choke-point protocol** (reservation, priority, or virtual traffic light). This is OTTO + VDA 5050 + Nav2, shrunk.
2. **Comms-loss mode:** when the “master” socket drops, robots keep last velocity command for N seconds then switch to **local right-of-way rules**. Measure extra delay vs oracle. This is the actual industrial gap.
3. **Dynamic re-allocation:** inject a new high-priority order or a blocked aisle; compare stop-and-wait vs replan. Ocado does this; MAPF papers do this.
4. **Zone hierarchy:** 4 zones × 5 robots beats 20-agent global CBS on a Pi, and is how Amazon floors actually decompose.
5. **Metrics that a reviewer will respect:** extra wait at intersections, throughput (goals/min), deadlock count, messages/s, recovery time after radio drop. Not “2–3× vs humans.”
6. **Middleware honesty:** ROS 2 + fake packet loss, or Zenoh, is more on-trend than a custom TCP mesh you will not finish.

### 7.2 Theater (avoid, or label as toy)

1. **Calling a Pi swarm “Amazon-scale decentralized architecture.”** Amazon is centralized traffic + onboard safety. Say you are implementing the **fail-soft / intersection** module those systems still lack in brownfield Wi-Fi sites.
2. **Safety theater:** printing “ISO 3691-4 compliant” without a safety scanner or a documented e-stop path.
3. **Cloud-in-the-loop demos** that die when the laptop Wi-Fi hiccups — the PS is arguing *against* that.
4. **Benchmarking against humans** or against a broken planner to hit 20%. Use **stop-and-wait** and **central A\* with perfect comms** as the two brackets.
5. **P2P blockchain / CRDT swarm** unless you have a week to waste. Not what DHL buys.
6. **Heterogeneous fleets** with no VDA 5050-like schema — one YAML of poses is enough; don’t fake a WMS.

### 7.3 What “good” looks like for a hackathon / NeurIPS workshop paper

A credible narrative:

> Production AMRs already do onboard collision avoidance and central task assignment (Locus, Geek+, Isaac, VDA 5050). They still fail closed on radio loss and still queue at choke points. We implement a lightweight decentralized policy for those two gaps, on edge-class compute, and show ~20% less delay than stop-and-wait under packet loss — the same *shape* of gain Amazon reports (10%) and MAPF papers report (25%) on different baselines.

That sentence is defensible with the sources in this report. “We invented decentralized warehouses” is not.

---

## 8. Source appendix (high-value URLs)

**Analyst / government**

- Interact Analysis, Jan 2026: [https://interactanalysis.com/mobile-robots-market-outpaces-fixed-automation/](https://interactanalysis.com/mobile-robots-market-outpaces-fixed-automation/)
- Interact Analysis, Jan 2025: [https://interactanalysis.com/macro-economic-factors-cause-slowdown-in-global-mobile-robot-market/](https://interactanalysis.com/macro-economic-factors-cause-slowdown-in-global-mobile-robot-market/)
- BLS NAICS 493 earnings: [https://data.bls.gov/timeseries/CEU4349300003](https://data.bls.gov/timeseries/CEU4349300003)
- McKinsey warehouse automation, Sep 2024: [https://www.mckinsey.com/industries/industrials-and-electronics/our-insights/distribution-blog/navigating-warehouse-automation-strategy-for-the-distributor-market](https://www.mckinsey.com/industries/industrials-and-electronics/our-insights/distribution-blog/navigating-warehouse-automation-strategy-for-the-distributor-market)
- Descartes labor study, Jan 2024: [https://www.descartes.com/resources/news/descartes-study-reveals-76-supply-chain-and-logistics-operations-are-experiencing](https://www.descartes.com/resources/news/descartes-study-reveals-76-supply-chain-and-logistics-operations-are-experiencing)
- IDC edge spending, Mar 2025: [https://my.idc.com/getdoc.jsp?containerId=prUS53261225](https://my.idc.com/getdoc.jsp?containerId=prUS53261225)
- LogisticsIQ warehouse automation: [https://www.thelogisticsiq.com/research/warehouse-automation-market](https://www.thelogisticsiq.com/research/warehouse-automation-market)
- Mordor warehouse automation: [https://www.mordorintelligence.com/industry-reports/warehouse-automation-market](https://www.mordorintelligence.com/industry-reports/warehouse-automation-market)

**Operators / vendors**

- Amazon 1M robots + DeepFleet: [https://www.aboutamazon.com/news/operations/amazon-million-robots-ai-foundation-model](https://www.aboutamazon.com/news/operations/amazon-million-robots-ai-foundation-model)
- Amazon Science DeepFleet: [https://www.amazon.science/blog/amazon-builds-first-foundation-model-for-multirobot-coordination](https://www.amazon.science/blog/amazon-builds-first-foundation-model-for-multirobot-coordination)
- DeepFleet paper: [https://arxiv.org/html/2508.08574v2](https://arxiv.org/html/2508.08574v2)
- Ocado bots: [https://www.ocadogroup.com/newsroom/stories/meet-the-bots-that-power-ocado-groups-online-grocery-fulfilment-across-the-globe](https://www.ocadogroup.com/newsroom/stories/meet-the-bots-that-power-ocado-groups-online-grocery-fulfilment-across-the-globe)
- Geek+ 1H2026: [https://www.prnewswire.com/news-releases/subscription-based-services-boom-geek-reports-2026-interim-results-orders-up-35-5-breakthroughs-across-the-business-spectrum-302867104.html](https://www.prnewswire.com/news-releases/subscription-based-services-boom-geek-reports-2026-interim-results-orders-up-35-5-breakthroughs-across-the-business-spectrum-302867104.html)
- Locus: [https://locusrobotics.com/](https://locusrobotics.com/)
- AutoStore Q4 2025: [https://news.cision.com/autostore-as/r/autostore--q4-2025-financial-results,c4306434](https://news.cision.com/autostore-as/r/autostore--q4-2025-financial-results,c4306434)
- Boston Dynamics / DHL: [https://bostondynamics.com/news/dhl-signs-mou-for-additional-1000-robot-deployment/](https://bostondynamics.com/news/dhl-signs-mou-for-additional-1000-robot-deployment/)
- NVIDIA Mission Control: [https://github.com/nvidia-isaac/isaac_mission_control](https://github.com/nvidia-isaac/isaac_mission_control)
- VDA 5050: [https://www.vda.de/dam/jcr:f0c9c019-1506-4dee-998a-e92723fbf025/EN-VDA5050-V2_0_0.pdf](https://www.vda.de/dam/jcr:f0c9c019-1506-4dee-998a-e92723fbf025/EN-VDA5050-V2_0_0.pdf)

**Resilience / wireless / edge**

- Synergy / FreightWaves downtime: [https://theproducewire.com/warehouses-face-100k-hour-downtime-risk-as-cloud-outages-mount/](https://theproducewire.com/warehouses-face-100k-hour-downtime-risk-as-cloud-outages-mount/)
- Cisco factory AGV wireless CRD: [https://www.cisco.com/c/en/us/td/docs/solutions/Verticals/Industrial_Automation/IA_Verticals/Factory/IA-Factory-CRD1/IA-Factory-CRD1.html](https://www.cisco.com/c/en/us/td/docs/solutions/Verticals/Industrial_Automation/IA_Verticals/Factory/IA-Factory-CRD1/IA-Factory-CRD1.html)
- Eclipse Zenoh ROS 2: [https://github.com/eclipse-zenoh/zenoh-plugin-ros2dds](https://github.com/eclipse-zenoh/zenoh-plugin-ros2dds)

**Academic**

- Lifelong MAPF RL-priority, ~25% throughput: [https://arxiv.org/html/2603.23838](https://arxiv.org/html/2603.23838)
- OSHA robot SIR analysis: [https://www.sciencedirect.com/science/article/abs/pii/S0003687024001017](https://www.sciencedirect.com/science/article/abs/pii/S0003687024001017)
- Virtual traffic lights hybrid MRS: [https://arxiv.org/pdf/2511.07811](https://arxiv.org/pdf/2511.07811)

**YC**

- [https://www.ycombinator.com/companies/industry/robotics](https://www.ycombinator.com/companies/industry/robotics)
- [https://www.ycombinator.com/companies/manifold-2](https://www.ycombinator.com/companies/manifold-2)

---

## 9. Limitations (read before citing in a pitch)

- Market-size firms **do not share a definition** of AMR vs AGV vs warehouse automation. Always name the firm.
- Throughput multiples are **almost always vendor-measured**. Amazon’s 10% is the rare case of a *sophisticated* baseline.
- We did not obtain paywalled Interact full PDFs, Amazon 10-K robot-count line items, or OSHA’s raw SIR dump for a re-count. Where that matters, it is tagged.
- “Decentralized” in marketing (GreyMatter, LocusONE, Skild Brain) usually means **software-defined and hardware-agnostic**, not **leaderless**.

**Bottom line:** The economic problem is genuine (labor, $5B→$14B mobile robots, 1 million Amazon robots, 81k Geek+ units, 17k Ocado bots, 76% of logistics leaders short-staffed). The engineering problem the PS names (latency, Wi-Fi, SPOF, choke points, re-routing) is what DeepFleet, VDA 5050, Isaac Mission Control, and hybrid WMS are all spending money on. The industry answer in 2026 is **hybrid edge**, not a leaderless Pi mesh — and that still leaves a sharp, publishable gap exactly where a student team can work.
