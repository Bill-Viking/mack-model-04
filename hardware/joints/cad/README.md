# J04-C01 — editable joint cartridge study

**D01 / example geometry / not for manufacture.** This is the first original Mack
joint solid model. It explores a supported **hip-spread** output, not the complete
three-axis leg. Every dimension in the example file is provisional. None came
from measurements of the RayCue clock or a selected motor/bearing.

Open [the offline 3D preview](exports/preview.html) in a browser after downloading
the folder. GitHub displays HTML source rather than running the viewer. The viewer
uses WebGL and contains its own meshes; no network, account or CAD install is
required. Drag to rotate, move the angle slider, or separate the parts to inspect
them. The latter is illustrative spacing, not an assembly instruction or collision
test. Keyboard arrows rotate the focused model; +/− zoom.

## Deliverables

| File | Purpose |
| --- | --- |
| [joint_cartridge.py](joint_cartridge.py) | Editable build123d geometry, validation and export source. |
| [j04-c01.example.json](j04-c01.example.json) | Millimetre parameters, marked as example inputs. |
| [Assembly STEP](exports/j04-c01-draft.step) | Six named solids with colours, for CAD import trials. |
| [Yoke STEP](exports/yoke-draft.step), [link STEP](exports/output_link-draft.step), [shaft STEP](exports/shaft-draft.step) | Separate draft solids for inspection. |
| [Geometry report](exports/geometry-check.json) | Volumes, nominal overlap, sampled link clearance and STEP round trip. |
| [Viewer template](viewer-template.html) | Source for the standalone interactive preview. |

The six bodies are a yoke, shaft, hub/link, two simple annular bearing envelopes,
and a rectangular motor envelope. Bearing rings have no races, rolling elements
or seals. The motor block has no output shaft or mount. These are space
reservations, not representations of purchased components.

Local **Z** is the shaft axis. Local **+Y** is the neutral link direction. Rotate
this coordinate frame into the measured body assembly later; local Z corresponds
to the proposed hip-spread axis along body X. This fixture orientation is not a
downward leg installation. The neutral overall envelope is **40 × 108 × 100 mm**,
including the motor placeholder. It is not a proposed final cartridge size.

The example uses an 8 mm shaft, 22 × 8 × 7 mm bearing envelopes, a 32 mm fork gap,
12 mm link thickness and 55 mm output-hole pitch. These values demonstrate a
parametric model; they do not establish a bearing designation, fits or capacity.
All mating cylindrical sizes are nominal and untoleranced.

## What is verified

The generator checks connected positive-volume solids and neutral intersections.
It rotates the output link through **33 poses**, −80° to +80° in 5° increments,
against the yoke, bearing and motor envelopes. The example returns **10.0 mm**
minimum sampled clearance. Shaft/bore contact is intentional and excluded from
that clearance figure. The script also re-imports the assembly STEP and checks
solid count, validity, total volume and bounding box.

This is discrete rigid-body geometry checking. It is not proof of continuous
clearance, realistic joints, static strength, fatigue life, robot stability or
self-righting. The preview slider interpolates angles visually; that does not add
verified sample points to the report. Colours do not specify materials.

## Open mechanical interfaces

- Motor/reduction choice, bracket and positive torque coupling to the shaft.
- Positive shaft-to-hub torque connection; the current round bore alone cannot
  transmit the required torque as a designed joint.
- Bearing shoulders, axial retention, shaft retention, fits and assembly order.
- Cradle attachment, fastener selection, head/tool clearance and joint preload.
- Output encoder, reference/home sensing, travel stops and guarded cable loop.
- Fillets, process access, tolerances, mass properties, materials and load cases.
- Actual leg interfaces, neighboring joints, protective covers and shell clearance.

The motor envelope is intentionally separated from the shaft end by an unmodeled
coupling space. No linkage, mounting or retention should be inferred from it.
Do not send these solids as a load-bearing fabrication release. No STL is supplied
as a ready-to-print functional part. Follow the [engineering workflow](../../engineering-workflow.md)
to develop a fitted, toleranced design and a restrained test fixture.

## Rebuild

Use a separate Python 3.12 environment. Mack's voice `.venv` is unrelated and must
not be changed for CAD. [build123d](https://build123d.readthedocs.io/en/latest/installation.html)
is installed from PyPI; this study pins **0.12.0**. Mac arm64/Python 3.12 is verified.
Windows generation and Creo/Ansys imports remain to be checked on the Dell.

From this repository's root, on Bill's Mac:

```sh
/opt/homebrew/bin/python3.12 -m venv runtime/cad/venv
runtime/cad/venv/bin/python -m pip install -r hardware/joints/cad/requirements-macos-arm64.lock.txt
runtime/cad/venv/bin/python hardware/joints/cad/joint_cartridge.py
```

The lock file records the packages used on this Mac. It is not a promise that
identical wheels exist on every platform. For a fresh Windows environment, first
inspect the available Python installations; if Python 3.12 is present:

```powershell
py -3.12 -m venv runtime\cad\venv
runtime\cad\venv\Scripts\python.exe -m pip install -r hardware\joints\cad\requirements.txt
runtime\cad\venv\Scripts\python.exe hardware\joints\cad\joint_cartridge.py --out runtime\cad\dell-check
```

Record the actual Windows dependency versions and import results before treating
that platform as verified. Keep scratch exports in `runtime/`; tracked exports
must be regenerated with their source/parameters and reviewed together. Use
`--parameters <file>` and `--out <folder>` for controlled experiments. Retain the
example file as an explicitly synthetic baseline; actual observations belong in
[measurements.csv](../../measurements.csv).

The Python source is the **D01 master**. Importing STEP transfers boundary solids;
it does not automatically produce a native Creo feature history. If the next
revision is rebuilt in Creo, name that native model as the master and keep these
files as the D01 reference. Avoid two independently edited masters for one revision.
