# Mack's virtual practice room

Training plan T04-D01 · 2026-10-21 · **future work; no simulator or trained policy installed**.

Bill wants a modest virtual physical environment where Mack can learn walking,
maneuvering and obstacles, including steps. Start with a small configurable room,
simple shapes and repeatable lessons. Accurate contacts and a credible body model
matter more for this first stage than elaborate scenery.

## Proposed tools

Start by evaluating **MuJoCo with Python** on the Mac for model inspection,
contact tests, baseline control and replay. Its engine models articulated bodies
and contacts, uses editable MJCF scenes and can load URDF. Its documented Python
viewer supports macOS, with `mjpython` required for the passive viewer. This is a
recommendation, not an installation or measured performance result.
[Engine overview](https://mujoco.readthedocs.io/en/stable/overview.html),
[Python interface](https://mujoco.readthedocs.io/en/stable/python.html).

Use boxes, planes and simple obstacle collision shapes first; add height-field
terrain where appropriate. Keep visual meshes separate from carefully checked
collision geometry. [MuJoCo model reference](https://mujoco.readthedocs.io/en/stable/XMLreference.html#asset-hfield).

If larger training batches become useful, evaluate
[MuJoCo Playground](https://github.com/google-deepmind/mujoco_playground), an
open-source framework for accelerated robot learning and transfer to hardware.
Its example robots and policies are references, not Mack's model or pretrained
walking skill. Check the available accelerator, supported backend, precision and
measured throughput before choosing a training setup. Do not assume this Mac's
GPU or the home Dell supports a particular training stack.

[Isaac Lab](https://docs.nvidia.com/isaaclab/2.3/isaac-lab/local-installation) is
another future option, with its own platform and Isaac Sim requirements. A
heavy rendering stack is not a prerequisite for this first room. No cloud training
service, dependency install, model download or long training run is started here.
Primary documentation checked 2026-10-21; pin actual versions when implementation begins.

## One room, progressively harder lessons

| Lesson | Simple environment | What Mack practices |
| --- | --- | --- |
| 1. Stand and stop | Clear level floor and a marked goal area. | Balanced stance, crouch, stand, hold, commanded stop and interrupted motion. |
| 2. Walk and maneuver | Open lane, turns and a few widely spaced blocks. | Slow forward/backward walking, side steps, turning and controlled approach to a goal. |
| 3. Avoid obstacles | Boxes, cylinders representing furniture legs, narrow passages and a dead end. | Go around, slow down, reverse out or stop when a route is unavailable. |
| 4. Thresholds and ramps | Adjustable low blocks and gentle slopes, varied approach angles. | Foot clearance, weight transfer, ascent and descent. Increase difficulty only within achievable geometry. |
| 5. Small steps | One step, then a short staircase with adjustable rise and tread. | Ascend/descend, pause and turn near the approach. Household-stair capability is not assumed for the short-legged body. |
| 6. Grip and disturbances | Patchy friction, mild unevenness and bounded pushes. | Recover balance and adapt steps without excessive slip or joint demand. |
| 7. Falls and recovery | A clear recovery area with controlled starting orientations. | The directed front/back, sideways, inverted and mixed-contact cases in [R04](../hardware/joints/recovery-envelope.md). |
| 8. Edges and blocked routes | Simulated drop-offs, missing readings and a blocked goal. | Detect uncertainty, stop before an edge and decline an unreachable route. No physical table-edge trial implied. |

Make obstacle height, tread depth, spacing, ramp angle, friction and starting pose
configurable, with units and recorded random seeds. Size the course from Mack's
actual width, foot workspace and stopping distance. Keep a fixed evaluation course
and unseen layouts separate from the scenes used for training.

## Build the virtual body from the engineering record

The current J04-C01 file is a single example joint; it is not a complete simulation
model. The first practice-room build needs a deliberately labeled approximate
whole-body model. Replace each assumed value with measured evidence as available:

- Link geometry, joint axes/zero positions/limits, collision shapes, mass, center
  of mass and inertia. Check CAD mm versus simulator units explicitly.
- Selected actuator torque-speed behavior, transmission friction/backlash,
  compliance, command delay, rate limits and supply limits. Position commands
  must not create unrealistic unlimited actuator strength.
- Foot friction/compliance, body guards, curved face and camera-window exclusions.
  Include any added recovery mechanism and optional solar roof mass/keep-outs.
- Sensor placement, field of view, noise, latency, dropouts and observations that
  will actually be available on the robot. Simulator truth can support evaluation
  or a training teacher, but must not silently become a deployment-only input.

Match simple simulated tests to a restrained joint/leg fixture before trusting
whole-body training: motion response, static force, friction, contact deflection
and stopping. Simulation is also a way to discover that a proposed leg or recovery
arm cannot do the job; training cannot compensate for unreachable contacts.

## How the learning fits Mack

First establish a transparent baseline stance/stepping controller. Then compare
optimization or reinforcement learning against that baseline. In reinforcement
learning, repeated trials adjust a movement policy using measured outcomes.
Score stable progress toward the command, stopping and foot clearance; penalize
slip, collisions, excessive effort and unstable motion. Verify that the policy is
not exploiting contact artifacts or merely standing still to avoid penalties.
Rewards are not a substitute for hard actuator and stopping limits.

Keep navigation and locomotion distinct. A route planner chooses a feasible route
or stop; the movement policy handles balance and steps. Mack's conversational AI
requests bounded skills through the [body contract](architecture.md#proposed-softwarebody-contract).
A tested local controller enforces limits, command freshness and stopping even
if the policy or conversation process fails. Exact interfaces and loop rates await
the selected body hardware.

Train on the development computer; aim to run the accepted movement policy locally
on Mack without internet. Benchmark its actual inference deadline and memory use
on the selected onboard processor. Walking-policy versions are separate from
conversation models, personality and personal memory. Keep training episodes in
engineering logs, clearly simulated, rather than writing fictional experiences
into Bill's conversation history.

## Transfer and acceptance

Vary mass, center of mass, friction, actuator strength/delay and sensor errors
within defensible ranges. This reduces dependence on one idealized setup; it does
not prove real-world reliability. Validate on unseen layouts and parameter sets,
including stop, stale-sensor, lost-command and failed-recovery cases.

Log model/configuration hashes, simulator/solver settings, time step, seed,
training code/checkpoint, sensor/action interface, limits and evaluation results.
Report falls, slip, collisions, energy estimates, actuator-limit violations,
stop distance/time and recovery outcomes alongside task completion. Videos alone
do not qualify a controller. Change the time step/contact settings to check for
numerical artifacts before selecting a policy.

Promote a version through replay and interface tests → restrained joint/leg trials
→ representative dummy body → supervised floor trials on integrated Mack. Preserve
the previous qualified policy for rollback. A body, actuator or mass change triggers
review and relevant retesting. No automatic experimental-policy deployment or
unbounded learning on the physical robot is part of this plan.

**First implementation milestone:** an inspectable approximate Mack body, a flat
floor, a block, a ramp and one adjustable step, with reset/replay and explicit
simulation labels. Demonstrate model loading, plausible contacts and bounded
baseline commands before training. The room can then grow with the curriculum.
A future humanoid can reuse scene generators and test ideas, while requiring a
new body model, movement policy and hardware qualification.
