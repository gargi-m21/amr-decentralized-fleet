# Architecture Lock-In

**Date:** 2026-09-04  
**Inputs:** reports `01`, `02`, `03`, `04`, `05`, `06` (read end-to-end) plus the papers in `papers/` (RHCR AAAI 2021, CS-PIBT ICRA 2025, Follower AAAI 2024, MAPF-GPT AAAI 2025, PIBT IJCAI 2019, LaCAM AAAI 2023, PBS AAAI 2019, CBS 2015, Token-Passing AAMAS 2017, CBBA T-RO 2009, ORCA ISRR 2011, Nav2 IROS 2020, CADRL IROS 2018).  
**Constraints from you:** quality over “beginner/time” shortcuts; edge inference is real; a 2D top-down pygame window is **not** the judged demo; do not copy GitHub as the product.

This document is the freeze. Later engineering changes the *implementation*, not the contracts below, unless a paper or a hardware measurement falsifies a contract.

---

## How the open questions were settled

### Q1 — What is a compelling, honest, decentralized demo?

**Lock-in: one laptop as the judged demo, N Docker containers as N robots, Gazebo as the world, a sixth process as a spectator dashboard that also shows each robot’s local view.**

Not five physical laptops as the *primary* system. Not a single Python process with a shared `FleetState`. Not pygame as the thing judges watch.

**Why this, from first principles.**

Honesty in this PS is not “how many keyboards are on the table.” Honesty is: **no robot’s planner may read another robot’s memory**. The only legal channel is a serialized message (pose + intent + bids + tokens) that can be delayed, dropped, or captured on the wire. Report 01’s unplug test is the same idea: if killing a process changes another robot’s brain, that process was the tower.

Docker on one laptop is the strongest *scientific* realization of that contract:

- Each AMR is a **separate PID namespace, filesystem, and CPU budget**. `docker inspect` shows it. `tcpdump` on the compose network shows Intent packets. Judges can `docker stop dashboard` mid-run.
- The same compose file is the **edge story**: pin each container to 1–2 CPU cores and 1–2 GB RAM (Pi 4/5 class). Optionally move **one** container onto a real Raspberry Pi 5 / Orin Nano that joins the same Zenoh mesh. That is software-in-the-loop, which report 03 already named as the only honest “runs on edge” claim without welding robots.
- `tc netem` on the docker bridge (50–150 ms delay, 20–30% drop, partition one robot) is a **reproducible** Wi-Fi dead-zone demo. Five laptops on café Wi-Fi are theater that **destroys** the 20% makespan experiment (clock skew, uncontrolled loss, unre-runnable CSVs). Report 01 requires frozen seeds and the same clock. Docker gives you that.
- Local-view **cards** on the dashboard (each robot’s lidar/camera crop, costmap, reserved cells, last-heard neighbors) prove that robots do not share a god camera. Five extra laptop screens showing the same cards are optional stagecraft, not architecture.

**Where five laptops sit.** They are a **stretch theater pass**, after the docker system is already scoring 0 collisions and ≥20%. Topology: laptop 0 runs Gazebo + dashboard; laptops 1–5 each run one robot container against that world over Ethernet. Same images, same messages. If that works, you have a distributed-systems photo. It is not required to *be* the system.

**Why not “single laptop, many ROS nodes, no Docker”?** Namespaced ROS 2 nodes *can* be honest if they only subscribe to `/fleet/intent` and never import a sibling’s Python object. Judges will not believe that without process isolation. Docker makes the isolation *visible*. Use Docker.

**Why 3D, not 2D top view.** Report 03 said pygame is the fastest *spine*. You overrode the “impress the judges” axis: a grid of disks is MAPF homework. The judged window is **Gazebo Harmonic + AWS small-warehouse SDF** (shelves, pallets, choke aisles, cameras). The **discrete coordinator still plans on a 2D occupancy graph** of that same world (RHCR’s own execution note: Hönig-style post-process from grid plans to kinematics). Headless 2D remains the **eval harness** for N=10 seeded trials. The live demo is physics.

