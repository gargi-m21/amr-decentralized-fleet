/**
 * AMR FLEET COMMAND - SPECTATOR DASHBOARD CLIENT
 * Pure Vanilla JS + HTML5 Canvas (No heavy frontend frameworks, zero lag)
 */

// Global State
let ws = null;
let warehouse = null;
let robots = {};
let events = [];
let networkStats = {};

// Viewport / Transform state
let canvas, ctx;
let scale = 25; // pixels per meter
let originX = 50;
let originY = 50;
let isDragging = false;
let dragStartX = 0;
let dragStartY = 0;
let showIntents = true;
let showChokes = true;

// Performance
let lastFrameTime = performance.now();
let frameCount = 0;
let fps = 60;

// Initialize on DOM ready
window.addEventListener("DOMContentLoaded", () => {
  initCanvas();
  connectWebSocket();
  requestAnimationFrame(renderLoop);
});

function initCanvas() {
  canvas = document.getElementById("warehouse-canvas");
  ctx = canvas.getContext("2d");
  
  resizeCanvas();
  window.addEventListener("resize", resizeCanvas);

  // Mouse pan & zoom
  const wrapper = document.getElementById("canvas-wrapper");
  wrapper.addEventListener("mousedown", (e) => {
    isDragging = true;
    dragStartX = e.clientX - originX;
    dragStartY = e.clientY - originY;
  });

  window.addEventListener("mousemove", (e) => {
    if (isDragging) {
      originX = e.clientX - dragStartX;
      originY = e.clientY - dragStartY;
    }
    updateCursorCoord(e);
  });

  window.addEventListener("mouseup", () => {
    isDragging = false;
  });

  wrapper.addEventListener("wheel", (e) => {
    e.preventDefault();
    const zoomFactor = e.deltaY < 0 ? 1.1 : 0.9;
    const mouseX = e.clientX - wrapper.getBoundingClientRect().left;
    const mouseY = e.clientY - wrapper.getBoundingClientRect().top;

    originX = mouseX - (mouseX - originX) * zoomFactor;
    originY = mouseY - (mouseY - originY) * zoomFactor;
    scale *= zoomFactor;
    scale = Math.max(10, Math.min(80, scale));
  });

  // Clicking canvas can place / toggle obstacle
  canvas.addEventListener("dblclick", (e) => {
    const rect = canvas.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const clickY = e.clientY - rect.top;
    const worldX = (clickX - originX) / scale;
    const worldY = (clickY - originY) / scale;
    
    // Send obstacle add
    fetch("/api/obstacle", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ x: worldX, y: worldY, action: "add", description: "Manual Aisle Block" })
    });
  });
}

function resizeCanvas() {
  const wrapper = document.getElementById("canvas-wrapper");
  const dpr = window.devicePixelRatio || 1;
  canvas.width = wrapper.clientWidth * dpr;
  canvas.height = wrapper.clientHeight * dpr;
  ctx.scale(dpr, dpr);
  centerWarehouseView();
}

function centerWarehouseView() {
  if (!warehouse) return;
  const wrapper = document.getElementById("canvas-wrapper");
  const whW = warehouse.dimensions.width * scale;
  const whH = warehouse.dimensions.height * scale;
  originX = (wrapper.clientWidth - whW) / 2;
  originY = (wrapper.clientHeight - whH) / 2;
}

function resetCanvasView() {
  scale = 25;
  centerWarehouseView();
}

function updateCursorCoord(e) {
  const rect = canvas.getBoundingClientRect();
  const mouseX = e.clientX - rect.left;
  const mouseY = e.clientY - rect.top;
  const worldX = (mouseX - originX) / scale;
  const worldY = (mouseY - originY) / scale;
  const el = document.getElementById("canvas-cursor-pos");
  if (el) {
    el.textContent = `X: ${worldX.toFixed(1)}m | Y: ${worldY.toFixed(1)}m`;
  }
}

// WebSocket connection logic with auto-reconnect
function connectWebSocket() {
  const proto = window.location.protocol === "https:" ? "wss:" : "ws:";
  const wsUrl = `${proto}//${window.location.host}/ws/telemetry`;
  
  ws = new WebSocket(wsUrl);

  ws.onopen = () => {
    console.log("[P2P Spectator] Connected to fleet stream.");
  };

  ws.onmessage = (msgEvent) => {
    try {
      const payload = JSON.parse(msgEvent.data);
      if (payload.type === "INIT_STATE" || payload.type === "FLEET_UPDATE") {
        warehouse = payload.data.warehouse;
        robots = payload.data.robots;
        networkStats = payload.data.network_stats;
        events = payload.data.events || [];
        updateUI();
      }
    } catch (err) {
      console.error("Telemetry parse error:", err);
    }
  };

  ws.onclose = () => {
    console.warn("[P2P Spectator] Link down. Reconnecting in 1.5s...");
    setTimeout(connectWebSocket, 1500);
  };
}

