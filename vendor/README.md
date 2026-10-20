# Upstream snapshots and notices

These are selected reference files, copied unchanged at the revisions in [SOURCES.json](../SOURCES.json). They are not installed or wired into a Mack runtime. Each source has its own SOURCE.md explaining scope and omissions.

| Snapshot | License recorded from upstream |
| --- | --- |
| [WonderMac](wondermac/SOURCE.md) | GPL v2 as declared in its README; LICENSE retained. |
| [Macintosh Mini](macintosh-mini/SOURCE.md) | Hardware: CERN-OHL-S-2.0. Control software: GPL-3.0-or-later. Documentation/drawings: CC-BY-SA-4.0. REUSE.toml and license texts retained. |
| [AgentBridge](agentbridge/SOURCE.md) | Modern MCP server: GPL v3. Classic client has a separate modified PolyForm Noncommercial license; only its notice is retained, not the client implementation. |
| [Continuum Hexapod](continuum-hexapod/SOURCE.md) | No upstream LICENSE found at this revision. Bill-owned local source copied at his request for this project. No public redistribution license is asserted. |

No single license is applied across these snapshots. Original M.A.C. Model 04 work has no public license selected yet. Keep copyright and source-location notices with any later adaptations under the applicable upstream terms.

Excluded from these tracked imports: Apple ROM/OS images and chimes, emulator binaries, the separately attributed Waveshare overlay, third-party render models, personal databases, credentials, machine-specific session records, and deployment scripts.

Upstream README files may link to files outside the selected subset. Those complete trees remain available in the pinned ignored checkouts or at the upstream commit links in each SOURCE.md. These notes do not silently repair or modify upstream text.

Verify exact bytes from the repo root with `python3 tools/sources.py check`. The check tolerates only these index/provenance notes in addition to the recorded upstream files.
