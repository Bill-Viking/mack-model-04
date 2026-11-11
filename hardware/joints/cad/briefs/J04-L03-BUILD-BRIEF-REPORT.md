STATE: DONE — Both packaging variants, full sweeps, STEP files, embedded previews and summary were built headlessly with the proximal foot-centroid interpretation recorded below.

# J04-L03 build report

The supplied parameters are unchanged. All dimensions and derived values below come from the corresponding generated model or its supplied parameter provenance. No fitted candidate was created.

## Commands and bounds

The command runner invoked each generator command once, sequentially, with a 900 s timeout per command. The generator had no implementation failures or retries.

| Command | Exit | Wall time (s) |
|---|---:|---:|
| `runtime/cad/venv/bin/python hardware/joints/cad/leg_base_packaging.py --quick` | 0 | 67.1 |
| `runtime/cad/venv/bin/python hardware/joints/cad/leg_base_packaging.py` | 0 | 156.7 |
| `runtime/cad/venv/bin/python hardware/joints/cad/leg_base_packaging.py --variant proximal` | 0 | 376.6 |
| `runtime/cad/venv/bin/python -B runtime/cad/l03-verify.py` | 1 | 2.7 |
| `runtime/cad/venv/bin/python -B runtime/cad/l03-verify.py` | 0 | 6.3 |

The first verification invocation stopped on a verifier error that treated provenance URLs embedded as text as network dependencies. The verifier was corrected to test external script and stylesheet references, then rerun. The generator commands each ran once.

The build commands were supervised by `runtime/cad/venv/bin/python -B runtime/cad/l03-run-checks.py`. Verification was bounded at 300 s. Build stdout, stderr, input hashes and command receipts are in `runtime/cad/l03-*` scratch files.

Read-only setup used `date`, `pwd`, `git rev-parse --show-toplevel`, a path-scoped `git status --short`, `ls -ld`, `wc -lc`, `cat`, `sed -n`, `tail`, and Python JSON reads. The initial `ls` reported that the new output paths did not exist. All CAD Python commands used `runtime/cad/venv/bin/python`. An independent quick STEP inventory imported 80 labelled solid leaves and exited 0.

## Proof scope

The generator validates single solid leaves, lists every neutral pair with overlap above 1e-5 mm³, lists all neutral inside-shell volumes, runs the five prescribed posing triples, evaluates the bounded discrete sweep, and checks STEP re-import validity, leaf count, summed volume and bounding size. It solves each height using the posed foot solid bounding box. Collisions are retained as results.

The separate verification re-imported both final STEP assemblies, checked every leaf volume and centroid against its report, recomputed the five centroid poses, checked stance overlap volumes and floor clearances, checked all six solved height rows, reconciled masses and CoM, independently evaluated torque lever arms, reconciled sweep indices and class counts, checked input/output hashes, and parsed the embedded preview model and three sliders.

**Browser proofs are UNRUN.** Both previews contain embedded meshes and offline controls. Browser rendering, slider interaction, WebGL and console behavior remain for the caller to check.

The sweep contains 175 samples per full run and 36 in the quick run. It establishes discrete-envelope results. All torque values use the specified vertical load at the specified contact point, with equal sharing among the stated number of feet. Masses and positions tagged ASSUMED in the parameters drive the CoM and support results.

| Variant | Valid STEP leaves | STEP volume error (mm³) | STEP bbox error (mm) | Five-pose centroid error (mm) | Sweep time (s) |
|---|---:|---:|---:|---:|---:|
| direct | 80 | 1.285e-07 | 2.137e-11 | 1.421e-14 | 150.1 |
| proximal | 112 | 5.239e-08 | 8.805e-11 | 3.082e-14 | 367.5 |

Numerical proof errors use scientific notation so the 1e-6 mm pose threshold remains visible. Printed dimensional, angular and mass values round once to 0.1, torques to 0.001 N·m and percentages to whole numbers. JSON retains full floats.

## Results and height sweeps

### Direct

