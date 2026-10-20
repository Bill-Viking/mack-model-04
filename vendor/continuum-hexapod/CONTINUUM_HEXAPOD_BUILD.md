# CONTINUUM HEXAPOD — BUILD & IMPLEMENTATION PLAN
Platform: Freenove Big Hexapod (FNK0052) + Raspberry Pi 5. Architecture: Brain (Claude API) / Spine (Pi daemon) / Hand (servo layer) / Scribe+Continuum (memory).

**PROJECT STATUS (2026-07-17):** Hexapod kit purchased; supporting electronics (Pi 5, batteries, charger, SD) selected — see Phase 0 table. Next milestone: hardware arrives → flash Pi (Phase 2 software-first, before assembly) → servo calibration → assembly. Software: Phases 3–5 implemented against MockHand (Spine daemon, Brain loop w/ Claude API, Continuum store + consolidation + place-estimation v1); real Freenove adapter pre-written from vendor source (CALIBRATE tags pending hardware); SKILL.md contract prompt done; deployment prep in ops/ (systemd unit, deploy/estop scripts, Pi provisioning checklist) and operator CLI tools/hexctl.py — see per-phase status lines. Dev env: `.venv` (Python 3.12) at repo root; run tests `.venv/bin/python -m pytest tests/`; run Spine `.venv/bin/python -m spine.spine`. Owner: Bill. This doc is the single source of truth for the project; update statuses in place.

---

## Phase 0 — Bill of materials (DECIDED — as of 2026-07-17)
Status: **hexapod kit PURCHASED.** Remaining items below with chosen links.

