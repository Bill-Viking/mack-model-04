lane: RayCue/Research
written: 2026-10-20T20:57:10-07:00
by: ACT — RayCue/Research: Mac OS 9 and walking robot
on: MAC
head: cad1575
status_updated: 2026-10-20T20:57:10-07:00
where: Complete Mack product defined; Linux foundation confirmed; host desktop remains runnable
next: machine
depends_on: nothing for host runtime; clock measurements for fitted electronics and mechanics
open_in: /Users/bill/Projects/RayCue Mac · reuse RayCue Mac · ACT — RayCue/Research: Mac OS 9 and walking robot · existing chat or fresh session
judgment: Implement the integrated runtime; select physical parts only against measured packaging and loads
model: Not reselected; preserve the user's choice and read the live dial
---
Read STATUS.md and docs/product-spec.md first, then docs/architecture.md, docs/roadmap.md and hardware/integration-plan.md. Read software/desktop/README.md for the runnable component.

WHERE WE ARE

Bill clarified that Mack is a complete original OS/AI/robotics product: its own operating environment, intelligence, memory, sensing, fitted electronics and four-leg body. He explicitly selected Mack's own system on Linux. Do not re-ask this choice. The new kernel option was not selected. The formal name remains M.A.C. Model 04 (Mobile Autonomous Computer); everyday name Mack. The accepted concept image remains the visual baseline.

The repository now distinguishes agreed intent, proposed engineering architecture, and built components. Product requirements P01–P10 and gates G0–G8 cover a complete personal robot and reproducible build; commercial production is a separate scope. The integration plan covers packaging zones, sensors, electrical work, structural loads and physical testing. hardware/system-budget.csv has 12 assembly rows with blank measured values, not invented ratings. No board, actuator, battery, camera, AI provider, offline model or wire protocol is selected.

NEXT MACHINE WORK

Build the G2 local Mack runtime: desktop interface, durable local memory, replaceable conversation boundary, service-state events, and explicitly simulated body. Prove requests, acknowledgments/results, expiry, cancellation and failure/recovery without live motors. Then add selected live inference and microphone capture. The future Linux device image must boot into Mack and provide installation/update recovery; it does not exist yet.

NEXT PHYSICAL INPUT

Clock model/revision, exterior dimensions and total mass, then internal clearances and retained-component masses. Use hardware/measurements.csv and system-budget.csv. CAD and motor choices depend on these values. The concept picture is not printable or load-qualified geometry. The controller's local limits and stopping must survive host/AI failure; exact deadlines and stop response require the actual body.

BUILT AND VERIFIED

Mack Desktop Preview 0.1 remains available at http://127.0.0.1:9844/. Start Mack.command launches a Python standard-library loopback server with no package install. Menus, draggable/resizable windows, browser-local notes, recoverable Trash, preferences, scripted replies, local browser speech and six labeled expression previews work. No live AI, microphone or hardware is connected. Browser notes are not the proposed device memory service.

Previous implementation validation: eight JavaScript and eleven Python tests passed, plus browser interaction checks at three viewport sizes. This documentation change checked owned links, CSV structure and all 93 imported hashes; no executable code changed. The server health endpoint still identifies mack-desktop 0.1. The session intentionally leaves it running for Bill's trial, without a login item or automation. Earlier PID 39534 is historical; verify before using it. Voice was off and a disposable test note remains in browser Trash.

The private repository is https://github.com/Bill-Viking/mack-model-04. GitHub is the hub-confirmed carrier; RAY-TX-001 is historical. Keep vendor snapshots unchanged and attributed. No hardware purchase/modification, upstream installer, emulator or motor runtime was run. The loose root PNG remains untracked and untouched. This chat stays active.