| Metric | Model |
|---|---:|
| Stance a / b / c (deg) | 12.0 / -50.6 / 101.2 |
| Under shell (mm) | 55.0 |
| Overall height (mm) | 167.0 |
| Leg mass (g) | 90.5 |
| Four legs (g) | 362.2 |
| Total mass (g) | 981.5 |
| CoM height above floor (mm) | 75.6 |
| Stance reached / in range / ground contact | True / True / False |
| CoM XYZ (mm) | 0.0 / 0.0 / 20.6 |
| width_across_hips_mm | 158.5 |
| overall_width_mm | 158.7 |
| overall_length_mm | 142.6 |
| beyond_face_mm | 25.8 |
| track_width_mm | 105.3 |
| wheelbase_mm | 56.3 |
| base_height_mm | 27.0 |
| base_below_shell_mm | 27.0 |
| inside_shell_mm | 0.0 |
| margin_front (mm) | 28.1 |
| margin_rear (mm) | 28.1 |
| margin_left (mm) | 52.6 |
| margin_right (mm) | 52.6 |
| Minimum-margin tip angle (deg) | 20.4 |
| Lifted FL, signed margin (mm) | 0.0 |
| Lifted FR, signed margin (mm) | 0.0 |
| Lifted RL, signed margin (mm) | 0.0 |
| Lifted RR, signed margin (mm) | 0.0 |
| Sweep total / colliding / clear poses | 175 / 154 / 21 |

| Height target / actual (mm) | a / b / c (deg) | Reached | Knee forward (mm) | Beyond face (mm) | Own / base / shell / neighbour pairs | J1 / J2 / J3 (N m), 1 kg / 4 feet |
|---|---|---|---:|---:|---|---|
| 50.0 / 50.0 | 12.0 / -56.2 / 112.4 | True | 24.9 | 27.2 | 1 / 0 / 0 / 0 | 0.068 / 0.010 / 0.070 |
| 55.0 / 55.0 | 12.0 / -50.6 / 101.2 | True | 23.2 | 25.8 | 1 / 0 / 0 / 0 | 0.070 / 0.009 / 0.065 |
| 60.0 / 60.0 | 12.0 / -44.5 / 88.9 | True | 21.0 | 23.8 | 1 / 0 / 0 / 0 | 0.073 / 0.008 / 0.059 |
| 65.0 / 65.0 | 12.0 / -37.6 / 75.2 | True | 18.3 | 21.0 | 1 / 0 / 0 / 0 | 0.075 / 0.007 / 0.051 |
| 70.0 / 70.0 | 12.0 / -29.4 / 58.9 | True | 14.7 | 17.1 | 1 / 0 / 0 / 0 | 0.078 / 0.006 / 0.041 |
| 75.0 / 75.0 | 12.0 / -18.3 / 36.6 | True | 9.4 | 10.8 | 0 / 0 / 0 / 0 | 0.081 / 0.004 / 0.026 |

| Additional stance measurement | Model |
|---|---:|
| Requested range (mm) | 50.0 to 60.0 |
| Achievable height at c in [0, 130] (mm) | 41.5 to 78.2 |
| Straight leg at stance spread (mm) | 78.2 |
| Reference a / b / c (deg) | 12.0 / -35.0 / 70.0 |
| Reference under shell / overall (mm) | 66.7 / 178.7 |
| Lowest non-foot solid | shank_channel_plus |
| Its floor clearance (mm) | -1.1 |
| Base mass (g) | 47.4 |

| Picture reference comparison | Model (mm) | ASSUMED reference (mm) | Difference (mm) |
|---|---:|---:|---:|
| visible_base_below_shell | 27.0 | 15.0 | 12.0 |
| track_width_at_feet | 105.3 | 115.0 | -9.7 |
| width_across_hips | 158.5 | 100.0 | 58.5 |

Height-sweep loads and stall shares use the 1.0 kg reference mass and four feet.

| Height (mm) | Load per foot (N) | J1 / J2 / J3 stall share |
|---|---:|---|
| 50.0 | 2.452 | 13% / 2% / 13% |
| 55.0 | 2.452 | 13% / 2% / 12% |
| 60.0 | 2.452 | 14% / 2% / 11% |
| 65.0 | 2.452 | 15% / 1% / 10% |
| 70.0 | 2.452 | 15% / 1% / 8% |
| 75.0 | 2.452 | 16% / 1% / 5% |

#### Static holding torques

