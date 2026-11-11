# J04-L02-V01 — build brief: animated views of the leg and of Mack walking (kinematic illustration)

Quality bar: beyond-Apple quality — the machine notices, the human never checks; one plain
sentence at the moment it is needed; state visible on the surface; nothing superfluous.
Design principle served: make the interface truthful. Every frame says on its own face that it
is a kinematic illustration, and the report states what was and was not checked.

complexity: complex — inverse kinematics, mesh export, a WebGL animation and a frame-capture
path in one build; still a settled brief with no open ruling. If you meet a decision this brief
does not settle, stop and return it under OPEN; do not decide it.

## What you build

1. `hardware/joints/cad/leg_animation.py` — a generator run with
   `runtime/cad/venv/bin/python hardware/joints/cad/leg_animation.py` (Python 3.12, build123d
   0.12.0, Pillow 13; no pip, no network). It imports `leg_packaging.py` (read it first; reuse
   `read_parameters`, `Model`, its frames `body`, `carrier`, `upper`, `lower`, its `chain` and
   its tessellation/export conventions), builds placement A with the direct knee from
   `hardware/joints/cad/j04-l02.candidate-A-under.json` (do not change that file or
   `leg_packaging.py`), and writes into `hardware/joints/cad/exports/l02-animation/`:
   - `animation.html` — one self-contained offline page (no external script, font or fetch),
     derived from `hardware/joints/cad/leg-viewer-template.html` (reuse its look, shader, camera
     and `poseVertex` approach; read it first).
   - `gait-check.json` — the report in §5.
2. `hardware/joints/cad/render_frames.py` — turns a browser DOM dump into image files (§4).
3. A hand-back as your final message (§6).

Nothing else changes. No file outside `hardware/joints/cad/` is written.

## 1. Geometry in the page

- **Prototype** (`look: "prototype"`): the front-left leg's solids exactly as `Model.build()`
  makes them (carrier, links, three benchmark actuator blocks, foot, transmission envelopes if
  any), the cradle plate and the body box, each mesh tagged with its frame and colour. Leave out
  the frozen envelopes of the three other legs: the page makes the other three legs itself by
  mirroring the front-left meshes (front-right: mirror Y; rear-left: mirror X; rear-right: both),
  exactly as the generator's static neighbours are mirrored (read how `build()` places them and
  match it; fix triangle winding or disable culling for mirrored instances).
- **Concept** (`look: "concept"`): appearance only, same hip points, axes and link lengths, so
  the same joint angles drive it. Build simple build123d solids in this generator:
  body = the 80 x 91 x 112 mm envelope as a rounded shell (3 mm edge fillets where build123d
  allows, else plain), warm beige; on the front face (+X) a recessed dark screen rectangle about
  52 wide x 40 tall centred high, and a thin horizontal slot line below it; no logo, no face, no
  text. A 6 mm skirt under the body hides the hip cases. Each leg: a round cap (cylinder along
  the joint axis, radius 9) at hip swing and knee, upper and lower links as slim rounded bars
  (14 x 8 section) between the caps, a dark rounded foot pad. Same frames as the prototype.
  Colours: beige body, slightly darker links, slate caps, near-black feet and screen.
- The page embeds `P1`, `P2`, `P3`, the foot point at the neutral pose, the stance angles
  (12, -35, 70) and the sweep limits from the parameter file, read through `leg_packaging`.

## 2. Motion: computed from the frame index only (no wall clock in the maths)

Body frame as in the model: +X forward, +Y left, +Z up; angles in degrees; a = hip spread about
X at P1, b = hip swing about Y at P2, c = knee about Y at P3 (same order as `poseVertex`).
Write the forward chain once in JavaScript and once in Python (the Python one must reproduce
`Model.chain` to 1e-6 mm on ten random poses; assert it).

Inverse kinematics: for a foot target in the leg's own (unmirrored front-left) frame, solve
a, b, c numerically (damped least squares from the previous frame's answer, starting at
stance), tolerance 0.05 mm. Mirrored legs solve in the mirrored frame and reuse the same solver.

Four scenes, each a loop whose last frame joins its first:
- `leg` — one front-left leg under a faint body outline, prototype look. Four equal parts:
  hip spread sweeps stance±15 and back; hip swing sweeps stance±25 and back; knee sweeps
  40 to 100 and back; then one step (the foot path of the walk below). An on-canvas label names
  the moving joint: "J1 hip spread", "J2 hip swing", "J3 knee", "One step".