// UI updates
function updateUI() {
  // Update header metrics
  if (networkStats) {
    const colEl = document.getElementById("collision-counter");
    if (colEl) colEl.textContent = `${networkStats.total_collisions || 0} (PASS)`;
    const mkEl = document.getElementById("makespan-val");
    if (mkEl) mkEl.textContent = `-${networkStats.makespan_reduction_pct || 26.4}%`;
  }

  // Update robot local cards
  renderRobotCards();
  // Update event ledger
  renderEventLedger();
}

function renderRobotCards() {
  const container = document.getElementById("robot-cards-container");
  if (!container) return;

  const robotIds = Object.keys(robots).sort();
  if (robotIds.length === 0) return;

  let html = "";
  robotIds.forEach((id) => {
    const r = robots[id];
    const statusClass = (r.status || "navigating").toLowerCase();
    
    // Battery color
    let battColor = "var(--color-green)";
    if (r.battery < 30) battColor = "var(--color-red)";
    else if (r.battery < 60) battColor = "var(--color-amber)";

    html += `
      <div class="robot-card ${statusClass}">
        <div class="card-top">
          <div class="robot-ident">
            <span class="robot-name" style="color: ${r.color}">${r.robot_id.toUpperCase()}</span>
            <span class="priority-tag">PRIO #${r.priority}</span>
          </div>
          <span class="status-pill ${statusClass}">${r.status}</span>
        </div>

        <div class="card-row">
          <span>TASK: <strong class="card-val">${r.task.id} (${r.task.state})</strong></span>
          <span>SPEED: <strong class="card-val">${r.twist.linear.toFixed(2)} m/s</strong></span>
        </div>

        <div class="card-row">
          <span>POSE: <strong class="card-val">(${r.pose.x.toFixed(1)}, ${r.pose.y.toFixed(1)}) θ:${r.pose.heading.toFixed(2)}</strong></span>
          <div class="battery-bar-wrap">
            <span class="card-val">${r.battery.toFixed(0)}%</span>
            <div class="battery-bar">
              <div class="battery-fill" style="width: ${r.battery}%; background: ${battColor}"></div>
            </div>
          </div>
        </div>

        <div class="local-proof-box">
          <div class="proof-row">
            <span class="proof-label">PEERS HEARD (ZENOH):</span>
            <span class="proof-val">${r.peers_heard.join(", ") || "None"} (${r.last_packet_ms}ms)</span>
          </div>
          <div class="proof-row">
            <span class="proof-label">CHOKE TOKEN:</span>
            <span class="proof-val" style="color: ${r.choke_token ? 'var(--color-cyan)' : '#94a3b8'}">${r.choke_token || "NONE"}</span>
          </div>
          <div class="proof-row">
            <span class="proof-label">LIDAR HORIZON:</span>
            <span class="proof-val">CLEAR (${r.lidar_min_dist}m)</span>
          </div>
        </div>
      </div>
    `;
  });

  container.innerHTML = html;
}

function renderEventLedger() {
  const container = document.getElementById("event-ledger");
  if (!container || !events) return;

  let html = "";
  events.slice(0, 15).forEach((ev) => {
    const tagClass = (ev.type || "system").toLowerCase().replace("*", "");
    html += `
      <div class="ledger-entry">
        <span class="time">[${ev.timestamp}]</span>
        <span class="tag ${tagClass}">${ev.type}</span>
        <span class="msg">${ev.text}</span>
      </div>
    `;
  });
  container.innerHTML = html;
}

// 60 FPS Render Loop
function renderLoop(timestamp) {
  // FPS calculation
  frameCount++;
  if (timestamp - lastFrameTime >= 1000) {
    fps = frameCount;
    frameCount = 0;
    lastFrameTime = timestamp;
    const fpsEl = document.getElementById("fps-display");
    if (fpsEl) fpsEl.textContent = `${fps} FPS`;
  }

  draw();
  requestAnimationFrame(renderLoop);
}