| Pose | Mass table | Feet | Load per foot (N) | J1 (N·m) | J2 (N·m) | J3 (N·m) | J1 / J2 / J3 stall share |
|---|---|---:|---:|---:|---:|---:|---|
| stance | reference_mass, 1000.0 g | 4 | 2.452 | 0.070 | 0.009 | 0.065 | 13% / 2% / 12% |
| stance | reference_mass, 1000.0 g | 3 | 3.269 | 0.094 | 0.012 | 0.086 | 18% / 2% / 17% |
| stance | reference_mass, 1000.0 g | 2 | 4.903 | 0.140 | 0.019 | 0.130 | 27% / 4% / 25% |
| stance | model_mass, 981.5 g | 4 | 2.406 | 0.069 | 0.009 | 0.064 | 13% / 2% / 12% |
| stance | model_mass, 981.5 g | 3 | 3.209 | 0.092 | 0.012 | 0.085 | 18% / 2% / 16% |
| stance | model_mass, 981.5 g | 2 | 4.813 | 0.138 | 0.018 | 0.127 | 27% / 3% / 24% |
| reference_pose | reference_mass, 1000.0 g | 4 | 2.452 | 0.076 | 0.007 | 0.048 | 15% / 1% / 9% |
| reference_pose | reference_mass, 1000.0 g | 3 | 3.269 | 0.102 | 0.009 | 0.064 | 20% / 2% / 12% |
| reference_pose | reference_mass, 1000.0 g | 2 | 4.903 | 0.153 | 0.014 | 0.096 | 29% / 3% / 19% |
| reference_pose | model_mass, 981.5 g | 4 | 2.406 | 0.075 | 0.007 | 0.047 | 14% / 1% / 9% |
| reference_pose | model_mass, 981.5 g | 3 | 3.209 | 0.100 | 0.009 | 0.063 | 19% / 2% / 12% |
| reference_pose | model_mass, 981.5 g | 2 | 4.813 | 0.150 | 0.014 | 0.095 | 29% / 3% / 18% |

#### Stance interferences and floor contact

The first table uses the same cross-frame pairs and intentional-contact skips as the sweep.

| Pair | Class | Overlap (mm³) |
|---|---|---:|
| upper_idler_plate / carrier_horn_plate | own_leg | 32.8 |

| Non-foot solid below the prescribed foot floor | Signed clearance (mm) |
|---|---:|
| shank_channel_plus | -1.1 |

The following exhaustive stance check includes pairs carried together in one rigid frame, the static parts and the neighbour envelopes. Its scope exceeds the sweep pair set.

| All-part stance overlap | Volume (mm³) | Intentional skipped contact, when declared |
|---|---:|---|
| carrier_horn_plate / upper_idler_plate | 32.8 | — |
| nb_FR_carrier_horn_plate / nb_FR_upper_idler_plate | 32.8 | — |
| nb_RL_carrier_horn_plate / nb_RL_upper_idler_plate | 32.8 | — |
| nb_RR_carrier_horn_plate / nb_RR_upper_idler_plate | 32.8 | — |

#### Sweep pair classes

| Class | Tested pairs | Pairs colliding somewhere | Pair-pose collisions |
|---|---:|---:|---:|
| own_leg | 122 | 9 | 405 |
| base | 45 | 4 | 140 |
| shell | 15 | 10 | 232 |
| neighbour | 855 | 24 | 233 |

Clear poses are recorded without truncation in `exports/l03-base-direct/geometry-check.json` under `sweep.clear_poses_deg` and `sweep.clear_poses_ignoring_neighbours_deg`. Each tested pair records its exact minimum distance, minimizing pose, overlap maximum, collision count and all colliding pose indices, with up to eight volume examples.

| Intentional pair skipped | Reason |
|---|---|
| carrier_horn_plate / j2_actuator | Carrier inner face on flat J2 case end face |
| carrier_hub_horn / j1_actuator_horn | J1 hub on boss |
| carrier_hub_idler / j1_actuator_idler | J1 hub on boss |
| carrier_idler_plate / j2_actuator | Carrier inner face on flat J2 case end face |
| j2_actuator_horn / upper_horn_plate | plate on J2 boss |
| j2_actuator_idler / upper_idler_plate | plate on J2 boss |
| knee_actuator_horn / upper_horn_plate | Direct knee boss outer face on thigh inner face |
| knee_actuator_idler / upper_idler_plate | Direct knee boss outer face on thigh inner face |

Neutral all-pair overlaps total 3. Neutral inside-shell volumes total 0. Full names, volumes and Z ranges are in the geometry report. Carrier web and upper web are absent. The J2 case clamped between the carrier plates provides their tie.

