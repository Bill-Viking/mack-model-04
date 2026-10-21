# M.A.C. Model 04 — software workspace

The [desktop preview](desktop/README.md) is the first runnable Mack interface. It uses original HTML, CSS, JavaScript, and SVG with no third-party frontend packages. The project-root **Start Mack.command** launcher serves it on loopback and opens a browser. Imported source remains reference code, not installed services.

| Component | Responsibility | Starting material |
| --- | --- | --- |
| Classic shell | Working menus, windows, conversation preview, notes, and expression previews. | [Original desktop implementation](desktop/). |
| Voice/conversation | Local scripted replies and optional local browser speech output; live AI and microphone input deferred. | [Conversation model](desktop/model.mjs); provider not selected. |
| Memory adapter | Persist and recall facts. | [Continuum memory](../vendor/continuum-hexapod/continuum/). |
| Motion supervisor | Validate bounded requests; default to mock hardware. | [Continuum spine](../vendor/continuum-hexapod/spine/) and tests. |
| Mack body adapter | Implement this body's controller commands and geometry. | [Interface reference](../vendor/continuum-hexapod/hand/hand_interface.py). |
| Clock controls | Dial/button events and brightness. | [Macintosh Mini controls](../vendor/macintosh-mini/maclock-build/), after GPIO review. |
| Optional legacy bridge | Shared-folder connection to a guest Mac. | [AgentBridge server](../vendor/agentbridge/src/) and protocol; deferred. |

Screen states and typed demo replies now work on the host. Notes persist in browser storage, independently of the imported Continuum database. The next step is a live conversation adapter, then a microphone-to-response path. Keep motors disconnected from that prototype.

The [Continuum tests](../vendor/continuum-hexapod/tests/) cover memory, validation, mock hardware, and simulation. They are retained at the same source revision and have not been run for this import. Its requirements are upstream's, not a Mack dependency lock.

Its brain uses an Anthropic API and its hardware adapter targets a Freenove hexapod. Those are prior-project choices. Adapt only the parts that fit Mack after tests. No old deployment scripts are installed or launched.

Use project-local ignored environments for later evaluation. Keep recordings, memory databases, credentials, and Apple media outside the tracked tree.
