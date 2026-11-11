# J04-L02-V01 — animated CAD views: build report

STATE: BUILT — headless implementation and numerical checks complete. Browser acceptance remains UNRUN and belongs to the caller.

The offline page contains the four scenes, play/pause, scene picker, walk look toggle, drag/keyboard camera controls, and the synchronous DOM capture path. The prototype reuses all 25 non-neighbour source meshes, including the cradle and body. Only the body and cradle are shared; other parts are mirrored as whole posed instances across Y, X, or both, matching Model.build(). Culling is disabled for mirrored instances. The appearance concept adds a rounded hollow beige body, recessed dark screen and slot, skirt, caps, slim links and dark rounded feet on the same joint frames. It is not a fitted final design.

Every composited frame draws the design-study plate, scene title, kinematic/no-physics/no-testing statement and the relevant benchmark or appearance statement. The one-leg scene also draws the moving-joint label. These labels are part of the 2D canvas, including the capture images.

## Files written

| File (relative to hardware/joints/cad/) | Bytes |
|---|---:|
| `leg_animation.py` | 29901 |
| `render_frames.py` | 6087 |
| `exports/l02-animation/animation.html` | 706145 |
| `exports/l02-animation/gait-check.json` | 14578 |
| `briefs/J04-L02-ANIMATION-BRIEF-REPORT.md` | 7996 |

No existing tracked file changed. The packaging generator, source viewer template and placement-A JSON match HEAD byte for byte. The pre-existing untracked PNG was untouched. No commit, push, sync, heartbeat, browser or GUI action was performed. Brain freshness was not established or claimed. All task writes stayed under hardware/joints/cad/; the decoder selftest's temporary folder was created there and removed.

## Numerical result

- Placement A, direct knee; stance 12°, −35°, 70°; links 50 and 30 mm.
- Full requested stride: 24 mm; no reduction needed. Lift: 10 mm. Body speed: 30 mm per cycle. Grid spacing: 30 mm, so the scrolling ground repeats at the loop seam.
- Maximum IK error over all four 60-frame scenes: 0.000009312950 mm (required ≤0.05).
- Maximum stance-foot slip, both walks: 0.000005912465 mm (required <0.2).
- Minimum nominal stance-foot height: -0.000005326425 mm. Maximum absolute stance-height error: 0.000008691705 mm (required ≤0.2).
- Foot-centre track width in the walk: 129.773871–129.773878 mm.
- All sampled joints stay inside the parameter file's viewing/search sweeps. These are not selected actuator or controller limits.

| Joint | Range across all four 60-frame scenes, degrees | Parameter sweep, degrees |
|---|---:|---:|
| a — hip spread | -2.917828 to 26.917828 | −30 to 30 |
| b — hip swing | -59.863047 to -10.136953 | −90 to 90 |
| c — knee | 40.164343 to 100.988283 | 0 to 120 |

The JSON retains results for each rendered leg in each scene (only FL is present in the one-leg scene). The overview keeps all feet fixed while the body moves down 15 mm and back up. The crawl uses rear-left, front-left, rear-right, front-right offsets 0, 0.25, 0.5, 0.75, a 0.2 swing fraction and 0.8 stance fraction, with a smooth sideways body shift away from the swing leg. Its compensated foot targets keep ground Y fixed during the body shift. The one-leg step starts and ends at stance by starting the walking path at phase 0.6.

Ground measurement convention: the IK foot datum is the nominal prototype pad's centroid in XY and its lowest rigid-box support in Z. Ground Z is −111.788215943178 mm in the source body frame. Slip measures that centroid XY against an unwrapped ground frame, including body travel and lateral shift. It does not measure slip of a rotating contact patch. A separate headless check compared this datum with transformed CAD foot solids at ten representative poses: maximum discrepancy 0.000000000000030 mm. The concept uses the same nominal datum; its rounded foot surface is appearance only and is not a contact model.

## Checks actually run

- Generator run using runtime/cad/venv/bin/python (Python 3.12; build123d 0.12.0; Pillow 13.0.0), with a 180-second subprocess timeout. No install or network was used.
- Python forward chain agrees with Model.chain on ten seeded random poses to <1e-6 mm (reported maximum: 0 mm).
- Python gait gates pass for all four scenes over 60 frames; stride selection also checks a 240-frame walk.
- Generated page JavaScript parsed with node --check. Python versus JavaScript compared all four scenes at 60 and 240 frames: maximum joint-angle difference 1.058708676283e-11 degrees; maximum target-coordinate difference 2.842170943040e-14 mm. A boundary classification mismatch found in the first comparison was corrected by canonicalizing phase boundaries to 1e-12 in both languages; the final comparison passed.
- 240-frame crawl check: at most one swing leg, sideways shift ≤5 mm, and four-foot stance intervals.
- Capture control-flow check in Node with stub canvas/WebGL objects: each of the four scenes rendered three compositing calls, added three image entries, used one zero-delay timer, invoked no requestAnimationFrame and drew the required scope labels each time. This does not prove WebGL rendering, PNG encoding or browser behaviour.
- render_frames.py --selftest: PASS. Three-frame fake DOM decoded into a looping three-frame GIF, looping three-frame lossless WebP and one-frame PNG poster. All opened with Pillow at the expected dimensions/frame counts. Missing payload and CAPTURE ERROR title cases were refused. Printed sizes: GIF 670 bytes; WebP 306 bytes; poster 206 bytes. Temporary artifacts were removed.
- SHA256 values in gait-check.json were recomputed and matched the parameter JSON, both scripts and animation.html. Source generator and source template hashes are also recorded. Offline source check found no external script or fetch.

## Not checked

The page was not opened in a browser by this job. Actual WebGL rendering, console cleanliness, 30 fps playback performance, visual composition, label legibility, camera interactions, browser DOM dumping and the real PNG/GIF/WebP capture of these scenes are UNRUN here and belong to the caller. No GIF/WebP of the real CAD scenes is claimed delivered.

The following are expressly not checked: interference between parts in motion; static stability or centre of mass; joint torque or speed; any load. The packaged leg has named overlaps in its hinge frames at sampled poses; this animation does not resolve them. Nothing is built or physically tested. The concept's rounded shell and feet are appearance only.

OPEN: none — no new design ruling was made. The ground datum and its limitations are explicit above for caller review.

## Exact capture URL examples

`file://<repo>/hardware/joints/cad/exports/l02-animation/animation.html?capture=leg&frames=60&w=800&h=600`

`file://<repo>/hardware/joints/cad/exports/l02-animation/animation.html?capture=overview&frames=60&w=800&h=600`

`file://<repo>/hardware/joints/cad/exports/l02-animation/animation.html?capture=walk-prototype&frames=60&w=800&h=600`

`file://<repo>/hardware/joints/cad/exports/l02-animation/animation.html?capture=walk-concept&frames=60&w=800&h=600`

Defaults are 60 frames, 800 × 600, 15 fps. The browser must dump the completed DOM after its title reads CAPTURE DONE <scene> <N>; dumping the original file source will not contain the capture payload. Decode the dump with runtime/cad/venv/bin/python hardware/joints/cad/render_frames.py <dump.html> --out <folder>. The decoder writes <scene>.gif, <scene>.webp and <scene>-poster.png and prints each file's size. Capture uses one setTimeout(..., 0) and synchronously renders frame indices 0 through N−1; no requestAnimationFrame runs in that branch.

ANIMATION BUILD DONE — four offline CAD animation scenes built; numerical and decoder checks passed; browser proofs unrun.
