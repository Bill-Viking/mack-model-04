# M.A.C. Model 04 — references and reuse

Checked 2026-10-20. Full revisions and per-file hashes live in [SOURCES.json](../SOURCES.json). Public reference HEADs matched the existing checkouts when checked; no newer upstream commits were needed. All imports are unchanged snapshots.

## Material brought into this repository

| Source | Imported material | Mack use and limits |
| --- | --- | --- |
| [ThisDoesNotCompute / WonderMac](https://github.com/ThisDoesNotCompute/wondermac) | [Conversion guides](../vendor/wondermac/) and GPL v2 license. | Original clock-to-Pi build background. Its Mini vMac route is not OS 9. Emulator ZIP binaries were omitted. |
| [Wells Riley / Macintosh Mini](https://github.com/wr/macintosh-mini) | [Bezel CAD/STL/STEP](../vendor/macintosh-mini/maclock-screen-bezel/), [KiCad board](../vendor/macintosh-mini/maclock-pcb/), build guide/drawings, brightness/button code and tests, license files. | Main physical-fit reference. Verify the actual clock revision, power design, and pin map before adapting. Installer, Apple chimes, and the separately attributed Waveshare overlay were omitted. |
| [SeanFDZ / AgentBridge](https://github.com/SeanFDZ/agentbridge) | [Protocol](../vendor/agentbridge/agentbridge-protocol-spec.md), modern TypeScript server source, package metadata, README, and license notices. | Optional classic-app integration. Classic client source and binaries were not imported. No npm install was run. |
| [Bill / Continuum Hexapod](https://github.com/Bill-Viking/continuum-hexapod) | [Memory](../vendor/continuum-hexapod/continuum/), brain, [control supervisor](../vendor/continuum-hexapod/spine/), hardware interfaces, simulation, tests, configuration and design notes. | Candidate reuse for memory, bounded requests, mock hardware, and watchdog concepts. Six-leg geometry and limits are not Mack settings. No data, secrets, session records, or deployment scripts were imported. |

The original local projects remain unchanged. The tracked snapshots travel with this repository; ignored full clones can be recreated with the source utility.

## References retained for later

- [Petoi OpenCat ESP32 quadruped firmware](https://github.com/PetoiCamp/OpenCatEsp32-Quadruped-Robot): candidate walking-controller reference. Not imported or selected; payload and controller fit are unknown.
- [Freenove Big Hexapod material](https://github.com/Freenove/Freenove_Big_Hexapod_Robot_Kit_for_Raspberry_Pi): existing local kit reference. Its six-leg controller is not a four-leg driver. Do not push to its vendor upstream.
- [SheepShaver](https://sheepshaver.cebix.net/) and [macemu source fork](https://github.com/kanjitalk755/macemu): optional authentic Mac OS 9.0.4 path.
- [Basilisk II](https://basilisk.cebix.net/): supports through Mac OS 8.1; useful context, not OS 9.
- [MacinAI](https://oldapplestuff.com/MacinAI/): classic chat-interface inspiration.
- [MacinAI Local](https://github.com/alexhoopes/MacinAI-Local): experimental classic-Mac inference, not a benchmark for our target.

## Joint and recovery research — checked 2026-10-21

The [Mack J04 study](../hardware/joints/README.md#references-and-what-they-actually-establish) links MIT Mini Cheetah, Open Dynamic Robot Initiative actuator/leg/test-stand designs, and the ANYmal recovery research and author supplementary repository. These are newly reviewed references only; nothing from them has been imported or installed. Their geometries, loads and policies are not Mack parameters. The existing pinned source manifest is unchanged.

## Build material

The [T04 motion-training plan](motion-training.md) links MuJoCo's engine, Python
and terrain documentation, Google DeepMind's MuJoCo Playground and NVIDIA's Isaac
Lab installation guidance (checked 2026-10-21). These inform a future small physics
practice room. No simulator, example robot, policy or dependency was imported.

The [S04 solar study](../hardware/solar-feasibility.md) uses Voltaic P124's
August 2026 datasheet, Epishine MultiCell v1.6.5, Raspberry Pi's own load discussion
and TI's solar-charger documentation (checked 2026-10-21). Panel output is kept
separate from assumed conversion factors and unmeasured Mack loads. No solar
hardware or supplier document was imported.

The [R04 recovery study](../hardware/joints/recovery-envelope.md) applies the
force/moment formulation from [Lynch and Park, Modern Robotics §3.4](https://modernrobotics.northwestern.edu/nu-gm-book-resource/3-4-wrenches/)
(checked 2026-10-21) to distinguish pitch from roll authority. Its proposed
mechanisms and test matrix are Mack design work, not externally validated results.

The [F04 face and vision study](../hardware/display-and-vision.md) records primary
Waveshare, Raspberry Pi, ZUIKI, Visionox, FlexEnable, optical-supplier, ST and
under-display-camera research sources checked on 2026-10-21. Catalogued parts are
leads, not selected Mack hardware. Some manufacturer pages were available only as
indexed excerpts. No optical CAD or camera code was imported.

The [CAD guide](../hardware/joints/cad/README.md) records build123d 0.12.0 as a
development dependency installed from PyPI. Original J04 source is outside
`vendor/`; no upstream joint CAD was copied. The
[engineering workflow](../hardware/engineering-workflow.md) links primary PTC,
Ansys and Protolabs documentation reviewed on 2026-10-21. Those are workflow and
process references, not proof of Dell license capabilities or a manufacturing
release. The pinned imported-source manifest remains unchanged.

- [Original WonderMac video](https://www.youtube.com/watch?v=dRr5iVjMfqs).
- [Macintosh Mini build video](https://www.youtube.com/watch?v=zAbAf5-H5Yo).
- [Waveshare 2.8-inch DPI panel](https://www.waveshare.com/2.8inch-dpi-lcd.htm) and [setup documentation](https://www.waveshare.com/wiki/2.8inch_DPI_LCD).
- [Pi Zero 2 W specifications](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/).
- [PETG material guide](https://help.prusa3d.com/article/petg_2059) and [flexible-material guide](https://help.prusa3d.com/article/flexible-materials_2057).

These links are references, not a purchase-ready selection. The prior investigation and printer estimate remain in [research notes](research-notes.md). The videos were identified from upstream links, not watched in this session.

## Corrections to carry forward

1. **Emulator ranges:** SheepShaver supports through 9.0.4; Basilisk II through 8.1. Macintosh Mini's 8.5 reference and AgentBridge's SheepShaver/9.2.2 table must not be treated as compatibility evidence.
2. **Power:** Macintosh Mini documents approximately 4 V unregulated battery power to the Pi and audio noise. Review a regulated robot power architecture.
3. **Header numbering:** the PCB README says pins 35–47, beyond the 40-pin Pi header. Resolve wiring from the actual schematic, guide, board revision, and hardware; do not repeat that row as a pin map.
4. **GPIO actions:** imported button code can shut down Linux and launch emulator/setup commands. It is a reference, not a service to run on this Mac.
5. **OS assumptions:** WonderMac's 32-bit guide and Macintosh Mini's 64-bit setup are different installations. Do not combine their commands.
6. **Performance and validation:** upstream warns that SheepShaver is slow on Pi Zero. AgentBridge PowerPC support is marked builds, untested. Neither the Mack integration nor the imported robot tests have been demonstrated here.
7. **Licensing:** Macintosh Mini separates hardware, software, and documentation licenses. AgentBridge's modern server and classic client have different licenses. [Vendor notices](../vendor/README.md) preserve that distinction.

## Updating a source

Keep imported files unchanged. Review the new upstream revision, select files deliberately, preserve notices, and update the manifest hashes together. Run the source checks before committing. Adapted Mack files belong outside `vendor/` and should record their source and applicable notices.
