CHANGES REQUIRED

The build is a useful packaging study, but neither variant establishes a workable standing pose at 55 mm. The calculations largely follow the brief. The brief’s contact-point definition also needs correction before these numbers become design requirements.

**1. Did the build follow the brief?**

- **The main geometry and calculations follow it.** The base, actuator placement, 30/30 mm links, solved stance and collision reporting match the prescribed construction. Collisions are findings, not generator failures. My checks found matching current parameter and generator hashes in both geometry reports. [J04-L03-BUILD-BRIEF.md:42](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/briefs/J04-L03-BUILD-BRIEF.md:42), [leg_base_packaging.py:179](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/leg_base_packaging.py:179)
- **The proximal centroid check changes meaning.** Its foot spans −20.5 to +56.5 mm relative to P5 along the axis. Its centre is therefore 18.0 mm from P5. The reported 3.1e−14 mm error checks the correctly offset centroid; the literal centroid-to-P5 error is 18.0 mm. I accept the offset calculation as correct for the prescribed geometry, but it must remain a declared exception to the literal check. [J04-L03-BUILD-BRIEF.md:56](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/briefs/J04-L03-BUILD-BRIEF.md:56), [leg_base_packaging.py:347](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/leg_base_packaging.py:347)
- **The proximal thigh retains bearing holes.** These qualify the brief’s common thigh outline and remove approximately 0.475 g per leg compared with solid plates. This is a reasonable, disclosed interpretation of the inherited bearing construction. [leg_base_packaging.py:227](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/leg_base_packaging.py:227), [J04-L03-BUILD-BRIEF-REPORT.md:391](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/briefs/J04-L03-BUILD-BRIEF-REPORT.md:391)
- **“Clear poses” means clear within the tested moving-pair set.** It excludes overlaps between parts sharing a frame, internal overlaps in the stationary neighbours, floor penetration and continuous motion between samples. Neighbours remain at the 55 mm stance during the height sweep. Thus 21 and 25 are not counts of usable whole-robot standing or walking poses. This is a scope limitation, not a newly discovered solver failure. [leg_base_packaging.py:243](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/leg_base_packaging.py:243), [leg_base_packaging.py:394](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/leg_base_packaging.py:394), [leg_base_packaging.py:515](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/leg_base_packaging.py:515)

**2. Independent calculation: the model agrees with the brief’s chain.**

Source: [J04-L03-BUILD-BRIEF.md:50](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/briefs/J04-L03-BUILD-BRIEF.md:50), [j04-l03.base-short.json:58](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/j04-l03.base-short.json:58).

I ran a separate standard-library script with the designated Python interpreter and `-B`. It imported no generator code and wrote no files. All calculations retained full floating-point precision.

For direct, with \(a=12°\), \(\theta=c/2\), and \(b=-\theta\):

\[
H=14-20.5\sin(a)+65\cos(\theta)\cos(a)+5\cos(a).
\]

The −20.5 term combines the 33.5 mm hip offset and the foot’s −13 mm lower axis end.

| Quantity | Independent result |
|---|---:|
| P2, mm | (32.000000000000, 56.767944624582, −7.034958357605) |
| Solved direct stance, degrees | 12 / −50.581870962393 / 101.163741924787 |
| Direct straight-leg height, mm | 78.208142389602 |
| Proximal stance, degrees | 12 / −51.545380925192 / 103.090761850383 |
| Proximal straight-leg height, mm | 79.039789152873 |
| Direct load, 1 kg / four feet, N | 2.451662500000 |
| Direct J1 / J2 / J3, N·m | 0.070199047550 / 0.009263006171 / 0.064841043196 |
| Direct stall shares, percent | 13.499816836622 / 1.781347340556 / 12.469431383889 |

Direct knee-angle disagreement is only 4.8e−10 degrees; torque disagreement is below 2.3e−13 N·m. The model is right against the specified chain.

**The contact rule itself is geometrically approximate.** It combines the axis endpoint’s Y with the cylinder surface’s lowest Z. The actual lowest rim point lies another \(r\sin(a)=1.039558454089\) mm outward. Correcting this changes direct track from 105.3 to **107.3 mm** and J1 torque from 0.070199 to **0.072748 N·m**. J2 and J3 remain unchanged. The proximal track becomes **99.2 mm**. These remain hypothetical foot reactions where the direct channel touches first. [J04-L03-BUILD-BRIEF.md:158](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/briefs/J04-L03-BUILD-BRIEF.md:158), [leg_base_packaging.py:541](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/leg_base_packaging.py:541)