| Item | Choice | Link | Status |
|---|---|---|---|
| Platform | Freenove Big Hexapod FNK0052 (18 leg servos + pan/tilt head, control shield, camera, ultrasonic; NO Pi, NO batteries included) | amazon.com/dp/B08M5DXS2P or store.freenove.com/products/fnk0052 | ✅ purchased |
| Compute | Raspberry Pi 5 4GB Starter Kit (board + official 27W PSU + case w/ fan + 64GB card + reader) | amazon.com/dp/B0CRPF3BX3 | pending |
| — or à la carte | Pi 5 board + official Active Cooler (amazon.com/dp/B0CLXZBR5P) + official 27W USB-C PSU (amazon.com/dp/B0D3MFLNC1) | | alt |
| Batteries | 4× Samsung 25R 18650 (2500mAh, 20A, flat-top, unprotected) — specialty vendor, NOT Amazon (counterfeit risk) | 18650batterystore.com/products/samsung-25r-18650 | pending |
| — or | Molicel P28A (2800mAh, 35A) — P26A is superseded | imrbatteries.com flat-top collection | alt |
| Charger | XTAR VC2SL (USB-C, LCD, internal-resistance readout) | amazon.com/dp/B09WRDVS34 | pending |
| microSD | Samsung EVO Select 128GB (A2/U3/V30 — note: 64GB variant is only A1, don't substitute down) | amazon.com/dp/B09B1JFY24 | pending |

BOM notes:
- Bundle case: NOT used on the robot — the Freenove shield needs the bare 40-pin GPIO header. Case is bench-only. Verify Active Cooler clearance under the shield against the Freenove manual before attaching.
- Battery spec is strict: **flat-top, unprotected, high-discharge (10A+ CDR), 65mm class.** Button-top/protected cells may not fit the holder; low-drain cells brown out the Pi under 18-servo load (looks like a software crash — check battery before debugging code). Cross-check cell length vs the battery page in the Freenove tutorial PDF before ordering.
- 4 cells = two pairs for hot-swap; sessions run ~20–40 min.
- Official 27W PSU is for bench development (Pi on wall power); battery rail powers servos via shield in all cases — never from Pi 5V.
- Nothing else needed: no motor drivers, servo boards, extra camera, jumper wires, or soldering. Kit is solder-free.

## Phase 1 — Physical build (the "hardwiring")
Good news: there is no custom wiring. The kit's control shield mounts on the Pi's 40-pin GPIO header and everything plugs into labeled connectors.

1. **Flash the Pi first, build second.** You want the calibration script working before legs go on.
2. **Servo zeroing is the critical step.** Before attaching any leg linkage, power each servo and command it to its center position (Freenove's calibration routine does this), THEN attach the horn/linkage in the neutral pose shown in the manual. A leg assembled off-zero will bind or fight its neighbors forever. Do not skip; do not eyeball.
3. Servo cables route to numbered 3-pin headers on the shield — the manual maps leg/joint → header number. Label as you go (masking tape); you will thank yourself during debugging.
4. Camera ribbon → Pi CSI port (contacts facing per manual; Pi 5 uses the smaller connector — kit includes/documents the adapter cable).
5. Ultrasonic module → dedicated shield header. Battery holder → shield power input. **Servos are powered from the battery rail via the shield, never from the Pi's 5V.** The shield handles this; just don't "improve" it.
6. Mind 18650 polarity in the holder. Reversed cells kill boards instantly.
7. **Build a test stand**: any box that lifts the body so all six legs hang free. Every new gait or Spine change gets tested on the stand before floor contact. This is your hardware-in-the-loop rig.

## Development workflow (applies to all phases)
- **Headless Pi.** Flash SD with Raspberry Pi Imager on Bill's Mac; pre-configure Wi-Fi, hostname `hexapod`, SSH user, and public key in Imager before first boot. No monitor/keyboard ever. All access: `ssh <user>@hexapod.local` from the Mac. (Bill's Mac shell is tcsh — use full paths for Homebrew tools on the Mac side; Pi side is stock bash.)
- **Editing.** VS Code Remote-SSH or Claude Code. Claude Code may run on the Mac (deploying over SSH) or on the Pi via SSH session for hardware-in-the-loop iteration. This doc is the opening context for every session.
- **Version control.** One git repo (`continuum-hexapod/`) holding hand.py adapter, spine/, brain/, continuum/, limits.yaml, SKILL.md prompts, this doc. Pi and Mac both clone; deploy = git pull on the Pi. Vendor repo stays separate and untouched. **Commit at the end of every session** (message discipline loose, but commit) — this doc's status lines plus git history are how any future session reconstructs exactly where the project stands. Code sessions: check `git log` on start, commit before ending.
- **Brain placement.** During development, brain.py runs on the Mac (fast iteration, logs local, API key stays off-robot) and talks to the Spine over Wi-Fi. Once stable, same file runs on the Pi (config change only: SPINE host localhost). E-stop and reflexes are unaffected by Brain placement — they're Spine-local by design.
- **Secrets.** ANTHROPIC_API_KEY via environment/keychain only. Never committed, never in this doc, never echoed in logs.
- **Deployment.** Spine installs as a systemd unit (`continuum-spine.service`), enabled at boot — the same mechanism used to disable Freenove's server, now pointed at ours. Boot sequence: power on → Spine up, torque off, e-stop armed → waits for Brain or operator.
- **First-light test** (before anything else): SSH in, move one servo through hand.py adapter. Proves Mac → Wi-Fi → Pi → shield → servo chain end to end.

## Phase 2 — Pi bring-up
```bash
# Raspberry Pi OS (64-bit) via Raspberry Pi Imager; enable SSH + Wi-Fi in imager
sudo raspi-config       # enable I2C, camera (if not auto)
git clone https://github.com/Freenove/Freenove_Big_Hexapod_Robot_Kit_for_Raspberry_Pi
cd Freenove_Big_Hexapod_Robot_Kit_for_Raspberry_Pi
# follow their setup.py / requirements install per tutorial PDF
```
Run their stock server + phone app once. Verify: all servos respond, camera streams, ultrasonic reads, battery ADC reads. Do not build anything of ours until the vendor stack fully works — it is your known-good baseline and your Hand layer.

Key vendor files to read (names approximate; confirm in repo):
- `Control.py` — inverse kinematics + gait engine. This IS the Hand. We call it; we don't rewrite it.
- `Servo.py` / PCA9685 driver — raw PWM
- `Ultrasonic.py`, `ADC.py`, camera server — sensor access

**Vendor software policy — KEEP vs KILL:**
- KEEP (imported by Spine as a library): IK/gait engine, servo drivers, sensor classes, calibration tool
- KILL (never launched in our runtime): Freenove phone-app server, voice control, face recognition, LED shows, demo modes — all replaced by the Spine daemon; personality/voice, if any, lives in the Brain layer
- Do NOT delete the repo or fork destructively — stock app doubles as the hardware diagnostic (if our stack misbehaves, run stock app to isolate hardware vs. our code) and keeps vendor updates/calibration available
- Disable any vendor service from auto-starting on boot; only the Spine daemon autostarts

**Phase 2.5 status (2026-07-17):** vendor repo cloned to `~/Projects/Freenove_Big_Hexapod_Robot_Kit_for_Raspberry_Pi` (Mac, sibling dir — stays out of our git) and key files read: `control.py` (Control: run_gait/move_position/relax — IS the Hand), `servo.py` (PCA9685, head = channels 0/1), `ultrasonic.py` (cm, may return None), `adc.py` (`read_battery_voltage()` returns a TUPLE of two channels despite its `-> float` annotation). Real adapter **written**: `hand/freenove_hand.py` — lazy vendor imports, keeper modules only, never starts their condition_monitor thread; wiring tested against fake vendor modules (9 tests). All physical mappings tagged `CALIBRATE` pending the stand; provisioning click-by-click in `ops/PI_PROVISIONING.md`.

**Gutting procedure (Phase 2.5, after the one diagnostic session with stock app):**
1. Kill autostart: `systemctl list-units --type=service | grep -iE "freenove|hexapod|server"` → `sudo systemctl disable --now <unit>`. Also check `crontab -l`, `/etc/rc.local`, `/etc/xdg/autostart/`. Reboot; verify clean with `ps aux`.
2. Client side: never reinstall their phone/PC app. 
3. Adapter pattern: create our `hand.py` importing ONLY keeper modules (Control, Servo/PCA9685, Ultrasonic, ADC), exposing exactly the Spine primitives (walk/turn/look/posture/stop). Never import their main.py/Server.py/buzzer/LED/face modules. Do not edit vendor source — override in adapter.
4. Import side-effect audit (on the STAND): import each keeper module individually, observe physical behavior (vendor modules may init hardware on import — chirps, LED flashes, servo twitch). Suppress unwanted init in adapter.
5. Rollback: stock service remains on disk; `systemctl start <unit>` resurrects vendor robot for hardware diagnostics anytime.

## Phase 3 — Spine daemon
Status: **IMPLEMENTED against mock hand (2026-07-17)** — `spine/` (schema.py, limits.py, watchdog.py, spine.py) wired to `hand/mock_hand.py`; 40 tests green; smoke-tested live via `python -m spine.spine` + curl. NOT yet run against hardware; swap MockHand → Freenove adapter in Phase 2.5.

A single Python service on the Pi wrapping vendor code behind a validated action API. FastAPI + uvicorn, localhost only.

**Action schema (the return contract):**
```json
{
  "action": "walk | turn | look | posture | stop | idle",
  "params": {"heading_deg": 0, "steps": 4, "speed": 0.5,
              "pan_deg": 0, "tilt_deg": 0, "stance": "normal|high|low"},
  "rationale": "one sentence",
  "expected_outcome": "one sentence",
  "memory_ops": [ {"op": "upsert", "table": "objects", "data": {}} ]
}
```
Malformed or out-of-schema → reject, log, no-op. The Brain retries. Never "best effort" a motor command.

**Limit table (`limits.yaml`):**
```yaml
walk:   {steps: {max: 10}, speed: {min: 0.2, max: 0.8}}
turn:   {heading_deg: {min: -180, max: 180}}
look:   {pan_deg: {min: -80, max: 80}, tilt_deg: {min: -30, max: 60}}
battery: {cutoff_v: 6.6, warn_v: 7.0}
reflex:  {sonar_stop_cm: 12}
```

**Spine responsibilities (all local, network-independent):**
- Validate every action against schema + limits before dispatch
- Reflexes: sonar < 12cm during walk → immediate stop, report `interrupted: obstacle`
- Watchdog: no Brain contact for N seconds mid-task → posture(safe), stop
- Dead-man: physical or SSH kill switch → servo torque off
- Battery monitor: warn at 7.0V, force sit-and-refuse at 6.6V
- State endpoint: `GET /state` → commanded joint angles, last action result, sonar, battery, uptime

**Skeleton:**
```python
# spine.py
from fastapi import FastAPI
from pydantic import BaseModel
import vendor.control as hexapod   # Freenove Control.py wrapped

app = FastAPI()
LIMITS = load_yaml("limits.yaml")

class Action(BaseModel):
    action: str
    params: dict = {}
    rationale: str = ""
    expected_outcome: str = ""
    memory_ops: list = []

@app.post("/act")
def act(a: Action):
    err = validate(a, LIMITS)
    if err: return {"ok": False, "error": err}
    result = dispatch(a)            # calls hexapod gait/look primitives
    scribe.enqueue(a.memory_ops)    # memory writes go through Scribe, never direct
    return {"ok": True, "result": result}

@app.get("/state")
def state(): return sensors.snapshot()
```

## Phase 4 — Brain loop
Status: **IMPLEMENTED (2026-07-17)** — `brain/brain.py`: full tick (frame → state → recall → Claude → /act → episode log) with injectable FrameSource (StaticFrameSource for Mac dev, PiCameraFrameSource stubbed until hardware), injectable SpineClient (HTTP + in-process Local for tests), strict JSON parse (fail → no-op + retry), and episode logging through the Scribe. Contract prompt is `SKILL.md` with `{{LIMITS}}` rendered from limits.yaml at runtime — numbers live in config only. Model split DECIDED: `claude-sonnet-4-6` ticks (effort low), `claude-opus-4-8` planning, `claude-haiku-4-5` consolidation. 10 tests via fake Claude client; NOT yet run against the live API (needs ANTHROPIC_API_KEY, run `python -m brain.brain "<goal>"`).

Runs on the Pi (fine) or your Mac (easier to iterate). One tick:

```python
# brain.py
import anthropic, base64, requests
client = anthropic.Anthropic()

def tick(goal):
    frame = capture_frame_b64()                       # picamera2 → JPEG → b64
    state = requests.get(SPINE + "/state").json()
    recall = continuum.recall(state, goal)            # relevant places/objects/skills
    msg = client.messages.create(
        model="claude-sonnet-4-6",                    # sonnet for ticks; opus for planning
        max_tokens=1000,
        system=SPINE_CONTRACT_PROMPT + recall,
        messages=[{"role": "user", "content": [
            {"type": "image", "source": {"type": "base64",
              "media_type": "image/jpeg", "data": frame}},
            {"type": "text", "text": f"Goal: {goal}\nState: {state}\nRespond ONLY with action JSON."}
        ]}])
    action = parse_json_strict(msg)                   # fail → no-op + retry
    result = requests.post(SPINE + "/act", json=action).json()
    continuum.log_episode(goal, action, result)       # expected vs actual = learning signal
    return result
```
Tick policy: event-driven, not continuous. New tick on: action completed, reflex interrupt, operator command, or timeout. Target dozens of calls per session, not thousands.

## Phase 5 — Continuum store
Status: **IMPLEMENTED incl. consolidation (2026-07-17)** — `continuum/` (store.py schema per below, scribe.py sole writer w/ per-table field whitelists + dedupe + confidence rules, recall.py read-only token-overlap recall). Consolidation written (`consolidate.py`): mechanical skills-stats pass + optional cheap-model promotion pass whose proposals flow through Scribe validation like any memory_op; session summary row; run `python -m continuum.consolidate <session> [--with-model]`. Place-estimation v1 written (`place_estimate.py`: last confirmed landmark + dead reckoning + confidence decay) — not yet wired into the Brain tick.

SQLite at `~/continuum/continuum.db` (user-owned, rsync-able, MYTHOS pattern).

```sql
CREATE TABLE places   (id INTEGER PRIMARY KEY, label TEXT, descriptor TEXT,
                       links TEXT, last_seen TEXT, confidence REAL);
CREATE TABLE objects  (id INTEGER PRIMARY KEY, label TEXT, descriptor TEXT,
                       last_place INTEGER, last_seen TEXT, notes TEXT);
CREATE TABLE skills   (id INTEGER PRIMARY KEY, name TEXT, context TEXT,
                       params TEXT, success_rate REAL, uses INTEGER);
CREATE TABLE episodes (id INTEGER PRIMARY KEY, session TEXT, ts TEXT, goal TEXT,
                       action TEXT, expected TEXT, actual TEXT, surprise INTEGER);
```
- **Scribe**: sole writer. Validates memory_ops (schema, dedupe, confidence rules), commits or drops. Brain has read-only recall.
- **recall(state, goal)**: pull top-k places/objects/skills by relevance to goal + current place estimate; inject as a compact context block.
- **Consolidation** (end of session, cron or manual): cheap model call reads episodes → promotes repeated observations to places/objects, tunes skill params/success rates, prunes, writes a session summary row. The dreaming pass.

## Phase 6 — Test ladder
0. **Sim (no hardware): full stack against the virtual world** — `sim/` package, added 2026-07-17. SimHand is a third HandInterface implementation (2D apartment world: 3 rooms, doorways, colored objects; raycast sonar; battery drain; noisy motion; walls physically block). SimFrameSource renders first-person JPEG frames (crude by design — rectangles + distance shading). Run: `python -m sim.run` (Spine on :8080, drive with hexctl), `--save-frame view.jpg`, or `--brain N --goal "..."` for live Claude ticks in-process. **Sim db is separate** (`~/continuum/sim-<world>.db`) — virtual memories never mix with real recall. Policy: new Brain/Continuum changes debut in the sim, the way new gait params debut on the stand. Already paid for itself: first sim drive exposed that the sonar reflex only ran pre/post walk, so a multi-step walk crossed the whole 12 cm envelope and bumped the wall — Spine now wires its reflex into the hand's `cycle_hook` (mid-walk abort; `FreenoveHand` had the hook waiting, `SimHand` matches, regression test asserts zero collisions).
1. Stand: every action type via curl to Spine, no Brain
2. Stand: Brain loop with goal "describe what you see and look around" (look-only, no locomotion)
3. Floor, open room: "explore and map this room" — verify places table populates
4. Floor: "find the [object] and approach it"
5. Multi-session: power cycle, verify recall changes behavior (the whole point) — **provable in sim today**: `tests/test_sim.py::TestBrainInSim::test_memory_survives_across_sim_sessions` runs it in miniature (session 1 records a place, fresh stack over the same db recalls it in session 2).

## Safety invariants (non-negotiable)
- Limits + reflexes + watchdog live in Spine, never in prompts
- E-stop works with Wi-Fi down
- Scribe mediates all memory writes
- New gait/param changes debut on the stand
- Battery cutoff enforced in firmware

## Open items for the code session
- [x] Write SPINE_CONTRACT_PROMPT as SKILL.md (Bill's pattern) — done 2026-07-17; `{{LIMITS}}` renders from limits.yaml at runtime
- [x] Confirm vendor repo file names/API on clone; wrap, don't fork — done 2026-07-17; adapter written, see Phase 2.5 status
- [x] Place-estimation heuristic v1 (last confirmed landmark + dead reckoning) — done 2026-07-17 (`continuum/place_estimate.py`); wiring into Brain tick still open
- [x] Decide Opus-for-planning / Sonnet-for-ticks split — decided 2026-07-17: sonnet-4-6 ticks / opus-4-8 planning / haiku-4-5 consolidation (constants in brain.py)
- [ ] Wire PlaceEstimate into the Brain tick (confirm-on-recognition + feed as_context() into recall)
- [ ] First live-API Brain tick — now via the sim: `python -m sim.run --brain 5 --goal "explore"` (needs ANTHROPIC_API_KEY on the Mac)
- [ ] Sonar rides the pan head (real + sim): a walk with the head panned sideways is reflex-blind forward. Decide policy — e.g. Spine forces look(0,0) before walk, or reflex uses last forward-facing reading
