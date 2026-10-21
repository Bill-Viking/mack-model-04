# M.A.C. Model 04

**Mobile Autonomous Computer · “Mack”**

Project repository: [Bill-Viking/mack-model-04](https://github.com/Bill-Viking/mack-model-04).

M.A.C. Model 04, called **Mack (she/her)**, is an original personal robot built around the compact Mac form of a RayCue alarm clock. Her own operating environment on Linux brings together a classic Mac OS 9-inspired interface, intelligence, memory, sensors, fitted electronics, and four walking legs. We are engineering those parts as one complete device.

The screen is her way of expressing herself. A conversation can appear in a classic dialog. A remembered detail can become a little note. Listening, thinking, and resting can have their own quiet desktop behaviors. The finished Mack should boot into her own interface, interact with Bill, understand her immediate surroundings, and move within a tested physical envelope. The aim is a robot that feels like a tiny Mac has come to life.

**Our long-term goal is to grow a personalized intelligence:** a companion who comes to know her person through conversation, shared projects, preferences and memories they choose to keep. Mack should build a history with Bill, become more useful through experience, and retain a recognizable personality as her models, tools and abilities improve.

The little four-legged Mac is her first physical target. Years from now, the goal is to carry that same personalized intelligence into a humanoid body for a fuller interaction experience: conversation, perception, gestures, movement and practical participation in everyday life. Her identity and remembered history should continue across that change. Each body will need its own engineered controller and tested abilities. See [identity and embodiment](docs/architecture.md#identity-across-bodies).

**We’re building Mack in public, from the first concept to a working robot.** The classic desktop, local AI conversation and lasting memory already run on a development Mac. The physical robot is still being engineered. Follow the [build log](docs/build-log.md), [roadmap](docs/roadmap.md) and commit history for progress, experiments and remaining work.

The formal designation has the deliberately industrial tone of an old computing instrument. “04” nods to its four legs. In conversation, it is simply Mack.

> **M.A.C. MODEL 04**
>
> MOBILE AUTONOMOUS COMPUTER
>
> Ambulatory Configuration · Four-Leg Assembly
>
> Everyday name: **Mack**

![Mack build target: ivory compact Mac, four short legs, and a classic desktop saying Hello, Bill.](concepts/raycue-build-target.png)

*Concept rendering, not a photograph of completed hardware. This is the exact image confirmed as the build target on 2026-10-20. Dimensions and mechanisms still require engineering.*

## Try Mack on your Mac

**Mack Local AI 0.3 is working.** In Finder, double-click **Start Mack.command** in this repository. It opens Mack at **http://127.0.0.1:9844/**. Keep the launcher window open. Python 3 and a running local Ollama model are required; both are already present on Bill’s Mac.

Mack answers through **Qwen3.6:35b**, keeps completed conversations in a local SQLite archive, and saves curated facts when asked. Try **“Remember that I like jazz”**, then ask what music you like. Memories can be inspected, corrected, moved to Trash, and restored. They survive restarts and model changes. Control Panels can select another installed conversational model.

A tool-capable local model can check Mack's actual status, read the local clock, and search saved facts and past conversations. Try **“Check your status. What can you actually do?”** or **“Check the clock. What time is it?”** These are read-only tools; curated fact saves still require an explicit request. Completed exchanges are archived automatically.

Mack’s approved voice v1 generates new speech locally from Bill’s chosen SAL reference. Bill accepted the light-echo delivery on October 21, 2026; its model, reference fingerprints, settings and audition fingerprint are preserved in a [versioned voice profile](software/mack/voice-profile.json). It is the default for new voice preferences; dry delivery and a stock voice remain explicit alternatives. Click **Talk to Mack** and watch a **live local transcript** appear while speaking, then **Finish & send**. Draft words can correct themselves. Qwen3-ASR checks the final transcript on this Mac; Mack answers in approved voice v1. **Conversations** provides searchable history and recoverable Trash. [Local listening setup and verification](software/mack/LISTENING.md). There is no always-on microphone. Sensors, motors and project service bridges remain disconnected. [Desktop guide](software/desktop/README.md) · [Model research and upgrade plan](docs/model-strategy.md).

## Visual design target

Mack's conversational manner now follows a [SAL-inspired personality](docs/personality-and-voice.md):
calm, warm, curious and plain-spoken, with candor preserved under pressure. Control
Panels identifies **Mack · approved voice v1** and **Approved v1 · light echo**.
Her voice and manner are core design requirements. The voice direction is accepted;
long-form speech quality, disconnected reboot, onboard performance and
physical mannerisms still need qualification.

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

Bill confirmed the Linux foundation on 2026-10-20. The first software prototype runs on the existing Mac; the target robot carries its own compute and control. Speech recognition, Qwen3.6 inference, recall and approved speech output passed process-scoped tests with internet access denied; cold reboot and onboard performance remain to be qualified. Onboard compute, microphones, motors, battery, and controller are still to be selected. The [product definition](docs/product-spec.md) governs completion; the desktop preview is one component.

Real vintage Mac applications are an optional extra. A separate emulator may eventually run Mac OS 9.0.4, but the everyday personality and robot functions will use modern software. Emulation is not a prerequisite for the first prototype.

## Where the project stands

The desktop, local AI conversation and durable memory run on the host Mac. The repository also contains the concept, architecture, model research, build plan, hardware intake sheets, and pinned upstream source material. A working leg and verified electrical design remain to be built.

- **Ready:** the interactive desktop, local Qwen conversation, durable editable memories and conversation archive, local speech input, bounded read-only tools, she/her identity and SAL-inspired personality, installed-model selection, optional local speech output, expression previews, accepted concept and pinned CAD/PCB/robot references.
- **Next software milestone:** test everyday microphone use, evaluate model quality/latency, and implement the explicitly simulated body contract. Continuum, Terrarium and Exocortex adapters are proposed separate services.
- **Next hardware milestone:** measured clock geometry/mass and a unified packaging, sensing and power budget, followed by a restrained loaded-leg test.
- **Finished personal prototype:** boot-to-Mack, conversation and memory, working sensors, onboard power, qualified four-leg motion, interruption/recovery, and documented assembly/service. [Acceptance requirements](docs/product-spec.md).

## Start here

| Read | What it contains |
| --- | --- |
| [Build log](docs/build-log.md) | The project’s progress from the first concept onward. |
| [Public introduction](docs/public-introduction.md) | Shareable descriptions of Mack's personalized intelligence and long-term humanoid goal. |
| [Product definition](docs/product-spec.md) | Agreed vision, original system on Linux, and evidence required for completion. |
| [Model strategy](docs/model-strategy.md) | Current candidates, downloadable upgrades, memory ownership and proposed project services. |
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

Original work here has no public license selected yet. Imported material retains its own licenses; see [source notices](vendor/README.md). The project is maintained in the public [mack-model-04 repository](https://github.com/Bill-Viking/mack-model-04).
