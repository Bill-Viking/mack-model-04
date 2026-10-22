# Home Dell — Mack CAD and analysis handoff

Prepared 2026-10-21. This is an engineering brief for the session running on Bill's
home Dell. Bill confirmed personal Creo and Ansys installations there; no version,
module, native import or automation capability has been verified from the Mac.
This file prepares future Dell work; it does not start another chat or transfer
the current writer claim.

## Mission and first deliverable

Continue Mack's J04 joint development from the original [D01 parametric model](joints/cad/README.md).
First deliver a local tool/import report, a correctly scaled native inspection
assembly and an explicit list of measured inputs needed for the next revision.
Do not present the placeholder solids as completed mechanisms or run a meaningless
stress analysis using invented loads and materials.

Public project: <https://github.com/Bill-Viking/mack-model-04>. Read the project's
STATUS.md and OPENER.md before choosing the next action. The latest committed
version of this brief, source, parameters and exports must travel together.

## Local startup and ownership

Follow the Dell's current Exocortex AGENTS instructions from their source files.
Read `~/.claude/exocortex-laws.md`, `~/Exocortex/dossier/LAWS.md` and
`~/Exocortex/openai/ONBOARD.md` in order. Read the machine clock; perform the
prescribed brain pull with `python "$env:USERPROFILE\orchestrator-sync\sync.py" pull`.
Use `~/orchestrator-sync/machine.json` to locate the actual home project root and
hub; do not assume the Mac's path exists. Apply the current stamp, one-writer and
mail rules. Inspect for an existing Mack checkout before considering a clone.

Confirm the Git remote is Bill-Viking/mack-model-04, inspect local modifications,
branch and HEAD, and establish an uncontested engineering lane before editing.
If another session holds the same work, stop that overlapping work and resolve
ownership. Do not reset, clean or overwrite local changes. A clean authorized
checkout can be advanced with `git pull --ff-only`; divergence requires review.
No changes to repository visibility, collaborators, protected local-only projects,
or personal voice/memory files are part of this task.

## Inspect and record the installation

Read the actual Creo About/version information and installed capabilities. Record
the Ansys release, geometry tools and available solver modules. Distinguish
standalone Mechanical from Creo Ansys extensions. Record which supported local
interfaces the session can actually use: application UI, scripts/APIs or batch
tools. Do not claim remote control from the Mac merely because the software exists
on the Dell. Do not modify licenses, credentials or purchase extensions.

Inspect the available Python versions if regenerating the scripted CAD is useful.
Keep its environment under `runtime/cad/`; leave Mack's speech environment alone.
The CAD guide provides optional Windows commands for a verified Python 3.12
installation. Record resolved dependency versions; the Mac lock is not a Windows
qualification result.

## Import trial

1. Import `hardware/joints/cad/exports/j04-c01-draft.step` into a new scratch
   workspace under this project's ignored `runtime/cad/`. Set/verify mm explicitly.
2. Verify **six solids**, names/colours where supported and the neutral overall
   size **40 × 108 × 100 mm**. Compare volume/geometry against
   `exports/geometry-check.json`; inspect all three principal views and a section.
   Note any healing, missing surfaces, changed body count or unit conversion.
3. Check the separate yoke, output-link and shaft exports if needed to establish
   part ownership and assembly structure. Identify them as D01 reference geometry,
   not native parametric designs. Save the inspection assembly separately.
4. Import the same revision into the available Ansys geometry route and confirm
   units and body separation. Stop before assigning invented materials, restraints
   or loads. Record the supported exchange path and any translation problems.

The nominal coincident shaft/bore and bearing/yoke surfaces do not specify
press/slip fits. The moving link has no keyed, splined or clamped connection yet.
Bearing retention, motor mount/coupler, encoder, cables, stops and covers are open.
The current motor envelope is a box, and the two bearing envelopes are plain rings.

## Advance the design when inputs exist

Use [engineering-workflow.md](engineering-workflow.md), the J04 study,
measurements.csv, system-budget.csv and product requirements as the engineering
record. First integrate actual enclosure datums and component dimensions. Select
one master for the next revision: build123d source or a native Creo model. If Creo
becomes the master, rebuild the needed features and document that transition;
do not silently edit an imported STEP and call its source parametric.

Develop coupling/retention and a restrained one-joint fixture before expanding to
the three-axis leg. Define numeric load cases and limits from the actual design,
then prepare Ansys models with contact review, convergence and hand-calculation
checks. Retain solver projects and large intermediates locally under runtime;
publish original compact reports and approved source/export files by revision.
Keep third-party restricted CAD and personal license information out of the public
repo. Manufacturing upload and expenditure are later steps against a reviewed
release and concrete quote.

## Return evidence

Update STATUS.md and the appropriate opener with observed Creo/Ansys versions,
available interfaces, import body count/units/bounds, saved native-file locations,
screenshots, unresolved translation issues and the next engineering input. Clearly
separate observations from proposals. Include no license keys, private paths from
other projects, personal conversation data or supplier-restricted files.

Commit the relevant original engineering files and report to the uncontested
project branch, push and verify the remote revision under the project's ownership
rules. Preserve D01 and its example label. If imports fail, retain the failing
export and diagnostics and report the exact failure without claiming success.
