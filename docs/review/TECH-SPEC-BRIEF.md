# Draft the Mack technical specification: one page an engineer can read top to bottom and critique

One bounded run. You write two new files and nothing else:
`docs/technical-spec.md` and `.github/ISSUE_TEMPLATE/design-feedback.md`.
Do not edit any existing file; another builder is redrawing `hardware/joints/figures/*.svg`
in place (the three file names stay).

## Why
Bill, the owner, in his words: lay out the "full technical spec so an engineer could look at
our designs, on all levels, mechanical, AI, electrical etc, sensors, and follow along and make
helpful suggestions if maybe we hadn't considered something". Today the design is spread over
about forty documents and a visitor cannot find the joint design. The reader is a practising
engineer (mechanical, electrical or software) with ten minutes and no knowledge of this
project. Success is that they understand what is decided, what is only proposed, what is
unknown, and exactly where their critique is wanted.

## Inputs (read in this order; tracked files only, never ignored folders)
1. `docs/review/FACTS-PASS-BRIEF-REPORT.md` — a fact digest of every document with file and
   line references. Use it as your index; open the source document before you state a number.
2. `docs/review/design-review-2026-11-11.md` — the judge's review. Its findings must appear in
   the spec as open issues and reviewer questions, in neutral words, linked to the review.
3. `docs/product-spec.md`, `docs/roadmap.md`, `docs/architecture.md`, `docs/model-strategy.md`,
   `hardware/integration-plan.md`, `hardware/battery-power.md`, `hardware/charging-dock.md`,
   `hardware/display-and-vision.md`, `hardware/solar-feasibility.md`, `hardware/joints/README.md`,
   `hardware/joints/leg-layout.md`, `hardware/joints/leg-packaging.md`,
   `hardware/joints/recovery-envelope.md`, `hardware/workshop-road.md`, `hardware/parts.csv`,
   `hardware/system-budget.csv`, `software/README.md`, `software/desktop/README.md`,
   `software/mack/LISTENING.md`, `software/mack/VOICE.md`, `README.md`.

## Rules that outrank style
- Invent nothing. No new decision, number, part choice or target. Every number is copied from
  a source document and carries that document's standing in a tag: `DECIDED` (Bill's ruling,
  with date), `PROPOSED`, `CATALOG`, `CALCULATED`, `ASSUMED`, `MEASURED`, or `OPEN`.
  Nothing on hardware is MEASURED yet; say so once, early.
- Where the repository is silent on something an engineer would expect, write
  `Not yet addressed.` and add it to that section's reviewer questions. Silence stated plainly
  is the point of this document.
- Link every claim's source with a relative Markdown link from `docs/` (for example
  `[leg packaging study](../hardware/joints/leg-packaging.md)`). Check each link target exists.
- Nothing is built, printed, ordered or tested on hardware; the host software runs on a
  development computer. Never blur that line.
- No private material: no home folder paths, no voice reference assets, no memory contents,
  no employer, no personal details beyond the owner's first name as the documents use it.
  Name commercial parts only as the source documents already do.
- Plain engineering English. Short sentences. Tables for anything with more than three
  parallel items. No marketing words. No first person.

## Shape of `docs/technical-spec.md` (2,600 to 3,800 words)
0. Title, one-paragraph summary, a `Status at a glance` table (one row per subsystem: state in
   five words, standing tag, link), and the tag legend.
1. `System overview` — a Mermaid `flowchart` (GitHub renders ```mermaid fences) showing the
   body, base and legs, actuators and their controller, power, compute, sensors, display and
   face, AI runtime and memory, the dock; solid lines for what exists in software today,
   dashed for proposed hardware. Then one paragraph on the two control levels (conversation
   and mind; independent body controller) from the architecture document.
2. `Requirements and release gates` — P01 to P13 in one compact table (ID, requirement in a
   dozen words), G0 to G8 in another with current state.
3. `Mechanical` — body and shell, base, legs (axes, links, the three placements, both knee
   drives with their masses and heights), joint cartridge, feet, recovery envelope, printing.
   Embed the three figures with Markdown image syntax and one-line captions:
   `../hardware/joints/figures/leg-axes.svg`, `actuator-space.svg`, `knee-layouts.svg`;
   link the 3D models folder `../hardware/joints/models/` ("models a visitor can turn in the
   browser") and the interactive viewers and animation under `../hardware/joints/cad/exports/`.
4. `Actuation` — benchmark, candidates, what is unknown (continuous torque, thermal), the
   review's static torque table by reference.
5. `Electrical and power` — battery direction and the B04 sizing examples, rails, protection,
   charging dock, optional solar; what is unselected.
6. `Compute and control` — host today, proposed onboard computer and body controller, the
   command contract, stop behaviour.
7. `Sensing` — functions required, candidates named, none selected.
8. `Display, face and vision`.
9. `AI and software` — what runs today (models, memory, tools, listening, voice), the
   onboard and assisted modes as decided, what remains open.
10. `Budgets` — say plainly that the budget table is blank; reproduce the review's first-pass
    mass estimate as an estimate for discussion with its tags and a link.
11. `Verification` — the proof order from the integration plan; what has actually been
    checked so far and on what (software on the host; CAD checks; nothing on hardware).
12. `Open issues and where review would help most` — a numbered list of 12 to 18 specific
    questions an outside engineer could answer, grouped by discipline, each one sentence,
    each linked to the section or document it concerns. Include the nine review findings.
13. `How to give feedback` — open an issue on the repository using the "Design feedback"
    template; say what helps (which section, what you would change, why, a reference).
14. `Document map` — a table of the detailed documents by discipline.
End each of sections 3 to 9 with a short `Questions for reviewers` list (2 to 4 items).

## `.github/ISSUE_TEMPLATE/design-feedback.md`
A standard issue template with YAML front matter (`name: Design feedback`, `about:` one line,
`title: "[feedback] "`, `labels: feedback`), then four short prompts: which section or file;
what you would change or what was missed; why (experience, a calculation, a reference); how
confident you are. Under twenty lines.

## Checks you run before handing back
Word count of the spec; every relative link target exists on disk (list any that do not);
every number in the spec appears in a source document (list the number, the source file and
line for each, in the hand-back); the Mermaid block has balanced brackets and no HTML;
no line contains a home folder path; the tag legend's tags are the only tags used.

## Hand-back
`STATE:` DRAFTED or STOPPED · the two file paths with sizes and the word count · the
number-to-source table · links that failed · anything in the brief you could not satisfy ·
`OPEN:` decisions you met and did not make, or none. End with `SPEC DRAFT DONE`.
