# Simulation Environments & Edge Viability

**Problem statement (this report):** a **decentralized multi-AMR warehouse** demo with at least 3 robots, aisle / choke-point maps, optional P2P comms, a planner that can also run on Raspberry Pi / Jetson-class boards, and a **monitoring-only** fleet dashboard.

**Date:** 2026-09-04. Sources are current as of Isaac Sim 6.0 / Isaac ROS 4.6, ROS 2 Jazzy, Gazebo Harmonic, and AWS RoboMaker’s September 2025 shutdown.

**Headline recommendation for a first-time team:** do **not** start in Isaac Sim. Run a **2D occupancy-grid warehouse on the laptop** (pygame or Nav2 dummy world), keep the **planner as a pure Python/C++ library** with the same API on Pi, and optionally dress it up later in **Gazebo Harmonic + ROS 2**. That is the only architecture that survives a 1–2 week hackathon *and* still looks like robotics.

---

## 1. Decision criteria

Every environment below was scored against the *same* ten axes. Scores in §7 are 1–5 (higher is better for *this* PS). Typical laptop FPS numbers are order-of-magnitude, measured or reported on a mid-range 2023–2025 laptop (Intel i7 / Ryzen 7, 16–32 GB RAM, optional RTX 3060/4060). They are not lab-grade benchmarks.

| Criterion | What we actually scored | Why it matters here |
|---|---|---|
| **Fidelity** | Physics, sensors, kinematics vs grid/toy | Needed for a convincing warehouse demo, not for the planner itself |
| **Multi-robot quality** | Native N≥3, namespaces, TF isolation, spawn APIs | PS requires ≥3 AMRs; many “ROS sims” are single-robot with a comment |
| **Warehouse assets** | Aisles, shelves, docks, choke points out of the box | Time-to-demo killer if you have to model a warehouse |
| **Comms simulation** | Range, drop, RF path-loss, or at least easy UDP/MQTT hooks | Decentralized P2P is a *feature*; most sims ignore the radio |
| **Laptop performance** | Real-time factor with 3–8 AMRs, cameras optional | Team laptops, often Windows + WSL2 |
| **ROS 2 support** | Humble / Jazzy first-class, not a stale bridge | Engineering-fidelity track and Nav2 reuse |
| **License** | Apache/BSD/MIT vs Edu-only vs GPU-locked proprietary | Hackathon + possible NeurIPS code release |
| **Learning curve** | Hours to first 3 robots moving | 1–2 week constraint |
| **Dashboard-ability** | Topics / websocket / JSON poses without becoming the planner | Monitoring-only fleet view |
| **Edge export** | Can the *planner* (not the sim) run identically on Pi 4/5 or Jetson | “Sim on laptop, planner identical on Pi” is non-negotiable |

**Scoring rule of thumb.** If an environment cannot (a) host 3 robots on a warehouse-like map in a week, (b) leave the planner as a portable library, and (c) stay license-clean, it is a research sidecar, not the demo stack.

**Architecture constraint we optimized for:**

```
┌──────────────── laptop ─────────────────┐     ┌────── edge (Pi / Orin) ──────┐
│  World (2D grid or Gazebo)              │     │  same planner.py / .so       │
│  sensors → OccupancyGrid + Pose + peers │────▶│  A* / D* Lite + ORCA         │
│  dashboard ← poses / battery / task     │     │  UDP / Zenoh / MQTT P2P      │
└─────────────────────────────────────────┘     └──────────────────────────────┘
        planner API is identical on both sides
```

The simulator is a *world*. The planner is a *library*. Mixing those two is how teams miss the edge requirement.

---

## 2. Catalog of existing sims

At least twelve environments, plus warehouse-specific and “mention-only” items. Each entry: name, license, language, 2D/3D, ROS, multi-robot, warehouse relevance, wireless/P2P, GPU, typical laptop FPS, links.

### 2.1 Gazebo / Gazebo Harmonic + ROS 2

