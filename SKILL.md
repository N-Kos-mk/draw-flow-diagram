---
name: draw-flow-diagram
description: Draw documentation diagrams of a system — configuration (architecture/network) diagrams, overview flows, step-by-step swimlane flows, and side-process diagrams — as reproducible code that emits SVG and PNG, following explicit drawing rules (things are boxes, actions are labelled chips on lines with auto/manual tags, product icons, minimal text, every fact verified in the code or official docs). Use this skill whenever the user asks to draw, create, redraw, fix or extend a flowchart, flow diagram, process diagram, swimlane, system/architecture/configuration/network diagram, or any 図 for a manual, README or design doc — e.g. 「フロー図を作って」「構成図を描いて」「工程の図」「全体図をコードで作成して」「この図を直して」「図が分かりにくい」 — even if they don't say "flowchart" or mention SVG. Not for data charts (bar/line plots) or UI mockups.
---

# Draw flow diagrams

A diagram in a manual exists so that a reader grasps *how the system works* at a glance, then reads the text for details. Each rule below prevents a specific misreading. When a rule seems to conflict with what the user asks, follow the user and mention the conflict.

Diagram labels default to Japanese (the 自動・手動・任意 tags and the fonts). To draw in another language, change `TAGS` and `FONT` in `scripts/diagram_kit.py`.

Bundled files:

| File | When to read |
|---|---|
| `references/diagram-types.md` | Step 2 — choosing the diagram type and its layout pattern |
| `references/review-checklist.md` | Step 6 — inspecting the rendered PNG |
| `scripts/diagram_kit.py` | Step 5 — SVG building blocks (cards, cylinders, chips with auto/manual/optional tags, lanes, scope frames, arrows, dotted references and trigger lines) |
| `scripts/icons.py`, `scripts/icons_extra.json` | Step 5 — icons: core Lucide set, plus fetched product icons (Simple Icons) and more Lucide icons |
| `scripts/fetch_icons.py` | Step 5 — add product or generic icons to `icons_extra.json` |
| `scripts/render.py` | Step 5 — SVG → PNG (Playwright Chromium) |
| `examples/minimal_steps.py` | Step 5 — a small working diagram; start new diagrams from it |
| `examples/pypi_trusted_publishing.py` | Step 5 — a full example: product icons, a scope frame with an optional approval, a side-column card, references |

## Workflow

### 1. Learn the real system first

Read the code, scripts, configs and existing docs that implement each flow before drawing anything. For a public system you cannot read the code of, use its owner's official documentation. Docs drift; a diagram that repeats a wrong doc is worse than none. Typical traps found this way: a machine that looks like it "sends" files is actually read by another machine that does the sending; one button runs two steps; two steps the docs merge are separate scripts run at different times; a step a tutorial presents as required is optional in the system itself.

Write down what you verified and where (file and function, or URL). If something cannot be verified, say so instead of guessing.

### 2. Decide the one question the diagram answers

One diagram answers one question. Pick the type from `references/diagram-types.md`:

- **Configuration** — what machines/services exist and where the boundaries are
- **Overview flow** — which machines the work passes through, in order
- **Step flow (swimlane)** — what happens to one item, step by step, and what is automatic
- **Side processes** — independent processes that run beside the main flow

If the diagram belongs to a set (e.g. configuration → overview → steps), reuse the same layout, colors and step numbers across the set so the reader can move between them.

### 3. Make an inventory

Before laying out, list:

- **Things** — images, files, records, queues, lists, databases. Each gets a shape by kind (rule 4).
- **Actions** — fetch, register, convert, judge, send, request. For each: automatic or manual, which machine or person triggers it, and the real script/button it corresponds to.
- **Places** — machines, services, network zones, external parties. Each place gets a fixed color for the whole set. Note which product each place or thing is (GitHub, Cloudflare, a smartphone…) so it can carry that product's icon (rule 4).

Cut what the reader of *this* diagram does not need (rule 1). Keep a list of what you cut so you can tell the user.

### 4. Sketch, and agree before building a new diagram

For a new diagram or a large redesign, show the user an ASCII sketch plus the inventory and wait for approval. Small fixes to an existing diagram need no sketch.

### 5. Build it as code

The diagram must be reproducible: a script that writes SVG, then PNG at 2× scale. If the project already has diagram code, extend it and reuse its parts. Otherwise copy `scripts/diagram_kit.py`, `scripts/icons.py`, `scripts/icons_extra.json`, `scripts/fetch_icons.py` and `scripts/render.py` into the project's diagram folder and write one script per diagram, starting from `examples/minimal_steps.py` (adjust its `sys.path` line to the folder that holds the kit). `examples/pypi_trusted_publishing.py` shows the larger patterns. Fetch any product icons the inventory needs (rule 4) into the project's copy.