### Proximal

| Metric | Model |
|---|---:|
| Stance a / b / c (deg) | 12.0 / -51.5 / 103.1 |
| Under shell (mm) | 55.0 |
| Overall height (mm) | 167.0 |
| Leg mass (g) | 118.2 |
| Four legs (g) | 472.8 |
| Total mass (g) | 1092.2 |
| CoM height above floor (mm) | 73.4 |
| Stance reached / in range / ground contact | True / True / True |
| CoM XYZ (mm) | 0.0 / 0.0 / 18.4 |
| width_across_hips_mm | 239.7 |
| overall_width_mm | 249.8 |
| overall_length_mm | 129.0 |
| beyond_face_mm | 19.0 |
| track_width_mm | 97.1 |
| wheelbase_mm | 56.2 |
| base_height_mm | 27.0 |
| base_below_shell_mm | 27.0 |
| inside_shell_mm | 0.0 |
| margin_front (mm) | 28.1 |
| margin_rear (mm) | 28.1 |
| margin_left (mm) | 48.5 |
| margin_right (mm) | 48.5 |
| Minimum-margin tip angle (deg) | 20.9 |
| Lifted FL, signed margin (mm) | 0.0 |
| Lifted FR, signed margin (mm) | 0.0 |
| Lifted RL, signed margin (mm) | 0.0 |
| Lifted RR, signed margin (mm) | 0.0 |
| Sweep total / colliding / clear poses | 175 / 150 / 25 |

| Height target / actual (mm) | a / b / c (deg) | Reached | Knee forward (mm) | Beyond face (mm) | Own / base / shell / neighbour pairs | J1 / J2 / J3 (N m), 1 kg / 4 feet |
|---|---|---|---:|---:|---|---|
| 50.0 / 50.0 | 12.0 / -57.1 / 114.2 | True | 25.2 | 20.7 | 1 / 0 / 0 / 0 | 0.058 / 0.010 / 0.070 |
| 55.0 / 55.0 | 12.0 / -51.5 / 103.1 | True | 23.5 | 19.0 | 1 / 0 / 0 / 0 | 0.060 / 0.009 / 0.066 |
| 60.0 / 60.0 | 12.0 / -45.5 / 91.1 | True | 21.4 | 16.9 | 1 / 0 / 0 / 0 | 0.063 / 0.009 / 0.060 |
| 65.0 / 65.0 | 12.0 / -38.8 / 77.6 | True | 18.8 | 14.3 | 1 / 0 / 0 / 0 | 0.065 / 0.008 / 0.053 |
| 70.0 / 70.0 | 12.0 / -30.9 / 61.9 | True | 15.4 | 10.9 | 1 / 0 / 0 / 0 | 0.068 / 0.006 / 0.043 |
| 75.0 / 75.0 | 12.0 / -20.5 / 41.1 | True | 10.5 | 6.0 | 0 / 0 / 0 / 0 | 0.071 / 0.004 / 0.029 |

| Additional stance measurement | Model |
|---|---:|
| Requested range (mm) | 50.0 to 60.0 |
| Achievable height at c in [0, 130] (mm) | 42.3 to 79.0 |
| Straight leg at stance spread (mm) | 79.0 |
| Reference a / b / c (deg) | 12.0 / -35.0 / 70.0 |
| Reference under shell / overall (mm) | 67.5 / 179.5 |
| Lowest non-foot solid | lower_plate_in |
| Its floor clearance (mm) | 2.6 |
| Base mass (g) | 47.4 |

| Picture reference comparison | Model (mm) | ASSUMED reference (mm) | Difference (mm) |
|---|---:|---:|---:|
| visible_base_below_shell | 27.0 | 15.0 | 12.0 |
| track_width_at_feet | 97.1 | 115.0 | -17.9 |
| width_across_hips | 239.7 | 100.0 | 139.7 |

Height-sweep loads and stall shares use the 1.0 kg reference mass and four feet.

| Height (mm) | Load per foot (N) | J1 / J2 / J3 stall share |
|---|---:|---|
| 50.0 | 2.452 | 11% / 2% / 14% |
| 55.0 | 2.452 | 12% / 2% / 13% |
| 60.0 | 2.452 | 12% / 2% / 12% |
| 65.0 | 2.452 | 13% / 1% / 10% |
| 70.0 | 2.452 | 13% / 1% / 8% |
| 75.0 | 2.452 | 14% / 1% / 6% |

