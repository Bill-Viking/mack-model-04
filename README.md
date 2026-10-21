# M.A.C. Model 04

**Mobile Autonomous Computer · “Mack”**

Project repository: [Bill-Viking/mack-model-04](https://github.com/Bill-Viking/mack-model-04) (private).

M.A.C. Model 04, called **Mack**, is an original personal robot built around the compact Mac form of a RayCue alarm clock. Its own operating environment on Linux brings together a classic Mac OS 9-inspired interface, intelligence, memory, sensors, fitted electronics, and four walking legs. We are engineering those parts as one complete device.

The screen is its way of expressing itself. A conversation can appear in a classic dialog. A remembered detail can become a little note. Listening, thinking, and resting can have their own quiet desktop behaviors. The finished Mack should boot into its own interface, interact with Bill, understand its immediate surroundings, and move within a tested physical envelope. The aim is a robot that feels like a tiny Mac has come to life.

The formal designation has the deliberately industrial tone of an old computing instrument. “04” nods to its four legs. In conversation, it is simply Mack.

> **M.A.C. MODEL 04**
>
> MOBILE AUTONOMOUS COMPUTER
>
> Ambulatory Configuration · Four-Leg Assembly
>
> Everyday name: **Mack**

![Mack build target: ivory compact Mac, four short legs, and a classic desktop saying Hello, Bill.](concepts/raycue-build-target.png)

*The exact image Bill supplied and confirmed as the build target on 2026-10-20. It defines the intended appearance; dimensions and mechanisms still require engineering.*

## Try Mack on your Mac

The first desktop preview is working. In Finder, double-click **Start Mack.command** in this repository. It opens Mack in your browser at **http://127.0.0.1:9844/**. Keep the launcher window open while using it. Python 3 is required; there are no packages to install.

Try saying **“hello”**, **“what time is it?”**, or **“Remember that I like jazz.”** Open **Memories** to read notes, **Trash** to restore removed notes, and **Control Panels** to change the desktop or preview Mack’s expressions. Drag, collapse, zoom, and resize the windows. A local browser voice can read replies aloud when available.

This version uses clearly labeled, scripted local replies. Live AI, microphone input, and robot control are not connected. Notes and preferences stay in this browser; conversation text resets on reload. [Desktop guide and checks](software/desktop/README.md).

## Visual design target

- The beige compact-Mac enclosure remains the dominant shape, including the screen surround, carry-handle recess, vents, and floppy-slot detail.
- A compact base sits directly beneath the Mac.
- Four short articulated legs have rounded beige covers and dark visible joints.
- Rounded dark feet provide the contact points.
- The screen shows a classic Mac desktop with a menu bar, icons, and dialogs such as “Hello, Bill.”
- Personality comes through the desktop, voice, and stance.

Use this image as the baseline for CAD and packaging decisions. Preserve its overall proportions as the actual clock, motors, battery, and joint supports are fitted. Keep the [original generated concept](concepts/raycue-walking-mac-v1.png) for history.

## What we are building

| Layer | Job |
| --- | --- |
| Mack system on Linux | Boot, device services, original classic interface, configuration, diagnostics, updates, and recovery. |
| Voice and mind | Conversation, personality, durable local memory, and behavior. |
| Perception | Microphone and body/environment sensors, observations, and sensor health. |
| Robot controller | Bounded actions, joint control, movement limits, and stopping independent of AI response time. |
| Electronics and power | Fitted compute, controller, audio, sensors, battery, regulated supplies, and serviceable wiring. |
| Physical body | The RayCue enclosure, structural base, four articulated legs, supported joints, and replaceable feet. |

Bill confirmed the Linux foundation on 2026-10-20. The first software prototype runs on the existing Mac; the target robot carries its own compute and control. Fully offline AI capability remains to be benchmarked. Onboard compute, microphones, motors, battery, and controller are still to be selected. The [product definition](docs/product-spec.md) governs completion; the desktop preview is one component.

Real vintage Mac applications are an optional extra. A separate emulator may eventually run Mac OS 9.0.4, but the everyday personality and robot functions will use modern software. Emulation is not a prerequisite for the first prototype.

## Where the project stands

The browser desktop preview runs on the host Mac. The repository also contains the concept, architecture, build plan, hardware intake sheets, and pinned upstream source material. Live AI integration, a working leg, and a verified electrical design remain to be built.

- **Ready:** the interactive desktop, browser-local notes, optional local speech output, expression previews, accepted concept, CAD/PCB references, and reusable robot software snapshots.
- **Next software milestone:** a local Mack runtime connecting the desktop, durable memory, a conversation adapter, and an explicitly simulated body; then microphone input and live inference.
- **Next hardware milestone:** measured clock geometry/mass and a unified packaging, sensing and power budget, followed by a restrained loaded-leg test.
- **Finished personal prototype:** boot-to-Mack, conversation and memory, working sensors, onboard power, qualified four-leg motion, interruption/recovery, and documented assembly/service. [Acceptance requirements](docs/product-spec.md).

## Start here

| Read | What it contains |
| --- | --- |
| [Product definition](docs/product-spec.md) | Agreed vision, original system on Linux, and evidence required for completion. |
| [Architecture](docs/architecture.md) | Screen, AI, memory, and motion boundaries. |
| [Build roadmap](docs/roadmap.md) | Small milestones with a demonstration for each. |
| [References and reuse](docs/references.md) | Which projects we use, what we brought in, and what needs adaptation. |
| [Hardware workspace](hardware/README.md) | CAD/PCB entry points, measurements, and candidate parts. |
| [Hardware integration](hardware/integration-plan.md) | Fitted electronics, sensors, structure, power, and physical proof sequence. |
| [Software workspace](software/README.md) | Intended components and the Continuum code to evaluate first. |
| [Research notes](docs/research-notes.md) | Earlier investigation, printer/material recommendations, and source discrepancies. |
| [Current status](STATUS.md) | The working record and next decisions. |

## Source material

The tracked [vendor folder](vendor/README.md) contains selected, unmodified upstream files with their original notices. [SOURCES.json](SOURCES.json) records full Git revisions and a SHA-256 for each imported file. The larger upstream checkouts live in the ignored `sources/` folder.

The source utility can verify the tracked snapshots or restore the pinned public checkouts. These are developer commands from the repository root; neither installs or launches upstream software:

```sh
python3 tools/sources.py check
python3 tools/sources.py fetch
```

The local Continuum snapshot is included in Git and does not depend on a second machine having Bill's original folder. Its Freenove-specific adapter is reference material; it is not a driver for the proposed four-leg body.

## Project boundaries

- Keep the original RayCue exterior where it fits the engineered design.
- Design and test the walking mechanism around measured weight and balance.
- Keep motor control and stopping independent of both the classic desktop and AI.
- Review upstream wiring and power circuits against the actual unit.
- Keep Apple ROMs, OS disk images, credentials, and personal robot memories out of Git.

Original work here has no public license selected yet. Imported material retains its own licenses; see [source notices](vendor/README.md). The project is maintained in the private [mack-model-04 repository](https://github.com/Bill-Viking/mack-model-04).
