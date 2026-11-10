# W04 — workshop road: printer, bench and first parts

Revision W04-D01, 2026-11-10. Bill asked for a road, not a shopping trip: design the prototype
parts so he can print them at home, choose a printer, set up an electronics bench, and source
parts such as servos and sensors that can be bought today. **Nothing here is selected or
purchased.** Model names and prices are RECALLED (knowledge to mid-2026) and get a live check
before any order; the gates are the ones in the [build roadmap](../docs/roadmap.md).

## The order, and why

Each stage is small, and each one unblocks a gate that is open today.

| Stage | Buy or do | What it unblocks | Bill's word needed |
|---|---|---|---|
| 0 — Measure | Digital calipers (150 mm), a small scale (0.1 g or finer), a steel rule, precision screwdrivers and opening tools | G1 clock intake: [measurements.csv](measurements.csv) is still empty, and every leg dimension hangs off the real shell | Go to buy |
| 1 — One actuator on the table | One or two sample servos and their USB adapter | Replaces the recalled 11 mm output-axis offset in the [leg packaging study](joints/leg-packaging.md) with a measured one; gives a real mass, a real horn and a servo that can be run | Which samples |
| 2 — Printer | A one-page comparison at today's prices, then the pick | Every printed part: fit coupons first, then the redrawn hinge frames of one leg | Printer class and budget |
| 3 — Bench | Supply, meter, iron, wiring and a controller board | Running one servo with its current logged, then one printed leg in a restrained fixture | Go to buy, after the list is priced |
| 4 — One leg, printed and driven | Print, assemble and test one leg | G5: range, load, current, temperature, stop and fault cases against recorded limits | Placement and knee-drive ruling from the leg study |
| 5 — Sensing and power | IMU, foot contact, dock ranging; the battery only after measured current | G4 and G6 inputs; [battery direction](battery-power.md) needs the measured peak current first | Later |

Stages 0 and 1 are cheap and do not wait on the printer. Stage 2 is the only large purchase.

## Stage 2 — the printer

What Mack's parts ask of it, from the catalog scale and the leg model (rigid-envelope numbers,
the clock itself still unmeasured):

| Need | Why | What it means |
|---|---|---|
| Small stiff hinge plates and webs, 2 to 3 mm thick, around an 18 g servo | The leg frames in J04-L02 | 0.4 mm nozzle, good first layer, repeatable hole and pocket sizes; a 0.2 mm nozzle is optional |
| A base under an 80 × 91 mm body, and later a dock saddle wider than the stance | [Mounting base](parts.csv), [D04 dock](charging-dock.md) | A bed near 250 mm prints both in one piece; a 180 mm bed prints the robot's parts and probably splits the dock |
| PLA for fit checks, PETG for brackets, TPU for feet | The [earlier recommendation](../docs/research-notes.md) stands | Any current heated-bed machine with a direct-drive extruder |
| Room to move to fibre-filled or higher-temperature filament if thin plates flex or creep | Hinge plates are stiffness parts; not yet load-checked | Hardened nozzle; an enclosure for ASA, nylon and their fibre-filled grades |
| Runs without a vendor account or cloud | The project's offline direction | Check LAN-only or card/USB operation for each candidate |
| Lives in a home | Noise and fumes | An enclosure helps both; ventilation still matters for ASA and nylon |

Three classes to compare. The names are candidates to price, not picks.

| Class | Recalled examples | Recalled price class | For | Against |
|---|---|---|---|---|
| Open-frame bed-slinger, 250 mm | Bambu Lab A1 (the 2026-10-19 recommendation) | about US$300–450 | Lowest cost; PLA, PETG and TPU are enough for first fit and function prints | No enclosure, so ASA and nylon are poor; a second machine if stiffness parts need them |
| Enclosed CoreXY, 250 mm | Bambu Lab P1S or P2S, Elegoo Centauri Carbon, Creality K-series | about US$350–800 | Adds ASA, nylon and fibre-filled grades; quieter, cleaner; faster on small parts | Cost; some are cloud-first by default |
| Enclosed, open and offline by design | Prusa Core One | about US$1,000–1,300 | Fully local operation, open firmware, long support | Highest cost |

**Lean, to be confirmed by the comparison:** an enclosed 250 mm machine. The earlier A1
recommendation was written before the leg model existed. The parts that matter now are thin
hinge plates whose stiffness sets joint accuracy, and an enclosure keeps the fibre-filled and
higher-temperature materials available without buying twice. If the budget says open-frame, the
A1 class still prints every first-stage part.