**3. The numerical height requirement is met; the standing configuration is not.**

Source: [direct geometry-check.json:35797](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/exports/l03-base-direct/geometry-check.json:35797), [proximal geometry-check.json:53947](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/exports/l03-base-proximal/geometry-check.json:53947).

Both solve to 55.0 mm under the shell and 167.0 mm overall, at the angles above.

- **Direct:** `shank_channel_plus` extends **1.0716 mm below the foot**. The actual lowest solid is at −56.0716 mm. Resting on that solid would put the shell 56.1 mm above the table and the top 168.1 mm above it, while leaving the intended feet unloaded. `upper_idler_plate` overlaps `carrier_horn_plate` by **32.7913 mm³**, repeated on all four legs.
- **Proximal:** the foot is lowest; the nearest non-foot part clears it by **2.5703 mm**. The carrier/thigh overlap is **33.6364 mm³** per leg. Additional undeclared-as-intentional overlaps include mount/bearing **1.5 mm³**, belt/shaft **58.9 mm³**, and tie/bearing **59.8 mm³ on each side**. Some arise from coarse envelopes, but none establishes a finished fit.

The stance has no reported moving-pair collisions with the base, shell or neighbours. That does not cancel the own-leg interference. [direct geometry-check.json:35839](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/exports/l03-base-direct/geometry-check.json:35839), [J04-L03-BUILD-BRIEF-REPORT.md:143](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/briefs/J04-L03-BUILD-BRIEF-REPORT.md:143), [J04-L03-BUILD-BRIEF-REPORT.md:275](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/briefs/J04-L03-BUILD-BRIEF-REPORT.md:275)

**4. Lower height costs knee bend, knee torque and forward projection.**

Source: [direct geometry-check.json:35961](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/exports/l03-base-direct/geometry-check.json:35961). Torque shares below use 1 kg and four feet.

| Under shell, mm | Knee bend | Knee stall share | Beyond face, mm | Tested own-leg overlaps |
|---:|---:|---:|---:|---:|
| 50 | 112.4° | 13% | 27.2 | 1 |
| 55 | 101.2° | 12% | 25.8 | 1 |
| 60 | 88.9° | 11% | 23.8 | 1 |
| 65 | 75.2° | 10% | 21.0 | 1 |
| 70 | 58.9° | 8% | 17.1 | 1 |
| 75 | 36.6° | 5% | 10.8 | 0 |

**75 mm is the lowest sampled direct pose I would carry as a provisional workable stationary pose.** It is not an accepted replacement for the owner’s requirement. It stands 187.0 mm overall, 15 mm above the allowed under-shell maximum.

My independent channel calculation gives 5.8532 mm floor clearance there. It crosses zero at 59.3976 mm; at 60 mm it clears by only 0.1581 mm, and the carrier/thigh overlap remains. Floor clearance alone therefore cannot rescue the requested range.

The exact lowest collision-free height between 70 and 75 mm was not established. Nor was a complete four-leg clearance margin at 75 mm. The proximal version’s fixed internal overlaps prevent treating its zero moving-pair count at 75 mm as an assembled fit. [leg_base_packaging.py:233](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/leg_base_packaging.py:233), [leg_base_packaging.py:737](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/leg_base_packaging.py:737)

**5. Height improves substantially; the base and hips still miss the picture.**

Source: [j04-l03.base-short.json:13](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/j04-l03.base-short.json:13), [l03-summary.json:263](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/exports/l03-summary.json:263), [l03-summary.json:821](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/exports/l03-summary.json:821). I inspected `concepts/raycue-build-target.png`; its dimensional references remain ASSUMED, with roughly 20% uncertainty.

| Measure | Picture reference | Direct | Proximal | Main drivers |
|---|---:|---:|---:|---|
| Under-shell height | 55 mm | 55.0 | 55.0 | Link lengths, hip Z, foot geometry and solved bend |
| Visible base | 15 mm | 27.0 | 27.0 | 3 + 22 + 2 mm stack; `z_top=0` |
| Hip width | 100 mm | 158.5 | 239.7 | P1 Y=24, lateral offsets 33.5/37, actuator depth, bosses and plates |
| Foot track, brief convention | 115 mm | 105.3 | 97.1 | Spread, height, lateral offset and lower foot-axis endpoint |

The direct hips are **58.5% wider** than the reference; proximal hips are **139.7% wider**. Both are well beyond the picture estimate’s stated uncertainty. The track shortfalls are within that rough uncertainty.