#### Static holding torques

| Pose | Mass table | Feet | Load per foot (N) | J1 (N·m) | J2 (N·m) | J3 (N·m) | J1 / J2 / J3 stall share |
|---|---|---:|---:|---:|---:|---:|---|
| stance | reference_mass, 1000.0 g | 4 | 2.452 | 0.060 | 0.009 | 0.066 | 12% / 2% / 13% |
| stance | reference_mass, 1000.0 g | 3 | 3.269 | 0.080 | 0.013 | 0.088 | 15% / 2% / 17% |
| stance | reference_mass, 1000.0 g | 2 | 4.903 | 0.120 | 0.019 | 0.131 | 23% / 4% / 25% |
| stance | model_mass, 1092.2 g | 4 | 2.678 | 0.066 | 0.010 | 0.072 | 13% / 2% / 14% |
| stance | model_mass, 1092.2 g | 3 | 3.570 | 0.088 | 0.014 | 0.096 | 17% / 3% / 18% |
| stance | model_mass, 1092.2 g | 2 | 5.355 | 0.131 | 0.021 | 0.144 | 25% / 4% / 28% |
| reference_pose | reference_mass, 1000.0 g | 4 | 2.452 | 0.067 | 0.007 | 0.048 | 13% / 1% / 9% |
| reference_pose | reference_mass, 1000.0 g | 3 | 3.269 | 0.089 | 0.009 | 0.064 | 17% / 2% / 12% |
| reference_pose | reference_mass, 1000.0 g | 2 | 4.903 | 0.133 | 0.014 | 0.096 | 26% / 3% / 19% |
| reference_pose | model_mass, 1092.2 g | 4 | 2.678 | 0.073 | 0.008 | 0.053 | 14% / 1% / 10% |
| reference_pose | model_mass, 1092.2 g | 3 | 3.570 | 0.097 | 0.010 | 0.070 | 19% / 2% / 13% |
| reference_pose | model_mass, 1092.2 g | 2 | 5.355 | 0.146 | 0.015 | 0.105 | 28% / 3% / 20% |

#### Stance interferences and floor contact

The first table uses the same cross-frame pairs and intentional-contact skips as the sweep.

| Pair | Class | Overlap (mm³) |
|---|---|---:|
| upper_idler_plate / carrier_horn_plate | own_leg | 33.6 |

| Non-foot solid below the prescribed foot floor | Signed clearance (mm) |
|---|---:|
| None | — |

The following exhaustive stance check includes pairs carried together in one rigid frame, the static parts and the neighbour envelopes. Its scope exceeds the sweep pair set.

