# M.A.C. Model 04 — software workspace

The [desktop preview](desktop/README.md) is the first runnable Mack interface. It uses original HTML, CSS, JavaScript, and SVG with no third-party frontend packages. The project-root **Start Mack.command** launcher serves it on loopback and opens a browser. Imported source remains reference code, not installed services.

Bill confirmed **Mack's own complete system on Linux** on 2026-10-20. The desktop belongs to a larger device stack: runtime, durable memory, voice/AI, perception, motion supervision, independent body firmware, and a bootable/recoverable Linux deployment. See the [product definition](../docs/product-spec.md) and [architecture](../docs/architecture.md). Local conversation and durable memory now run on the Mac. Perception, motion, project bridges and the Linux device image remain to be built.

| Component | Responsibility | Starting material |
| --- | --- | --- |
| Classic shell | Working menus, windows, real conversation, memory editing, and expression previews. | [Original desktop implementation](desktop/). |
| Voice/conversation | Local Qwen3-ASR input, Ollama inference and approved reference speech output. | [Local runtime](mack/runtime.py); Qwen3.6:35b is the initial installed model. |
| Memory adapter | SQLite conversation archive and explicit facts, edits/Trash and bounded retrieval. Continuum bridge remains proposed. | [Local runtime](mack/runtime.py); [Continuum reference](../vendor/continuum-hexapod/continuum/). |
| Motion supervisor | Validate bounded requests; default to mock hardware. | [Continuum spine](../vendor/continuum-hexapod/spine/) and tests. |
| Mack body adapter | Implement this body's controller commands and geometry. | [Interface reference](../vendor/continuum-hexapod/hand/hand_interface.py). |
| Clock controls | Dial/button events and brightness. | [Macintosh Mini controls](../vendor/macintosh-mini/maclock-build/), after GPIO review. |
| Optional legacy bridge | Shared-folder connection to a guest Mac. | [AgentBridge server](../vendor/agentbridge/src/) and protocol; deferred. |

Real conversation and lasting memories now work on the host through Mack Local AI 0.3. Facts and all completed exchanges persist independently of model weights; only explicit Remember requests or the memory editor create facts. The next work covers the mock body contract, everyday spoken-input trials and measured model evaluation. Read the [model and service strategy](../docs/model-strategy.md) for upgrade and cross-project boundaries. No live motor driver or cross-project bridge is implied by this host prototype.

The [Continuum tests](../vendor/continuum-hexapod/tests/) cover memory, validation, mock hardware, and simulation. They are retained at the same source revision and have not been run for this import. Its requirements are upstream's, not a Mack dependency lock.

Its brain uses an Anthropic API and its hardware adapter targets a Freenove hexapod. Those are prior-project choices. Adapt only the parts that fit Mack after tests. No old deployment scripts are installed or launched.

Use project-local ignored environments for later evaluation. Keep recordings, memory databases, credentials, and Apple media outside the tracked tree.