The base plates are only 56 mm wide, but that does not describe the mechanism’s width. Narrowing those plates alone cannot remove the actuator stack outside them. The proximal outboard motor, pulley and lower-plate spacing compound the problem.

The 27 mm base follows the earlier review’s proposed **25–30 mm** study, even though it exceeds the picture’s 15 mm reference. That conflict needs an explicit choice. A 20 mm-tall actuator cannot fit inside a wholly external 15 mm base merely by thinning its plates. [docs/review/design-review-2026-11-11.md:43](/Users/bill/Projects/RayCue%20Mac/docs/review/design-review-2026-11-11.md:43), [j04-l03.base-short.json:27](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/j04-l03.base-short.json:27)

**6. Hip-spread torque improves, but this is not actuator qualification.**

Source: [docs/review/design-review-2026-11-11.md:65](/Users/bill/Projects/RayCue%20Mac/docs/review/design-review-2026-11-11.md:65), [direct geometry-check.json:36211](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/exports/l03-base-direct/geometry-check.json:36211).

| Feet sharing 1 kg | Earlier review J1 | L03 direct, brief contact | L03 direct, corrected rim contact |
|---:|---:|---:|---:|
| 4 | 17% | 13% | 14% |
| 3 | 22% | 18% | 19% |
| 2 | 33% | 27% | 28% |

The improvement comes from reducing the nominal lateral reaction arm from about 35 mm to **28.6332 mm**, or **29.6728 mm** at the actual cylinder rim.

The knee moves in the opposite direction: the four-foot value rises from the earlier **0.042 N·m** to **0.064841 N·m**, about 54% more. Shorter standing height has redistributed load.

These are external vertical-force estimates. They omit motion, joint friction, transmission losses and full link-gravity torque accounting. A stall percentage does not establish continuous holding ability.

**7. Four-foot stability is conditional; lifting a foot has no reserve.**

Source: [direct geometry-check.json:36536](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/exports/l03-base-direct/geometry-check.json:36536), [proximal geometry-check.json:54713](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/exports/l03-base-proximal/geometry-check.json:54713).

Direct margins are **28.1 mm fore/aft** and **52.6 mm sideways**, with CoM **75.6 mm above the prescribed floor** and tip angle **20.4°**. Proximal gives **28.1/48.5 mm**, CoM height **73.4 mm**, and **20.9°**. Correcting rim contact adds 1.04 mm to each sideways margin; it does not improve the limiting fore/aft margin.

Every lifted-foot margin is **0.0 mm**. The centred CoM lies exactly on the remaining triangle’s diagonal edge. This is a balance boundary, not a crawl margin.

Moreover, three equal foot forces cannot balance this centred configuration: the two diagonal contacts must carry the weight while the third carries zero in the ideal static case. The three-foot torque row is therefore an assumed loading example, not the equilibrium of the reported stance.

The most consequential assumptions are:

- **Horizontal mass placement**, because any small shift can make a zero lifted-foot margin negative.
- **Retained clock and payload mass/height:** together 454 g, about 46% of direct total mass.
- **Battery placement:** lower leverage on CoM than the clock/payload, but its proposed position is inside an unmeasured shell.

For scale, moving the assumed payload 20 mm shifts total CoM by **4.6 mm** along that direction. Lowering it 20 mm raises the nominal four-foot tip angle only to **21.6°**; it does not create three-foot margin without a horizontal shift. [j04-l03.base-short.json:111](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/j04-l03.base-short.json:111)

**8. Keep direct as the next baseline; the current belt layout does not justify a redraw.**

Source: [direct geometry-check.json:34625](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/exports/l03-base-direct/geometry-check.json:34625), [proximal geometry-check.json:52407](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/exports/l03-base-proximal/geometry-check.json:52407), [leg_base_packaging.py:596](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/leg_base_packaging.py:596).

| Measure | Direct | Belt |
|---|---:|---:|
| Leg mass, including fixed J1 group and allowances | 90.5 g | 118.2 g |
| Robot mass | 981.5 g | 1,092.2 g |
| Mass moving about J2 | 35.3 g | 62.7 g |
| Neutral J2 lumped inertia | 48,835.7 g·mm² | 60,640.6 g·mm² |
| Stance J2 lumped inertia | 31,332.6 g·mm² | 39,797.5 g·mm² |
| Stance overall width | 158.7 mm | 249.8 mm |
| Tested clear poses | 21/175 | 25/175 |

