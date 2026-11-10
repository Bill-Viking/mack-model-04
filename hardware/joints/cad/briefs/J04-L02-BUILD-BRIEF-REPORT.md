# J04-L02 build brief report

The generator and offline viewer packages are built. Acceptance remains blocked by two contradictory requirements in the closed brief. No fitted candidate was created.

The original example and C01 sources are unchanged. No browser or GUI application, network operation, package installation, commit, push, wake pull or heartbeat kick ran. Brain freshness is unverified here. The caller retains the RayCue/Research claim; this job wrote only its authorized CAD deliverables and runtime/cad scratch files. The process-list probe was denied by the sandbox; no permission expansion or workaround was attempted.

## Built artifacts

- `leg_packaging.py`
- `leg-viewer-template.html`
- `exports/l02/j04-l02-direct.step`
- `exports/l02/geometry-check.json`
- `exports/l02/preview.html`
- `exports/l02-proximal/j04-l02-proximal.step`
- `exports/l02-proximal/geometry-check.json`
- `exports/l02-proximal/preview.html`
- `exports/l02-full/j04-l02-direct.step`
- `exports/l02-full/geometry-check.json`
- `exports/l02-full/preview.html`

The direct folders use the unchanged supplied example. The proximal folder is a branch verification only: `runtime/cad/l02-proximal-branch-test.json` changes only `knee.mount_side` from `inline` to `outboard`. Its parameter hash is recorded in its own geometry report. It is not a build of the unchanged example and is not a proposed fitted candidate.

## Requirements that cannot both be satisfied

1. Section 3 requires proximal `mount_side` to be `inboard` or `outboard` and to refuse any other value. The supplied JSON contains `inline`; section 7 also requires the unchanged-input proximal command to exit 0. The generator retains the explicit ValueError. No default side was silently selected and no check was disabled. The exact requested proximal command exits 1; the separate valid-side branch test exits 0.

2. Section 4 requires rigid lower-frame posing and also requires the foot centroid to equal P4 minus an unrotated world-Z half-pad offset. Rigid posing gives P4 + Rx(a) Ry(b+c) (0,0,-foot.Z/2). Both targets and their measured errors are retained in `pose_formula_check`. The rigid transform is checked on every build; a failed rigid-chain check raises ValueError as invalid posed geometry. The contradictory literal target is reported false and is not hidden by changing the transforms.

| Pose (a,b,c), deg | Rigid formula error, mm | Literal brief target error, mm |
| --- | --- | --- |
| 0, 0, 0 | 0 | 0 |
| 12, -35, 70 | 2.00971835e-14 | 3.15236731 |
| -30, 90, 120 | 2.04087863e-14 | 9.35414347 |
| 30, -90, 0 | 8.8817842e-16 | 7.07106781 |
| 15, 45, -30 | 7.58859974e-15 | 1.83012702 |

Maximum rigid error: 2.04087863e-14 mm. Maximum literal-target error: 9.35414347 mm.

## Commands, exits and measured wall time

All generator commands ran from the repository root with the prescribed interpreter, closed stdin and a parent subprocess timeout. Exit 124 denotes timeout termination. Raw stdout JSON, stderr progress and receipts are in `runtime/cad/`; no timed-out check is counted as a pass. Exploratory reads and inline checks did not retain separate process wall times.

| Run | Command | Exit | Wall seconds | Limit seconds |
| --- | --- | --- | --- | --- |
| proximal-example-quick | `runtime/cad/venv/bin/python hardware/joints/cad/leg_packaging.py --variant proximal --quick` | 1 | 2.275 | 600 |
| direct-quick | `runtime/cad/venv/bin/python hardware/joints/cad/leg_packaging.py --quick` | 0 | 524.822 | 600 |
| proximal-branch-quick | `runtime/cad/venv/bin/python hardware/joints/cad/leg_packaging.py --parameters runtime/cad/l02-proximal-branch-test.json --variant proximal --quick` | 124 | 600.023 | 600 |
| direct-quick-final | `runtime/cad/venv/bin/python hardware/joints/cad/leg_packaging.py --quick` | 0 | 84.544 | 600 |
| proximal-branch-quick-final | `runtime/cad/venv/bin/python hardware/joints/cad/leg_packaging.py --parameters runtime/cad/l02-proximal-branch-test.json --variant proximal --quick` | 0 | 165.033 | 600 |
| direct-full | `runtime/cad/venv/bin/python hardware/joints/cad/leg_packaging.py` | 0 | 272.367 | 900 |
| proximal-example-release | `runtime/cad/venv/bin/python hardware/joints/cad/leg_packaging.py --variant proximal --quick` | 1 | 4.097 | 30 |
| direct-quick-release | `runtime/cad/venv/bin/python hardware/joints/cad/leg_packaging.py --quick` | 0 | 127.274 | 600 |
| proximal-branch-quick-release | `runtime/cad/venv/bin/python hardware/joints/cad/leg_packaging.py --parameters runtime/cad/l02-proximal-branch-test.json --variant proximal --quick` | 0 | 232.590 | 600 |
| direct-full-release | `runtime/cad/venv/bin/python hardware/joints/cad/leg_packaging.py --out hardware/joints/cad/exports/l02-full` | 0 | 292.012 | 900 |
| final-verification | `runtime/cad/venv/bin/python runtime/cad/verify_l02_outputs.py` | 0 | 3.667 | 60 |

The first valid-side proximal sweep hit its 600-second bound. The sweep was then changed to reuse exact results for unchanged or rigidly equivalent configurations, enumerate all common volumes before distance queries, and order exact distance candidates by conservative AABB lower bounds. Every requested pose remains represented; collisions and near misses are never converted into build failures.

The direct real-input regression compared 1602 pairs. Collision counts and maximum overlap volumes were identical; maximum minimum-distance delta was 1.42108547e-14 mm. Initial coarse sweep: 516.941 s; optimized comparison sweep: 77.265 s. Those are measured runs, not a timing guarantee.

A final code audit added the P3 disc when a direct upper plate extends past P3 with a downward-facing knee case, and used the specified above-far-end web interval for that case. These branches were checked with real CAD solids in scratch. The supplied direct up-case geometry is unchanged. All final packages were regenerated after the correction; their generator hashes match the file on disk.