Isaac Sim is a **visual twin**, not the development loop, unless an RTX 4080-class GPU is actually on the table (report 03: Isaac 6.0 min 16 GB VRAM). If it is, spawn the *same* docker brains against Isaac via ROS 2 bridge. Do not fork the planner.

### Q2 — Where is learning genuine, how do you train, which pretrained weights?

**Lock-in: classical stack is the product. Learning is a fork on three modules only, always behind a shield. Public pretrained weights are used for perception and as a FollowerLite preference net. You train travel-time and (optionally) your own imitator on *your* map.**

This is not taste. It is what the 2024–2026 papers measured:

- **CS-PIBT (ICRA 2025):** large-scale imitation *without* a 1-step collision shield is weak. The *same* net plus CS-PIBT, trained in **minutes** on **one** scene’s worth of data, beats prior ML MAPF. They warn: always compare to **PIBT with greedy heuristic**, because a net that just copies “move downhill” is PIBT in a trench coat. Future nets should spend capacity on **longer horizon** (target conflicts, bottlenecks), not on 1-step dodges.
- **Follower (AAAI 2024):** do **not** ask RL to solve lifelong MAPF end-to-end. Split: heuristic search builds a path (with congestion-aware edge costs); a small policy follows the **next waypoint** and detours locally. FollowerLite has **~3,678 parameters**, trains in **~30 minutes** on a single GPU, ships as **19 KB ONNX**. Their *problem setting* assumes **no communication of goals/paths** — that **contradicts our PS**. We take the hybrid, we **add** P2P intent (report 01/05: brake lights).
- **RHCR (AAAI 2021, Amazon Robotics co-authors):** lifelong warehouses are windowed (`w` horizon, `h` replan). Resolving collisions over the whole remaining path is often **unnecessary** because new goals arrive. Throughput similar, runtime much smaller. **The solver is centralized.** Industry report 02 says the same: production is **hybrid** (onboard dodge + fleet manager). Our PS forbids the manager in the live loop. We keep RHCR as an **offline expert / quality oracle**, not as `CentralPlanner.plan(all)`.
- **MAPF-GPT (AAAI 2025):** 1B expert pairs from LaCAM, transformer, 2M/6M/85M public weights. Strong among *learnable* solvers, **no collision certificate**. Use 2M as a laptop ablation. Not the Pi coordinator.
- **Report 06:** there is **no** public trained warehouse coordinator. YOLO11n / EfficientDet-lite0 / PeopleNet are the real edge weights. Follower-lite is the only tiny MAPF net.

Training steps for each fork are in §B.7. You do not need to train anything for a passing demo. You **should** train the travel-time regressor if you want the ML story to be honest rather than a YOLO sticker.

---

# A. What the problem statement is

## A.1 Core ask (the product)

- A **fleet of at least 3 AMRs** in a **dynamic warehouse** (aisles, racks, choke points, work that changes mid-run).
- Each robot **plans and negotiates onboard** (Pi / Jetson-class compute). **No cloud path-planning API** in the loop.
- Robots **talk to each other** (not to a tower) to share **position and intent**.
- When two or more robots want the **same narrow space**, they **do not collide** and they **do not freeze forever**.
- When an aisle dies or a robot cannot finish a job, the fleet **re-routes** and/or **re-assigns** pickups **without a human re-clicking goals**.
- A **dashboard watches** poses and battery. It does not drive.
- **Score:** zero inter-robot collisions **and** ≥20% lower **makespan** than a **fair stop-and-wait** baseline on **overlapping paths**.

## A.2 What “done” looks like (passing vs fake)

- **Passing decentralization:** N independently instantiable agent binaries; sibling state arrives **only** as messages; dashboard kill does not stop the fleet; packet capture exists.
- **Fake decentralization:** shared `FleetState`; one `planner` node that emits everyone’s `cmd_vel`; MQTT broker that **computes** paths; Open-RMF traffic schedule as the only “algorithm.”
- **Passing dynamics:** mid-run blockage, new job, or robot dropout actually changes paths/owners.
- **Fake dynamics:** static CBS at t=0; blockage ignored; “reassign” = restart sim.
- **Passing edge:** same coordinator library runs under CPU/RAM caps; optional one real SBC. Replan budget ~50–200 ms on Pi-class for the discrete layer; ORCA/CBF at 10–20 Hz.
- **Fake edge:** a 4090 transformer labeled “onboard.”