| All-part stance overlap | Volume (mm³) | Intentional skipped contact, when declared |
|---|---:|---|
| carrier_horn_plate / upper_idler_plate | 33.6 | — |
| knee_mount / knee_bearing_out | 1.5 | — |
| pulley_hip / belt | 339.3 | belt envelope on pulley |
| pulley_knee / belt | 339.3 | belt envelope on pulley |
| pulley_knee / knee_shaft | 117.8 | nominal shaft through bearing/pulley/plate |
| belt / knee_shaft | 58.9 | — |
| upper_tie / knee_shaft | 589.0 | Nominal shaft through upper tie |
| upper_tie / knee_bearing_in | 59.8 | — |
| upper_tie / knee_bearing_out | 59.8 | — |
| lower_plate_in / knee_shaft | 39.3 | nominal shaft through bearing/pulley/plate |
| lower_plate_out / knee_shaft | 39.3 | nominal shaft through bearing/pulley/plate |
| nb_FR_carrier_horn_plate / nb_FR_upper_idler_plate | 33.6 | — |
| nb_FR_knee_mount / nb_FR_knee_bearing_out | 1.5 | — |
| nb_FR_pulley_hip / nb_FR_belt | 339.3 | — |
| nb_FR_pulley_knee / nb_FR_belt | 339.3 | — |
| nb_FR_pulley_knee / nb_FR_knee_shaft | 117.8 | — |
| nb_FR_belt / nb_FR_knee_shaft | 58.9 | — |
| nb_FR_upper_tie / nb_FR_knee_shaft | 589.0 | — |
| nb_FR_upper_tie / nb_FR_knee_bearing_in | 59.8 | — |
| nb_FR_upper_tie / nb_FR_knee_bearing_out | 59.8 | — |
| nb_FR_lower_plate_in / nb_FR_knee_shaft | 39.3 | — |
| nb_FR_lower_plate_out / nb_FR_knee_shaft | 39.3 | — |
| nb_RL_carrier_horn_plate / nb_RL_upper_idler_plate | 33.6 | — |
| nb_RL_knee_mount / nb_RL_knee_bearing_out | 1.5 | — |
| nb_RL_pulley_hip / nb_RL_belt | 339.3 | — |
| nb_RL_pulley_knee / nb_RL_belt | 339.3 | — |
| nb_RL_pulley_knee / nb_RL_knee_shaft | 117.8 | — |
| nb_RL_belt / nb_RL_knee_shaft | 58.9 | — |
| nb_RL_upper_tie / nb_RL_knee_shaft | 589.0 | — |
| nb_RL_upper_tie / nb_RL_knee_bearing_in | 59.8 | — |
| nb_RL_upper_tie / nb_RL_knee_bearing_out | 59.8 | — |
| nb_RL_lower_plate_in / nb_RL_knee_shaft | 39.3 | — |
| nb_RL_lower_plate_out / nb_RL_knee_shaft | 39.3 | — |
| nb_RR_carrier_horn_plate / nb_RR_upper_idler_plate | 33.6 | — |
| nb_RR_knee_mount / nb_RR_knee_bearing_out | 1.5 | — |
| nb_RR_pulley_hip / nb_RR_belt | 339.3 | — |
| nb_RR_pulley_knee / nb_RR_belt | 339.3 | — |
| nb_RR_pulley_knee / nb_RR_knee_shaft | 117.8 | — |
| nb_RR_belt / nb_RR_knee_shaft | 58.9 | — |
| nb_RR_upper_tie / nb_RR_knee_shaft | 589.0 | — |
| nb_RR_upper_tie / nb_RR_knee_bearing_in | 59.8 | — |
| nb_RR_upper_tie / nb_RR_knee_bearing_out | 59.8 | — |
| nb_RR_lower_plate_in / nb_RR_knee_shaft | 39.3 | — |
| nb_RR_lower_plate_out / nb_RR_knee_shaft | 39.3 | — |

#### Sweep pair classes

| Class | Tested pairs | Pairs colliding somewhere | Pair-pose collisions |
|---|---:|---:|---:|
| own_leg | 237 | 5 | 230 |
| base | 69 | 4 | 140 |
| shell | 23 | 7 | 174 |
| neighbour | 1863 | 17 | 144 |

Clear poses are recorded without truncation in `exports/l03-base-proximal/geometry-check.json` under `sweep.clear_poses_deg` and `sweep.clear_poses_ignoring_neighbours_deg`. Each tested pair records its exact minimum distance, minimizing pose, overlap maximum, collision count and all colliding pose indices, with up to eight volume examples.

| Intentional pair skipped | Reason |
|---|---|
| belt / pulley_hip | belt envelope on pulley |
| belt / pulley_knee | belt envelope on pulley |
| carrier_horn_plate / j2_actuator | Carrier inner face on flat J2 case end face |
| carrier_hub_horn / j1_actuator_horn | J1 hub on boss |
| carrier_hub_idler / j1_actuator_idler | J1 hub on boss |
| carrier_idler_plate / j2_actuator | Carrier inner face on flat J2 case end face |
| j2_actuator_horn / upper_horn_plate | plate on J2 boss |
| j2_actuator_idler / upper_idler_plate | plate on J2 boss |
| knee_actuator_idler / upper_horn_plate | Proximal idler on mounting thigh outer face |
| knee_bearing_in / knee_shaft | nominal shaft through bearing/pulley/plate |
| knee_bearing_in / upper_idler_plate | bearing in matching OD plate hole |
| knee_bearing_out / knee_shaft | nominal shaft through bearing/pulley/plate |
| knee_bearing_out / upper_horn_plate | bearing in matching OD plate hole |
| knee_shaft / lower_plate_in | nominal shaft through bearing/pulley/plate |
| knee_shaft / lower_plate_out | nominal shaft through bearing/pulley/plate |
| knee_shaft / pulley_knee | nominal shaft through bearing/pulley/plate |
| knee_shaft / upper_horn_plate | nominal shaft through bearing/pulley/plate |
| knee_shaft / upper_idler_plate | nominal shaft through bearing/pulley/plate |
| knee_shaft / upper_tie | Nominal shaft through upper tie |