The belt adds **110.7 g per robot**, increases reported stance inertia **27.0%**, and gains only four clear samples. Its advantages are foot clearance and **6.8 mm less forward projection** at 55 mm.

The supplied description’s **249.8 mm “neutral” width is mislabeled**: it is the stance width. Mirroring the neutral leg extents gives **235.0 mm** for proximal and **149.0 mm** for direct. [proximal geometry-check.json:51061](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/exports/l03-base-proximal/geometry-check.json:51061)

These inertia values use centroid point masses, not complete solid inertia tensors or reflected motor inertia. They do not prove dynamic performance. They do show that the intended hip-swing inertia benefit has not appeared in this comparison.

**9. Three changes should govern the next iteration.**

1. **Make the 55 mm direct stance physically possible and report true contact.** Rework the carrier/thigh junction and shank termination. Move the **32.8 mm³ overlap to zero**, and the **−1.1 mm floor clearance to at least +1.5 mm** as a proposed clearance target. Re-solve height after changes and replace the axis-end contact approximation. [direct geometry-check.json:35839](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/exports/l03-base-direct/geometry-check.json:35839), [direct geometry-check.json:36609](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/exports/l03-base-direct/geometry-check.json:36609)
2. **Repackage the actuators around the required silhouette.** Move direct hip width **158.5 mm toward the 100 mm reference**, and visible base **27 mm toward 15 mm**. These are packaging targets, not demonstrated feasible edits. They require a changed actuator arrangement, smaller benchmark, or verified shell space; reducing plate thickness alone cannot deliver them. [j04-l03.base-short.json:20](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/j04-l03.base-short.json:20), [j04-l03.base-short.json:39](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/j04-l03.base-short.json:39)
3. **Design weight transfer before calling the pose walkable.** Introduce a body shift or revised contact placement before each lift. Move the minimum three-foot margin from **0.0 mm to a proposed +5 mm**, then calculate equilibrium foot loads and joint torques for that configuration. Lowering CoM helps tipping resistance but cannot replace the shift. [leg_base_packaging.py:619](/Users/bill/Projects/RayCue%20Mac/hardware/joints/cad/leg_base_packaging.py:619)

**FOR THE OWNER:**

The model reaches 55 mm under the shell, but neither version can stand as drawn. The direct leg bends its knee 101°, has plates overlapping, and puts a shank plate 1.1 mm below the foot. Its hips span 158.5 mm against the picture’s roughly 100 mm. The first promising sampled standing height is 75 mm, outside your chosen range. The belt version adds 110.7 g, spreads to 249.8 mm, and has higher reported swing inertia. Keep the direct layout as the starting point. Fix its contact and interference, narrow the mechanism, and give it a positive balance margin before lifting a foot.

**RULINGS NEEDED:**

- **Which height governs the next design?** Keep 55 mm, allowing 50–60 **[PICK]** / Accept 75 mm. Why: 75 mm eases this mechanism but changes the owner’s chosen proportions.
- **Which appearance goal governs actuator packaging?** Pursue roughly 15 mm visible base and 100 mm hip width **[PICK]** / Accept the current 27 mm base and 158.5 mm direct hips. Why: the current benchmark arrangement cannot be treated as matching the picture.
- **Which knee layout gets the next detailed build?** Direct **[PICK]** / Belt. Why: the present belt adds mass, width and reported inertia without removing the shared stance interference.

**LIMITS:**

- Independently run here: full-precision chain/height/torque arithmetic; cylinder-contact correction; direct channel-clearance calculation; mass/CoM summation; sweep-count reconciliation; selected summary-to-report comparisons; current parameter/generator hash comparisons; source and reference-image inspection.
- Generator builds, BRep overlap calculations, STEP re-imports and the builder’s verifier were **not rerun**. Their exit codes, 80/112 valid solids and centroid proof results are reported evidence, not new proofs from this review.
- Browser proofs are **UNRUN HERE**. The caller supplied evidence of captures showing shell, base and four legs. Slider operation and console behaviour were not independently checked.
- Physical fit, measured shell space, structural strength, actuator continuous duty, full dynamic inertia, gait feasibility and the exact minimum workable height remain unverified.
- Historical input preservation and commit contents were not independently audited. Brain freshness was not established or claimed.
- No files were edited. This final message is the verdict for launcher offload to `hardware/joints/cad/briefs/J04-L03-REVIEW-BRIEF-VERDICT.md`.

DONE J04-L03 — review brief: — REVISE — Retain the numerical study, but correct contact geometry and resolve stance interference, proportions and lifted-foot stability before accepting the 55 mm design.