## A.3 Edge cases the design must survive

These are not extras. They are how judges probe the three numbered requirements.

### Communication

- **Packet loss / delay:** 20–30% drop, 50–150 ms RTT. Stale intent expires (TTL). Missing neighbor is treated as an **inflated obstacle**, not as empty space and not as “wait forever.”
- **Partition:** one robot radio-silent for T seconds. Others replan around last known intent + conservative footprint; the isolated robot runs **ORCA on lidar** + deadlock watchdog. When radio returns, consensus on task ownership (CBBA) heals double-booking.
- **Clock skew:** space-time reservations use **sender timestamp + one-way estimate**, not a global sim god-clock on the robot (sim clock is allowed *inside Gazebo* only).
- **Discovery vs planning:** Zenoh/DDS discovery dying is not an excuse for a central planner. Static peer lists as fallback.
- **Bandwidth:** do not flood occupancy grids or cameras. Payload = id, pose, velocity, next K waypoints, reserved cells, priority, task id, battery, status, seq. K ≈ 5 s of path, not 400 cells.

### Conflict / deadlock (report 05 taxonomy, now requirements)

- **Type A — head-on 1-lane aisle:** ORCA alone **deadlocks** (paper + report 05). Need corridor **token** or reverse-to-passing-bay (degree ≥ 3).
- **Type B — intersection who-goes-first:** pipelined reservations, not mutex of the whole box (mutex **is** the baseline you must beat).
- **Type C — cyclic wait:** wait-for graph + **PIBT priority inheritance** (if A needs B’s cell, B inherits A’s urgency and is pushed).
- **Type D — priority inversion:** same inheritance. Lowest-ID-always-wins is a fake that dies at N=6.
- **Type E — goal occupation:** idle robots **leave the pick face** to a park cell; a robot at goal still **yields** if someone needs the cell.
- **Type F — planner timeout:** if discrete repair > budget, **execute ORCA/PIBT this tick**. Never block the motors on CBS.
- **Livelock:** oscillating yield. Watchdog: if no progress N ticks, reverse to last intersection, re-auction if cost exploded.
- **Three-robot cycle:** A waits B waits C waits A. This is why N≥3 is the gate, not the product spec. Demo N=5–8 as stretch.
- **Non-fleet obstacles:** human / forklift / fallen pallet. Local costmap + optional YOLO. Other AMRs are **teammates with intent**, not lidar blobs.

### Task allocation / re-routing

- **Re-route ≠ re-assign.** Same ticket, new path vs ticket changes owner. Oscillation if you mash them: **release only if** new path cost > ρ × old (ρ ≈ 1.5) **or** path infeasible.
- **Double booking:** two robots think they own pick 12. CBBA consensus (or lowest-bid + lowest-id + lease timeout).
- **Robot dies / battery floor:** remaining bundle returns to the market; others re-bid.
- **New job mid-run:** idle or lowest opportunity-cost robot takes it; moving robots do not dump current jobs unless the new job is strictly better **and** a replacement exists (CBBA bundle scores).
- **Blocked aisle that was the only path:** cost → ∞ → release → winner takes the long way. Baseline also gets the same map update (report 01 fairness).
- **Shared dock / pick face:** reservation of the last k cells, P2P, not a central station server (Pouya’s station reservation is the anti-pattern to upgrade).

### Simulation / scoring

- **Independent A\* of the scenario must contain ≥2 space-time conflicts.** If not, the 20% is hollow.
- **Collision definition frozen:** disk overlap **or** vertex/edge conflict on the grid **plus** Gazebo contact as a secondary log. Zero means zero. Near-misses logged separately.
- **Fair stop-and-wait:** FCFS mutex on labeled choke segments and intersections; same map, kinematics, tasks, blockage; still allowed to move in **disjoint** resources. Not “everyone frozen.” Not “wait at every waypoint.” If baseline deadlocks, give it the **same watchdog** so you compare policies.
- **Primary metric:** makespan of the job batch. Also report sum-of-costs. Do not substitute SOC for the 20% claim.
- **N ≥ 10 seeds**, listed. Mean Δ ≥ 0.20. Collisions_ours = 0 on all scored seeds.
- **God-mode localization** is allowed in sim **if** each robot only *publishes* its own pose and others never peek at `/gazebo/model_states`.