| | |
|---|---|
| **License** | Apache 2.0 |
| **Language** | C++ core, SDF/URDF, Python launch |
| **2D vs 3D** | 3D (ODE / DART / Bullet physics; Ogre2 render) |
| **ROS** | First-class ROS 2 via `ros_gz` / `ros_gz_bridge`. Pairing: Humble↔Garden/Harmonic (distro-dependent), Jazzy↔Harmonic. Classic Gazebo 11 is EOL (Jan 2025) — do not start new work there. |
| **Multi-robot** | Good, but *you* must namespace TF, topics, and plugins. Documented pattern: world SDF owns physics/render/sensors systems; each robot URDF owns wheels. Community examples spawn 3–4 TurtleBot3/AMRs with per-robot Nav2. 15–20 robots is architecturally possible, rarely laptop-real-time with lidars. |
| **Warehouse** | Strong. TurtleBot 4 simulator ships a `warehouse` world. AWS RoboMaker **small warehouse** SDF (shelves, pallets, clutter) is still on GitHub even though RoboMaker the *service* is dead. Open-RMF has building/robot Gazebo plugins. |
| **Wireless / P2P** | **Yes, uniquely among 3D ROS sims.** Gazebo Harmonic has `RFComms` (log-distance path loss, max range, tx power, noise floor; ported from DARPA SubT) plus a generic comms system. You can also ignore that and just run UDP/MQTT between namespaced nodes. |
| **GPU** | Optional. GPU lidar / cameras want an NVIDIA GPU; physics-only + 2D lidar works on CPU. Dual Intel/NVIDIA laptops often silently run on Intel and look broken. |
| **Laptop FPS** | 3 differential AMRs + 2D lidars, warehouse, GUI: often **15–40 FPS** / RTF 0.5–1.0 on a decent laptop. Headless + no cameras: closer to real-time. Cameras + 8 robots: RTF collapses. WSL2 is slower; turn cameras off. |
| **Links** | [Gazebo Harmonic docs](https://gazebosim.org/docs/harmonic), [feature comparison (RFComms)](https://gazebosim.org/docs/harmonic/comparison/), [RFComms API](https://gazebosim.org/api/sim/8/classgz_1_1sim_1_1systems_1_1RFComms.html), [ros_gz](https://github.com/gazebosim/ros_gz), [TB3 multi-robot Jazzy](https://github.com/arshadlab/tb3_multi_robot), [warehouse AMR Jazzy](https://github.com/Pouya-Mansournia/warehouse-amr-ros2), [TurtleBot 4 sim (warehouse world)](https://github.com/turtlebot/turtlebot4_simulator), [Open-RMF sim plugins](https://github.com/open-rmf/rmf_simulation) |

**Verdict for this PS:** best *engineering* 3D choice. Not the fastest path to a NeurIPS-style algorithm paper.

### 2.2 NVIDIA Isaac Sim

| | |
|---|---|
| **License** | GitHub source Apache 2.0; **runtime needs Omniverse Kit + assets** under NVIDIA’s Additional Software and Materials License. Free for internal R&D. Redistributing Isaac+Kit as a product/service needs NVIDIA AI Enterprise. |
| **Language** | Python 3.11/3.12 extensions, USD, C++ Kit |
| **2D vs 3D** | High-fidelity 3D (PhysX, RTX ray-traced sensors) |
| **ROS** | ROS 2 Bridge (Humble/Jazzy depending on Sim version). Isaac Sim 5.1 was Python 3.11; **6.0 (current docs) is Python 3.12 + ROS 2 Bridge**. Isaac ROS (perception stack) is a *separate* product — see §3. |
| **Multi-robot** | Excellent in theory (Nova Carter, O3dyn, forklifts). NVIDIA’s own ROS2-bridge benchmark for *one* Nova Carter is already ~13–18 FPS on high-end GPUs. Multi-Carter with full sensors is a **multi-GPU server** story. |
| **Warehouse** | Best-in-class assets: `warehouse.usd`, `warehouse_multiple_shelves.usd`, `full_warehouse.usd`, modular warehouse props, Warehouse Creator. This is the “looks like Amazon” sim. |
| **Wireless / P2P** | No first-class RF model comparable to Gazebo RFComms. You simulate comms in ROS/Zenoh outside the renderer. |
| **GPU** | **Hard requirement.** Isaac Sim 6.0 min: RTX 4080-class, **16 GB VRAM**, 32 GB RAM. GPUs without RT cores (A100/H100) unsupported. aarch64 Isaac Sim is **DGX Spark only**, not Jetson. |
| **Laptop FPS** | On a typical student laptop (RTX 3060 6 GB): often **unusable** for warehouse + 3 robots + lidars. On RTX 4080: warehouse scene 50–150+ FPS *without* ROS sensors; ROS2 render+publish of one Nova Carter ~15 FPS. |
| **Links** | [Requirements 6.0](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/requirements.html), [Benchmarks](https://docs.isaacsim.omniverse.nvidia.com/latest/reference_material/benchmarks.html), [Warehouse assets](https://docs.isaacsim.omniverse.nvidia.com/4.2.0/features/environment_setup/assets/usd_assets_environments.html), [License FAQ](https://docs.isaacsim.omniverse.nvidia.com/6.0.0/common/license-faq.html), [Isaac ROS getting started](https://nvidia-isaac-ros.github.io/getting_started/index.html) |

**Verdict:** gorgeous digital twin, wrong default for a first-time hackathon team without an RTX 4080+. Keep as a stretch visualizer, not the development loop.

### 2.3 Webots

| | |
|---|---|
| **License** | Apache 2.0 (Cyberbotics; `webots_ros2` also Apache 2.0) |
| **Language** | C/C++/Python/Java/MATLAB controllers; PROTO worlds |
| **2D vs 3D** | 3D, lighter than Gazebo/Isaac |
| **ROS** | Official `webots_ros2` (latest tag **2025.0.x**). Extern controllers + `WEBOTS_CONTROLLER_URL` per robot. |
| **Multi-robot** | Native and cleaner than Gazebo (each robot is a node with an extern controller). Examples include multi-arm; ground AMR fleets are DIY but straightforward. |
| **Warehouse** | No famous public warehouse world on the scale of AWS/Isaac. You build aisles from boxes/PROTOs. Fine for a stylized warehouse. |
| **Wireless / P2P** | Emitter/Receiver devices exist (IR/radio-like). Not a full RF path-loss stack. Easy to also use ROS topics / UDP. |
| **GPU** | OpenGL; integrated GPU often enough for 3 robots without cameras. |
| **Laptop FPS** | Typically **real-time** for 3–6 simple AMRs. Often the least painful 3D ROS 2 sim on a laptop. |
| **Links** | [Webots](https://cyberbotics.com/), [webots_ros2](https://github.com/cyberbotics/webots_ros2), [multi-robot launch example](https://github.com/cyberbotics/webots_ros2/blob/master/webots_ros2_universal_robot/launch/multirobot_launch.py) |

**Verdict:** best 3D *laptop* alternative to Gazebo if the team hates SDF/plugin debugging. Weaker warehouse assets.

### 2.4 CoppeliaSim (ex V-REP)

| | |
|---|---|
| **License** | **Edu free** (students/teachers; org email). Pro is commercial. Hobbyists can request a key. This is a friction point for a public NeurIPS repo. |
| **Language** | Lua embedded; Python/C++/Java remote API; ROS 2 plugin `libsimROS2` |
| **2D vs 3D** | 3D, multiple physics engines selectable |
| **ROS** | ROS 2 plugin exists; historically more brittle than `ros_gz`. ZeroMQ remote API is often easier than ROS. |
| **Multi-robot** | Historically excellent (the old selling point). Scene files with many robots are common. |
| **Warehouse** | You build it. No canonical open warehouse pack. |
| **Wireless / P2P** | Script your own; no RFComms equivalent. |
| **GPU** | Not RTX-locked; integrated GPU OK. |
| **Laptop FPS** | 3–8 AMRs often **real-time** in Edu. |
| **Links** | [Coppelia Robotics](https://www.coppeliarobotics.com/), [ROS 2 tutorial](https://manual.coppeliarobotics.com/en/ros2Tutorial.htm), [Edu register](https://coppeliarobotics.com/eduRegister) |

**Verdict:** capable, license-awkward for a hackathon that wants to publish code. Skip unless someone on the team already lives in Coppelia.

### 2.5 Unity ML-Agents / Unity Robotics Hub

| | |
|---|---|
| **License** | Unity Editor (free Personal / Pro); ML-Agents Apache 2.0; Robotics Hub components various Unity packages |
| **Language** | C# in-engine; Python trainers; ROS TCP Endpoint (C#/ROS) |
| **2D vs 3D** | 3D, game-engine pretty |
| **ROS** | ROS-TCP-Connector / Endpoint. ROS 2 *was* documented. **Unity Robotics Hub is effectively unmaintained** as of 2025–2026 (last meaningful robotics commits ~2021–2022; open “is this deprecated?” issues with no staff reply). ML-Agents itself is still alive (4.x in 2025–2026) but that is RL training, not AMR Nav2. |
| **Multi-robot** | Easy to spawn N prefabs. Coordination is your job. |
| **Warehouse** | Unity Asset Store has warehouses; not ROS-ready. Old “Pick and Place” tutorial is a manipulator, not a fleet. |
| **Wireless / P2P** | Game-engine networking or custom. Not scientific RF. |
| **GPU** | Want a discrete GPU for the Editor; builds can be lighter. |
| **Laptop FPS** | Editor: 30–60 with simple AMRs. |
| **Links** | [Unity Robotics Hub](https://github.com/Unity-Technologies/Unity-Robotics-Hub) (stale), [ML-Agents](https://github.com/Unity-Technologies/ml-agents) (active), [ROS-TCP-Connector](https://github.com/Unity-Technologies/ROS-TCP-Connector) |

**Verdict:** do not bet a 2-week robotics demo on an unmaintained ROS bridge. ML-Agents is fine for a *pure RL* NeurIPS sidecar, not for Nav2/edge export.

### 2.6 AWS RoboMaker — status as of 2026

**Dead as a service.** AWS discontinued RoboMaker on **10 September 2025**. After that date the console and APIs are gone. Official migration path is **AWS Batch** multi-container jobs, not a robotics product.

**What you can still steal:**

- [aws-robomaker-small-warehouse-world](https://github.com/aws-robotics/aws-robomaker-small-warehouse-world) — Gazebo SDF warehouse (shelves, buckets, box clusters, pallet jack). This is the default “looks like a warehouse” world for ROS people. MIT-style AWS sample; still the right asset even though the cloud service is gone.
- Other AWS sample worlds (bookstore, small house) — less relevant.

**Do not** design the project around RoboMaker cloud sim, Gazebo in the cloud billing, or the old RoboMaker ROS bundle. Treat it as a **world-file graveyard**, which is still valuable.

References: [AWS full-shutdown list](https://docs.aws.amazon.com/general/latest/gr/full_shutdown_services.html), [Robot Report shutdown article](https://www.therobotreport.com/aws-robomaker-shuts-down-after-failing-to-gain-traction/).

### 2.7 PyBullet

| | |
|---|---|
| **License** | zlib (Bullet / PyBullet) |
| **Language** | Python (C++ Bullet under the hood) |
| **2D vs 3D** | 3D physics, weak graphics |
| **ROS** | No first-class ROS 2 distro package. Community wrappers exist (publish `/odom`, `/scan`, subscribe `/cmd_vel`). Fine for a custom bridge. |
| **Multi-robot** | Easy `loadURDF` in a loop. Not a fleet framework. |
| **Warehouse** | No stock warehouse. Load boxes as aisles. |
| **Wireless / P2P** | None; you own sockets. |
| **GPU** | CPU physics; EGL rendering optional. |
| **Laptop FPS** | **Hundreds to thousands** of steps/sec headless for simple AMRs; GUI ~60. |
| **Links** | [pybullet.org](https://pybullet.org/), [bullet3](https://github.com/bulletphysics/bullet3), example multi-robot ROS 2: [saiga006/Multi-Robot-Sim-Formation-Control](https://github.com/saiga006/Multi-Robot-Sim-Formation-Control) |

**Verdict:** good *physics unit test* for a custom planner, bad “warehouse look.” Use if the team is Python-only and refuses ROS for week 1.

### 2.8 MuJoCo

| | |
|---|---|
| **License** | Apache 2.0 (DeepMind / Google, open-sourced 2022) |
| **Language** | C, Python (`pip install mujoco`), MJX/JAX for batched RL |
| **2D vs 3D** | 3D contact-rich (arms, humanoids, locomotion). Wheeled AMRs are possible but not the sweet spot. |
| **ROS** | [`mujoco_ros2_control`](https://github.com/ros-controls/mujoco_ros2_control) exists (Humble/Jazzy/Kilted) — ros2_control SystemInterface, not a full Nav2 warehouse stack. |
| **Multi-robot** | Native MJCF can instance many bodies; RL people batch *environments*, not warehouse fleets. |
| **Warehouse** | Poor. No aisle library. |
| **Wireless / P2P** | None. |
| **GPU** | CPU fine; MJX wants GPU for huge RL batches. |
| **Laptop FPS** | Very fast for contact RL; irrelevant for 2D MAPF. |
| **Links** | [google-deepmind/mujoco](https://github.com/google-deepmind/mujoco), [mujoco_ros2_control](https://github.com/ros-controls/mujoco_ros2_control) |

**Verdict:** wrong physics problem (manipulation/locomotion RL), not warehouse AMR coordination. Skip for this PS unless you add a manipulator on the AMR later.

### 2.9 Stage / Flatland (2D ROS simulators)

**Stage** (2.5D, the ancient Player/Stage lineage):

| | |
|---|---|
| **License** | GPL (Stage); `stage_ros2` often GPL-3.0 |
| **Language** | C++; world files |
| **2D vs 3D** | 2.5D (flat robots, 2D lidar) |
| **ROS** | ROS 1 `stage_ros` was standard. ROS 2: community [`tuw-robotics/stage_ros2`](https://github.com/tuw-robotics/stage_ros2) (Jazzy branch, multi-robot TF). Not an official Open Robotics product. |
| **Multi-robot** | This is what Stage *is for*. Dozens of robots at real-time. |
| **Warehouse** | Bitmap occupancy; you draw aisles. |
| **Wireless / P2P** | None built-in. |
| **GPU** | No. |
| **Laptop FPS** | **Real-time at 20–50 robots** easily. |
| **Links** | [rtv/Stage](https://github.com/rtv/Stage), [tuw-robotics/stage_ros2](https://github.com/tuw-robotics/stage_ros2) |

**Flatland** (Avidbots, Box2D, YAML worlds) — **not** the NeurIPS railway Flatland:

| | |
|---|---|
| **License** | BSD-3-Clause |
| **Language** | C++; YAML models; plugins |
| **2D vs 3D** | 2D / 2.5D layers |
| **ROS** | Original is ROS 1. ROS 2: small fork [JoaoCostaIFG/flatland](https://github.com/JoaoCostaIFG/flatland) (Humble). Arena-Rosnav still lists Flatland as one of three backends. |
| **Multi-robot** | Good; designed as a Gazebo alternative for ground robots. |
| **Warehouse** | Occupancy layers from map_server. You supply the PGM. |
| **GPU** | No. |
| **Laptop FPS** | Real-time, time-accelerable (useful for RL). |
| **Links** | [avidbots/flatland](https://github.com/avidbots/flatland), [docs](https://flatland-simulator.readthedocs.io/) |

**Verdict:** Stage/Flatland match the *computational* needs of this PS (2D, many robots, laptop). ROS 2 support is community-grade. A custom pygame grid is *faster to write* than debugging a 2017 simulator’s ROS 2 fork — unless you already know Stage.

### 2.10 Pedsim / social-force crowd

| | |
|---|---|
| **License** | libpedsim LGPL; ROS wrappers BSD (`srl-freiburg/pedsim_ros`) |
| **Language** | C++; XML scenes |
| **2D vs 3D** | 2D crowd; optional Gazebo actors |
| **ROS** | Original ROS 1 (Melodic). ROS 2 ports: [lehoangan2906/pedsim_ros2](https://github.com/lehoangan2906/pedsim_ros2) (Humble), [stephenadhi/pedsim_ros](https://github.com/stephenadhi/pedsim_ros). **Better ROS 2 bet in 2026:** [HuNavSim](https://github.com/robotics-upo/hunav_sim) (Humble, Gazebo Classic / Fortress / Webots wrappers, Social Force Model via [lightsfm](https://github.com/robotics-upo/lightsfm)). Arena-Rosnav uses `hunav` as the human simulator. |
| **Multi-robot** | Pedsim is *humans*; robots are a separate stack. Relevant if the warehouse has pickers walking aisles. |
| **Warehouse** | XML walls + waypoints. Can look like a warehouse floor with pedestrians. |
| **Wireless / P2P** | N/A (crowd, not radios). |
| **GPU** | No. |
| **Laptop FPS** | Hundreds of pedestrians real-time in 2D. |
| **Links** | [srl-freiburg/pedsim_ros](https://github.com/srl-freiburg/pedsim_ros), [HuNavSim](https://github.com/robotics-upo/hunav_sim), Helbing SFM paper: <http://arxiv.org/pdf/cond-mat/9805244.pdf> |

**Verdict:** **optional add-on**, not the AMR sim. Use if the PS needs “blocked aisle because a human is standing there.” Do not make Pedsim the core.

### 2.11 Custom pygame / matplotlib 2D grid warehouse

| | |
|---|---|
| **License** | Whatever you choose (MIT recommended) |
| **Language** | Python 3 |
| **2D vs 3D** | 2D top-down (grid or continuous) |
| **ROS** | Optional. You can publish `nav_msgs/OccupancyGrid` + `PoseStamped` if you want Foxglove later. You can also skip ROS entirely for week 1. |
| **Multi-robot** | Trivial: a list of agents. 3 to 50 robots at 30–60 FPS. |
| **Warehouse** | Load MovingAI `.map` files (`@` = shelf, `.` = aisle) or draw aisles as rectangles. Pickup stations = designated cells. |
| **Wireless / P2P** | **Best place to simulate it honestly:** range circles, packet drop probability, latency jitter, bandwidth caps — 50 lines of Python. Gazebo RFComms is overkill if the algorithm only needs “I can talk to neighbors within 8 m.” |
| **GPU** | No. |
| **Laptop FPS** | **60 FPS** with matplotlib blit or pygame for 10 robots; thousands of steps/sec headless. |
| **Edge export** | **Perfect.** `planner.py` imports the same `Grid`, `astar()`, `orca_step()`. Sim is just `env.step(actions)`. |
| **Links** | MovingAI maps (§5), [PegasusGTV/mapf](https://github.com/PegasusGTV/mapf) (minimal MovingAI env + GIF viz), [openplan-labs/pymapf](https://github.com/openplan-labs/pymapf) |

**Verdict:** **fastest path to a working decentralized demo.** Looks less “ROS industrial” until you wrap poses in a websocket dashboard. That is a one-day job.

### 2.12 Warehouse-specific: RAWSim-O, Amazon-style grids, RWARE / VMAS / Jumanji, railway Flatland, MAPF benchmarks

#### RAWSim-O

| | |
|---|---|
| **License** | GPL-3.0 |
| **Language** | C# (.NET), tiny Python |
| **2D vs 3D** | 2D discrete-event RMFS (Kiva / Amazon Robotics style: robots *carry shelves* to pick stations) |
| **ROS** | No. |
| **Multi-robot** | This is the point — hundreds of AGVs, order streams, pod storage. |
| **Warehouse** | Highest *logistics* fidelity of anything here (SKU assignment, replenishment, station choice). Lowest *robotics* fidelity (no lidar, no ROS). |
| **Wireless / P2P** | Centralized by design (RMFS typically is). |
| **GPU** | No. |
| **Laptop FPS** | Discrete-event; “FPS” is not the metric. Runs fast. |
| **Links** | [merschformann/RAWSim-O](https://github.com/merschformann/RAWSim-O) (v1.0.13 in 2024) |

Use if the research question is *fulfillment system decision policies*, not decentralized AMR navigation. GPL may infect derivative code.

#### Amazon sorting-grid / RMFS literature (not a downloadable sim)

Canonical academic line: Kiva / Amazon Robotics **Robotic Mobile Fulfillment Systems** — robots drive under pods, lift, deliver to pickers. MAPF papers treat this as a grid with narrow aisles. There is no official Amazon sim. Practical stand-ins:

- MovingAI **warehouse-*** maps (aisle geometry from that literature).
- [League of Robot Runners](https://www.leagueofrobotrunners.org/) — Amazon-sponsored lifelong MAPF competition, up to **10k agents**, 1 second per step, sortation-center maps. Code/benchmarks: [MAPF-Competition/Benchmark-Archive](https://github.com/MAPF-Competition/Benchmark-Archive), [Code-Archive](https://github.com/MAPF-Competition/Code-Archive). ICAPS 2024 system demo: Chan et al., “The League of Robot Runners.”
- [WareRover](https://github.com/HHH-X/WareRover) (2026) — Python RMFS sim coupling **order scheduling + MAPF**, heterogeneous AGVs, failures. Site: <https://hhh-x.github.io/WareRover/>. Paper: arXiv:2602.13999.
- Jiaoyang Li warehouse page: <https://jiaoyangli.me/research/warehouse/>.

#### RWARE (Multi-Robot Warehouse)

| | |
|---|---|
| **License** | MIT |
| **Language** | Python, Gymnasium |
| **2D vs 3D** | Discrete grid, shelf-carrying robots |
| **ROS** | No. |
| **Multi-robot** | Native MARL (`rware-tiny-2ag-v2`, etc.). Tiny 10×11 to large 16×29. |
| **Warehouse** | Yes, by construction (request shelves, workstations). **Very toy visually.** |
| **Wireless / P2P** | Partial observability / sensor range parameters — not a radio model. |
| **GPU** | No (CPU env). |
| **Laptop FPS** | Thousands of steps/sec. |
| **Links** | [semitable/robotic-warehouse](https://github.com/semitable/robotic-warehouse) (use this, not the archive fork), Gymnasium-registered `rware-*` |

**Jumanji RobotWarehouse:** JAX rewrite for huge batched MARL. [docs](https://instadeepai.github.io/jumanji/environments/robot_warehouse/), [instadeepai/jumanji](https://github.com/instadeepai/jumanji). Collision-terminates-episode differs from original RWARE. Use for NeurIPS-scale RL, not edge Nav.

#### VMAS (Vectorized Multi-Agent Simulator)

| | |
|---|---|
| **License** | GPL-3.0 |
| **Language** | PyTorch 2D physics, Gymnasium / TorchRL / BenchMARL |
| **2D vs 3D** | Continuous 2D, vectorized |
| **ROS** | No. |
| **Multi-robot** | Excellent for MARL; scenarios are mostly *toy physics* (transport, sampling, navigation) not a warehouse CAD. |
| **Warehouse** | You would write a scenario. GPL. |
| **GPU** | Optional (batched on GPU). |
| **Links** | [proroklab/VectorizedMultiAgentSimulator](https://github.com/proroklab/VectorizedMultiAgentSimulator), [docs](https://vmas.readthedocs.io) |

#### Flatland (NeurIPS railway — *different* Flatland)

| | |
|---|---|
| **License** | MIT (flatland-rl) |
| **Language** | Python |
| **What it is** | NeurIPS 2020 / AIcrowd railway **vehicle rescheduling**: 2D grid with *restricted transitions* (tracks, switches). Multi-agent, conflicts on shared infrastructure. |
| **Warehouse analog** | **Conceptual only.** Aisles ≈ tracks, choke points ≈ single-track sections, P2P coordination ≈ conflict resolution. Geometry is railways, not shelves. Winning solution was **MAPF (CBS-family)**, not RL: [Jiaoyang-Li/Flatland](https://github.com/Jiaoyang-Li/Flatland). |
| **Links** | [flatland.aicrowd.com](https://flatland.aicrowd.com/intro.html), [flatland-rl](https://gitlab.aicrowd.com/flatland/flatland), [Flatland 3 book](https://flatland-association.github.io/flatland-book/challenges/flatland3.html) |

Cite it in a NeurIPS-flavored related-work slide. Do not use it as the warehouse env.

#### MAPF benchmarks (MovingAI + mapf.info)

| | |
|---|---|
| **License** | Benchmark data free to use with citation (Stern et al. MAPF survey / MovingAI). |
| **Format** | ASCII `.map` + `.scen` start-goal pairs |
| **Warehouse maps** | `warehouse-10-20-10-2-1` (161×63), `warehouse-20-40-10-2-1`, `warehouse-20-40-10-2-2`, etc. Added 2019. Long aisles, narrow corridors, classic choke points. |
| **ROS** | None; trivial to convert to `OccupancyGrid`. |
| **Multi-robot** | 25 scenario sets × 2; agent counts from handfuls to hundreds. |
| **Laptop FPS** | N/A (static maps). Your solver’s runtime *is* the benchmark. |
| **Links** | [movingai.com/benchmarks/mapf](https://movingai.com/benchmarks/mapf.html), [map index](https://movingai.com/benchmarks/mapf/index.html), community results: [mapf.info](http://www.mapf.info/), survey citation: Stern et al., “Multi-Agent Pathfinding: Definitions, Variants, and Benchmarks,” SoCS 2019. |

**This is the map source you should use even if the *simulator* is pygame or Gazebo.**

#### POGEMA (ICLR 2025-adjacent PO-MAPF)

Partially observable grid MAPF, PettingZoo / SampleFactory. Built for **decentralized** (no shared map, no comms by default). Extremely on-theme for this PS’s algorithm, toy visually.

- [Cognitive-AI-Systems/pogema](https://github.com/Cognitive-AI-Systems/pogema) (MIT)

### 2.13 CARLA (mention only)

CARLA is an urban **autonomous driving** sim (Unreal, LGPL, ROS bridge exists). Maps are cities and highways, sensors are cameras/lidar for cars, multi-agent is traffic, not AMR aisles. **Not relevant** to a warehouse AMR PS unless you are doing last-mile delivery *outside* the building. Skip.

- <https://carla.org/>

### 2.14 Nav2 multi-robot (not a simulator — the runtime)

[Nav2](https://docs.nav2.org/) is the ROS 2 navigation stack. It is what you run *inside* Gazebo/Webots/Isaac/Stage, and what you *might* run on a Pi.

- **Multi-robot:** namespaced bringup (`/robot1/`, `/robot2/`), separate costmaps, `navigate_to_pose` per robot. There is **no** built-in decentralized fleet coordinator. Collision avoidance is local (costmap + DWB/MPPI). Global conflicts (two robots in a one-way aisle) are *your* algorithm.
- **Jazzy note:** `turtlebot3_gazebo` is not released past Humble; clone from source or use TurtleBot 4 / custom AMR.
- **Composition:** `use_composition:=true` is mandatory on edge (see §3).
- **RMW CPU (Nav2 docs, TurtleBot 4 sim, Dec 2025 rolling):** Zenoh ~4.5% CPU, FastDDS ~6.8%, CycloneDDS ~18.3% on that test. Zenoh is the edge-friendly RMW.
- **Open-RMF / free_fleet:** *centralized* fleet adapter over Zenoh. Useful as a *dashboard/task dispatcher* if you keep planning on-robot. Dangerous if it becomes the brain. [open-rmf/free_fleet](https://github.com/open-rmf/free_fleet)

Docs: [Nav2](https://docs.nav2.org/), [tuning / RMW](https://docs.nav2.org/tuning/index.html), [OSRF multi-robot book](https://osrf.github.io/ros2multirobotbook/).

### 2.15 Arena-Rosnav (Arena 4.0)

| | |
|---|---|
| **License** | MIT |
| **Language** | Python/C++, ROS 2 Humble (officially Ubuntu 22.04 only) |
| **2D vs 3D** | Backends: **Gazebo, Unity, Flatland** |
| **ROS** | ROS 2 Humble; they compile ROS inside the workspace (~80 GB, >1 hour install) |
| **Multi-robot** | `robot:=jackal[2]` syntax; evaluation of multiple robots/planners |
| **Warehouse** | Dynamic obstacle / DRL *local* navigation benchmark worlds, not a fulfillment warehouse. Humans via HuNav. |
| **Wireless / P2P** | Not the focus. |
| **GPU** | Depends on backend (Unity/Gazebo). |
| **Laptop FPS** | Heavy install; runtime similar to chosen backend. |
| **Links** | [Arena-Rosnav/arena-rosnav](https://github.com/Arena-Rosnav/arena-rosnav), [docs](https://arena-rosnav.readthedocs.io/en/latest/), [install](https://arena-rosnav.readthedocs.io/en/latest/tutorials/installation/) |

**Verdict:** excellent if you already wanted a DRL local planner benchmark. **Too heavy** as the *only* stack for a 2-week decentralized warehouse demo (80 GB, Ubuntu-locked, three simulators). Steal worlds/planners, do not adopt the whole distro unless a teammate has used it.

### 2.16 MiniGrid / PettingZoo (too toy — say so)

| | |
|---|---|
| **MiniGrid** | Farama discrete grid RL, **single-agent**. Apache 2.0. [Farama-Foundation/Minigrid](https://github.com/Farama-Foundation/Minigrid). Multi-agent forks exist ([ini/multigrid](https://github.com/ini/multigrid)). |
| **PettingZoo** | API, not a warehouse. You *wrap* RWARE/POGEMA/MultiGrid as `ParallelEnv`. |
| **Why too toy** | 8×8 rooms, keys/doors, pixel observations. No kinematics, no aisles-as-choke-points unless you build them, no OccupancyGrid, no edge robot. Fine for a unit test of a learned policy; **not a warehouse AMR sim**. |

If you need a Gym API, use **RWARE or POGEMA**, not MiniGrid.

### 2.17 Extra environments worth knowing (still in the catalog)

| Name | Why it exists | Use here? |
|---|---|---|
| **Open-RMF** | Building-scale fleet OS (doors, lifts, traffic graphs), Gazebo plugins, Zenoh free_fleet | Dashboard / task tickets only — do not let RMF become the planner |
| **SMART** (arXiv:2503.04798) | Execute MAPF plans in physics (ARGoS / Isaac) with delays and comms | Research execution layer later |
| **ARGoS** | Swarm robotics, thousands of robots, C++ | Overkill; no warehouse assets |
| **Isaac Lab** | GPU-parallel RL on Isaac Sim | NeurIPS RL sidecar if you have the GPU |
| **gym-pybullet-drones** | Multi-quad PyBullet | Wrong morphology |

---

## 3. What can actually run on the EDGE (Pi / Jetson Nano)

Be blunt: **“Jetson Nano” in 2026 usually means the 2019 4 GB board**, which is a different planet from **Jetson Orin Nano (2023) / Orin Nano Super**. Raspberry Pi 4 (2019, Cortex-A72) is similarly not a Pi 5 (2023, Cortex-A76, ~3× CPU).

### 3.1 Hardware reality check

| Board | Year | RAM | Where it sits | Honest role in this PS |
|---|---|---|---|---|
| **Raspberry Pi 4** (4/8 GB) | 2019 | 4–8 GB | Ubuntu 22.04 + **ROS 2 Humble** | Can run a **slim Nav2** *or* a custom 2D planner. Full SLAM+Nav2+cameras: 70–90% CPU, thermal throttle. Community reports Nav2 without composition saturates all 4 cores. |
| **Raspberry Pi 5** (4/8 GB) | 2023 | 4–8 GB | Ubuntu 24.04 + **ROS 2 Jazzy** (Pi 5 does **not** officially run Ubuntu 22.04 / Humble cleanly) | **Sweet spot.** Nav2 + 2D lidar + IMU is comfortable. No CUDA. Best $ for this PS if the planner is geometric, not a big net. |
| **Jetson Nano** (4 GB) | 2019 | 4 GB | JetPack 4.6, Ubuntu **18.04**, CUDA 10.2 | **Do not target Isaac ROS.** Max realistic: ROS 2 Foxy/Humble in Docker (painful), TFLite tiny nets, 2D A*, ORCA. 128 Maxwell CUDA cores are obsolete. Treat as “we have a Pi with a weak GPU.” |
| **Jetson Orin Nano 8 GB** | 2023 | 8 GB | JetPack 5.1+ historically; **Isaac ROS 4.6 (2026) wants JetPack 7.2** on Orin/Thor | Minimum board NVIDIA still talks about for Isaac ROS (from 2023 forum: Orin Nano 8 GB min; classic Nano cannot run JetPack 5.1.2). |
| **Jetson Orin Nano Super** | 2024/25 | 8 GB | ~67 TOPS, JetPack 6.2/7.x | Fine for YOLO-class vision + Nav2. Overkill if you only need A*. |
| **Orin NX / AGX Orin / Thor** | 2022–2026 | 8–128 GB | Isaac ROS first-class | Research / product, not a hackathon BOM |

**Isaac Sim does not run on any of these.** Isaac Sim 6.0 aarch64 is **DGX Spark only**. Jetson is for **Isaac ROS** (perception), not the simulator.

### 3.2 Candidate runtimes

#### ROS 2 (Humble / Jazzy) on Pi

- **Pi 4:** Humble on Ubuntu 22.04 Server 64-bit. Apt packages exist for arm64.
- **Pi 5:** Jazzy on Ubuntu 24.04 Server. Do not fight Humble onto Pi 5.
- Use **Server**, not Desktop. SSH. No onboard RViz.
- `use_sim_time` only in sim; on the robot set it false.
- Built-in Wi-Fi on Pi 4 steals CPU when you stream scans to a laptop RViz — USB Wi-Fi or Ethernet helps.

Docs: [ROS 2 Humble install](https://docs.ros.org/en/humble/Installation.html), [Jazzy](https://docs.ros.org/en/jazzy/Installation.html).

#### Nav2 on edge

**Feasible on Pi 5; painful on Pi 4; possible on Orin Nano.**

Must-dos:

1. `use_composition: true` (single process, shared memory). This is the difference between “works” and “100% CPU” on Pi 4 ([SO thread](https://robotics.stackexchange.com/questions/114197/nav2-overloading-raspberry-pi-cpu)).
2. Planner: **NavFn** or **Smac 2D** at 1–5 Hz, not 20 Hz. Controller 10–20 Hz.
3. Costmap: 5–10 cm resolution, rolling window ~3–6 m. No voxel layer unless you need it.
4. No AMCL particle flood; 500–1000 particles or use slam_toolbox localization-only.
5. Do **not** run RViz, Foxglove, or `ros2 bag` on the robot.
6. Prefer **Zenoh** or FastDDS over CycloneDDS on ARM (Nav2 tuning guide, 2025–2026).

Nav2 is a *local* stack (global planner + controller + recovery). **Aisle contention still needs your decentralized layer** sitting *above* or *beside* Nav2 (reserve corridor, ORCA preferred velocity, token for choke point).

#### DDS / Zenoh / MQTT / UDP P2P

| Transport | Runs on Pi? | P2P-ish? | Use |
|---|---|---|---|
| **Fast DDS** (default many distros) | Yes | DDS discovery is multicast; Wi-Fi + N robots = storms | OK on one LAN with `ROS_DOMAIN_ID` and XML peer lists |
| **Cyclone DDS** | Yes | Same multicast problem; **higher CPU** in Nav2’s TB4 test | Avoid on Pi if you can |
| **rmw_zenoh** | Yes (Humble/Jazzy/Lyrical) | **Router-based**, TCP, no multicast. One `rmw_zenohd` per machine, connect routers. Topic allow/deny filters. | **Best ROS-native choice for multi-AMR Wi-Fi** |
| **zenoh-bridge-ros2dds** | Yes | Filter/rate-limit topics between robots and a laptop dashboard | Used by Open-RMF free_fleet |
| **MQTT** (Mosquitto) | Trivial on Pi | Broker is a *rendezvous*, not a planner, if you only pub poses/intents | Simplest hackathon P2P-over-broker |
| **Raw UDP** | Trivial | True P2P, range simulated in software | Best for “decentralized comms” *algorithm* papers; you own discovery and loss |

Zenoh docs: [rmw_zenoh](https://github.com/ros2/rmw_zenoh), StereoLabs guide: [using Zenoh as middleware](https://docs.stereolabs.com/docs/integrations/ros-2/using-zenoh-as-middleware).

**Do not** put the global CBS solver behind a cloud MQTT topic and call it decentralized.

#### ORCA / RVO2 / local collision avoidance

**This is the edge-native multi-robot layer.** Each agent uses neighbors’ positions/velocities (from P2P) and computes a collision-free velocity. O(N) in neighbors, milliseconds on a Pi.

- C++: [RVO2](https://gamma.cs.unc.edu/RVO2/)
- Python: [sybrenstuvel/Python-RVO2](https://github.com/sybrenstuvel/Python-RVO2)
- Nav2 already has DWB/MPPI *obstacle* avoidance; ORCA is better when **peers are robots with known velocity**, not lidar blobs.

**Fits the PS perfectly.** Run ORCA at 10–20 Hz on Pi; keep A* for the static map.

#### CBS / ECBS / PBS MAPF — which are too heavy

| Algorithm | What it is | Edge? | Notes |
|---|---|---|---|
| **CBS** | Optimal two-level search | **No** as a 10 Hz onboard fleet solver | Fine offline / laptop for ≤10 agents on small maps; explodes in aisles |
| **ECBS / EECBS** | Bounded-suboptimal CBS | **Laptop / server** | EECBS solves ~1000 agents in 60 s *on a workstation* (AAAI 2021). Not a Pi control loop. |
| **PBS** | Priority-based search | Borderline on laptop; **not** 10 Hz on Pi for 20+ agents | [Jiaoyang-Li related solvers](https://github.com/Jiaoyang-Li); libCBS: [whoenig/libMultiRobotPlanning](https://github.com/whoenig/libMultiRobotPlanning) |
| **PIBT / LaCAM / windowed LNS** | Fast iterative / lifelong MAPF | **Laptop real-time** for hundreds of agents; **maybe** a Pi for 3–8 agents if windowed | LoRR winners (WPPL) plan 10k agents in **1 second on a beefy CPU**, not a Pi |
| **Prioritized A\*** | Plan robots in order | **Yes on Pi** for 3–8 agents on a warehouse grid | Deadlocks possible; pair with ORCA |

**Rule:** centralized optimal MAPF is a **research baseline on the laptop**. On-robot, use **independent A\* + ORCA + explicit choke-point protocol** (token, right-hand rule, reservation of a 2-cell lock). That *is* a NeurIPS-valid decentralized method; CBS-on-Pi is not.

Implementations: [libMultiRobotPlanning](https://github.com/whoenig/libMultiRobotPlanning) (CBS, ECBS, CBS-TA), [EECBS](https://github.com/Jiaoyang-Li/EECBS), LoRR: [leagueofrobotrunners.org](https://www.leagueofrobotrunners.org/).

#### Lightweight 2D occupancy grid A* / D* Lite

**This is the planner you should actually ship on Pi.**

- Grid from the same MovingAI map (sim) or `nav_msgs/OccupancyGrid` (robot).
- **A\***: replan from scratch when the local window changes. 100×100 grid is microseconds–milliseconds in Python/numpy; C++ is overkill until you profile.
- **D\* Lite**: incremental, better when obstacles appear (blocked aisle). ROS 2 example: [Shailesh-Pawar-12/D_Star_Lite_Path_Planner](https://github.com/Shailesh-Pawar-12/D_Star_Lite_Path_Planner) (Humble). Older ROS 1: [jhu-asco/dsl_gridsearch](https://github.com/jhu-asco/dsl_gridsearch).
- Keep the map **2D**. No 3D planning on Pi 4.

Nav2’s NavFn is Dijkstra/A\* on the costmap — same complexity class. A standalone A\* is easier to *prove identical* between pygame and Pi.

#### ONNX / TFLite tiny nets

If you add a learned component (local policy, congestion predictor):

- **Pi 4/5:** TFLite INT8 or ONNX Runtime + XNNPACK. Tiny CNNs / 3-layer MLPs only. 2026 ARM64 comparisons still show TFLite slightly faster on Cortex-A76 for ResNet-50 INT8; **ONNX is the better interchange** if you train in PyTorch.
- **Jetson Nano (2019):** TensorRT 8 / TFLite; keep models <10 ms. YOLO-nano-class is the ceiling.
- **Orin Nano:** TensorRT / Isaac ROS. This is where YOLO11 / visual SLAM become realistic.
- **Do not** put MAPF inside a transformer and expect Pi 4 to run it.

Isaac ROS is **not** a tiny-net story; it is GPU perception (cuVSLAM, nvblox, DNN). Wrong layer for a 2D warehouse coordinator.

#### What Isaac / Isaac ROS actually needs

| Product | Runs on | Does not run on |
|---|---|---|
| **Isaac Sim 6.0** | x86_64 Ubuntu 22.04/24.04 or Win11, **RTX 4080+ 16 GB**, 32 GB RAM | Jetson Nano, Orin Nano, Pi, most laptops |
| **Isaac ROS 4.6** (Aug 2026 notes) | Jetson **Thor / Orin** + JetPack **7.2**, 128 GB+ NVMe; or x86 Ampere+ GPU, Ubuntu 24.04, ROS 2 **Jazzy** | **Jetson Nano 2019**, Pi, JetPack 4.x |
| **Isaac ROS historically** | Orin Nano **8 GB** was the documented minimum (2023 NVIDIA forum) | Nano 4 GB |

Forum (2023, still directionally true): *“Isaac ROS packages will run at a minimum on the Orin Nano 8GB. The Jetson Nano cannot run JetPack 5.1.2.”*  
Current getting started: [nvidia-isaac-ros.github.io](https://nvidia-isaac-ros.github.io/getting_started/index.html).

**If the BOM says “Jetson Nano,” write the planner in portable Python/C++ and ignore Isaac ROS.** If someone can buy an **Orin Nano Super**, Isaac ROS is a *perception* upgrade, not a substitute for the coordinator.

### 3.3 Recommended architecture: sim on laptop, planner identical on Pi

```
                    ┌──────────────────────────────────────────┐
                    │  planner/  (THE PRODUCT)                 │
                    │  grid.py  astar.py  orca.py  p2p.py      │
                    │  Protocol: OccupancyGrid, Pose, Peers[]  │
                    │            → Path or Twist               │
                    └───────────────┬──────────────────────────┘
                                    │ same import / same .so
              ┌─────────────────────┴─────────────────────┐
              ▼                                           ▼
   adapters/sim_pygame.py                      adapters/ros2_node.py
   adapters/sim_gazebo.py                      (runs on Pi 5 / Orin)
              │                                           │
              ▼                                           ▼
   Laptop: 3–8 agents,                         Robot: lidar→costmap
   MovingAI warehouse map,                     UDP/Zenoh peers
   simulated radio (range+loss)                real Wi-Fi
              │
              ▼
   dashboard: websocket poses only
   (Foxglove / Flask / React)
```

**Rules:**

1. The planner never imports `pygame`, `gz`, or `rclpy` in its core modules.
2. Comms are an interface: `broadcast(intent)`, `neighbors()` — implemented by simulated radio *or* Zenoh/MQTT/UDP.
3. Time is just `dt`. `use_sim_time` is an adapter concern.
4. First demo: pygame + 3 robots + blocked aisle. Second demo: same planner as a ROS 2 node in Gazebo. Third: same node on a Pi with a fake lidar from the 2D sim streamed over the network (if you lack three physical AMRs).

This is how you satisfy “edge-runnable” without pretending Gazebo runs on a Pi.

---

## 4. Recommended stacks for THIS PS

### Tier A — Fastest to demo (hackathon 1–2 weeks)

**Stack:** Python 3 + pygame (or matplotlib) + MovingAI warehouse map + A* + Python-RVO2 + UDP or MQTT + a 200-line Flask/websocket dashboard.

- Day 1–2: load `warehouse-10-20-10-2-1.map`, spawn 3 agents, A* to goals, draw aisles.
- Day 3: ORCA so they do not freeze in a corridor.
- Day 4: P2P intents (next 5 waypoints) with range limit + 10% drop.
- Day 5: blocked-aisle scenario + D* Lite or replan.
- Day 6: dashboard (dots on a grid, not a planner).
- Day 7+: wrap `planner/` in a ROS 2 node *if* time remains.

**Why it wins the clock:** zero SDF, zero DDS, zero GPU, runs on Windows laptops. The science (decentralized coordination under comms limits) is fully visible.

### Tier B — Best engineering fidelity (ROS 2)

**Stack:** Ubuntu 24.04 + **ROS 2 Jazzy** + **Gazebo Harmonic** + namespaced **Nav2** (composition on) + AWS small-warehouse SDF or TurtleBot 4 `warehouse` world + `RFComms` *or* `rmw_zenoh` + Foxglove Bridge (subscribe-only).

Concrete starting repos:

- [arshadlab/tb3_multi_robot](https://github.com/arshadlab/tb3_multi_robot) (Jazzy/Harmonic, 4 TB3s)
- [Pouya-Mansournia/warehouse-amr-ros2](https://github.com/Pouya-Mansournia/warehouse-amr-ros2) (Jazzy, N robots, stations, web dashboard — note their coordination is *station reservation*, still centralized-ish)
- [aws-robotics/aws-robomaker-small-warehouse-world](https://github.com/aws-robotics/aws-robomaker-small-warehouse-world)
- Optional humans: HuNavSim

**Planner:** still *your* library. Nav2 follows a path or a `navigate_to_pose` that *you* compute. Do not let NavFn silently become the multi-robot brain.

**Edge story:** same ROS 2 node, `RMW_IMPLEMENTATION=rmw_zenoh_cpp`, Pi 5.

**Cost:** 3–7 days of ROS pain (namespaces, TF, `Twist` vs `TwistStamped` on Jazzy). Budget that honestly.

### Tier C — Best research / NeurIPS-flavored

**Stack (algorithm):** POGEMA or RWARE or custom grid + MovingAI warehouse maps + LoRR lifelong MAPF baselines (PIBT/LNS) vs **your decentralized** method. Metrics: success rate, flowtime, messages/byte, robustness to drop/delay. Optional JAX/Jumanji for scale.

**Stack (systems paper):** SMART-style “plan on grid, execute in Gazebo/Isaac with delay and RFComms.”

**Stack (RL):** VMAS or RWARE + MAPPO/IPPO; Jumanji if you need 100× env steps. Say clearly it is *not* the edge binary.

**Do not** submit Isaac Sim screenshots as the scientific contribution unless you have the GPU *and* an ablation that needs photorealism (you will not, for coordination).

### Clear winner for a first-time team

**Tier A as the spine, with a Tier B skin if Ubuntu is available.**

Justification:

1. The PS grades **decentralized coordination + edge planner**, not RTX reflections on pallet wrap.
2. First-time ROS 2 + multi-robot + Gazebo Harmonic routinely consumes the entire hackathon.
3. A pygame grid loaded with a **standard warehouse MAPF map** is *more scientifically comparable* than a custom SDF nobody else can rerun.
4. The portable `planner/` package is the only artifact that credibly “runs on Pi.”
5. Isaac Sim / Arena-Rosnav / Unity Hub fail at least two of: laptop GPU, maintenance, time-to-demo.
6. If judges want “real robotics,” a **single** Gazebo launch of 3 namespaced robots executing the *same* planner is enough theater — built in the last 48 hours, not the first 48.

**Explicit non-winners:** Isaac Sim (hardware), Unity Robotics Hub (unmaintained), AWS RoboMaker (shut down 2025-09-10), MiniGrid (toy), CARLA (wrong domain), full Nav2-on-Pi-4 (thermals).

---

## 5. Warehouse map / scenario assets

### Maps (use these)

| Asset | What you get | Link |
|---|---|---|
| **MovingAI MAPF warehouse maps** | Aisle grids, choke points, standard agent scenarios | [index](https://movingai.com/benchmarks/mapf/index.html) — download maps (73K), even/random scenarios |
| Named maps | `warehouse-10-20-10-2-1` (161×63), `warehouse-20-40-10-2-2`, etc. | Same; cite Stern et al. 2019 |
| **LoRR / sortation-center** | Huge Amazon-like sortation (e.g. 500×140), lifelong tasks | [leagueofrobotrunners.org](https://www.leagueofrobotrunners.org/), [Benchmark-Archive](https://github.com/MAPF-Competition/Benchmark-Archive) |
| **mapf.info** | Published solver results to compare against | <http://www.mapf.info/> |
| **PegasusGTV/mapf** | Python loader + GIF demo on warehouse maps | [GitHub](https://github.com/PegasusGTV/mapf) |
| **pymapf** | Warehouse / bottleneck / maze families + CBS/PIBT | [openplan-labs/pymapf](https://github.com/openplan-labs/pymapf) |

### 3D worlds (if you need look)

| Asset | Simulator | Link |
|---|---|---|
| AWS small warehouse (shelves, pallets, clutter) | Gazebo SDF | [aws-robomaker-small-warehouse-world](https://github.com/aws-robotics/aws-robomaker-small-warehouse-world) |
| TurtleBot 4 `warehouse` / depot / maze | Gazebo Harmonic | [turtlebot4_simulator](https://github.com/turtlebot/turtlebot4_simulator) |
| Isaac `full_warehouse.usd` + modular props | Isaac Sim | [Environment assets](https://docs.isaacsim.omniverse.nvidia.com/4.2.0/features/environment_setup/assets/usd_assets_environments.html), [static warehouse tutorial](https://docs.isaacsim.omniverse.nvidia.com/6.0.0/digital_twin/warehouse_logistics/tutorial_static_assets.html) |
| Open-RMF traffic maps / office-warehouse demos | Gazebo + RMF | [open-rmf](https://github.com/open-rmf) |
| RAWSim-O layouts | C# RMFS | [RAWSim-O](https://github.com/merschformann/RAWSim-O) |
| WareRover JSON maps (boxes, receivers, wait zones) | Python | [HHH-X/WareRover](https://github.com/HHH-X/WareRover) |
| RWARE built-in tiny/small/medium/large | Gymnasium | [robotic-warehouse](https://github.com/semitable/robotic-warehouse) |

### Scenario recipes (build these, not a pretty empty floor)

1. **Nominal 3-AMR pickup:** three stations on the warehouse perimeter, random goals, no comms loss.
2. **Blocked aisle:** close a corridor at t=T (occupancy flip). D* Lite / replan vs stuck Nav2.
3. **Choke-point deadlock:** two robots opposite directions in a 1-cell aisle. Your protocol (yield / token) vs naive A*.
4. **Comms degradation:** range 5 m, 20% drop — decentralized vs “global MQTT planner” cheat.
5. **Human in aisle (optional):** HuNavSim / pedsim walker occupying a cell.
6. **Pickup station contention:** two robots, one dock — reservation must be *P2P or token*, not a central server (or if you use a reservation, call it out as a limited shared blackboard).

Convert MovingAI maps to Gazebo by extruding `@` cells as boxes, or keep Gazebo for kinematics only and plan on the 2D map (SMART’s philosophy).

---

## 6. Dashboard options that stay “monitoring only”

**Invariant:** the dashboard **subscribes**. It never publishes goals that the fleet *must* obey, never runs CBS, never assigns tasks (unless you explicitly label a separate “operator injects a task” debug button). If Foxglove can call `/navigate_to_pose`, **disable publish** in production layouts.

| Tool | Role | How to keep it dumb | Links |
|---|---|---|---|
| **Foxglove** | Best modern fleet view (3D, plots, image, topic table) | `foxglove_bridge` on the **laptop**, not on the Pi. Layout with Pose, Path, OccupancyGrid. Do not add Teleop panels for the demo. | [ROS 2 docs](https://docs.foxglove.dev/docs/getting-started/frameworks/ros2), [bridge](https://docs.foxglove.dev/docs/fleet/bridge) |
| **RViz2** | Standard ROS 2 3D | Laptop only. Displays TF, costmaps, plans. Easy to accidentally click Nav2 goals — disable the tool. | `sudo apt install ros-$ROS_DISTRO-rviz2` |
| **PlotJuggler** | Time-series (RTT, drop rate, CPU, path length) | Subscribe via [plotjuggler_bridge](https://github.com/PlotJuggler/plotjuggler_bridge) or native ROS. Perfect for *comms* plots. | [facontidavide/PlotJuggler](https://github.com/facontidavide/PlotJuggler) |
| **rosbridge + roslibjs** | Browser dashboard | HTML canvas of the map + dots. Team owns the UI. Used by several warehouse-AMR student repos. | [rosbridge_suite](https://github.com/RobotWebTools/rosbridge_suite) |
| **Custom React / websocket** | Hackathon-pretty | Backend reads JSON poses from MQTT/UDP. **No planner in Node.** | Any ws library |
| **Flask / FastAPI** | Fastest custom | `/state` JSON + simple SVG/canvas grid. 150 lines. | stdlib |
| **Open-RMF web** | Building fleet UI | Tempting, but RMF *is* a coordinator. Use only if you strip it to visualization. | [open-rmf](https://github.com/open-rmf/rmf-web) |

**Recommended combo:**

- **Week 1 (pygame):** Flask + websocket, SVG warehouse, robot IDs, last-heard timestamp (makes packet loss *visible*).
- **Week 2 (ROS):** Foxglove on the operator laptop via `foxglove_bridge`; PlotJuggler for comms metrics.
- **Never:** Nav2 rviz goal tool, RMF dispatcher, or a “central planner” tab as the live controller.

---

## 7. Comparison table

Top 8 environments for *this* PS. Scores 1–5.

| Environment | Time-to-first-demo | Warehouse look | Multi-robot | Edge-export | Dashboard | Realism of comms | Notes |
|---|---|---|---|---|---|---|---|
| **Custom pygame 2D + MovingAI** | **5** | 2 | **5** | **5** | 4 (easy JSON) | **4** (you implement RF) | **Winner for first-time team** |
| **Gazebo Harmonic + ROS 2** | 2 | **4** | **4** | **4** (planner node) | **5** (Foxglove/RViz) | **5** (RFComms) | Best engineering; slow start |
| **Webots + webots_ros2** | 3 | 3 | 4 | 4 | 4 | 3 | Kindest 3D on a laptop |
| **Stage / Flatland 2D** | 3 | 2 | **5** | 4 | 4 | 2 | Great scale; ROS 2 forks |
| **PyBullet** | 4 | 2 | 4 | 4 | 3 | 2 | Physics sandbox, ugly warehouse |
| **Isaac Sim** | 1 | **5** | 4 | 2 (Sim≠Jetson) | 4 | 2 | Needs RTX 4080+; not edge |
| **RWARE / POGEMA** | **5** | 2 | **5** | 3 (policy ≠ Nav) | 2 | 3 (PO, not RF) | NeurIPS MARL; toy look |
| **Unity Robotics Hub** | 2 | 4 | 4 | 2 | 3 | 2 | **Unmaintained ROS bridge** |

CoppeliaSim would score ~Webots but **Edu license** hurts a public repo. Arena-Rosnav is a *distribution* on top of Gazebo/Unity/Flatland, not an 8th world. RAWSim-O wins logistics, loses robotics. AWS RoboMaker scores 0 as a service; its warehouse **world** still feeds the Gazebo row.

---

## Appendix A — Link dump (quick)

**Sims:** [Gazebo Harmonic](https://gazebosim.org/docs/harmonic) · [Isaac Sim reqs](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/requirements.html) · [Webots ROS 2](https://github.com/cyberbotics/webots_ros2) · [Coppelia ROS 2](https://manual.coppeliarobotics.com/en/ros2Tutorial.htm) · [Unity Robotics Hub](https://github.com/Unity-Technologies/Unity-Robotics-Hub) · [PyBullet](https://github.com/bulletphysics/bullet3) · [MuJoCo](https://github.com/google-deepmind/mujoco) · [Stage ROS 2](https://github.com/tuw-robotics/stage_ros2) · [Flatland 2D](https://github.com/avidbots/flatland) · [pedsim_ros](https://github.com/srl-freiburg/pedsim_ros) · [HuNavSim](https://github.com/robotics-upo/hunav_sim)

**Warehouse / MAPF:** [MovingAI MAPF](https://movingai.com/benchmarks/mapf.html) · [mapf.info](http://www.mapf.info/) · [RWARE](https://github.com/semitable/robotic-warehouse) · [Jumanji RobotWarehouse](https://instadeepai.github.io/jumanji/environments/robot_warehouse/) · [VMAS](https://github.com/proroklab/VectorizedMultiAgentSimulator) · [POGEMA](https://github.com/Cognitive-AI-Systems/pogema) · [RAWSim-O](https://github.com/merschformann/RAWSim-O) · [WareRover](https://github.com/HHH-X/WareRover) · [LoRR](https://www.leagueofrobotrunners.org/) · [AWS warehouse world](https://github.com/aws-robotics/aws-robomaker-small-warehouse-world) · [NeurIPS Flatland](https://flatland.aicrowd.com/intro.html)

**ROS / edge:** [Nav2](https://docs.nav2.org/) · [rmw_zenoh](https://github.com/ros2/rmw_zenoh) · [Isaac ROS](https://nvidia-isaac-ros.github.io/) · [Arena-Rosnav](https://github.com/Arena-Rosnav/arena-rosnav) · [libMultiRobotPlanning](https://github.com/whoenig/libMultiRobotPlanning) · [Python-RVO2](https://github.com/sybrenstuvel/Python-RVO2) · [Foxglove ROS 2](https://docs.foxglove.dev/docs/getting-started/frameworks/ros2)

**Dead:** AWS RoboMaker — discontinued **2025-09-10**. Do not build on it. Reuse the GitHub worlds.

---

## Appendix B — First-week checklist (operational)

1. Freeze the planner API (`plan(grid, self, peers) -> path`).
2. Load one MovingAI warehouse map; three agents; screenshot.
3. Add ORCA; show a choke-point yield.
4. Add simulated radio; plot delivery ratio in PlotJuggler or matplotlib.
5. Only then: ROS 2 namespaced Gazebo *or* Pi 5 node with the **same** files.
6. Dashboard last, subscribe-only.

If step 2 is not done by end of day 2, you picked the wrong simulator.