- `overview` — prototype look, four legs at stance, camera orbits 360 degrees once while the
  body lowers 15 mm and rises again (all four feet fixed on the ground, solved by IK).
- `walk-prototype` — prototype look. `walk-concept` — concept look. Same gait:
  a crawl, one foot in the air at a time, order rear-left, front-left, rear-right, front-right,
  phase offsets 0, 0.25, 0.5, 0.75; swing takes 0.2 of the cycle, stance 0.8. In the body frame
  each stance foot moves straight back along X at constant speed over a stride of 24 mm centred
  on its stance position; in swing it returns forward with a smooth lift of 10 mm
  (lift = 10·sin²(π·s), x eased with (1−cos(π·s))/2). The body shifts sideways by up to 5 mm,
  smoothly, away from the leg in swing. The ground is a grid that scrolls backward at body
  speed so stance feet stay on fixed grid points; the camera stays with the body, three-quarter
  front view, slow 10 degree yaw drift. If any joint leaves the parameter file's sweep range,
  shrink the stride in 2 mm steps until it does not, and record the stride used.

Normal mode: play/pause, a scene picker (four buttons), a look toggle on the walk scenes,
drag to rotate, 30 frames per second from `requestAnimationFrame`, phase from an integer frame
counter. Console clean.

## 3. What every frame must say

Drawn INTO the frame (composite the WebGL canvas onto a 2D canvas, then draw text; use
`preserveDrawingBuffer: true`), so it survives export:
- top left, small caps: `M.A.C. MODEL 04 · J04-L02 · DESIGN STUDY`
- top left under it, the scene title: "How one leg moves" / "Proposed layout, four legs" /
  "First prototype layout: walk cycle" / "Final-design concept: walk cycle"
- bottom left, always: `Kinematic animation from CAD. No physics. Nothing is built or tested yet.`
- prototype scenes add: `Benchmark actuator blocks, not selected parts.`
- concept scene adds: `Appearance concept only.`
Text in the page's existing type and colours; legible at 800 x 600.

## 4. Capture path (the browser runs outside your sandbox; you cannot run it)

`animation.html?capture=<scene>&frames=<N>&w=<W>&h=<H>` (defaults 60, 800, 600): with no
`requestAnimationFrame` and no timers beyond one `setTimeout(…,0)`, render frames 0..N−1 of
one loop synchronously, push each composited frame's `toDataURL('image/png')` into an array,
write `JSON.stringify({scene, frames:N, w, h, fps:15, images:[…]})` into
`<script type="application/json" id="capture-frames">`, then set `document.title` to
`CAPTURE DONE <scene> <N>`. On any error set the title to `CAPTURE ERROR <message>`.

`render_frames.py <dump.html> --out <folder>`: reads that script element from a DOM dump,
decodes the PNGs with Pillow and writes `<scene>.gif` (looping, 15 fps, adaptive palette),
`<scene>.webp` (animated, looping) and `<scene>-poster.png` (frame 0); prints one line per file
with its size; exits 1 with a plain reason if the element is missing or the title says ERROR.
Include `--selftest`: builds a three-frame fake dump in a temp folder and checks all three
outputs open and have the right frame count. Run the selftest.

## 5. `gait-check.json` (computed in Python, same maths as the page)

For each scene over 60 frames and each leg: maximum IK position error (mm); minimum and maximum
of a, b, c; whether all stay inside the sweep ranges; for the walk, stride used, lift, and the
maximum slip of any stance foot against the ground frame (mm; must be under 0.2); minimum foot
height of a stance foot against the ground plane (must be within 0.2 of 0); foot-centre track
width. Top-level `not_checked`: `["interference between parts in motion", "static stability
or centre of mass", "joint torque or speed", "any load"]`, and `known_from_J04-L02-D01`:
`"the packaged leg has named overlaps in its hinge frames at sampled poses; this animation does
not resolve them"`. Include sha256 of the parameter file, both scripts and `animation.html`.
The generator exits non-zero if a `must` fails.

## 6. Hand-back (your final message)

`STATE:` BUILT or STOPPED · files written with sizes · the gait-check headline numbers (stride
used, max IK error, max slip, joint ranges against limits) · the selftest result · what you
could not check (the page was not opened in a browser by you: say so) · `OPEN:` decisions you
met, or none · exact capture URL examples. End with `ANIMATION BUILD DONE`.
