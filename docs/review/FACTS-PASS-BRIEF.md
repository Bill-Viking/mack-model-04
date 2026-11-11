# Facts pass: what the Mack repository says today, by engineering discipline (read-only digest)

One bounded run. You change no file except your hand-back report. No judgment, no
recommendations, no rewriting: you extract what the tracked documents say, with where they
say it. A judge reads your digest next and must be able to trust every line.

## Read
Every tracked document below (use `git ls-files` to confirm; never open ignored folders such as
`sources/`, `private-media/`, `runtime/`, `recordings/`, `.env*`, and skip `vendor/` except each
`SOURCE.md` and `vendor/README.md`):
`README.md`, `STATUS.md` (the `## Important` section in full, the newest ten dated entries of
`## Now`, every open `- [ ]` item), `docs/*.md`, `hardware/*.md`, `hardware/*.csv`,
`hardware/joints/*.md`, `hardware/joints/cad/README.md`, `hardware/joints/cad/*.json` (keys and
provenance lines, not meshes), `hardware/joints/cad/exports/l02-comparison.json` (headline
values), `software/README.md`, `software/desktop/README.md`, `software/mack/*.md`,
`software/mack/identity.json`.

## Write (your hand-back report IS the digest), in this order, plain Markdown, at most 650 lines
Every bullet ends with its source as `file:line`. Quote decision-critical values verbatim
(numbers with units, dates, names of parts). Tag each number with the document's own word for
its standing: MEASURED, CATALOG, ASSUMED, RECALLED, CALCULATED, or UNTAGGED if the document
gives none.

1. `IDS` — every identifier scheme in use (for example J04-L02, B04, D04, R04, W04, G1 to G5)
   and what each names, one line each.
2. `DECIDED` — every decision the documents attribute to Bill, with its date.
3. `COMPLETION` — how the documents define the finished product and the first prototype
   (product spec, roadmap, integration plan): the stated criteria, stages and gates, verbatim
   where short.
4. One section per discipline, each with three lists, `SAYS` (facts and numbers), `SELECTED OR
   NOT` (parts and approaches chosen, proposed, or explicitly unselected), `OPEN` (questions and
   gates the documents themselves name):
   `MECHANICAL` (body, shell, cradle, legs, joints, feet, recovery, printing),
   `ACTUATION` (servos, torque, speed, bus, thermal),
   `ELECTRICAL AND POWER` (battery, rails, protection, charging, dock, solar, wiring),
   `COMPUTE AND CONTROL` (onboard computer, motion controller, interfaces, timing, stop behaviour),
   `SENSING` (IMU, ranging, contact, current, camera, microphone),
   `DISPLAY AND FACE` (screen, optics),
   `AI AND SOFTWARE` (models, memory, voice, listening, desktop, tools, what runs today and where),
   `SAFETY AND TEST` (limits, stop, qualification tests, what has actually been tested),
   `BUDGETS` (mass, power, energy, cost: every budget line with its tag).
5. `CONTRADICTIONS` — pairs of statements in different places that disagree (a number, a status,
   a selection), each with both sources. Include statements a later entry supersedes while the
   older document still reads as current.
6. `SILENT` — for each discipline, topics a hardware or robotics reviewer would look for that no
   document mentions at all (list the topic only; do not advise).
7. `MAP` — every document read, one line: path, what it covers, last date it mentions.

End the report with `FACTS PASS DONE`.
