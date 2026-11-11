# J04-M01 — model export hand-back

STATE: BUILT

Recorded: 2026-11-11T09:40:12-08:00 · Sol headless build from the settled brief.

Created `hardware/joints/cad/export_models.py`, the four binary STL files below, `hardware/joints/models/README.md`, and `hardware/joints/models/models-check.json`.

| File in hardware/joints/models/ | Bytes | Triangles | Solid envelopes | Maximum CAD/mesh box error (mm) |
| --- | ---: | ---: | ---: | ---: |
| joint-cartridge.stl | 176,884 | 3,536 | 6 | 0.00000000 |
| leg-direct-knee.stl | 182,084 | 3,640 | 24 | 0.00052667 |
| leg-belt-knee.stl | 313,284 | 6,264 | 29 | 0.00249310 |
| mack-four-legs-prototype.stl | 726,884 | 14,536 | 94 | 0.00052667 |

All models use millimetres with Z up. The cartridge maps its local (x, y, z) to world (z, x, y), so its mounting base is horizontal and its shaft follows world X. The leg models keep the source body frame and placement A stance (12°, −35°, 70°). The direct knee uses the example’s 50 mm upper link; the proximal belt knee uses its 30 mm upper link. The single-leg files include the complete cradle and exclude the body box and neighbour legs. The full prototype includes the body box and cradle once, plus all four complete legs mirrored by `leg_animation.LEGS`.

Tessellation: absolute linear deflection 0.25 mm and angular tolerance 0.2 rad for every file. OCCT receives absolute deflection explicitly; build123d’s default relative deflection is not used. No coarsening was needed. A finite three-step tolerance ladder is available if a future example exceeds 5,000,000 bytes.

Checks: PASS. The required command completed with exit 0 on Python 3.12 / build123d 0.12.0 within a 180-second outer limit. Each binary was reopened and verified against 84 + 50 × its header triangle count. Every file is below 5,000,000 bytes and above 200 triangles. Bounds come from the written float32 triangle vertices; every stance bound is within 0.5 mm of the selected posed CAD solids. No triangle has zero area or nonfinite coordinates. Stored normals agree with triangle winding. Every component has positive signed volume within 2% of its CAD volume; the largest measured relative error is below 0.17%. Single reflections reverse winding. The JSON records each file’s SHA256, the script SHA256, source hashes, tolerance, components, bounds, and pass/fail checks. The exporter returns non-zero and writes STOPPED on a failed check.

Independent headless read: PASS. A separate NumPy binary reader recomputed sizes, header counts, SHA256, bounding boxes, triangle normals and per-component signed volumes from the final files. Every FR, RL and RR component exactly matches the reflected FL triangles with determinant-correct winding. README link targets exist.

Negative cases: PASS. In-memory tests refused a truncated STL and an inward mirrored component. Injecting a truncated encoded output through main returned 1 and wrote a STOPPED receipt in memory. Delivered files were untouched by these tests.

Protected inputs: the three imported CAD sources and both named parameter files match the hashes read before the build. No edits were made to them, `leg_figures.py`, or `hardware/joints/figures/`. Other builders’ work was left alone. No commit, push, network access, browser, GUI, wake pull, or heartbeat kick was run. Brain freshness is unverified here.

Could not check: the models were not viewed. Repository-host rendering, appearance, mouse rotation and browser proof are UNRUN here and belong to the caller. Known packaging-study overlaps remain; fit, printability, dynamics, load qualification and physical testing are outside this export task. Nothing is built or physically tested.

OPEN: none. No unresolved implementation decision was needed; caller browser proof remains unrun as requested.

MODELS BUILD DONE — four binary Z-up STL models built; all headless checks passed; browser proof unrun.