### Dashboard

- **Unplug test.** Command buttons off. Operator may **inject a blockage or a job** (WMS-like seed); that is not path planning.
- Battery may be `100% − k·distance`; say so. Battery **must** be able to trigger a yield (otherwise the field is decoration).

---

# B. Tech stack, components, architecture lock-in

## B.1 One-sentence system

**Each AMR is a Dockerized onboard stack: sensors → local map → A\*/D\* path → optional learned preference → P2P windowed PIBT + corridor tokens → ORCA velocity filter → Nav2/pure-pursuit tracker; tasks are CBBA over Zenoh; the world is Gazebo Harmonic; the dashboard only subscribes, including per-robot local-view cards.**

## B.2 Runtime topology (the demo machine)

```
┌──────────────────────────── judged laptop ─────────────────────────────┐
│  Host network namespace                                                │
│                                                                        │
│  [gz-sim]  Gazebo Harmonic + AWS small-warehouse SDF                   │
│            physics, lidar, optional RGB, RFComms optional              │
│                 │ sensor topics (namespaced, per robot)                │
│                 ▼                                                      │
│  docker compose network  (bridge + optional netem)                     │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐     ┌────────────┐     │
│  │ amr_01     │ │ amr_02     │ │ amr_03     │ ... │ amr_0N     │     │
│  │ Nav2 track │ │            │ │            │     │            │     │
│  │ coord.so   │ │ coord.so   │ │ coord.so   │     │ coord.so   │     │
│  │ zenoh peer │◄┼────────────┼─┤  Intent /  │     │ bids/token │     │
│  │ YOLO/ORT   │ │            │ │  BLOCKED   │     │            │     │
│  └─────┬──────┘ └─────┬──────┘ └─────┬──────┘     └─────┬──────┘     │
│        │ local_view   │              │                  │            │
│        └──────────────┴──────────────┴──────────────────┘            │
│                                   │ subscribe only                   │
│  [dashboard]  FastAPI + React/SVG  3D Foxglove optional              │
│               fleet map | battery | tasks | alerts | N local cards   │
│               NO planner  NO NavigateToPose as authority             │
└──────────────────────────────────────────────────────────────────────┘

Stretch: one amr_* image on a Pi 5 / Orin, same Zenoh router list.
Stretch: Isaac Sim as drop-in world if RTX 4080+ exists.
Eval: headless 2D twin of the same coord.so for 10-seed CSVs.
```

**Contracts:**

1. `coord` never imports `gz`, `pygame`, `rclpy` in its core. Adapters wrap it.
2. Planning uses **neighbor cache from messages**, never `world.get_model_state(others)`.
3. Dashboard process crash is a no-op for motion.
4. Compose file is the spec of decentralization.

## B.3 Layer cake (rates and owners)