## Final measured build scope

| Package | Solids | Poses | Colliding poses | Colliding pairs | Near misses | Sweep seconds |
| --- | --- | --- | --- | --- | --- | --- |
| Direct quick, supplied example | 94 | 36 | 36 | 75 | 27 | 116.223 |
| Proximal quick, valid-side scratch | 114 | 36 | 36 | 61 | 28 | 224.040 |
| Direct full, supplied example | 94 | 175 | 175 | 88 | 27 | 280.994 |

`sweep_seconds` is elapsed wall time inside the discrete sweep, including shape preparation. The command table separately records full process wall time, including model build, checks, STEP round trip, tessellation and file writes. Full direct results are in `exports/l02-full/geometry-check.json`; the default direct folder retains the quick build.

Every build validates each leaf as exactly one valid, nonempty solid; cuts and records the cradle window; checks all neutral pairs; performs the five pose checks; enumerates the requested sweep pairs; measures stance, reach, mass and datums; exports one Compound whose children are labelled coloured solid leaves; re-imports STEP; and writes parameter/generator/STEP SHA256 provenance. A separate final verification re-imported each final STEP again and checked report fields, hashes, provenance echo, embedded meshes, frame tags, floor Z, three slider ranges, unique HTML IDs and absence of external asset tags.

| Package | STEP solids | Volume error, mm³ | Bounding-box error, mm |
| --- | --- | --- | --- |
| Direct quick | 94 | 4.56348062e-08 | 1.02886588e-11 |
| Proximal scratch | 114 | 5.93718141e-08 | 9.10063136e-11 |
| Direct full | 94 | 4.56348062e-08 | 1.02886588e-11 |

Additional focused checks passed: negative actuator width refused; unsupported upward J2 case refused; invalid proximal inline side refused; actuator API returned three valid named coloured solid leaves; downward direct case built; inboard proximal case built. Python compilation passed. Browser opening, WebGL rendering, slider interaction, zoom, separation and console cleanliness were **unrun here**, as explicitly required by the headless instructions. Static HTML/data validation does not establish those browser proofs.

## Packaging measurements and unresolved design facts

| Quantity | Direct example | Proximal scratch |
| --- | --- | --- |
| Foot bottom Z, mm | -70.3053474 | -70.3053474 |
| Overall height, mm | 182.305347 | 182.305347 |
| Clock-bottom clearance, mm | 70.3053474 | 70.3053474 |
| Mirrored foot-centre stance width, mm | 113.61601 | 113.61601 |
| Leg total including 3 hardware allowances, g | 90.4806151 | 115.445207 |
| Four legs arithmetically, g | 361.92246 | 461.780828 |
| Cradle after window, g | 30.18 | 30.18 |

Masses use the supplied assumed densities and fixed allowances. J1 case and mount belong to the carrier mass subtotal as hip hardware fixed to the cradle. Foot mass is separate from the lower-link subtotal. Three hardware allowances are lumped at P1, posed P2 and P3; the moving knee allowance is at P3. Inertia is centroid-lumped Σm r², not tensor inertia. Neighbours have zero counted mass. Catalog complete clock mass is 229 g; retained clock mass is unknown, so body-envelope mass is excluded.

The supplied P1 case reaches Z = 0, and the J2 near-end datum reaches Z = +1. The cradle through-window is X [7,43] mm, Y [22,62] mm for both final models. J1/cradle common volume after the window is 1144 mm³ over Z [-4,0] mm; it is an unknown-shell-interior intake question, recorded under `inside_shell_envelope`, rather than a claim about measured shell material. J2/body-envelope neutral common volume is listed in the tables below.

Two further direct-case interface distances were measured on the model: J2 case to each carrier side plate = 8 mm; upper horn plate to upper_channel_plus = 17.838638192 mm. The brief’s prescribed `upper_plates_too_short` inequality does not flag the supplied up-case values. Those measured gaps, the contradictory foot target and the missing valid proximal side remain matters for the design session. No geometry was adjusted to clear the example. The belt is the specified filled rectangular envelope; its supplied belt_thickness value does not change that envelope.

## Interference lists

Depth findings below precede window cutting where marked. Neutral tables contain every measured positive common volume, including fixed neighbouring envelopes and intentional transmission-envelope overlaps. Sweep tables give every colliding pair and its maximum measured common volume over that package’s grid; complete minimum distances, minimum-distance poses, collision counts and up to eight collision samples per pair are in the JSON. Touching faces with zero volume are excluded. The JSON explicitly lists nominal contact pairs omitted from the sweep. Shell-envelope overlaps establish packaging questions, not physical shell collisions.

### Direct example — quick

| Parameter finding | Depth, mm | Common volume, mm³ | Phase |
| --- | --- | --- | --- |
| j1_case_into_cradle | 4 | n/a | before_windows |
| knee_case_into_j2_case | 16 | 8320 | neutral parameter geometry |

Neutral common volumes:

