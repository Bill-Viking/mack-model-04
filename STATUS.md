# STATUS — RayCue Mac

## Now

HANDOFF CAPTURE (hub button-up 2026-10-19, mechanical — verbatim tail, no model read): codex rollout-2026-10-19T10-43-29-01a15542-e3b4-7723-a847-ad64a8445eba · last message 2026-10-19T11:16:58-07:00
  the thread's own title: ACT — RayCue/Research: Mac OS 9 and walking robot
  lane RayCue/Research (the folder's only lane) · ASTRA · 470.9 min ago at the capture
  the repo, read before this capture: 1 untracked, not carried: ChatGPT Image Oct 19, 2026, 11_03_05 AM.png
  the last exchange, verbatim:
  --- [2026-10-19T18:12:52.469Z] USER
  that's what i wnat ot build.... what kidn of 3d priter woudo I need to make these parts

  --- [2026-10-19T18:13:24.461Z] ASSISTANT
  **RAYCUE MAC** · `MAC · ASTRA`

  I’ll check which printers and materials fit these parts, including the leg housings, joints, and mounting base.

  --- [2026-10-19T18:15:37.677Z] ASSISTANT
  A regular filament printer can make the housings and brackets for this. I’d lean toward the Bambu A1 for its larger print area, using PETG for structural prototypes and flexible TPU for the feet. The moving joints would also use purchased motors, bearings, and fasteners.

  --- [2026-10-19T18:16:58.156Z] ASSISTANT
  **RAYCUE MAC** · `MAC · ASTRA`

  **You need a desktop filament printer—called FDM. My pick for this project would be the Bambu Lab A1.**

  It has automatic calibration, a **256 × 256 × 256 mm printing space**—about 10 inches each way—and supports the three plastics we’d start with. That gives us room to print the legs, mounting base, and covers as separate pieces. [Bambu A1](https://us.store.bambulab.com/products/a1)

  Here’s how I’d make the parts:

  | Part | Starting material |
  |---|---|
  | Early shapes and fit checks | **PLA** — easy prototype material |
  | Beige leg housings, brackets, and base | **PETG** — a practical candidate for mechanical parts |
  | Black, flexible feet | **TPU** — rubberl …[+1005 chars]
  this block quotes; it does not explain. A session with a model may upgrade it to plain words (`buttonup.py capture --work-order`).


Research started 2026-10-19 on the Mac. Bill wants to turn his RayCue Macintosh-shaped alarm clock into an intelligent robot with a classic Mac OS appearance and personality. Walking is the eventual body goal; real vintage app use is minor. The folder was empty and was not a Git repository at arrival. No existing RayCue memory folder or competing claim was found.

Bill clarified the intended experience on 2026-10-19: a Mac OS 9 shell/wrapper over AI/robotics, then emphasized that app use would be minor and the main attraction is a cool robot that looks and seems to run a Mac OS app. Prioritize robot character, responsive voice/screen interaction and embodiment. Authentic classic app emulation is optional, deferred, and never a prerequisite or primary hardware-selection driver. Do not re-ask this settled priority.

The original conversion is ThisDoesNotCompute/wondermac. wr/macintosh-mini offers a fuller hardware reference. Real OS 9 requires the SheepShaver route (up to 9.0.4), not the default Mini vMac/Basilisk II path. The modern shell/voice/robot workload and power needs require a bench proof before final hardware selection; emulator performance only matters for the optional legacy mode. AgentBridge is a promising AI connector, but its PowerPC path is marked untested. Existing continuum-hexapod and Freenove reference repos were found locally and inspected without modification.

README.md holds the researched links, candidate parts, architecture, source discrepancies, and next steps. SOURCES.json records reference checkout revisions. No emulator, installer, AI service or hardware was run. No Apple ROM or OS disk image was obtained. Exact RayCue hardware remains unverified.

On 2026-10-19, generated and displayed the first requested walking-robot concept. Saved image and exact prompt in `concepts/`: compact ivory Mac body, four short articulated legs and a Mac OS 9-style desktop saying “Hello, Bill.” Bill then accepted the pictured direction: “that's what I want to build.” Its compact four-leg appearance is the target; dimensions, mechanisms and load capacity remain unengineered.

Bill asked which 3D printer would make these parts. Initial recommendation is a Bambu A1-class FDM printer, PLA fit prototypes, PETG housings/brackets and TPU feet. A1 mini is a conditional smaller option. README records specifications, material sources and the estimated budget; current checkout pricing could not be verified. No printer or purchase selected.

## To do

- [x] Find original and expanded clock conversion repos and build material.
- [x] Identify an OS 9 emulator and AI bridge candidates.
- [x] Find existing local robot work and public walking-control references.
- [x] Show and save a first walking RayCue / Mac OS 9 screen concept (2026-10-19).
- [ ] Confirm the exact RayCue model and inspect its exterior, label and internal hardware.
- [x] Record Bill's priority: a cool intelligent robot with a classic Mac shell; app use minor (2026-10-19).
- [ ] Define the robot character and Mac OS 9-style screen behavior; prove one responsive voice/screen interaction on a bench.
- [ ] Optional, deferred: select legacy apps/media and prove OS 9.0.4 emulation only if desired after the core robot experience.
- [ ] Choose the compute board, display, regulated power, microphone and audio after the proof and fit check.
- [ ] Establish an early robot mass, space and power budget, then build and weigh the stationary prototype.
- [ ] Select a walking platform from payload and balance measurements; test with dummy weight first.

## Important

- Research and visual concept work so far; no purchase or physical modification has been authorized by a parts selection.
- Local reference clones in `sources/` are ignored separate Git repositories. Their provenance is in SOURCES.json; recreate from upstream when absent on another machine. Do not push to vendor upstreams.
- This parent repository has no remote configured. Its research notes currently live on the Mac.
- `private-media/` is reserved and ignored for any separately supplied ROM or OS media. It is not populated.
- SheepShaver supports up to 9.0.4; Basilisk II supports up to 8.1. Some third-party guides overstate those ranges.
- AgentBridge PowerPC/SheepShaver compatibility needs actual validation. Do not treat a successful build as a runtime test.
- Macintosh Mini documents unregulated approximately 4 V Pi power and audio noise; review power and wiring before using the design. Its PCB README has a header-numbering error.
- Robot control limits, watchdog and stopping must operate independently of the AI and classic OS.
- No writes to any iCloud path. Other project repos remain untouched.
