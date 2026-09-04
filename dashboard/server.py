import asyncio
import json
import logging
from typing import Set, Dict, Any, List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
import uvicorn
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("DashboardServer")

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Auto-start simulation loop in background
    try:
        import mock_fleet_publisher
        sim_task = asyncio.create_task(mock_fleet_publisher.run_simulation_loop())
        logger.info("Decentralized AMR fleet simulation task started.")
    except Exception as e:
        logger.warning(f"Could not auto-start mock_fleet_publisher: {e}")
        sim_task = None
    yield
    if sim_task:
        sim_task.cancel()

app = FastAPI(title="AMR Decentralized Fleet Spectator Dashboard", lifespan=lifespan)
connected_clients: Set[WebSocket] = set()

# Shared state store (in-memory, fed by AMRs or mock publisher)
current_fleet_state: Dict[str, Any] = {
    "warehouse": {
        "dimensions": {"width": 36, "height": 24}, # in meters
        "grid_resolution": 1.0, # 1m cells
        "shelves": [
            {"id": "RACK_A1", "x": 6, "y": 4, "w": 2, "h": 6},
            {"id": "RACK_A2", "x": 6, "y": 14, "w": 2, "h": 6},
            {"id": "RACK_B1", "x": 14, "y": 4, "w": 2, "h": 6},
            {"id": "RACK_B2", "x": 14, "y": 14, "w": 2, "h": 6},
            {"id": "RACK_C1", "x": 22, "y": 4, "w": 2, "h": 6},
            {"id": "RACK_C2", "x": 22, "y": 14, "w": 2, "h": 6},
            {"id": "RACK_D1", "x": 30, "y": 4, "w": 2, "h": 6},
            {"id": "RACK_D2", "x": 30, "y": 14, "w": 2, "h": 6},
        ],
        "choke_zones": [
            {"id": "CHOKE_ALPHA", "x": 5.5, "y": 10.5, "w": 3.0, "h": 3.0, "name": "Rack A Cutout (1-Lane)"},
            {"id": "CHOKE_BETA", "x": 13.5, "y": 10.5, "w": 3.0, "h": 3.0, "name": "Rack B Cutout (1-Lane)"},
            {"id": "CHOKE_GAMMA", "x": 21.5, "y": 10.5, "w": 3.0, "h": 3.0, "name": "Rack C Cutout (1-Lane)"},
            {"id": "CHOKE_DELTA", "x": 29.5, "y": 10.5, "w": 3.0, "h": 3.0, "name": "Rack D Cutout (1-Lane)"}
        ],
        "stations": [
            {"id": "DOCK_1", "type": "CHARGER", "x": 2.5, "y": 2.0, "label": "Dock 1"},
            {"id": "DOCK_2", "type": "CHARGER", "x": 2.5, "y": 12.0, "label": "Dock 2"},
            {"id": "DOCK_3", "type": "CHARGER", "x": 2.5, "y": 22.0, "label": "Dock 3"},
            {"id": "PICK_1", "type": "PICK", "x": 11.0, "y": 2.0, "label": "Pick Bay 1"},
            {"id": "PICK_2", "type": "PICK", "x": 19.0, "y": 2.0, "label": "Pick Bay 2"},
            {"id": "PICK_3", "type": "PICK", "x": 27.0, "y": 2.0, "label": "Pick Bay 3"},
            {"id": "DROP_1", "type": "DROP", "x": 11.0, "y": 22.0, "label": "Outbound Drop 1"},
            {"id": "DROP_2", "type": "DROP", "x": 19.0, "y": 22.0, "label": "Outbound Drop 2"},
            {"id": "DROP_3", "type": "DROP", "x": 27.0, "y": 22.0, "label": "Outbound Drop 3"},
        ],
        "dynamic_obstacles": []
    },
    "robots": {},
    "network_stats": {
        "packet_loss_rate": 0.0,
        "p2p_packets_sec": 30,
        "active_mesh_peers": 3,
        "total_collisions": 0,
        "conflicts_resolved": 14,
        "makespan_reduction_pct": 26.4
    },
    "events": []
}