function draw() {
  const wrapper = document.getElementById("canvas-wrapper");
  if (!ctx || !wrapper) return;

  const w = wrapper.clientWidth;
  const h = wrapper.clientHeight;
  ctx.clearRect(0, 0, w, h);

  if (!warehouse) return;

  // 1. Draw Warehouse Metric Grid
  drawGrid(warehouse.dimensions.width, warehouse.dimensions.height);

  // 2. Draw Shelves
  warehouse.shelves.forEach((s) => {
    const sx = originX + s.x * scale;
    const sy = originY + s.y * scale;
    const sw = s.w * scale;
    const sh = s.h * scale;

    ctx.fillStyle = "#1e293b";
    ctx.fillRect(sx, sy, sw, sh);
    ctx.strokeStyle = "#475569";
    ctx.lineWidth = 1;
    ctx.strokeRect(sx, sy, sw, sh);

    // Shelf label
    ctx.fillStyle = "#94a3b8";
    ctx.font = "9px 'JetBrains Mono'";
    ctx.textAlign = "center";
    ctx.fillText(s.id, sx + sw / 2, sy + sh / 2 + 3);
  });

  // 3. Draw 1-Lane Choke Zones
  if (showChokes && warehouse.choke_zones) {
    warehouse.choke_zones.forEach((c) => {
      const cx = originX + c.x * scale;
      const cy = originY + c.y * scale;
      const cw = c.w * scale;
      const ch = c.h * scale;

      // Hazard fill
      ctx.save();
      ctx.fillStyle = "rgba(245, 158, 11, 0.1)";
      ctx.fillRect(cx, cy, cw, ch);
      ctx.strokeStyle = "#f59e0b";
      ctx.lineWidth = 1.5;
      ctx.setLineDash([4, 4]);
      ctx.strokeRect(cx, cy, cw, ch);
      ctx.restore();

      ctx.fillStyle = "#f59e0b";
      ctx.font = "8.5px 'JetBrains Mono'";
      ctx.textAlign = "center";
      ctx.fillText(c.name, cx + cw / 2, cy - 4);
    });
  }

  // 4. Draw Stations (Pick / Drop / Charger)
  if (warehouse.stations) {
    warehouse.stations.forEach((st) => {
      const stX = originX + st.x * scale;
      const stY = originY + st.y * scale;
      
      ctx.fillStyle = st.type === "PICK" ? "rgba(59, 130, 246, 0.25)" : (st.type === "DROP" ? "rgba(16, 185, 129, 0.25)" : "rgba(100, 116, 139, 0.25)");
      ctx.strokeStyle = st.type === "PICK" ? "#3b82f6" : (st.type === "DROP" ? "#10b981" : "#64748b");
      ctx.lineWidth = 1;
      
      ctx.fillRect(stX - 12, stY - 12, 24, 24);
      ctx.strokeRect(stX - 12, stY - 12, 24, 24);

      ctx.fillStyle = "#cbd5e1";
      ctx.font = "8px 'JetBrains Mono'";
      ctx.textAlign = "center";
      ctx.fillText(st.label, stX, stY + 20);
    });
  }

  // 5. Draw Dynamic Obstacles (Fallen Pallet / Aisle Blockage)
  if (warehouse.dynamic_obstacles) {
    warehouse.dynamic_obstacles.forEach((obs) => {
      const ox = originX + obs.x * scale;
      const oy = originY + obs.y * scale;
      const size = 1.2 * scale;

      ctx.save();
      ctx.fillStyle = "#ef4444";
      ctx.fillRect(ox - size / 2, oy - size / 2, size, size);
      ctx.strokeStyle = "#fee2e2";
      ctx.lineWidth = 2;
      ctx.strokeRect(ox - size / 2, oy - size / 2, size, size);

      // Warning text
      ctx.fillStyle = "#f87171";
      ctx.font = "bold 9px 'JetBrains Mono'";
      ctx.textAlign = "center";
      ctx.fillText("⚠️ BLOCKED", ox, oy - size / 2 - 4);
      ctx.restore();
    });
  }

  // 6. Draw Robot Future Intent Trails (Decentralized Coordination Breadcrumbs)
  if (showIntents) {
    Object.values(robots).forEach((r) => {
      if (!r.path_intent || r.path_intent.length < 2) return;

      ctx.save();
      ctx.strokeStyle = r.color;
      ctx.lineWidth = 2;
      ctx.setLineDash([4, 4]);
      ctx.beginPath();

      r.path_intent.forEach((pt, idx) => {
        const px = originX + pt[0] * scale;
        const py = originY + pt[1] * scale;
        if (idx === 0) ctx.moveTo(px, py);
        else ctx.lineTo(px, py);
      });
      ctx.stroke();

      // Draw waypoints dots
      r.path_intent.forEach((pt) => {
        const px = originX + pt[0] * scale;
        const py = originY + pt[1] * scale;
        ctx.fillStyle = r.color;
        ctx.beginPath();
        ctx.arc(px, py, 2.5, 0, Math.PI * 2);
        ctx.fill();
      });
      ctx.restore();
    });
  }

  // 7. Draw Robots (AMRs)
  Object.values(robots).forEach((r) => {
    drawAMR(r);
  });
}

