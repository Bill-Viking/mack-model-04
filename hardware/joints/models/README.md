# 3D packaging studies

Click a file to turn it with the mouse.

Packaging-study envelopes with benchmark actuator blocks and example dimensions; nothing built or tested.

All models use millimetres with Z up. Bounding boxes list X, Y, Z.

| File | What it is | Bounding box in mm (min → max; size) | Triangles |
| --- | --- | --- | ---: |
| [joint-cartridge.stl](joint-cartridge.stl) | J04-C01 joint cartridge, all six assembly solids | (-67.00, -20.00, -46.00) → (33.00, 20.00, 62.00); (100.00, 40.00, 108.00) | 3,536 |
| [leg-direct-knee.stl](leg-direct-knee.stl) | Front-left leg, placement A, direct knee, with cradle | (-43.50, -38.00, -111.79) → (70.18, 82.53, 0.00); (113.68, 120.53, 111.79) | 3,640 |
| [leg-belt-knee.stl](leg-belt-knee.stl) | Front-left leg, placement A, belt knee and transmission envelopes, with cradle | (-43.50, -38.00, -101.59) → (53.21, 82.55, 0.00); (96.71, 120.55, 101.59) | 6,264 |
| [mack-four-legs-prototype.stl](mack-four-legs-prototype.stl) | Prototype body box, cradle and four direct-knee legs at stance | (-70.18, -82.53, -111.79) → (70.18, 82.53, 112.00); (140.36, 165.07, 223.79) | 14,536 |

Placement A stance: 12° hip spread, −35° hip swing, 70° knee bend. The example uses a 50 mm upper link for the direct knee and 30 mm for the belt knee.

Known study overlaps remain; these separate envelopes are for viewing, not manufacture.

[Editable sources](../cad/) · [STEP files](../cad/exports/) · [Leg packaging study](../leg-packaging.md) · [Mesh checks](models-check.json)

Rebuild from the repository root: `runtime/cad/venv/bin/python hardware/joints/cad/export_models.py`.