class ObstacleCommand(BaseModel):
    x: float
    y: float
    action: str = "add" # "add" or "clear"
    description: str = "Fallen Pallet"

class NetworkConfig(BaseModel):
    packet_loss_rate: float # 0.0 to 0.5

@app.get("/api/warehouse")
async def get_warehouse_layout():
    return current_fleet_state["warehouse"]

@app.post("/api/obstacle")
async def handle_obstacle(obs: ObstacleCommand):
    dyn_obs = current_fleet_state["warehouse"]["dynamic_obstacles"]
    if obs.action == "clear":
        dyn_obs.clear()
        event_msg = {
            "timestamp": "JUST NOW",
            "type": "OBSTACLE_CLEARED",
            "text": "All dynamic aisle obstacles cleared by operator"
        }
    else:
        new_obs = {"id": f"OBS_{len(dyn_obs)+1}", "x": round(obs.x, 1), "y": round(obs.y, 1), "desc": obs.description}
        dyn_obs.append(new_obs)
        event_msg = {
            "timestamp": "JUST NOW",
            "type": "OBSTACLE_DETECTED",
            "text": f"Dynamic blockage reported at ({new_obs['x']}, {new_obs['y']}). Gossip broadcast initiated."
        }
    
    current_fleet_state["events"].insert(0, event_msg)
    if len(current_fleet_state["events"]) > 25:
        current_fleet_state["events"].pop()
    
    await broadcast_state()
    return {"status": "ok", "obstacles": dyn_obs}

@app.post("/api/network")
async def set_network_sim(config: NetworkConfig):
    current_fleet_state["network_stats"]["packet_loss_rate"] = max(0.0, min(0.6, config.packet_loss_rate))
    event_msg = {
        "timestamp": "JUST NOW",
        "type": "NET_CONFIG",
        "text": f"P2P Network degradation set to {int(config.packet_loss_rate*100)}% packet loss."
    }
    current_fleet_state["events"].insert(0, event_msg)
    await broadcast_state()
    return {"status": "ok", "packet_loss": current_fleet_state["network_stats"]["packet_loss_rate"]}

async def broadcast_state():
    if not connected_clients:
        return
    payload = json.dumps({
        "type": "FLEET_UPDATE",
        "data": current_fleet_state
    })
    disconnected = set()
    for client in connected_clients:
        try:
            await client.send_text(payload)
        except Exception:
            disconnected.add(client)
    connected_clients.difference_update(disconnected)

@app.get("/api/fleet_state")
async def get_fleet_state():
    return current_fleet_state

@app.websocket("/ws/telemetry")
async def websocket_telemetry_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    logger.info(f"New spectator dashboard connected. Total spectators: {len(connected_clients)}")
    
    try:
        init_payload = json.dumps({
            "type": "INIT_STATE",
            "data": current_fleet_state
        })
        await websocket.send_text(init_payload)
        
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)
            if msg.get("type") == "ping":
                await websocket.send_text(json.dumps({"type": "pong"}))
                continue
            if msg.get("action") == "toggle_obstacle":
                x = msg.get("x", 18.0)
                y = msg.get("y", 11.0)
                obs_list = current_fleet_state["warehouse"]["dynamic_obstacles"]
                if obs_list:
                    obs_list.clear()
                    current_fleet_state["events"].insert(0, {
                        "timestamp": "JUST NOW",
                        "type": "OBSTACLE_CLEARED",
                        "text": "Aisle blockage removed. D* Lite restored shortest paths."
                    })
                else:
                    obs_list.append({"id": "OBS_1", "x": x, "y": y, "desc": "Blocked Aisle Pallet"})
                    current_fleet_state["events"].insert(0, {
                        "timestamp": "JUST NOW",
                        "type": "OBSTACLE_DETECTED",
                        "text": f"Aisle blockage dropped at ({x}, {y}). D* Lite replanned routes."
                    })
                await broadcast_state()
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        logger.info(f"Spectator disconnected. Remaining: {len(connected_clients)}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        if websocket in connected_clients:
            connected_clients.remove(websocket)

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def root():
    return FileResponse(os.path.join(static_dir, "index.html"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)
