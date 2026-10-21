# M.A.C. Model 04 — build roadmap

The accepted four-leg concept is the visual target. Each milestone earns the next hardware or integration decision. This is dependency order, not a calendar estimate.

| Milestone | Build or learn | Done when |
| --- | --- | --- |
| 0 — Repository | Introduction, source inventory, CAD/code references, and provenance. | Source hashes verify and README explains the project. |
| 1 — Clock intake | Identify and measure the unit, mounting points, screen space, and mass. | Measurements have observations and notes; unknowns stay explicit. |
| 2 — Screen character (host preview built) | Classic menus/windows, conversation preview, saved notes, and idle/listening/thinking/speaking/resting/fault expressions. | Browser interactions checked at 1024×768, 640×480 and the narrow app panel. Actual physical display remains untested. |
| 3 — One conversation | Microphone, speech response, visible state, and one remembered fact. | A spoken request gets a response; restart preserves the fact; disconnection is visible. |
| 4 — Stationary Mac | Fit selected display, compute, microphone, audio, and reviewed power. | Shell closes without strain; voice/display work under measured power and temperature. |
| 5 — One leg | CAD around selected motors, supported joints, fasteners, and replaceable foot. | Restrained test moves a representative load with current and stopping behavior recorded. |
| 6 — Four-leg base | Use dummy mass matching the Mac and battery. | Base stands, steps, and stops within a tested envelope. |
| 7 — Companion | Mount Mac and connect status, bounded behavior, and personality. | It responds, remembers, and moves; interruption cases are demonstrated. |
| Optional — Vintage apps | Separate OS 9.0.4 emulator and possibly AgentBridge. | Selected apps work without making voice or motor control depend on the emulator. |

Clock intake and the screen prototype can progress independently. CAD for the legs depends on measured geometry and selected actuators. The existing bezel is printable reference material; the robot picture does not contain printable leg geometry.

Immediate design work: try the [desktop preview](../software/desktop/README.md), connect a live conversation adapter and microphone input, populate the [measurement sheet](../hardware/measurements.csv), sketch packaging and a mass budget, and evaluate the imported Continuum mock tests.

No purchase-ready BOM, leg CAD, deployment script, or live Mack motor driver is implied by this foundation.
