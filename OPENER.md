lane: RayCue/Research
written: 2026-10-20T20:44:11-07:00
by: ACT — RayCue/Research: Mac OS 9 and walking robot
on: MAC
head: 908c09c
status_updated: 2026-10-20T20:44:11-07:00
where: Mack desktop runs locally; live AI and microphone connection next
next: bill
depends_on: nothing for trying the desktop; exact clock measurements for fitted hardware
open_in: /Users/bill/Projects/RayCue Mac · reuse RayCue Mac · ACT — RayCue/Research: Mac OS 9 and walking robot · existing chat or fresh session
judgment: Choose the live conversation adapter and privacy behavior; engineer hardware from measured loads
model: Not reselected; preserve the user's choice and read the live dial
---
read the project status/memory first. Read software/desktop/README.md for the runnable preview and its verification, then README.md, docs/architecture.md and docs/roadmap.md for the whole robot.

WHERE WE ARE

M.A.C. Model 04 is **Mack**, an intelligent companion in Bill’s RayCue Macintosh-shaped clock. The accepted target is the beige Mac body on four short articulated legs. The classic desktop is its personality; authentic vintage apps are optional. Do not re-ask those decisions.

1. The private repository https://github.com/Bill-Viking/mack-model-04 contains the project foundation and pinned source library. The hub confirmed GitHub transport; RAY-TX-001 remains historical.
2. **Mack Desktop Preview 0.1 is built.** It runs in a browser at http://127.0.0.1:9844/. The project-root Start Mack.command starts the loopback server and opens the browser with no package installation. It requires Python 3.
3. Menus, movable/resizable windows, notes, recoverable Trash, desktop preferences, scripted replies, optional local browser speech, and six expression previews work. AI, microphone input, and motors are not connected. Saved notes stay in that browser; conversation resets on reload.
4. Eight JavaScript and eleven Python tests passed; all 93 imported hashes match. The browser checks covered persistence, recovery, speech events, expressions, window controls, keyboard menus and three viewport sizes. Screenshot: docs/images/mack-desktop-preview.png. Speech sound quality and the physical display need human assessment.

Bill’s next move is to try Mack and judge its look and feel. The next machine work is a provider-neutral live conversation adapter, then microphone input and real connection/error states. No AI provider or credential has been selected. Keep the deterministic demo available and label it honestly.

The desktop server was deliberately left running for Bill’s trial (PID 39534, exec session 66162, 127.0.0.1:9844 at verification). Check it rather than trusting a carried PID. The browser tab was marked as a deliverable. The launcher reuses an existing server from this checkout; there is no installed login item or scheduled task. Voice is off and the desktop periwinkle after QA. A disposable test note is in the browser’s recoverable Trash.

Clock identification/measurements remain necessary for fitted hardware. No motors, emulator, upstream installer, or imported robot runtime were started. The loose PNG at the project root remains untouched and untracked. The chat stays active.
