# AMR Decentralized Fleet Spectator Dashboard
### *BEL SIH-26123 • Zero-SPOF Architecture • High-Density Industrial Monitor*

Inspired by industrial fleet monitors (**Open-RMF Web, Foxglove Studio, Siemens Industrial Edge, and OTTO Fleet Manager**), this dashboard acts as a **strictly read-only spectator**. It visualizes peer-to-peer AMR coordination, dynamic obstacle rerouting, and corridor token contention without ever acting as a central planner.

---

## 1. Key Features

1. **Spatial Warehouse Twin (HTML5 Canvas 2D)**:
   - Metric warehouse coordinate grid (36.0m × 24.0m) with shelves, pallet racks, and stations.
   - **1-Lane Choke Points** (`CHOKE_ALPHA`, `CHOKE_BETA`) marked with hazard striping.
   - Real-time robot hulls with heading orientation pointers and collision safety envelopes.
   - **Broadcasted Intent Ribbons**: visualizes the next 6-8 waypoints shared over P2P mesh.
   - Interactive smooth pan & zoom (scroll wheel to zoom, drag to pan, double-click to drop obstacles).

2. **Per-Robot Local View Cards (The Decentralization Proof)**:
   - Displays what each robot knows individually (**no god-view memory**).
   - Shows current state (`NAVIGATING`, `TOKEN_HELD`, `YIELDING`, `REROUTING`).
   - Lists **last-heard P2P radio neighbors** with packet round-trip latencies.
   - Displays choke token status and local LiDAR horizon.

3. **Fault Injection & Presentation Triggers**:
   - **"Inject Blocked Aisle (Drop Pallet)"**: drops a dynamic obstacle at an active choke point, triggering D* Lite dynamic route repairs and CBBA re-auctioning in real-time.
   - **"Wi-Fi Loss Simulation"**: toggles 0%, 15%, or 30% packet loss to showcase graceful fail-soft degradation.
   - **"Unplug-Safe Spectator"**: killing or disconnecting this dashboard does not pause robot navigation.

---

## 2. How to Run

### Start the Dashboard Server
From the project root:
```bash
cd dashboard
python server.py
```
This automatically starts:
- The FastAPI WebSocket telemetry server on `0.0.0.0:8000`.
- The background 10 Hz decentralized multi-AMR simulation loop (`mock_fleet_publisher.py`).

---

## 3. How to Show It to Your Team on Their Systems

Because the server binds to `0.0.0.0`, any device connected to the **same Wi-Fi router, local network, or mobile hotspot** can access it instantly:

1. **On your machine**:
   Open: [http://localhost:8000](http://localhost:8000)

2. **On your teammates' laptops or phones**:
   Find your machine's local IP address (e.g. `192.168.1.19`):
   ```bash
   ipconfig
   ```
   Give your teammates this URL:
   ```
   http://192.168.1.19:8000
   ```
   They can open it in Chrome, Edge, Safari, or Firefox with **zero installation needed on their machines**.

---

## 4. How Teammates Plug in Their Real ROS 2 / Zenoh Nodes

When the core coordinator or Gazebo containers are ready, they can send live `Intent.msg` state packets to the dashboard via WebSocket or simple HTTP POST:
- **WebSocket**: Connect to `ws://<dashboard-ip>:8000/ws/telemetry` and publish JSON.
- **REST**: POST state to `/api/fleet_state`.