| Parts | Volume, mm³ |
| --- | --- |
| body_envelope / j2_actuator | 140 |
| body_envelope / upper_web | 264 |
| body_envelope / nb_FR_j2_actuator | 284.053141 |
| body_envelope / nb_FR_upper_web | 220.499903 |
| body_envelope / nb_RL_j2_actuator | 284.053141 |
| body_envelope / nb_RL_upper_web | 220.499903 |
| body_envelope / nb_RR_j2_actuator | 284.053141 |
| body_envelope / nb_RR_upper_web | 220.499903 |
| cradle / j1_actuator | 1144 |
| cradle / nb_FR_j1_actuator | 2808 |
| cradle / nb_FR_j2_actuator | 537.823447 |
| cradle / nb_FR_carrier_idler_plate | 49.431243 |
| cradle / nb_FR_carrier_hub_idler | 74.1468646 |
| cradle / nb_FR_upper_idler_plate | 31.3048244 |
| cradle / nb_FR_upper_web | 95.0053311 |
| cradle / nb_RL_j1_actuator | 2808 |
| cradle / nb_RL_j2_actuator | 537.823447 |
| cradle / nb_RL_carrier_idler_plate | 49.431243 |
| cradle / nb_RL_carrier_hub_idler | 74.1468646 |
| cradle / nb_RL_upper_idler_plate | 31.3048244 |
| cradle / nb_RL_upper_web | 95.0053311 |
| cradle / nb_RR_j1_actuator | 2808 |
| cradle / nb_RR_j2_actuator | 537.823447 |
| cradle / nb_RR_carrier_idler_plate | 49.431243 |
| cradle / nb_RR_carrier_hub_idler | 74.1468646 |
| cradle / nb_RR_upper_idler_plate | 31.3048244 |
| cradle / nb_RR_upper_web | 95.0053311 |
| j1_actuator / j2_actuator | 4800 |
| j1_actuator / j2_actuator_idler | 226.194671 |
| j1_actuator / knee_actuator | 720 |
| j1_actuator / upper_idler_plate | 508.93801 |
| j2_actuator / knee_actuator | 8320 |
| carrier_web / knee_actuator | 1040 |
| lower_horn_plate / lower_web | 48 |
| lower_idler_plate / lower_web | 48 |
| nb_FR_j1_actuator / nb_FR_j2_actuator | 4808.93624 |
| nb_FR_j1_actuator / nb_FR_j2_actuator_idler | 226.194671 |
| nb_FR_j1_actuator / nb_FR_knee_actuator | 1025.38727 |
| nb_FR_j1_actuator / nb_FR_upper_idler_plate | 508.93801 |
| nb_FR_j1_actuator / nb_FR_upper_web | 110.884742 |
| nb_FR_j1_actuator_horn / nb_FR_knee_actuator | 33.942216 |
| nb_FR_j2_actuator / nb_FR_knee_actuator | 4869.12725 |
| nb_FR_j2_actuator / nb_FR_upper_web | 137.948761 |
| nb_FR_carrier_horn_plate / nb_FR_knee_actuator | 691.582103 |
| nb_FR_carrier_hub_horn / nb_FR_knee_actuator | 49.9843596 |
| nb_FR_carrier_web / nb_FR_knee_actuator | 642.32759 |
| nb_FR_carrier_web / nb_FR_upper_channel_minus | 0.0430256231 |
| nb_FR_knee_actuator / nb_FR_lower_web | 3.78655227 |
| nb_FR_lower_horn_plate / nb_FR_lower_web | 48 |
| nb_FR_lower_idler_plate / nb_FR_lower_web | 48 |
| nb_RL_j1_actuator / nb_RL_j2_actuator | 4808.93624 |
| nb_RL_j1_actuator / nb_RL_j2_actuator_idler | 226.194671 |
| nb_RL_j1_actuator / nb_RL_knee_actuator | 1025.38727 |
| nb_RL_j1_actuator / nb_RL_upper_idler_plate | 508.93801 |
| nb_RL_j1_actuator / nb_RL_upper_web | 110.884742 |
| nb_RL_j1_actuator_horn / nb_RL_knee_actuator | 33.942216 |
| nb_RL_j2_actuator / nb_RL_knee_actuator | 4869.12725 |
| nb_RL_j2_actuator / nb_RL_upper_web | 137.948761 |
| nb_RL_carrier_horn_plate / nb_RL_knee_actuator | 691.582103 |
| nb_RL_carrier_hub_horn / nb_RL_knee_actuator | 49.9843596 |
| nb_RL_carrier_web / nb_RL_knee_actuator | 642.32759 |
| nb_RL_carrier_web / nb_RL_upper_channel_minus | 0.0430256231 |
| nb_RL_knee_actuator / nb_RL_lower_web | 3.78655227 |
| nb_RL_lower_horn_plate / nb_RL_lower_web | 48 |
| nb_RL_lower_idler_plate / nb_RL_lower_web | 48 |
| nb_RR_j1_actuator / nb_RR_j2_actuator | 4808.93624 |
| nb_RR_j1_actuator / nb_RR_j2_actuator_idler | 226.194671 |
| nb_RR_j1_actuator / nb_RR_knee_actuator | 1025.38727 |
| nb_RR_j1_actuator / nb_RR_upper_idler_plate | 508.93801 |
| nb_RR_j1_actuator / nb_RR_upper_web | 110.884742 |
| nb_RR_j1_actuator_horn / nb_RR_knee_actuator | 33.942216 |
| nb_RR_j2_actuator / nb_RR_knee_actuator | 4869.12725 |
| nb_RR_j2_actuator / nb_RR_upper_web | 137.948761 |
| nb_RR_carrier_horn_plate / nb_RR_knee_actuator | 691.582103 |
| nb_RR_carrier_hub_horn / nb_RR_knee_actuator | 49.9843596 |
| nb_RR_carrier_web / nb_RR_knee_actuator | 642.32759 |
| nb_RR_carrier_web / nb_RR_upper_channel_minus | 0.0430256231 |
| nb_RR_knee_actuator / nb_RR_lower_web | 3.78655227 |
| nb_RR_lower_horn_plate / nb_RR_lower_web | 48 |
| nb_RR_lower_idler_plate / nb_RR_lower_web | 48 |

Sweep interferences:

| Parts | Colliding poses | Maximum overlap, mm³ |
| --- | --- | --- |
| j2_actuator / body_envelope | 36 | 658.476918 |
| j2_actuator / j1_actuator | 36 | 4839.98405 |
| j2_actuator_idler / j1_actuator | 36 | 226.194671 |
| knee_actuator / j2_actuator | 36 | 5360.88856 |
| knee_actuator / carrier_horn_plate | 18 | 665.197397 |
| knee_actuator / carrier_hub_horn | 18 | 435.59219 |
| knee_actuator / carrier_idler_plate | 18 | 665.197397 |
| knee_actuator / carrier_hub_idler | 18 | 435.59219 |
| knee_actuator / carrier_web | 18 | 770.877823 |
| knee_actuator / body_envelope | 6 | 739.395666 |
| knee_actuator / cradle | 18 | 633.343249 |
| knee_actuator / j1_actuator | 36 | 1440 |
| knee_actuator / j1_actuator_horn | 18 | 136.985757 |
| knee_actuator / j1_actuator_idler | 18 | 136.985757 |
| knee_actuator / nb_RL_carrier_idler_plate | 9 | 483.62839 |
| knee_actuator_idler / cradle | 3 | 1.82702665 |
| upper_idler_plate / body_envelope | 12 | 0.262613235 |
| upper_idler_plate / j1_actuator | 36 | 508.93801 |
| upper_web / j2_actuator | 18 | 123.244724 |
| upper_web / body_envelope | 24 | 333.331169 |
| upper_web / cradle | 6 | 4.5388745 |
| upper_web / j1_actuator | 36 | 138.876968 |
| upper_web / j1_actuator_horn | 9 | 162.89367 |
| upper_web / j1_actuator_idler | 9 | 162.89367 |
| upper_channel_minus / body_envelope | 9 | 7.88728933 |
| upper_channel_minus / cradle | 3 | 0.685251463 |
| lower_horn_plate / body_envelope | 2 | 0.0280558185 |
| lower_horn_plate / nb_RL_j2_actuator | 3 | 437.778057 |
| lower_horn_plate / nb_RL_j2_actuator_horn | 2 | 6.57273727 |
| lower_horn_plate / nb_RL_carrier_idler_plate | 4 | 47.8851382 |
| lower_horn_plate / nb_RL_carrier_web | 2 | 40.0000616 |
| lower_horn_plate / nb_RL_knee_actuator | 2 | 186.227775 |
| lower_horn_plate / nb_RL_upper_horn_plate | 2 | 232.759629 |
| lower_horn_plate / nb_RL_upper_web | 1 | 50.4701868 |
| lower_idler_plate / carrier_horn_plate | 3 | 11.9352131 |
| lower_idler_plate / carrier_hub_horn | 3 | 0.952878544 |
| lower_idler_plate / carrier_idler_plate | 6 | 11.9352131 |
| lower_idler_plate / carrier_hub_idler | 6 | 0.952878544 |
| lower_idler_plate / body_envelope | 8 | 802.064053 |
| lower_idler_plate / cradle | 12 | 268.345306 |
| lower_idler_plate / nb_RL_j1_actuator | 3 | 649.380204 |
| lower_idler_plate / nb_RL_j1_actuator_idler | 3 | 35.2181979 |
| lower_idler_plate / nb_RL_j2_actuator | 3 | 171.774817 |
| lower_idler_plate / nb_RL_j2_actuator_idler | 3 | 52.8799842 |
| lower_idler_plate / nb_RL_carrier_idler_plate | 7 | 56 |
| lower_idler_plate / nb_RL_carrier_hub_idler | 6 | 84 |
| lower_idler_plate / nb_RL_carrier_web | 1 | 50.3239856 |
| lower_idler_plate / nb_RL_knee_actuator | 1 | 5.66329492 |
| lower_idler_plate / nb_RL_upper_idler_plate | 3 | 301.986228 |
| lower_idler_plate / nb_RL_upper_web | 2 | 3.77067865 |
| lower_web / knee_actuator | 24 | 136.100333 |
| lower_web / upper_channel_minus | 12 | 14.8475315 |
| lower_web / j2_actuator | 3 | 157.00037 |
| lower_web / carrier_horn_plate | 3 | 113.143816 |
| lower_web / carrier_hub_horn | 3 | 0.0280558185 |
| lower_web / carrier_idler_plate | 6 | 120.088856 |
| lower_web / carrier_hub_idler | 3 | 0.0280558128 |
| lower_web / carrier_web | 3 | 104 |
| lower_web / body_envelope | 7 | 333.331169 |
| lower_web / cradle | 7 | 109.706244 |
| lower_web / nb_RL_carrier_idler_plate | 3 | 70.8012975 |
| lower_web / nb_RL_carrier_hub_idler | 6 | 318.714327 |
| foot / j2_actuator | 3 | 42.6423289 |
| foot / carrier_idler_plate | 3 | 192.615612 |
| foot / carrier_web | 6 | 297.025034 |
| foot / body_envelope | 7 | 2879.65291 |
| foot / cradle | 2 | 254.899084 |
| foot / nb_RL_j1_actuator | 3 | 1260 |
| foot / nb_RL_j2_actuator | 7 | 2880 |
| foot / nb_RL_carrier_idler_plate | 3 | 132.594993 |
| foot / nb_RL_carrier_hub_idler | 3 | 3.0019929 |
| foot / nb_RL_carrier_web | 3 | 320.532391 |
| foot / nb_RL_knee_actuator | 3 | 1971.41687 |
| foot / nb_RL_upper_horn_plate | 1 | 3.98966725 |
| foot / nb_RL_upper_web | 1 | 127.99342 |

### Direct example — full

| Parameter finding | Depth, mm | Common volume, mm³ | Phase |
| --- | --- | --- | --- |
| j1_case_into_cradle | 4 | n/a | before_windows |
| knee_case_into_j2_case | 16 | 8320 | neutral parameter geometry |

Neutral common volumes:

| Parts | Volume, mm³ |
| --- | --- |
| body_envelope / j2_actuator | 140 |
| body_envelope / upper_web | 264 |
| body_envelope / nb_FR_j2_actuator | 284.053141 |
| body_envelope / nb_FR_upper_web | 220.499903 |
| body_envelope / nb_RL_j2_actuator | 284.053141 |
| body_envelope / nb_RL_upper_web | 220.499903 |
| body_envelope / nb_RR_j2_actuator | 284.053141 |
| body_envelope / nb_RR_upper_web | 220.499903 |
| cradle / j1_actuator | 1144 |
| cradle / nb_FR_j1_actuator | 2808 |
| cradle / nb_FR_j2_actuator | 537.823447 |
| cradle / nb_FR_carrier_idler_plate | 49.431243 |
| cradle / nb_FR_carrier_hub_idler | 74.1468646 |
| cradle / nb_FR_upper_idler_plate | 31.3048244 |
| cradle / nb_FR_upper_web | 95.0053311 |
| cradle / nb_RL_j1_actuator | 2808 |
| cradle / nb_RL_j2_actuator | 537.823447 |
| cradle / nb_RL_carrier_idler_plate | 49.431243 |
| cradle / nb_RL_carrier_hub_idler | 74.1468646 |
| cradle / nb_RL_upper_idler_plate | 31.3048244 |
| cradle / nb_RL_upper_web | 95.0053311 |
| cradle / nb_RR_j1_actuator | 2808 |
| cradle / nb_RR_j2_actuator | 537.823447 |
| cradle / nb_RR_carrier_idler_plate | 49.431243 |
| cradle / nb_RR_carrier_hub_idler | 74.1468646 |
| cradle / nb_RR_upper_idler_plate | 31.3048244 |
| cradle / nb_RR_upper_web | 95.0053311 |
| j1_actuator / j2_actuator | 4800 |
| j1_actuator / j2_actuator_idler | 226.194671 |
| j1_actuator / knee_actuator | 720 |
| j1_actuator / upper_idler_plate | 508.93801 |
| j2_actuator / knee_actuator | 8320 |
| carrier_web / knee_actuator | 1040 |
| lower_horn_plate / lower_web | 48 |
| lower_idler_plate / lower_web | 48 |
| nb_FR_j1_actuator / nb_FR_j2_actuator | 4808.93624 |
| nb_FR_j1_actuator / nb_FR_j2_actuator_idler | 226.194671 |
| nb_FR_j1_actuator / nb_FR_knee_actuator | 1025.38727 |
| nb_FR_j1_actuator / nb_FR_upper_idler_plate | 508.93801 |
| nb_FR_j1_actuator / nb_FR_upper_web | 110.884742 |
| nb_FR_j1_actuator_horn / nb_FR_knee_actuator | 33.942216 |
| nb_FR_j2_actuator / nb_FR_knee_actuator | 4869.12725 |
| nb_FR_j2_actuator / nb_FR_upper_web | 137.948761 |
| nb_FR_carrier_horn_plate / nb_FR_knee_actuator | 691.582103 |
| nb_FR_carrier_hub_horn / nb_FR_knee_actuator | 49.9843596 |
| nb_FR_carrier_web / nb_FR_knee_actuator | 642.32759 |
| nb_FR_carrier_web / nb_FR_upper_channel_minus | 0.0430256231 |
| nb_FR_knee_actuator / nb_FR_lower_web | 3.78655227 |
| nb_FR_lower_horn_plate / nb_FR_lower_web | 48 |
| nb_FR_lower_idler_plate / nb_FR_lower_web | 48 |
| nb_RL_j1_actuator / nb_RL_j2_actuator | 4808.93624 |
| nb_RL_j1_actuator / nb_RL_j2_actuator_idler | 226.194671 |
| nb_RL_j1_actuator / nb_RL_knee_actuator | 1025.38727 |
| nb_RL_j1_actuator / nb_RL_upper_idler_plate | 508.93801 |
| nb_RL_j1_actuator / nb_RL_upper_web | 110.884742 |
| nb_RL_j1_actuator_horn / nb_RL_knee_actuator | 33.942216 |
| nb_RL_j2_actuator / nb_RL_knee_actuator | 4869.12725 |
| nb_RL_j2_actuator / nb_RL_upper_web | 137.948761 |
| nb_RL_carrier_horn_plate / nb_RL_knee_actuator | 691.582103 |
| nb_RL_carrier_hub_horn / nb_RL_knee_actuator | 49.9843596 |
| nb_RL_carrier_web / nb_RL_knee_actuator | 642.32759 |
| nb_RL_carrier_web / nb_RL_upper_channel_minus | 0.0430256231 |
| nb_RL_knee_actuator / nb_RL_lower_web | 3.78655227 |
| nb_RL_lower_horn_plate / nb_RL_lower_web | 48 |
| nb_RL_lower_idler_plate / nb_RL_lower_web | 48 |
| nb_RR_j1_actuator / nb_RR_j2_actuator | 4808.93624 |
| nb_RR_j1_actuator / nb_RR_j2_actuator_idler | 226.194671 |
| nb_RR_j1_actuator / nb_RR_knee_actuator | 1025.38727 |
| nb_RR_j1_actuator / nb_RR_upper_idler_plate | 508.93801 |
| nb_RR_j1_actuator / nb_RR_upper_web | 110.884742 |
| nb_RR_j1_actuator_horn / nb_RR_knee_actuator | 33.942216 |
| nb_RR_j2_actuator / nb_RR_knee_actuator | 4869.12725 |
| nb_RR_j2_actuator / nb_RR_upper_web | 137.948761 |
| nb_RR_carrier_horn_plate / nb_RR_knee_actuator | 691.582103 |
| nb_RR_carrier_hub_horn / nb_RR_knee_actuator | 49.9843596 |
| nb_RR_carrier_web / nb_RR_knee_actuator | 642.32759 |
| nb_RR_carrier_web / nb_RR_upper_channel_minus | 0.0430256231 |
| nb_RR_knee_actuator / nb_RR_lower_web | 3.78655227 |
| nb_RR_lower_horn_plate / nb_RR_lower_web | 48 |
| nb_RR_lower_idler_plate / nb_RR_lower_web | 48 |

Sweep interferences:

| Parts | Colliding poses | Maximum overlap, mm³ |
| --- | --- | --- |
| j2_actuator / body_envelope | 175 | 658.476918 |
| j2_actuator / j1_actuator | 175 | 4839.98405 |
| j2_actuator_idler / j1_actuator | 175 | 226.194671 |
| knee_actuator / j2_actuator | 175 | 8320 |
| knee_actuator / carrier_horn_plate | 75 | 1182.20007 |
| knee_actuator / carrier_hub_horn | 75 | 435.59219 |
| knee_actuator / carrier_idler_plate | 75 | 1182.20007 |
| knee_actuator / carrier_hub_idler | 75 | 435.59219 |
| knee_actuator / carrier_web | 75 | 1040 |
| knee_actuator / body_envelope | 20 | 739.395666 |
| knee_actuator / cradle | 55 | 633.343249 |
| knee_actuator / j1_actuator | 175 | 1440 |
| knee_actuator / j1_actuator_horn | 75 | 136.985757 |
| knee_actuator / j1_actuator_idler | 75 | 136.985757 |
| knee_actuator / nb_RL_carrier_idler_plate | 50 | 483.62839 |
| knee_actuator_idler / cradle | 10 | 1.83576757 |
| upper_idler_plate / body_envelope | 35 | 0.262613236 |
| upper_idler_plate / j1_actuator | 175 | 508.93801 |
| upper_web / j2_actuator | 100 | 123.244724 |
| upper_web / carrier_hub_horn | 25 | 4.91618278 |
| upper_web / carrier_hub_idler | 25 | 4.91618278 |
| upper_web / body_envelope | 135 | 434.477223 |
| upper_web / cradle | 45 | 4.73935946 |
| upper_web / j1_actuator | 165 | 207.458613 |
| upper_web / j1_actuator_horn | 50 | 162.89367 |
| upper_web / j1_actuator_idler | 50 | 162.89367 |
| upper_channel_minus / body_envelope | 25 | 7.88728933 |
| upper_channel_minus / cradle | 5 | 0.685251463 |
| lower_horn_plate / body_envelope | 3 | 45.0164412 |
| lower_horn_plate / nb_RL_j2_actuator | 12 | 437.778057 |
| lower_horn_plate / nb_RL_j2_actuator_horn | 6 | 6.57273727 |
| lower_horn_plate / nb_RL_carrier_idler_plate | 18 | 47.8851382 |
| lower_horn_plate / nb_RL_carrier_web | 11 | 104.768911 |
| lower_horn_plate / nb_RL_knee_actuator | 9 | 186.227775 |
| lower_horn_plate / nb_RL_upper_horn_plate | 14 | 421.506653 |
| lower_horn_plate / nb_RL_upper_web | 7 | 50.4701868 |
| lower_horn_plate / nb_RL_upper_channel_minus | 2 | 1.12232624 |
| lower_horn_plate / nb_RL_lower_idler_plate | 1 | 33.3318172 |
| lower_horn_plate / nb_RL_lower_web | 1 | 0.160552097 |
| lower_horn_plate / nb_RL_foot | 4 | 24.3169113 |
| lower_idler_plate / carrier_horn_plate | 30 | 11.9352131 |
| lower_idler_plate / carrier_hub_horn | 5 | 0.952878544 |
| lower_idler_plate / carrier_idler_plate | 40 | 32.7638592 |
| lower_idler_plate / carrier_hub_idler | 10 | 0.952878544 |
| lower_idler_plate / body_envelope | 33 | 845.380204 |
| lower_idler_plate / cradle | 45 | 308.910185 |
| lower_idler_plate / nb_RL_j1_actuator | 30 | 649.380204 |
| lower_idler_plate / nb_RL_j1_actuator_idler | 25 | 35.2181979 |
| lower_idler_plate / nb_RL_j2_actuator | 12 | 378.566861 |
| lower_idler_plate / nb_RL_j2_actuator_idler | 10 | 52.8799842 |
| lower_idler_plate / nb_RL_carrier_idler_plate | 37 | 65.9106065 |
| lower_idler_plate / nb_RL_carrier_hub_idler | 35 | 84 |
| lower_idler_plate / nb_RL_carrier_web | 2 | 74.5624418 |
| lower_idler_plate / nb_RL_knee_actuator | 2 | 120.543048 |
| lower_idler_plate / nb_RL_upper_idler_plate | 15 | 453.364993 |
| lower_idler_plate / nb_RL_upper_web | 16 | 64.590371 |
| lower_web / knee_actuator | 105 | 136.100333 |
| lower_web / upper_channel_minus | 70 | 14.8475315 |
| lower_web / j2_actuator | 10 | 157.00037 |
| lower_web / carrier_horn_plate | 5 | 113.143816 |
| lower_web / carrier_hub_horn | 5 | 0.0280558185 |
| lower_web / carrier_idler_plate | 15 | 120.088856 |
| lower_web / carrier_hub_idler | 5 | 0.0280558128 |
| lower_web / carrier_web | 25 | 144.807938 |
| lower_web / body_envelope | 21 | 434.477223 |
| lower_web / cradle | 19 | 120.4074 |
| lower_web / nb_RL_j1_actuator_idler | 5 | 3.7833109 |
| lower_web / nb_RL_carrier_idler_plate | 25 | 194.546366 |
| lower_web / nb_RL_carrier_hub_idler | 15 | 318.714327 |
| foot / j2_actuator | 10 | 42.6423289 |
| foot / carrier_idler_plate | 5 | 192.615612 |
| foot / carrier_web | 15 | 297.025034 |
| foot / body_envelope | 26 | 2880 |
| foot / cradle | 10 | 254.899084 |
| foot / nb_RL_j1_actuator | 30 | 1260 |
| foot / nb_RL_j1_actuator_idler | 5 | 13.59653 |
| foot / nb_RL_j2_actuator | 39 | 2880 |
| foot / nb_RL_j2_actuator_horn | 2 | 132.216128 |
| foot / nb_RL_carrier_idler_plate | 11 | 333.975451 |
| foot / nb_RL_carrier_hub_idler | 10 | 99.4388395 |
| foot / nb_RL_carrier_web | 14 | 320.532391 |
| foot / nb_RL_knee_actuator | 15 | 1971.41687 |
| foot / nb_RL_upper_horn_plate | 3 | 147.722262 |
| foot / nb_RL_upper_web | 15 | 311.048857 |
| foot / nb_RL_upper_channel_minus | 7 | 7.99605901 |
| foot / nb_RL_lower_idler_plate | 5 | 44.4246239 |
| foot / nb_RL_lower_web | 2 | 2.52717628 |
| foot / nb_RL_foot | 2 | 11.1725114 |

### Proximal valid-side scratch — quick (unchanged example refused)

| Parameter finding | Depth, mm | Common volume, mm³ | Phase |
| --- | --- | --- | --- |
| j1_case_into_cradle | 4 | n/a | before_windows |

Neutral common volumes:

| Parts | Volume, mm³ |
| --- | --- |
| body_envelope / j2_actuator | 140 |
| body_envelope / upper_web | 264 |
| body_envelope / nb_FR_j2_actuator | 284.053141 |
| body_envelope / nb_FR_upper_web | 220.499903 |
| body_envelope / nb_RL_j2_actuator | 284.053141 |
| body_envelope / nb_RL_upper_web | 220.499903 |
| body_envelope / nb_RR_j2_actuator | 284.053141 |
| body_envelope / nb_RR_upper_web | 220.499903 |
| cradle / j1_actuator | 1144 |
| cradle / nb_FR_j1_actuator | 2808 |
| cradle / nb_FR_j2_actuator | 537.823447 |
| cradle / nb_FR_carrier_idler_plate | 49.431243 |
| cradle / nb_FR_carrier_hub_idler | 74.1468646 |
| cradle / nb_FR_upper_idler_plate | 31.3048244 |
| cradle / nb_FR_upper_web | 95.0053311 |
| cradle / nb_RL_j1_actuator | 2808 |
| cradle / nb_RL_j2_actuator | 537.823447 |
| cradle / nb_RL_carrier_idler_plate | 49.431243 |
| cradle / nb_RL_carrier_hub_idler | 74.1468646 |
| cradle / nb_RL_upper_idler_plate | 31.3048244 |
| cradle / nb_RL_upper_web | 95.0053311 |
| cradle / nb_RR_j1_actuator | 2808 |
| cradle / nb_RR_j2_actuator | 537.823447 |
| cradle / nb_RR_carrier_idler_plate | 49.431243 |
| cradle / nb_RR_carrier_hub_idler | 74.1468646 |
| cradle / nb_RR_upper_idler_plate | 31.3048244 |
| cradle / nb_RR_upper_web | 95.0053311 |
| j1_actuator / j2_actuator | 4800 |
| j1_actuator / j2_actuator_idler | 226.194671 |
| j1_actuator / upper_idler_plate | 565.380204 |
| knee_mount / knee_bearing_out | 1.54197566 |
| pulley_hip / belt | 339.292007 |
| pulley_knee / belt | 339.292007 |
| pulley_knee / knee_shaft | 117.809725 |
| belt / knee_shaft | 58.9048623 |
| lower_plate_in / lower_web | 48 |
| lower_plate_in / knee_shaft | 39.2699082 |
| lower_plate_out / lower_web | 48 |
| lower_plate_out / knee_shaft | 39.2699082 |
| nb_FR_j1_actuator / nb_FR_j2_actuator | 4808.93624 |
| nb_FR_j1_actuator / nb_FR_j2_actuator_idler | 226.194671 |
| nb_FR_j1_actuator / nb_FR_upper_idler_plate | 599.410985 |
| nb_FR_j1_actuator / nb_FR_upper_web | 110.884742 |
| nb_FR_j2_actuator / nb_FR_upper_web | 137.948761 |
| nb_FR_carrier_horn_plate / nb_FR_knee_shaft | 14.324472 |
| nb_FR_carrier_web / nb_FR_knee_shaft | 157.408181 |
| nb_FR_knee_mount / nb_FR_knee_bearing_out | 1.54197566 |
| nb_FR_pulley_hip / nb_FR_belt | 339.292007 |
| nb_FR_pulley_knee / nb_FR_belt | 339.292007 |
| nb_FR_pulley_knee / nb_FR_knee_shaft | 117.809725 |
| nb_FR_belt / nb_FR_knee_shaft | 58.9048623 |
| nb_FR_lower_plate_in / nb_FR_lower_web | 48 |
| nb_FR_lower_plate_in / nb_FR_knee_shaft | 39.2699082 |
| nb_FR_lower_plate_out / nb_FR_lower_web | 48 |
| nb_FR_lower_plate_out / nb_FR_knee_shaft | 39.2699082 |
| nb_RL_j1_actuator / nb_RL_j2_actuator | 4808.93624 |
| nb_RL_j1_actuator / nb_RL_j2_actuator_idler | 226.194671 |
| nb_RL_j1_actuator / nb_RL_upper_idler_plate | 599.410985 |
| nb_RL_j1_actuator / nb_RL_upper_web | 110.884742 |
| nb_RL_j2_actuator / nb_RL_upper_web | 137.948761 |
| nb_RL_carrier_horn_plate / nb_RL_knee_shaft | 14.324472 |
| nb_RL_carrier_web / nb_RL_knee_shaft | 157.408181 |
| nb_RL_knee_mount / nb_RL_knee_bearing_out | 1.54197566 |
| nb_RL_pulley_hip / nb_RL_belt | 339.292007 |
| nb_RL_pulley_knee / nb_RL_belt | 339.292007 |
| nb_RL_pulley_knee / nb_RL_knee_shaft | 117.809725 |
| nb_RL_belt / nb_RL_knee_shaft | 58.9048623 |
| nb_RL_lower_plate_in / nb_RL_lower_web | 48 |
| nb_RL_lower_plate_in / nb_RL_knee_shaft | 39.2699082 |
| nb_RL_lower_plate_out / nb_RL_lower_web | 48 |
| nb_RL_lower_plate_out / nb_RL_knee_shaft | 39.2699082 |
| nb_RR_j1_actuator / nb_RR_j2_actuator | 4808.93624 |
| nb_RR_j1_actuator / nb_RR_j2_actuator_idler | 226.194671 |
| nb_RR_j1_actuator / nb_RR_upper_idler_plate | 599.410985 |
| nb_RR_j1_actuator / nb_RR_upper_web | 110.884742 |
| nb_RR_j2_actuator / nb_RR_upper_web | 137.948761 |
| nb_RR_carrier_horn_plate / nb_RR_knee_shaft | 14.324472 |
| nb_RR_carrier_web / nb_RR_knee_shaft | 157.408181 |
| nb_RR_knee_mount / nb_RR_knee_bearing_out | 1.54197566 |
| nb_RR_pulley_hip / nb_RR_belt | 339.292007 |
| nb_RR_pulley_knee / nb_RR_belt | 339.292007 |
| nb_RR_pulley_knee / nb_RR_knee_shaft | 117.809725 |
| nb_RR_belt / nb_RR_knee_shaft | 58.9048623 |
| nb_RR_lower_plate_in / nb_RR_lower_web | 48 |
| nb_RR_lower_plate_in / nb_RR_knee_shaft | 39.2699082 |
| nb_RR_lower_plate_out / nb_RR_lower_web | 48 |
| nb_RR_lower_plate_out / nb_RR_knee_shaft | 39.2699082 |

Sweep interferences:

| Parts | Colliding poses | Maximum overlap, mm³ |
| --- | --- | --- |
| j2_actuator / body_envelope | 36 | 658.476918 |
| j2_actuator / j1_actuator | 36 | 4839.98405 |
| j2_actuator_idler / j1_actuator | 36 | 226.194671 |
| upper_idler_plate / carrier_horn_plate | 9 | 56 |
| upper_idler_plate / carrier_hub_horn | 9 | 84 |
| upper_idler_plate / carrier_idler_plate | 9 | 56 |
| upper_idler_plate / carrier_hub_idler | 9 | 84 |
| upper_idler_plate / body_envelope | 12 | 0.525226469 |
| upper_idler_plate / cradle | 15 | 89.012994 |
| upper_idler_plate / j1_actuator | 36 | 716.591518 |
| upper_idler_plate / j1_actuator_horn | 9 | 35.2181979 |
| upper_idler_plate / j1_actuator_idler | 9 | 35.2181979 |
| upper_web / j2_actuator | 18 | 123.244724 |
| upper_web / body_envelope | 24 | 333.331169 |
| upper_web / cradle | 6 | 4.5388745 |
| upper_web / j1_actuator | 36 | 138.876968 |
| upper_web / j1_actuator_horn | 9 | 162.89367 |
| upper_web / j1_actuator_idler | 9 | 162.89367 |
| knee_shaft / carrier_web | 18 | 247.573456 |
| knee_shaft / cradle | 3 | 0.3216367 |
| knee_bearing_in / cradle | 3 | 17.3812064 |
| lower_plate_in / carrier_horn_plate | 3 | 1.8448186 |
| lower_plate_in / carrier_idler_plate | 6 | 1.84481861 |
| lower_plate_in / body_envelope | 8 | 802.064053 |
| lower_plate_in / cradle | 10 | 396.676472 |
| lower_plate_in / j1_actuator | 3 | 0.171522549 |
| lower_plate_in / nb_RL_j1_actuator | 4 | 649.380204 |
| lower_plate_in / nb_RL_j2_actuator | 2 | 28.6104365 |
| lower_plate_in / nb_RL_carrier_idler_plate | 7 | 38.8425655 |
| lower_plate_in / nb_RL_carrier_hub_idler | 3 | 58.2638483 |
| lower_plate_in / nb_RL_carrier_web | 1 | 49.7638122 |
| lower_plate_in / nb_RL_upper_idler_plate | 3 | 67.5078541 |
| lower_plate_in / nb_RL_upper_web | 2 | 24.4167706 |
| lower_plate_out / nb_RL_belt | 1 | 9.4887832 |
| lower_web / upper_horn_plate | 12 | 1.89870921 |
| lower_web / upper_idler_plate | 12 | 1.89870921 |
| lower_web / knee_actuator | 12 | 233.479081 |
| lower_web / knee_mount | 12 | 75.0257739 |
| lower_web / j2_actuator | 3 | 157.00037 |
| lower_web / carrier_horn_plate | 3 | 65.5464422 |
| lower_web / carrier_idler_plate | 6 | 120.088856 |
| lower_web / carrier_web | 3 | 104 |
| lower_web / body_envelope | 7 | 238.276878 |
| lower_web / cradle | 8 | 186.598516 |
| lower_web / nb_RL_carrier_idler_plate | 6 | 703.687523 |
| lower_web / nb_RL_carrier_hub_idler | 3 | 98.3655389 |
| lower_web / nb_RL_carrier_web | 1 | 5.64624017 |
| foot / j2_actuator | 3 | 42.6423289 |
| foot / carrier_idler_plate | 3 | 192.615612 |
| foot / carrier_web | 6 | 297.025034 |
| foot / body_envelope | 7 | 2879.65291 |
| foot / cradle | 2 | 254.899084 |
| foot / nb_RL_j1_actuator | 3 | 1260 |
| foot / nb_RL_j2_actuator | 7 | 2880 |
| foot / nb_RL_carrier_idler_plate | 3 | 132.594993 |
| foot / nb_RL_carrier_hub_idler | 3 | 3.0019929 |
| foot / nb_RL_carrier_web | 3 | 320.532391 |
| foot / nb_RL_upper_horn_plate | 1 | 3.98966725 |
| foot / nb_RL_upper_idler_plate | 1 | 0.0247332777 |
| foot / nb_RL_upper_web | 1 | 127.99342 |
| foot / nb_RL_knee_actuator | 1 | 59.0057347 |

## Fingerprints and limits

| Protected file | Result | SHA256 |
| --- | --- | --- |
| joint_cartridge.py | SAME | 23fd34bc707236270774dff8a93d5b1aa5974dd04196cad317171a26f7b61fec |
| viewer-template.html | SAME | ab98ddbe3543dae0da8288404ee05c43ff8ddf2489e86d28d9300fcaff1cd605 |
| j04-l02.example.json | SAME | 624fe965d56ab4bb5b5be0d2227d9f19e547de29f3cda013de424f35db00e1bd |
| j04-c01.example.json | SAME | 4657a464effe2569ce8392a554600072bc5ce7842ffae0580d5887f6df5c00f8 |

The final verifier also compared every tracked existing C01 STEP file against its HEAD blob and found it unchanged. Pre-existing candidate JSON files, packaging notes, the caller’s brief/log and the loose concept PNG were not edited. No STATUS, OPENER, memory, claim or stamp was written outside the task’s file scope.

Runtime: Python 3.12.13, build123d 0.12.0. Final generator SHA256: `f11df6d87e5b3a64fbbbe1bdae461059fe0e21da115049049a65d3cdc2f2ea51`. Original example SHA256: `624fe965d56ab4bb5b5be0d2227d9f19e547de29f3cda013de424f35db00e1bd`. Independent verification details: `runtime/cad/l02-final-verification.json`; command receipts: `runtime/cad/l02-command-receipts.jsonl`.

Scope: Nominal rigid envelopes; discrete pose samples, not a continuous collision proof. No cables, fasteners, stops, encoders, covers, batteries or measured shell interior.
No structural analysis or physical testing was performed. No strength, bearing, actuator selection, walking, continuous-clearance or measured-shell-fit claim is made.

FAIL — unchanged proximal input is invalid under the required check, and the literal foot-centre target contradicts rigid lower-frame posing; browser proofs remain caller-owned and unrun.