| Layer | Rate | Algorithm | Why this, not the alternative |
|---|---|---|---|
| **Safety filter** | 20 Hz | **ORCA** (RVO2), NH-ORCA if diff-drive tracking error is ugly | Converts “don’t hit in the next τ” into a 2D LP. Pi-cheap. CBF-QP is a peer; start ORCA because the library is Apache and the paper is the field standard. **Not** CADRL as default (TF1 archaeology; open-space; no aisle theory). |
| **Tracker** | 20 Hz | **Nav2 MPPI or DWB** (Orin/laptop); **pure-pursuit / DWB** on Pi | Nav2 is the industrial tracker (Macenski IROS 2020). It is **not** the multi-agent brain. Other robots must **not** be “just costmap obstacles” as the only coordination. |
| **Discrete coordination** | 2–10 Hz | **Windowed PIBT** on a grid abstraction of the warehouse, clique = radio neighbors | PIBT is the only fast MAPF primitive that is **decentralized if conflicting agents communicate** (CS-PIBT §II-B3). Priority inheritance **is** the Type C/D fix. LaCAM3 is the **offline expert**, not the 10 Hz loop (central joint search). CBS/ECBS/PBS as **runtime** contradict edge + no-tower (RHCR paper itself uses them *inside a central windowed solver*). |
| **Choke protocol** | event | **Corridor / intersection token** (Ma 2017 token idea, scoped to a resource, not to all MAPD) | Type A is a mutex on a 1-lane resource. Tokens prevent ORCA freeze. Pipelining: token is the *lane segment*, not the whole warehouse. This is how you beat stop-and-wait: opposite of “hold the entire aisle until empty” when a passing bay exists. |
| **Global path** | on event / 1 Hz | **A\***; **D\* Lite** on blockage | RHCR’s lesson: don’t resolve the whole remaining life. A\* to goal, PIBT for the next `w` steps. D\* Lite when occupancy flips. |
| **Tasks** | event | **CBBA** (Choi, Brunet, How, T-RO 2009) over Zenoh | Hungarian is optimal **and centralized**. Open-RMF dispatcher is a WMS. CBBA is the actual decentralized allocator: bundle bids + consensus. Sequential single-item auction is the slim sibling if bundles are size 1. |
| **Perception** | 1–5 Hz | **YOLO11n** (Orin TRT / Pi TFLite) or **EfficientDet-lite0** on Pi camera | Writes lethal cells + `BLOCKED` gossip. Not MAPF. |
| **Optional ML preference** | 2–5 Hz | **Follower-lite ONNX** or a tiny imitator, **then CS-PIBT** | See §B.7. Timeout: if inference > 10 ms, skip, use greedy PIBT. |
| **Transport** | 10 Hz pose/intent | **`rmw_zenoh` or zenoh-bridge-ros2dds`** (free_fleet pattern) | DDS multicast on warehouse Wi-Fi is a known failure (report 05). Custom UDP reinvents Zenoh badly (report 04). A Zenoh **router is not a planner**. |
| **World** | physics | **Gazebo Harmonic + AWS small-warehouse** | 3D judged look, RFComms available, Apache. Webots is the laptop-kinder 3D backup. |
| **Observer** | 10 Hz | Custom web + optional Foxglove | Subscribe-only. Local-view cards. |

**Rejected as live brain (with reason):**

- **RHCR+PBS onboard for all agents:** the AAAI 2021 algorithm *replans all agents every `h`* with a Windowed MAPF solver. That **is** a central tower. Keep as teacher.
- **Open-RMF traffic schedule:** production hybrid (report 02). Fails the PS wording if it is the deconfliction.
- **End-to-end MARL / QMIX on RWARE:** no public warehouse checkpoints (report 06); tens of millions of steps; no collision certificate.
- **MAPF-GPT-85M / ViNT / diffusion policies on Pi:** wrong compute class.
- **One-shot CBS:** Type F + dynamic goals (RHCR §2: resolving the whole horizon is often wasted work).

## B.4 Discrete vs continuous (the SMART split)

RHCR §3 assumes perfect discrete execution, then points at Hönig et al. to turn MAPF plans into kinodynamic commands. We lock that split:

1. Project Gazebo poses onto a **nav graph** (aisle centerlines + intersection nodes). MovingAI `warehouse-*` geometry is the **eval map**; the Gazebo world is an extrusion of a similar aisle graph, not a random mesh.
2. PIBT outputs the **next cell / next edge**.
3. Nav2 tracks the edge with ORCA filtering `cmd_vel` against **neighbor velocities from Intent**, not against a shared simulator handle.
4. If tracking error > ε, the robot **re-snaps** and flags `BLOCKED` if it cannot.

This is how you get both a photogenic 3D demo and a zero-collision **score** that is not “looks like they missed.”

## B.5 Message protocol (Intent)

Broadcast 10 Hz, best-effort for pose, reliable for bids/tokens:

`robot_id, t_send, pose, twist, path_prefix[K], reserved[(cell,t)], priority, task_id, task_state, battery, status, seq`

`status ∈ {IDLE, TO_PICK, TO_DROP, WAITING, BLOCKED, DEADLOCK, YIELD}`

On `BLOCKED(cells, until)`: local D\* / A\*; if cost ratio > ρ, CBBA release.

## B.6 Baseline (for the 20%)

Identical robots, map, tasks, blockage schedule, comms delay model.

1. Independent A\* ignoring others.
2. Stop at boundary of every **pre-labeled** choke (degree ≠ 2 corridors, intersection boxes).
3. Enter iff resource empty; FCFS by arrival; ID tie-break.
4. Same blockage map updates; **same auction if we want the stricter claim** (20% from motion only). Default PS claim: our stack vs this mutex. Report an ablation that shares auctions.

Win by **pipelining** (A entering as B leaving) and **detours** (one robot takes the long aisle while the other holds the short one), which stop-and-wait forbids.

## B.7 Learned forks (exact training, pretrained, when to skip)

Every row: **core path stays if you never train**. The fork is additive. CS-PIBT / ORCA remain on.

### Fork 1 — Blocked-aisle / human perception (pretrained, optional fine-tune)

- **Core:** lidar occupancy change detector (classical). Sufficient.
- **Pretrained:** **YOLO11n** (HF Ultralytics, AGPL — keep the repo public) or **EfficientDet-lite0 INT8 TFLite** (Apache, Pi-native). PeopleNet on Jetson Nano 2019 if that is the BOM (do not republish NGC weights).
- **If you train:** 50–200 labeled frames from *your* Gazebo cameras (`person`, `pallet`, `box`). Ultralytics fine-tune, export TFLite/TensorRT **on the target**. Loss: detection. **Never** backprop into `cmd_vel`.
- **Plug-in:** box → lethal costmap cells → `BLOCKED` gossip.
- **Edge:** Pi 5 ~2 FPS INT8 is enough (blockage is 1 Hz). Orin TRT is comfortable. Nano 2019: dusty-nv SSD, not current pip YOLO11.

### Fork 2 — Travel-time / congestion cost (you train; no public warehouse weights)

- **Core:** bid = `path_length / v_max`.
- **Why learn:** empty-map distance lies in queues (report 05; Follower’s own static+dynamic cell costs are the classical cousin).
- **Data:** run **classical** fleet 200–1000 episodes, random tasks + blockages. For each robot, log `(aisle_id, local_density, battery, measured_time)`. Features **must** be reconstructable from Intent + own map (no god-view).
- **Model:** ridge / tiny MLP (2×64). Loss: L1 on time. Desktop CPU is enough.
- **Plug-in:** replace the scalar inside CBBA bids. Unplug → old distance bids. Collisions must stay zero.
- **Do not** start here until classical already beats stop-and-wait (otherwise you will attribute pipelining to the net).

### Fork 3 — Local follow / preference (pretrained Follower-lite, optional own imitator)

- **Core:** PIBT greedy (heuristic = remaining distance). This **is** the CS-PIBT paper’s mandatory baseline.
- **Pretrained:** **Follower-lite ONNX (19 KB, MIT)** as a **preference over next cells**, then **CS-PIBT repairs**. Wrap OccupancyGrid → FOV patch → discrete action → shield. Follower paper trains PPO with reward **+0.01 for advancing the waypoint**, 20M steps / 30 min for Lite, 1B steps / 18 h for full 5M-param Follower. You do **not** need to repeat 1B.
- **If you train your own (recommended quality ML story, still small):**  
  1. Offline, on MovingAI warehouse maps **and** your Gazebo-projected grid, run **LaCAM3 or EECBS** (centralized expert) to dump `(local FOV, neighbor intents, next action)`. CS-PIBT paper: even **one** scene of labels can suffice **if the shield is on**; they also show tighter EECBS suboptimality → better path cost.  
  2. Architecture: tiny CNN or 2-layer MLP, **not** a transformer. Cross-entropy vs expert action. **Do not apply CS-PIBT during training** (they found it too slow).  
  3. Deploy: argmax preferences → **CS-PIBT** (priority inheritance + backtrack on the proposed ranking).  
  4. Hold-out seeds. Ablation: unplug net. If collisions appear, the shield was bypassed — a bug.  
  5. **Do not claim the 20% from this net** unless classical-only is already logged.
- **MAPF-GPT-2M:** laptop comparison vs your PIBT, same maps. Not onboard.
- **CADRL:** skip unless you enjoy TF1. ORCA covers the geometric dodge.

### Fork 4 — Learned CBBA bids (only after Fork 2 works)

- Same regressor as Fork 2, or a second head. Consensus rules **stay**. 2026 “learned CBBA” papers have **no public weights**.

### Fork 5 — Explicitly out of the live loop

- QMIX/MAPPO on RWARE as the demo coordinator.  
- LLM dispatch at 20 Hz.  
- Diffusion trajectory generators.  
- Training Follower-full 5M as the only collision layer (PRIMAL2-style freeze on conflict is weaker than CS-PIBT; Follower paper still used a simple one-succeeds-others-wait rule).

**Edge inference rule:** ONNX Runtime (+ TensorRT on Orin) **inside the robot container**. Guest call, 10 ms timeout, classical fallback. Safety loop stays C++/numba ORCA+PIBT.

## B.8 Why this is better than the “student clone” stacks

Adilnasceng: CBS+Hungarian+Flask — **central**, no-license. Pouya: pretty Jazzy fleet — **no MAPF, station reservation**. Open-RMF: best dashboard, **central traffic**. We take their **ops patterns** (namespaces, warehouse SDF, Zenoh bridge, web layout) and put **PIBT+token+CBBA+ORCA** where they put a tower. That is the contribution, not another CBS server.

---

# C. GitHub: extract patterns, do not copy the product

Use mode: **pattern / dependency / eval harness**. Not “fork and ship.” No-license student repos are **not** public forks. Prefer MIT/Apache implementations of the *algorithm* even if that means writing glue.

| Need | Repo | What to extract | What to reject / replace |
|---|---|---|---|
| 3D warehouse world | [aws-robomaker-small-warehouse-world](https://github.com/aws-robotics/aws-robomaker-small-warehouse-world) | SDF shelves, pallets, choke geometry | RoboMaker cloud (dead 2025-09-10) |
| Multi-robot bringup / namespaces | [Pouya-Mansournia/warehouse-amr-ros2](https://github.com/Pouya-Mansournia/warehouse-amr-ros2) **learn-from** (no license) or [shrikrishnarb/amr-ros](https://github.com/shrikrishnarb/amr-ros) (MIT, Docker) or [arshadlab/tb3_multi_robot](https://github.com/arshadlab/tb3_multi_robot) | Launch, TF, `ros2_control`, one-command up | Their coordination. Reimplement. |
| Eval harness | [boschresearch/remroc](https://github.com/boschresearch/remroc) | How they stub a coordinator node on Nav2 | Not the algorithm |
| P2P transport | [ros2/rmw_zenoh](https://github.com/ros2/rmw_zenoh), [open-rmf/free_fleet](https://github.com/open-rmf/free_fleet) | RMW + **selective topic filter**, aarch64 story | Putting planning behind one fleet adapter |
| Dashboard layout ideas | [open-rmf/rmf-web](https://github.com/open-rmf/rmf-web) **pattern**; write our own thin React/FastAPI | Map + robot table + tasks | Dispatch buttons; do not vendor-lock on RMF API |
| ORCA | [snape/RVO2](https://github.com/snape/RVO2) **dependency** | Half-plane LP | Using it as the only aisle protocol |
| PIBT / LaCAM | [Kei18/pibt2](https://github.com/Kei18/pibt2), [Kei18/lacam3](https://github.com/Kei18/lacam3) **algorithm + pybind** | Inheritance, backtrack, fast first solution | Running LaCAM as a central service every tick |
| Intersection / circular wait | [MuskaanMaheshwari/ros2-multi-amr-factory](https://github.com/MuskaanMaheshwari/ros2-multi-amr-factory) **MIT, learn-from** | Zone polygons, wait-for cycle detect | Battery greedy as the only allocator |
| Corridor token idea | [aaronreycast/Multirobot-Warehouse-Simulation](https://github.com/aaronreycast/Multirobot-Warehouse-Simulation) MATLAB **protocol**, or Ma token-passing papers | FIFO on a single-file resource | MATLAB as deliverable; token-for-all-MAPD |
| CBBA | [keep9oing/consensus-based-bundle-algorithm](https://github.com/keep9oing/consensus-based-bundle-algorithm) **reimplement cleanly** (stale but clear) | Bundle + consensus phases | Star-network assumption if our radio is range-limited — run CBBA on the **connected component** |
| RHCR oracle | [Jiaoyang-Li/RHCR](https://github.com/Jiaoyang-Li/RHCR) **research license — isolate** | Generate expert traces / quality upper bound | Live ROS node for all robots |
| Maps | MovingAI warehouse-*, LoRR sortation for stress | Standard geometry, cite Stern et al. 2019 | Custom empty square |
| Follower-lite weights | [Cognitive-AI-Systems/learn-to-follow](https://github.com/Cognitive-AI-Systems/learn-to-follow) | `follower-lite.onnx` | Using full 5M Follower as the only shield |
| Grid unit tests | [AIRI-Institute/pogema](https://github.com/AIRI-Institute/pogema) / [semitable/robotic-warehouse](https://github.com/semitable/robotic-warehouse) | Fast lifelong episodes | Toy look as the judged GUI |
| CS-PIBT pattern | [Rishi-V/ML-MAPF-with-Search](https://github.com/Rishi-V/ML-MAPF-with-Search) | Shield around logits | Drive file as a ROS dependency |

**Do not use as the product:** Adilnasceng CBS server; empty README stubs; ROS1 ORCA; GPL `karma_dmapf` inside a permissive stack; Isaac as required runtime; copying no-license code into a public repo.

**Glue you write (this is the repo):** nav-graph from the warehouse; Intent.msg; docker-compose; CS-PIBT wrapper; CBBA-over-Zenoh; metrics.py; netem profiles; local-view publishers.

---

# D. Tech features (what a user of the system actually gets)

These are operator / warehouse features, not algorithm names.

1. **Live 3D fleet picture** of every AMR in the aisle layout, with who is carrying which pick/drop.
2. **Per-robot local view** (what that robot’s lidar/camera and reserved cells look like), so a supervisor can see *why* a robot yielded without SSHing in.
3. **Battery-aware work** — low battery shows on the wall and actually causes the robot to **hand off** remaining picks instead of dying in an aisle.
4. **One-click (or scripted) aisle blockage** — the fleet **goes around or hands off** the job; nobody re-draws paths by hand.
5. **New orders while the shift is running** — robots **bid** and take work; two robots do not double-book a pick face.
6. **Intersection that keeps moving** — robots **filter through** a choke instead of forming a polite parking lot (the thing stop-and-wait does).
7. **Head-on aisle that unjams** — one robot **backs to a passing bay** or holds a **lane token** instead of two bumpers kissing until the shift ends.
8. **Radio trouble mode** — delay/loss you can toggle; robots **slow and stay safe** rather than freeze the building or drive through ghosts.
9. **Kill the control-room UI** — picking **continues**. The screen was never the brain.
10. **Safety log** — automatic collision and near-miss count, not “it looked fine.”
11. **Shift report** — time to finish the batch vs the conservative stop-and-wait policy, on the same orders, so a manager can see the **20%** as a number, not a vibe.
12. **Drop-in extra robot** — same image, new id, joins the mesh; no rewrite of a central schedule.
13. **Edge-shaped computers** — the same brain that ran in Docker is what you flash on a Pi/Orin; perception can use a tiny detector already on the board.
14. **Human in the aisle (optional)** — a person/forklift is seen, the aisle is marked dirty, jobs reflow.
15. **Operator injects a job or a pause** without becoming the path planner — WMS-like seeding, onboard negotiation after that.

---

## Judge script (the 90-second story)

1. Six panels: 3D warehouse + five (or three) **local brains**.  
2. Three robots enter a 1-lane choke from two directions — **token + PIBT**, no freeze, no hit.  
3. Pallet appears; YOLO/lidar paints the aisle; **re-route / re-auction** on the dashboard tickets.  
4. `docker stop dashboard` — robots keep talking (packet pane still on a sidecar tap).  
5. Slide: **0 collisions**, makespan **−≥20%** vs FCFS mutex, N=10 seeds.

If any of those five beats fail, the architecture was not executed. The papers and reports already say what to build. This file says **which** of those things is the system.
