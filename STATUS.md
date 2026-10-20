# STATUS — RayCue Mac

## Now

Bill's target is an intelligent walking companion made from his RayCue Macintosh-shaped alarm clock. It should look and feel like a little Mac with a Mac OS 9-style shell over modern voice, memory and robotics. Real vintage application use is minor and optional. Bill accepted the compact four-leg visual concept on 2026-10-19; the image is a target, not an engineered mechanism.

On 2026-10-20 Bill reattached the exact image and said “this is what I want to build.” Saved that attachment unchanged as concepts/raycue-build-target.png and made it the README hero and visual baseline. Preserve the dominant beige Mac body, compact underside base, four short articulated legs, rounded dark feet, and classic desktop/dialog personality. The original generated image remains separately preserved. This confirms appearance; it does not supply measured dimensions or a validated leg mechanism.

On 2026-10-20, Bill asked to start the repo with an introduction, references and useful material from the other Git repos. The existing local Git repository now has a project introduction and concept image in README, architecture and milestone documents, hardware measurement and parts sheets, a software workspace guide, and a reference index. Earlier research is preserved in docs/research-notes.md. The hub's mechanical handoff capture is preserved in commit d3058f6; this current record replaces its transcript dump with plain project state.

Imported 93 unmodified files (2,360,495 bytes) into vendor/ from four pinned sources: WonderMac guides, Macintosh Mini bezel CAD/exports and KiCad board plus clock controls, AgentBridge's optional modern server/protocol, and Bill's Continuum robot code/tests. SOURCES.json records full revisions, source paths, file hashes, sizes and original modes. Each snapshot retains its notices and has a SOURCE.md. Public remote HEADs matched the existing three source checkouts when checked; no upstream update was required. Other project checkouts were read only and remain clean.

Validation: all 93 hashes match; seven source-tool tests pass, including modified/missing imports and refusal to overwrite dirty or mismatched checkouts; a fresh WonderMac restore and repeat invocation passed in a temporary folder. Owned documentation links and CSV structure checked. These are repository-tool checks, not tests of the imported runtime. No upstream installer, vendor test suite, emulator, AI service or motor code was executed.

No integrated RayCue runtime, leg CAD or verified electrical design exists yet. The exact clock model, mass, internals, actuators, compute board and power design remain unknown. The initial printer recommendation remains an A1-class filament printer, PLA fit checks, PETG candidate structure and TPU feet; no printer or hardware purchase has been selected.

## To do

- [x] Find original clock conversion, expanded hardware, emulator and robotics references.
- [x] Show and save the walking Mac concept; record Bill's acceptance.
- [x] Build the project introduction, architecture, roadmap and reference index.
- [x] Import selected CAD, PCB, control, bridge and robot source with provenance and notices.
- [x] Add and verify source-integrity and pinned-checkout restore tools.
- [ ] Identify and measure the actual clock; populate hardware/measurements.csv.
- [ ] Define a first screen-state prototype and demonstrate one voice/screen interaction on the host.
- [ ] Evaluate imported Continuum mock tests and select reusable memory/control pieces.
- [ ] Develop packaging and mass/power budgets before choosing fitted hardware.
- [ ] Design and test one restrained leg with representative load.
- [ ] Build the four-leg base with dummy mass, then integrate the stationary Mac.
- [ ] Optional after core experience: prove OS 9.0.4 and selected legacy apps.

## Important

- The parent repository has no remote. The hub selected drive transport on 2026-10-19 (RAY-TX series); its prior RAY-TX-001 snapshot predates this foundation. No new transfer payload is claimed here.
- Full reference clones in sources/ remain ignored separate repositories. The tracked vendor/ subsets travel with the parent. Never push to vendor upstreams.
- Original RayCue work has no public license selected. Imports retain their individual licenses. Continuum is Bill-owned local source with no upstream LICENSE at the snapshot; no public redistribution license is asserted. The differently licensed AgentBridge classic client implementation is omitted.
- Apple ROMs, OS images, chimes and emulator binaries are not in the tracked imports. Keep media, credentials, recordings and memory databases in ignored local storage.
- The existing loose file ChatGPT Image Oct 19, 2026, 11_03_05 AM.png is untracked and untouched; it is byte-identical to the committed concepts/raycue-walking-mac-v1.png.
- Imported GPIO button code can shut down Linux or launch emulator/setup commands. Do not run it on this Mac. Imported Freenove geometry/limits are not four-leg RayCue settings.
- SheepShaver supports through 9.0.4; Basilisk II through 8.1. AgentBridge PowerPC is marked builds, untested. Source discrepancies and wiring/power concerns are documented in docs/references.md.
- Motor limits, timeout behavior and stopping must work independently of desktop and AI. The safe response must be validated for the actual body.
- No writes to iCloud. No purchase, hardware modification, external publication, or live robot operation occurred.