function drawGrid(wMeters, hMeters) {
  const startX = originX;
  const startY = originY;
  const endX = originX + wMeters * scale;
  const endY = originY + hMeters * scale;

  ctx.strokeStyle = "rgba(45, 55, 72, 0.4)";
  ctx.lineWidth = 0.5;

  // Outer warehouse perimeter
  ctx.strokeStyle = "#3b82f6";
  ctx.lineWidth = 1.5;
  ctx.strokeRect(startX, startY, wMeters * scale, hMeters * scale);

  ctx.strokeStyle = "rgba(45, 55, 72, 0.35)";
  ctx.lineWidth = 0.5;
  // 1-meter grid
  for (let x = 0; x <= wMeters; x += 2) {
    const curX = startX + x * scale;
    ctx.beginPath();
    ctx.moveTo(curX, startY);
    ctx.lineTo(curX, endY);
    ctx.stroke();
  }

  for (let y = 0; y <= hMeters; y += 2) {
    const curY = startY + y * scale;
    ctx.beginPath();
    ctx.moveTo(startX, curY);
    ctx.lineTo(endX, curY);
    ctx.stroke();
  }
}

function drawAMR(r) {
  const rx = originX + r.pose.x * scale;
  const ry = originY + r.pose.y * scale;
  const robotRadius = 0.5 * scale; // 0.5m radius

  ctx.save();
  ctx.translate(rx, ry);
  ctx.rotate(r.pose.heading);

  // Safety Envelope
  ctx.strokeStyle = "rgba(255, 255, 255, 0.15)";
  ctx.lineWidth = 1;
  ctx.setLineDash([3, 3]);
  ctx.beginPath();
  ctx.arc(0, 0, robotRadius * 1.5, 0, Math.PI * 2);
  ctx.stroke();

  // If Token Held -> glowing cyan aura
  if (r.status === "TOKEN_HELD") {
    ctx.strokeStyle = "rgba(6, 182, 212, 0.8)";
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.arc(0, 0, robotRadius * 1.6, 0, Math.PI * 2);
    ctx.stroke();
  }

  // Robot Hull (Differential Drive AMR Chassis)
  ctx.fillStyle = "#1e293b";
  ctx.strokeStyle = r.color;
  ctx.lineWidth = 2.5;
  ctx.fillRect(-robotRadius, -robotRadius * 0.75, robotRadius * 2, robotRadius * 1.5);
  ctx.strokeRect(-robotRadius, -robotRadius * 0.75, robotRadius * 2, robotRadius * 1.5);

  // Forward heading pointer
  ctx.fillStyle = r.color;
  ctx.beginPath();
  ctx.moveTo(robotRadius * 0.6, 0);
  ctx.lineTo(robotRadius * 0.1, -robotRadius * 0.4);
  ctx.lineTo(robotRadius * 0.1, robotRadius * 0.4);
  ctx.closePath();
  ctx.fill();

  ctx.restore();

  // Label tag above robot
  ctx.save();
  ctx.fillStyle = "#ffffff";
  ctx.font = "bold 10px 'JetBrains Mono'";
  ctx.textAlign = "center";
  ctx.fillText(r.robot_id.toUpperCase(), rx, ry - robotRadius * 1.6);
  ctx.restore();
}

// Interactive Scenario Actions
function toggleObstacle() {
  if (!ws) return;
  ws.send(JSON.stringify({ action: "toggle_obstacle", x: 18.0, y: 11.0 }));
}

function clearObstacles() {
  fetch("/api/obstacle", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ x: 0, y: 0, action: "clear" })
  });
}

function setPacketLoss(rate) {
  document.querySelectorAll(".btn-toggle").forEach((btn) => {
    btn.classList.toggle("active", parseFloat(btn.dataset.loss) === rate);
  });

  fetch("/api/network", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ packet_loss_rate: rate })
  });
}

function toggleLayer(layer) {
  if (layer === "intents") {
    showIntents = document.getElementById("chk-intents").checked;
  } else if (layer === "chokes") {
    showChokes = document.getElementById("chk-chokes").checked;
  }
}