**Compared 2026-11-10:** the [printer comparison](printer-comparison.md) read the makers' US
stores that day. The lineup had moved on from the recalled names above: Prusa's enclosed machine
is now the CORE One+, Elegoo's is the Centauri Carbon 2, and Bambu Lab has added the X2D. Its
recommended pick is the Bambu Lab P2S, with four alternatives each named for one reason.
Nothing is purchased.

First prints, whichever machine: a tolerance coupon (holes, shaft fits, a servo pocket, a
heat-set insert boss), then one leg's hinge frames once they are redrawn.

## Stage 3 — the bench

Essentials first. Planning allowance about US$250–450 for this list, RECALLED and unpriced.

| Item | Job | Note |
|---|---|---|
| Adjustable bench supply with current limit, 0–30 V, 3–5 A | Powers servos safely; the current limit protects a stalled joint | The first instrument for G5 current numbers |
| Multimeter | Voltage, continuity, small currents | |
| Temperature-controlled soldering iron, solder, flux, wick | Harness and connector work | A fume extractor or a fan and an open window |
| USB logic analyzer | Reads the servo bus when something does not answer | Low cost |
| Wire, crimp tool and connector kits (JST families), heat-shrink | Servo and sensor harnesses | Match the connector family to the chosen servo |
| Controller board with a half-duplex serial port | The local motion controller in [parts.csv](parts.csv): timeout and stop behaviour | ESP32-S3 or RP2040 class; not selected |
| Fasteners and inserts: M2, M2.5, M3 screws, heat-set inserts and a tip for the iron | Printed-part assembly | |
| Calipers and scale from stage 0 | Every measurement | |
| Storage, a silicone mat, tweezers, flush cutters, hex and precision drivers | Keeping small parts findable | |

Later, when a test asks for it: an oscilloscope, a thermocouple or thermal camera for servo
temperature, a force gauge or luggage scale for leg load, and a restrained one-leg fixture
(printed).

## Stage 1 and 5 — parts that can be bought today

All candidates. The leg study used one servo only as a size and mass benchmark.

| Part | Recalled candidates | Why these | Gate before more than samples |
|---|---|---|---|
| Leg actuator, 12 needed | ROBOTIS XL330-M288-T (the benchmark: 20 × 34 × 26 mm, 18 g, 5 V bus servo with position and current feedback); ROBOTIS XC330 in the same case with metal gears; Feetech STS3032 and SCS0009 bus servos | Small, daisy-chained, report position and load | Measured torque, speed, heat and the joint envelope (G5) |
| Servo USB adapter | ROBOTIS U2D2 for the first two; Feetech or Waveshare bus adapter for the others | Lets the Mac move and read one servo before any controller exists | — |
| Joint hardware | Small ball bearings, a 5 mm shaft and a short belt with pulleys only if the proximal knee is chosen | Named in the leg model | Knee-drive ruling |
| Inertial sensor | BNO08x or ICM-42688 class breakout | Body attitude for balance and recovery | Interface and mounting |
| Dock ranging | VL53L1X or VL53L4 class time-of-flight breakout | Short-range alignment to the dock | D04 inputs |
| Foot contact | Thin force-sensing resistor, a micro switch, or servo current alone | Knowing a foot is down | One-leg test |
| Current and voltage monitor | INA219 or INA228 class breakout | Logs what a leg draws | — |
| Battery | None yet | [B04](battery-power.md) needs measured peak current | Measured current |

A sensible first order is small: calipers, a scale, two benchmark servos and their adapter.
A measured servo also settles the output-axis offset that the leg study carries as RECALLED,
whether or not the maker's drawing is downloaded.

## The video Bill passed along

[Why I Indexed the Entire Humanoid Robot Industry, and Made It Free](https://www.youtube.com/watch?v=r7U0rbkrBxQ),
supplied 2026-11-10 as general information. Only its title could be read here; the video was
not watched and the index it describes was not identified. Humanoid supply chains (frameless
motors, precision reducers, roller screws) sit well above Mack's 18 g servo scale, so it informs
the later humanoid direction in the [product definition](../docs/product-spec.md) more than this
prototype. Nothing was taken from it.

## What this does not do

It selects no printer, servo, sensor or board, verifies no price, and approves no arrangement
or motor. The leg study's open rulings (placement, knee drive, the redrawn hinge frames) are
unchanged and still come first for stage 4.
