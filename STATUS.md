# STATUS — RayCue Mac

## Now

Research started 2026-10-19 on the Mac. Bill wants to turn his RayCue Macintosh-shaped alarm clock into an intelligent Mac OS 9 computer, with a future walking robot body. The folder was empty and was not a Git repository at arrival. No existing RayCue memory folder or competing claim was found.

Bill clarified the intended experience on 2026-10-19: both a Mac OS 9 shell/wrapper and an underlying intelligent AI/robotics system. Treat the classic desktop as the everyday interface to modern capabilities; preserve the option to run real classic apps through emulation. Do not ask the appearance-versus-AI question again.

The original conversion is ThisDoesNotCompute/wondermac. wr/macintosh-mini offers a fuller hardware reference. Real OS 9 requires the SheepShaver route (up to 9.0.4), not the default Mini vMac/Basilisk II path. The Pi Zero performance and power limits make a bench proof necessary before final hardware selection. AgentBridge is a promising AI connector, but its PowerPC path is marked untested. Existing continuum-hexapod and Freenove reference repos were found locally and inspected without modification.

README.md holds the researched links, candidate parts, architecture, source discrepancies, and next steps. SOURCES.json records reference checkout revisions. No emulator, installer, AI service or hardware was run. No Apple ROM or OS disk image was obtained. Exact RayCue hardware remains unverified.

## To do

- [x] Find original and expanded clock conversion repos and build material.
- [x] Identify an OS 9 emulator and AI bridge candidates.
- [x] Find existing local robot work and public walking-control references.
- [ ] Confirm the exact RayCue model and inspect its exterior, label and internal hardware.
- [x] Record Bill's preference: Mac OS 9 shell/wrapper over an intelligent AI/robotics system; both experiences together (2026-10-19).
- [ ] Identify the desired classic apps and separately supplied ROM/OS media.
- [ ] Define the modern Mac OS 9-style shell and prove one useful AI interaction on a bench.
- [ ] Separately prove real OS 9.0.4 app emulation and measure performance; keep the modern shell responsive independently.
- [ ] Choose the compute board, display, regulated power, microphone and audio after the proof and fit check.
- [ ] Build and verify the stationary Mac, then weigh it.
- [ ] Select a walking platform from payload and balance measurements; test with dummy weight first.

## Important

- Research scope only so far; no purchase or physical modification has been authorized by a parts selection.
- Local reference clones in `sources/` are ignored separate Git repositories. Their provenance is in SOURCES.json; recreate from upstream when absent on another machine. Do not push to vendor upstreams.
- This parent repository has no remote configured. Its research notes currently live on the Mac.
- `private-media/` is reserved and ignored for any separately supplied ROM or OS media. It is not populated.
- SheepShaver supports up to 9.0.4; Basilisk II supports up to 8.1. Some third-party guides overstate those ranges.
- AgentBridge PowerPC/SheepShaver compatibility needs actual validation. Do not treat a successful build as a runtime test.
- Macintosh Mini documents unregulated approximately 4 V Pi power and audio noise; review power and wiring before using the design. Its PCB README has a header-numbering error.
- Robot control limits, watchdog and stopping must operate independently of the AI and classic OS.
- No writes to any iCloud path. Other project repos remain untouched.