Neutral all-pair overlaps total 43. Neutral inside-shell volumes total 0. Full names, volumes and Z ranges are in the geometry report. Carrier web and upper web are absent. The J2 case clamped between the carrier plates provides their tie.

### L02 comparison

| L02 comparison | Value |
|---|---:|
| overall_height_mm | 223.8 |
| clock_bottom_clearance_mm | 111.8 |
| leg_mass_g | 97.1 |
| stance_width_mm | 129.8 |
| total / colliding poses | 175 / 175 |

These numbers were read from `exports/l02-A-under-direct/geometry-check.json`. Its SHA-256 is recorded in `exports/l03-summary.json` and its contents remained unchanged.

## Independent estimates

| Direct quantity | Brief estimate | Model | Difference |
|---|---:|---:|---:|
| stance_b_deg | -50.6 | -50.6 | 0.0 |
| stance_c_deg | 101.2 | 101.2 | -0.0 |
| straight_under_shell_mm | 78.2 | 78.2 | 0.0 |
| reference_under_shell_mm | 66.7 | 66.7 | 0.0 |
| height70_c_deg | 59.0 | 58.9 | -0.1 |

All direct estimates agree within the specified 1.5 mm or 1.5° tolerance. The posed P2 at a = 12.0° is (32.0, 56.8, -7.0) mm.

For the direct variant let theta=c/2 and hold a fixed. P5z=z1+s*d*sin(a)-(L1+L2+radius)*cos(theta)*cos(a). The foot bbox minimum is P5z-(D/2)*abs(sin(a))-radius*abs(cos(a)). Each reported height and solve uses the posed BRep bounding box.

## Interpretations and departures

- The proximal foot uses the required span between the outer lower-plate faces. This places its centroid 18.0 mm along the axis from P5. The five-pose rigid-centroid check therefore uses P5 plus that axial midpoint offset. The literal centroid-to-P5 error is also recorded and is 18.0 mm. The direct foot is symmetric about P5 and satisfies the literal comparison.
- The carrier neck ends at the J2 inboard case face. Its end rectangle occupies the case Y span, and its plates touch the case X end faces. No carrier web was added.
- The proximal thigh plates retain the L02 bearing OD holes required by the carried-over proximal construction. The lower plates end flat at P4 and have no end discs or lower web.
- The supplied L02 template is read without modification. Generated HTML has the L03 title, one-decimal displayed angles, continuous slider values and the solved stance embedded as its start and stance-button pose.
- The prescribed foot supports and four-foot stability calculations remain reported even when another solid reaches below the foot floor. Their ground-contact qualification is shown alongside them.
- The startup law-file read was truncated by tool output limits and is unproved. The closed headless task governed the file scope and workflow. Brain freshness was not established or claimed.

## OPEN

- Direct stance has the measured carrier/thigh overlap and a shank channel below the prescribed floor. The geometry and parameters retain those findings.
- The design session must rule on the proximal P5 axis-point versus foot-centroid convention and its measured 18.0 mm axial offset.
- Four-foot margins and lifted-leg margins depend on the ASSUMED retained-clock mass, payload, battery masses and placements. The shell interior remains unmeasured.
- Both variants have greater base height and hip width than the picture references. Their contact tracks are narrower than the reference. The actuator axis offset and boss envelopes retain their supplied RECALLED or proposed provenance.
- Browser rendering and interaction proofs remain unrun for the caller.

## Files and preservation

- `leg_base_packaging.py` implements the new generator and imports the existing read-only actuator/posing helpers.
- `exports/l03-base-direct/` and `exports/l03-base-proximal/` each contain the STEP, geometry report and embedded preview.
- `exports/l03-summary.json` contains both full variants, height rows, torques, support, pair-class counts and the read-only L02 comparison.
- Scratch command, verification and input-preservation receipts are under `runtime/cad/`.

The parameter file, L02 generator, viewer template, L02 brief and L02 comparison geometry report all matched their pre-build SHA-256 values. All task writes stayed in the authorized new CAD paths and CAD runtime scratch. No commits, pushes, browser launches or GUI launches were performed.

STATE: — DONE — Both variants built headlessly with the proximal centroid check including its 18.0 mm axial offset and browser proofs unrun.
