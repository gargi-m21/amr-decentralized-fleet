"""
Multi-Agent Warehouse Fleet Publisher
Simulates 3 independent AMRs running decentralized coordination:
- P2P Intent broadcasting (10 Hz)
- Corridor Token negotiation for 1-lane choke points (no head-on deadlocks)
- Dynamic route repair when dynamic obstacles are detected (D* Lite behavior)
- Independent state machines per AMR (no god-planner)
"""

import asyncio
import math
import time
import random
from typing import List, Dict, Tuple, Optional, Any
import server

class SimulatedAMR:
    def __init__(self, robot_id: str, start_x: float, start_y: float, color: str, priority_val: int):
        self.robot_id = robot_id
        self.x = start_x
        self.y = start_y
        self.heading = 0.0
        self.color = color
        self.priority = priority_val
        self.seq = 0
        self.battery = 98.0 - random.uniform(0, 5)
        self.status = "NAVIGATING" # NAVIGATING, TOKEN_HELD, YIELDING, BLOCKED, DOCKING
        self.task_id = f"TASK_{random.randint(100, 999)}"
        self.task_state = "TO_PICK" # TO_PICK, TO_DROP, RETURN
        self.speed = 1.2 # m/s max
        self.current_speed = 0.0
        
        # Waypoints queue
        self.waypoints: List[Tuple[float, float]] = []
        self.path_intent: List[List[float]] = []
        self.token_held: Optional[str] = None
        self.waiting_for_token: Optional[str] = None
        self.last_lidar_distance = 4.5
        
        self.assign_next_mission()

    def assign_next_mission(self):
        # Realistic warehouse loop: Pick station -> Across choke -> Drop station -> Return
        self.task_id = f"TICK_{random.randint(100, 999)}"
        if self.robot_id == "amr_01":
            # Traverses through CHOKE_BETA back and forth
            if self.task_state in ["RETURN", "IDLE"]:
                self.task_state = "TO_PICK"
                self.waypoints = [(10, 3), (12, 6), (15, 11), (18, 11), (21, 11), (24, 18), (26, 21)]
            else:
                self.task_state = "RETURN"
                self.waypoints = [(24, 18), (21, 11), (18, 11), (15, 11), (12, 6), (10, 3), (3, 3)]
        elif self.robot_id == "amr_02":
            # Opposite direction through CHOKE_BETA (causes head-on conflict)
            if self.task_state in ["RETURN", "IDLE"]:
                self.task_state = "TO_PICK"
                self.waypoints = [(26, 21), (22, 16), (20, 11), (18, 11), (15, 11), (12, 6), (10, 3)]
            else:
                self.task_state = "RETURN"
                self.waypoints = [(12, 6), (15, 11), (18, 11), (20, 11), (22, 16), (26, 21), (28, 22)]
        else: # amr_03
            # Patrols CHOKE_ALPHA / pick station 1
            if self.task_state in ["RETURN", "IDLE"]:
                self.task_state = "TO_PICK"
                self.waypoints = [(3, 12), (7, 11), (10, 11), (12, 11), (15, 16), (18, 21)]
            else:
                self.task_state = "RETURN"
                self.waypoints = [(15, 16), (12, 11), (10, 11), (7, 11), (3, 12)]

    def update_intent_path(self):
        # Next 6-8 waypoints for peer broadcasting
        pts = [[round(self.x, 2), round(self.y, 2)]]
        for wp in self.waypoints[:6]:
            pts.append([round(wp[0], 2), round(wp[1], 2)])
        self.path_intent = pts

    def step(self, dt: float, peer_states: Dict[str, Any], dynamic_obstacles: List[Dict[str, Any]], choke_locks: Dict[str, str]):
        self.seq += 1
        self.battery = max(10.0, self.battery - (0.003 * dt))
        
        # 1. Check Dynamic Obstacles within LiDAR range (D* Lite dynamic repair)
        replan_needed = False
        self.last_lidar_distance = 6.0
        for obs in dynamic_obstacles:
            dist_to_obs = math.hypot(self.x - obs["x"], self.y - obs["y"])
            if dist_to_obs < self.last_lidar_distance:
                self.last_lidar_distance = round(dist_to_obs, 2)
            
            # If obstacle blocks upcoming waypoints
            for wp in self.waypoints[:3]:
                if math.hypot(wp[0] - obs["x"], wp[1] - obs["y"]) < 2.0:
                    replan_needed = True
                    break
        
        if replan_needed:
            self.status = "REROUTING"
            # Dynamic bypass via alternate aisle (y=20 bypass corridor)
            if self.waypoints and self.waypoints[0][1] < 16:
                bypass_y = 20.0 if self.y < 16 else 6.0
                self.waypoints = [(self.x, bypass_y), (24.0, bypass_y)] + self.waypoints[2:]
                server.current_fleet_state["events"].insert(0, {
                    "timestamp": time.strftime("%H:%M:%S"),
                    "type": "D*_REPLAN",
                    "text": f"[{self.robot_id}] Blockage detected at ({obs['x']:.1f}, {obs['y']:.1f}). D* Lite repaired path via detour."
                })
        
        if not self.waypoints:
            self.assign_next_mission()
            return

        target = self.waypoints[0]
        dx = target[0] - self.x
        dy = target[1] - self.y
        dist = math.hypot(dx, dy)

        # 2. Check Choke Point Entry & Corridor Token
        approaching_choke = None
        # CHOKE_BETA is at x: 17.5-20.5, y: 10-12
        if 14.0 <= self.x <= 22.0 and 9.5 <= self.y <= 12.5:
            approaching_choke = "CHOKE_BETA"
        elif 6.5 <= self.x <= 13.0 and 9.5 <= self.y <= 12.5:
            approaching_choke = "CHOKE_ALPHA"

        # If inside or near choke point, request / hold token
        if approaching_choke:
            holder = choke_locks.get(approaching_choke)
            if holder is None or holder == self.robot_id:
                # Token acquired
                if self.token_held != approaching_choke:
                    choke_locks[approaching_choke] = self.robot_id
                    self.token_held = approaching_choke
                    self.status = "TOKEN_HELD"
                    server.current_fleet_state["events"].insert(0, {
                        "timestamp": time.strftime("%H:%M:%S"),
                        "type": "TOKEN_GRANT",
                        "text": f"[{self.robot_id}] P2P Token acquired for {approaching_choke}. Right of way granted."
                    })
            else:
                # Another robot holds token!
                # Yield and hold position outside the 1-lane choke
                self.status = "YIELDING"
                self.current_speed = 0.0
                self.update_intent_path()
                return
        else:
            # Exited choke zone -> release token
            if self.token_held:
                if choke_locks.get(self.token_held) == self.robot_id:
                    del choke_locks[self.token_held]
                server.current_fleet_state["events"].insert(0, {
                    "timestamp": time.strftime("%H:%M:%S"),
                    "type": "TOKEN_RELEASE",
                    "text": f"[{self.robot_id}] Cleared {self.token_held}. Token released back to peer mesh."
                })
                self.token_held = None
                self.status = "NAVIGATING"

        # 3. Target Navigation & Pure Pursuit
        if dist < 0.6:
            self.waypoints.pop(0)
            if not self.waypoints:
                self.assign_next_mission()
                return
            target = self.waypoints[0]
            dx = target[0] - self.x
            dy = target[1] - self.y
            dist = math.hypot(dx, dy)

        target_heading = math.atan2(dy, dx)
        # Turn towards target
        angle_diff = (target_heading - self.heading + math.pi) % (2 * math.pi) - math.pi
        self.heading += angle_diff * min(1.0, 5.0 * dt)
        
        # Move forward
        target_v = min(self.speed, dist * 1.5)
        self.current_speed += (target_v - self.current_speed) * 0.2
        self.x += self.current_speed * math.cos(self.heading) * dt
        self.y += self.current_speed * math.sin(self.heading) * dt
        
        if self.status != "TOKEN_HELD":
            self.status = "NAVIGATING"
            
        self.update_intent_path()

    def get_state(self, peer_ids: List[str]) -> Dict[str, Any]:
        return {
            "robot_id": self.robot_id,
            "seq": self.seq,
            "color": self.color,
            "pose": {
                "x": round(self.x, 2),
                "y": round(self.y, 2),
                "heading": round(self.heading, 3)
            },
            "twist": {
                "linear": round(self.current_speed, 2),
                "angular": 0.05
            },
            "status": self.status,
            "priority": self.priority,
            "task": {
                "id": self.task_id,
                "state": self.task_state
            },
            "battery": round(self.battery, 1),
            "voltage": round(24.0 + (self.battery / 100.0) * 1.8, 2),
            "path_intent": self.path_intent,
            "choke_token": self.token_held,
            "lidar_min_dist": self.last_lidar_distance,
            "peers_heard": [p for p in peer_ids if p != self.robot_id],
            "last_packet_ms": round(random.uniform(12, 45), 1)
        }