- Compute positions from named constants (rows, columns, gaps), not scattered literals, so later adjustments move whole groups.
- Draw in this order: zones/lanes → lines → things and chips. Chips then sit on top of the lines they label.
- Measure text with `text_width()` and size boxes from it, so labels never overflow.

### 6. Look at the PNG before saying it is done

Open the PNG with the Read tool and go through `references/review-checklist.md`. Fix every overlap, overflow and cramped gap, then look again. Once it reads correctly, compact it: shorten lanes to their content and pull columns together until no large empty area remains. Never report a diagram you have not looked at.

### 7. Report

Tell the user, briefly:

- what the diagram shows and which facts you verified, and where (code or official docs)
- judgment calls (auto vs manual, what you merged or cut, numbering), so they can overrule them
- anything in their instruction you did not follow exactly, and why
- mismatches you found between the code and the existing docs (report them; do not silently fix the docs)

### 8. Keep the project's rule file

Keep a `DRAWING_RULES.md` next to the diagram code. Record project decisions there: the color of each place, the step numbers, fixed label wording. When the user corrects a diagram, add the correction as a general rule (not "move box X left" but the principle behind it). Read this file first whenever you return to the project's diagrams. If a correction applies to any system, suggest adding it to this skill as well.

## Rules

### 1. Show only what the reader needs

The figure gives the shape of the mechanism; the text gives the details. Boxes carry names only. Tool names, paths, settings, rates and explanations go in the text. Avoid gray caption sentences; add one short note only when the shape of the diagram cannot carry the point. Captions compete with the shapes for attention, and a figure full of them is read as text instead of as a picture.

When a secondary flow would crowd out the main point, leave it out and tell the user what you left out.

### 2. Things are boxes; actions are chips on lines

Things (data, images, queues, lists) are boxes. Actions (fetch, register, remove, generate, classify, judge, send, roll back, request) are labelled chips placed on the line they move along. Do not draw an action as a box. Do not draw a whole process (a batch, "the main flow") as a box joined by arrows: break it into things and actions, or reuse the elements already drawn for it (rule 10).

A dashed **scope frame** (`scope_frame()`) may mark the part of a flow that runs inside one job, environment or permission scope, for example the steps an approval releases. It shows the real things and chips inside it, so it is a boundary, not a box:

- It encloses every thing and chip that runs in that scope, and nothing else. A chip of the scope left outside the frame contradicts it.
- No arrow that carries a thing ends on the frame. Arrows go to the things inside it.
- An instruction that releases the scope connects to the frame's edge with one dotted trigger line (rule 5).

### 3. An arrow between two things means "becomes"

Readers take thing → thing as "A turns into B". Use that form only when it really does (original image → cleaned image).

- An action that *creates data* (registering a task, recording a result) branches off the main path. It is not a stage the item passes through. Wrong: image → task → cleaned image (the image seems to become a task).
- An action that *reads* items and produces several outputs branches into each output: judge → result, judge → passed image. Wrong: image → classified image → result.

### 4. One shape per kind of thing

Do not draw everything as same-sized rectangles. Kinds must look different from one another:

| Kind | Shape (`diagram_kit`) |
|---|---|
| Image or file | white card with an icon — `thing()` |
| Queue, waiting list | stacked cards — `stacked()` |
| List or ledger of items | table with a header band — `table_card()` |
| Records in a database | cylinder — `cylinder()` |
| Machine or service (configuration diagrams) | card with icon circle, name, role, address — `card()` |
| Outside party | the same card, gray and dashed |

Inside each shape, the icon says *what* it is. When a place, service or thing is a specific product (GitHub, Notion, Cloudflare, a Python package, a React app, a smartphone), use that product's icon: readers recognize a logo faster than they read a label. Use a generic icon only when no specific one exists.

- Product icons come from Simple Icons and keep the brand color. Generic icons come from Lucide and take the place's color. Pass either name as `icon_name`; the kit tells them apart.
- Fetch missing icons with `scripts/fetch_icons.py` (`python fetch_icons.py github notion`, or `--lucide smartphone` for generic ones). It writes `icons_extra.json` next to the kit; keep that file with the diagram code so builds need no network. Fetching sends only the icon names to the CDN.
- Use a product icon only to identify a product that is really involved, and do not alter its shape. Some owners have had their logos removed from Simple Icons (for example Microsoft, AWS, Slack, OpenAI). For those, use a generic icon (cloud, server, chat) instead of copying the logo from elsewhere.
- A few icons carry their own license (for example Android and Git are CC-BY-3.0). `fetch_icons.py` prints a note for them and records the license and source in `icons_extra.json`. Tell the user, so the required notice is added where the diagrams are published.
- Keep the label beside the icon. The icon speeds recognition; the label carries the exact name.
- In the filled main-action chip, use a generic icon. Brand marks are drawn white there and lose their shape.

