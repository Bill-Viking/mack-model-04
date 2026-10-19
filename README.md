# RayCue Mac

Turn Bill's RayCue Macintosh-shaped alarm clock into an intelligent classic Mac, with a future walking body.

Research checked 2026-10-19. This is a project map, not an installation or a verified electrical design. The clock's exact model and internals have not been inspected.

## The repos to start with

| Job | Source | What it gives us |
| --- | --- | --- |
| Original clock conversion | [ThisDoesNotCompute/wondermac](https://github.com/ThisDoesNotCompute/wondermac) | Mini vMac setup, Pi/display preparation, compilation notes, and background reading. Excellent physical-build reference; its Mac II emulation does not run OS 9. |
| More complete clock hardware | [wr/macintosh-mini](https://github.com/wr/macintosh-mini) | Build guide, screen bezel STL/STEP, KiCad board files, and software for the dial, buttons, audio and emulators. The best starting hardware reference found. |
| Real Mac OS 9 | [kanjitalk755/macemu](https://github.com/kanjitalk755/macemu) | The emulator source fork used by Macintosh Mini, including SheepShaver. The original upstream is [cebix/macemu](https://github.com/cebix/macemu). |
| AI operating classic apps | [SeanFDZ/agentbridge](https://github.com/SeanFDZ/agentbridge) | Classic Mac app plus a modern MCP server, exchanging commands through a shared folder. |
| Walking body | [PetoiCamp/OpenCatEsp32-Quadruped-Robot](https://github.com/PetoiCamp/OpenCatEsp32-Quadruped-Robot) | ESP32/BiBoard quadruped control software. A candidate to study, not a proven carrier for the RayCue. |

Local reference clones are under `sources/wondermac`, `sources/macintosh-mini`, and `sources/agentbridge`. Their exact revisions are recorded in `SOURCES.json`. They are ignored by this parent repository, remain separate upstream checkouts, and have not been installed or executed.

## Build material

- [Original build video — This Does Not Compute](https://www.youtube.com/watch?v=dRr5iVjMfqs). The link is corroborated by Waveshare's project-resources page; the video itself was not played in this research session.
- [Macintosh Mini build guide](https://github.com/wr/macintosh-mini/blob/main/BUILD.md).
- [Macintosh Mini build video — Wells Riley](https://www.youtube.com/watch?v=zAbAf5-H5Yo), linked by its author.
- [Screen bezel: printable STL, editable STEP, and parameterized CAD](https://github.com/wr/macintosh-mini/tree/main/maclock-screen-bezel).
- [Breakout board: schematic, PCB, and parts information](https://github.com/wr/macintosh-mini/tree/main/maclock-pcb).
- [Waveshare 2.8-inch DPI LCD product](https://www.waveshare.com/2.8inch-dpi-lcd.htm) and [manufacturer setup material](https://www.waveshare.com/wiki/2.8inch_DPI_LCD).
- [Manual emulator setup](https://github.com/wr/macintosh-mini/tree/main/emulators).

The reference build uses a Pi Zero 2 W, the **DPI** version of the Waveshare 2.8-inch panel, a microSD card, a printed bezel, an audio/control board, a small speaker and an interposer or wiring. For voice, add a microphone and an audio path selected after the display's GPIO use is known. These are candidate parts, not a purchase-ready list for Bill's uninspected unit.

## Real Mac OS 9 changes the plan

[SheepShaver's official documentation](https://sheepshaver.cebix.net/) supports Mac OS through **9.0.4**. It requires a matching PowerMac ROM and OS media supplied separately. OS 9.1/9.2.2 need another emulator route; they are outside this first proposal.

[Basilisk II's official documentation](https://basilisk.cebix.net/) tops out at **8.1**. Macintosh Mini's references to Basilisk II running 8.5 are erroneous. Do not select its default emulator expecting OS 9.

The Macintosh Mini author warns that SheepShaver is very slow on a Pi Zero. The [Zero 2 W has 512 MB RAM and a 1 GHz Cortex-A53 CPU](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/). It is a good fit reference, but responsiveness with OS 9, voice and AI has not been demonstrated here. Benchmark the intended apps before committing to that board. A more powerful computer in a robot base, or a host elsewhere on the home network, is a design alternative; neither is a proven drop-in replacement for this enclosure/display wiring.

Do not merge the two projects' installation instructions: WonderMac describes 32-bit Pi OS, while the inspected Macintosh Mini installer targets 64-bit Pi OS.

## How to make it intelligent

Bill's direction, confirmed 2026-10-19: a **Mac OS 9 shell/wrapper with an underlying intelligent AI/robotics system**, combining the classic experience with modern capabilities.

Proposed architecture, not yet built:

- **Everyday desktop:** a modern interface styled like Mac OS 9, with classic windows, menus and icons. Its own apps can expose conversation, memory, alarms, camera and robot status.
- **Authentic classic apps:** a separate SheepShaver session running OS 9.0.4, reachable from that desktop. The everyday interface need not wait on emulation.
- **Intelligence underneath:** modern services for conversation, voice, memory and perception. The model could initially run on Bill's existing Mac over the home network. Standalone operation needs a separate compute, power and thermal decision.
- **Movement underneath:** a dedicated controller carries out bounded actions and maintains limits and stopping independently of both desktop and AI.

Example experience to explore: ask the Mac to remember something, see it as a note in a classic-looking window, open a vintage app, and eventually ask it to approach. These are design examples, not implemented features. The wrapper's implementation technology has not been selected.

[AgentBridge](https://github.com/SeanFDZ/agentbridge) is a promising connector for opening apps, reading windows, typing and exchanging clipboard text. Its README marks PowerPC/SheepShaver support **builds, untested**. Its table also lists OS 9.2.2 beside SheepShaver; that does not override SheepShaver's 9.0.4 limit. First proof: ping, read a window, and type into SimpleText under 9.0.4. Keep robot motion outside this classic-app connector.

Other useful material:

- [MacinAI](https://oldapplestuff.com/MacinAI/) is an existing classic-Mac chat client, with author-reported tests on System 7.5.3 and OS 9.2.2. It uses a relay service by default. It is a useful interface reference, but has not been tested here on 9.0.4 or with a private relay.
- [MacinAI Local](https://github.com/alexhoopes/MacinAI-Local) explores inference inside classic Mac OS. Its published performance is on vintage hardware, not this Pi/emulator combination. Treat it as an experiment, not evidence that useful onboard conversation will be fast.

## The walking robot

Bill already has relevant work locally:

- `../continuum-hexapod` — [Bill-Viking/continuum-hexapod](https://github.com/Bill-Viking/continuum-hexapod). Verified files include memory storage, the brain loop, a simulator, a hardware adapter, limits and a watchdog. Its STATUS says no live hardware or live API brain run has happened; this session did not retest it. This is a strong architecture reference and a candidate for reuse.
- `../Freenove_Big_Hexapod_Robot_Kit_for_Raspberry_Pi` — [Freenove's official kit material](https://github.com/Freenove/Freenove_Big_Hexapod_Robot_Kit_for_Raspberry_Pi). A local reference checkout exists. Physical possession, assembly and available payload have not been checked. Never push to its vendor upstream.

Start with four or six legs as a proposed base. A biped is possible as a separate, more demanding balance project. The complete clock assembly's mass, center of gravity, mounting points and servo load must determine the body. Neither OpenCat nor the existing hexapod is yet proven to carry it.

Use the modern brain for intentions, and a dedicated controller for joint timing, limits and stopping. A loss of network or a slow AI response must not leave walking dependent on the next model reply. Test the unloaded body and a dummy load before mounting the finished Mac.

## Hardware issues to resolve before ordering

1. Confirm the RayCue model, shell dimensions and connector/charging-board revision.
2. Select the desired OS 9 apps and measure acceptable emulator response.
3. Check power properly. The inspected Macintosh Mini guide runs the Pi from roughly 4 V battery output and documents audio noise; that is not a regulated 5 V design to copy into a robot.
4. Verify schematics and header mapping directly. The PCB README mentions pins beyond the Pi's 40-pin header, so its prose is not a wiring authority.
5. Budget the display GPIO use, USB audio, microphone, future camera, motor controller and separate motor power together.

## Proposed sequence

First prove the modern classic-looking shell and one AI interaction on a bench, then measure real OS 9.0.4 emulation separately. Confirm the clock's internals and settle the enclosure parts. Build the stationary talking Mac. Measure its finished weight. Finally choose and test the walking base around that payload.

The next physical information needed from Bill is the exact clock model or clear exterior/label photos. The combined shell-plus-intelligence direction is settled; specific classic apps and how much autonomy the robot should have remain design details.