async def run_simulation_loop():
    logger = server.logger
    logger.info("Initializing Decentralized Multi-AMR Publisher loop (10 Hz)...")
    
    robots = [
        SimulatedAMR("amr_01", 3.0, 3.0, "#3B82F6", priority_val=1),
        SimulatedAMR("amr_02", 28.0, 21.0, "#10B981", priority_val=2),
        SimulatedAMR("amr_03", 3.0, 12.0, "#F59E0B", priority_val=3)
    ]
    
    choke_locks: Dict[str, str] = {} # choke_id -> robot_id
    dt = 0.1 # 100ms step
    peer_ids = [r.robot_id for r in robots]

    while True:
        try:
            dyn_obs = server.current_fleet_state["warehouse"]["dynamic_obstacles"]
            peer_states = {r.robot_id: r for r in robots}
            
            # Step each autonomous robot independently
            for r in robots:
                r.step(dt, peer_states, dyn_obs, choke_locks)
                server.current_fleet_state["robots"][r.robot_id] = r.get_state(peer_ids)
            
            # Update network telemetry
            net_stats = server.current_fleet_state["network_stats"]
            loss_rate = net_stats.get("packet_loss_rate", 0.0)
            base_rate = 30 # 3 robots * 10 Hz
            net_stats["p2p_packets_sec"] = int(base_rate * (1.0 - loss_rate))
            
            # Broadcast to all connected web spectators
            await server.broadcast_state()
            
            await asyncio.sleep(dt)
        except Exception as e:
            logger.error(f"Error in simulation step: {e}")
            await asyncio.sleep(1.0)

if __name__ == "__main__":
    # Start both server and simulation loop
    loop = asyncio.get_event_loop()
    loop.create_task(run_simulation_loop())
    uvicorn.run(server.app, host="0.0.0.0", port=8000)
