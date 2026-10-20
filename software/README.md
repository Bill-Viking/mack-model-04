# Software workspace

No integrated RayCue runtime exists yet. This folder defines the first boundaries. Imported source is reference code, not installed services.

| Component | Responsibility | Starting material |
| --- | --- | --- |
| Classic shell | Desktop, dialog personality, listening/speaking states, faults. | Original modern UI; concept image. |
| Voice/conversation | Speech input/output and provider-neutral interaction. | No stack selected. |
| Memory adapter | Persist and recall facts. | [Continuum memory](../vendor/continuum-hexapod/continuum/). |
| Motion supervisor | Validate bounded requests; default to mock hardware. | [Continuum spine](../vendor/continuum-hexapod/spine/) and tests. |
| RayCue body adapter | Implement this body's controller commands and geometry. | [Interface reference](../vendor/continuum-hexapod/hand/hand_interface.py). |
| Clock controls | Dial/button events and brightness. | [Macintosh Mini controls](../vendor/macintosh-mini/maclock-build/), after GPIO review. |
| Optional legacy bridge | Shared-folder connection to a guest Mac. | [AgentBridge server](../vendor/agentbridge/src/) and protocol; deferred. |

First demonstrate screen states with scripted events on the host. Then connect one spoken request to an answer and show its state. Keep motors disconnected from that prototype.

The [Continuum tests](../vendor/continuum-hexapod/tests/) cover memory, validation, mock hardware, and simulation. They are retained at the same source revision and have not been run for this import. Its requirements are upstream's, not a RayCue dependency lock.

Its brain uses an Anthropic API and its hardware adapter targets a Freenove hexapod. Those are prior-project choices. Adapt only the parts that fit RayCue after tests. No old deployment scripts are installed or launched.

Use project-local ignored environments for later evaluation. Keep recordings, memory databases, credentials, and Apple media outside the tracked tree.