### 5. Every action chip says how it runs and who runs it

- Tag every action as automatic or manual (`自動` / `手動`). "Send" alone does not tell the reader whether a person has to do it.
- Emphasize the main processing step (filled blue chip, thick blue arrow — `main_action()`, `main_arrow()`).
- One action, one chip. When the same action moves two things along two lines, join the lines and place a single chip (`pair_action()`). Two chips with the same number confuse the reader.
- Mark optional steps. A step that only happens when someone has configured it (an approval gate, a retry, a notification) gets the `任意` tag (`optional=True`). Drawing it as always present misinforms the reader.
- Show who drives the action. If a passive place (a NAS, a bucket) seems to send something, the reader will believe it does. Put an actor chip in the driving machine's color and icon (`actor_chip()`), connected to that machine by a solid line from a dot on its edge.
- Show what an instruction starts. If it changes data, draw an arrow from the chip to that data. If it starts other actions, draw dotted trigger lines in the actor's color (`trigger_line()`), ending in a dot:
  - two or three actions: one trigger line to each chip, and give those chips the actor's border color
  - more, or one whole job: enclose them in a scope frame (rule 2) and draw one trigger line to the frame's edge
- When another place performs an action for the requester (a service call that returns something, such as exchanging a token), keep the things in the requester's lane, name the performer in the chip ("exchange at X"), and connect the chip to the performer, for example with a dotted reference from the data the performer checks. Drawing the request and the response as two long lines usually costs more clarity than it adds.
- Split numbers along the real operations (one script, one button = one number). Do not give one number to two operations that run at different times.

### 6. Do not bundle

Two things are two boxes with two lines, never one box labelled "A and B". Separate steps in an overview are listed one per line, not merged into "steps 2–4".

### 7. Dotted lines mean "refers to"

Use a dotted line when an action consults data without changing it (priority order, a reference classification).

- Draw one reference as one connected dotted line that branches. Stop each branch at the chip it affects and mark the end with a small dot (`ref_line()`, `ref_end()`), so the reader can tell a target from a line that only passes by.
- Lines may cross lines. Lines must not run over boxes or chips. Leave a clear gap on both sides of a line squeezed between two elements.

### 8. Layout and lettering

- Few bends; a return arrow should bend at most once.
- Order lanes so that every transfer, and above all the main action's line, runs between neighboring lanes. A line that crosses a lane it has nothing to do with makes the reader think the item passes through that place.
- Give a lane only to places where things stay or several steps happen. A place that only supplies one thing to one step (a token issuer, a lookup service, an outside destination) is a card in a side column to the right of the lanes, next to the step it serves.
- When a line must reach a lane that is not a neighbor, route it through the side column, outside the lanes it does not involve, and enter the target lane from its edge.
- Labels of places and lanes are horizontal (vertical text looks wrong), at the top-left inside the lane, with the place's icon and color.
- One color per place, the same in every diagram of the set. Show the boundary between inside (the LAN, the system) and outside.
- Size for the document: roughly 900–1300 px wide, so text stays readable when embedded. After adding elements, rework the layout instead of squeezing. Large empty areas are a sign of a poor lane order or a line routed too far out; fix the cause rather than filling the space.
- Break multi-line labels at meaningful points.

### 9. Words and facts

- Keep the user's wording for labels. If you think another word is better, propose it; do not switch silently. If an instruction seems to contain a slip (a different word for an established label), keep the established word and ask.
- Use the same terms as the document's glossary.
- When the user's instruction contradicts the code, follow the code in your proposal and explain the difference.
- When sources disagree (a tutorial says a step is required, the system's own docs call it optional), draw what the system itself does, according to its owner's docs, and report the difference.

### 10. Diagrams in a set refer to each other

When a diagram touches a flow drawn in another diagram, draw the same element with the same shape, label and step number (for example, "② register" leading into the "waiting tasks" stack) instead of a gray "see other diagram" box. The shared number tells the reader where it connects.

## Common mistakes

Check these first:

1. A process or action drawn as a box
2. Many gray caption sentences, tool names, ports or paths in the figure
3. thing → thing arrows that read as a transformation that does not happen
4. All things drawn as identical rectangles
5. Chips without an auto/manual tag, or with the same number twice
6. Two things bundled into one box
7. A dotted line whose targets are unclear, or a line running through a chip or card
8. Overflowing text or labels touching neighbors in the PNG
9. Labels changed without being asked
10. Flows drawn from the docs without checking the code
11. The main action's line crossing a lane it has nothing to do with
12. A minor supplier given its own lane between the lanes the main path joins
13. An arrow ending on a scope frame, or a chip of the scope left outside the frame
14. An optional step drawn as always present
15. Large empty areas left after the layout works
16. A well-known product (GitHub, Cloudflare, Python…) drawn with a generic icon
