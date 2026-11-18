# Diagram types and layout patterns

Pick one type per diagram. When a document needs several, make them a set: configuration first, then overview, then steps, then side processes. Each one adds detail to the previous one.

| Type | Question it answers | Main elements |
|---|---|---|
| Configuration | What exists, and where are the boundaries? | Machine cards, zones, short arrow labels |
| Overview flow | Which machines does the work pass through, in what order? | Configuration layout + numbered actions between machines |
| Step flow (swimlane) | What happens to one item, step by step? | Lanes per machine, things by kind, action chips |
| Side processes | What runs beside the main flow, and where does it connect? | Same lanes, one column per process |

## Configuration diagram

```
            [ Outside party ]  (gray, dashed)
                  │ [auto] what comes in
 ┌ LAN ───────────▼──────────────────────────┐
 │ [ Machine A ] ⇄ (what is exchanged) ⇄ [ People's PCs ] (stacked = several) │
 │      ⇅                                    │
 │ [ Machine B ] ── what ──▶ [ Machine C ]   │
 │      │      ( C drives this ) ← actor chip, dotted to C │
 └──────┼────────────────────────────────────┘
        ▼
  [ Outside destination ]  (gray, dashed)
```

- Cards: icon in a tinted circle, name, one-line role, address (monospace). Leave out addresses that change.
- A grid of 2 columns × 2–3 rows fits a document well. Put the path of the data down one column and the people's machines in the other.
- Zone frame (`zone()`) around everything inside the network. Outside parties go outside it, gray and dashed.
- Arrow labels name *what* moves, in a few words. Use a 2-way arrow when traffic goes both ways.
- If a passive node appears to send something (a storage server "sending" to a file server), put an actor chip on the arrow naming the machine that really drives it, connected to that machine by a dotted line.

## Overview flow

Same layout and size as the configuration diagram, so the reader recognizes it.

- Numbered actions (①, ②, …) label the arrows between machines.
- Steps that happen inside one machine are listed inside its card, one per line, with their numbers. Do not merge them into one line.
- Unnumbered extras (manual corrections, side uploads) are allowed, but keep them few.
- The numbers must be the same as in the step flow.

## Step flow (swimlane)

```
                 [ Outside ]
                     │ [auto] ① fetch
┌ Machine A ─────────▼──────────────────────────────┐
│ [queue]◀─② register─ [original] ─③ clean─▶ [cleaned] │
│   ┆ (priority, dotted to ①③④)                ║ ④ generate (blue) │
│ [ledger]                                 [result]   │
└─────────────────────┼──────────────────────┼───────┘
                [manual] ⑤ send (one chip, two lines)
┌ Machine B ──────────▼──────────────────────▼───────┐
│                 [original]               [result]   │
└─────────────────────────────────────────────────────┘
```

- One horizontal lane per machine, stacked top to bottom in the order the item visits them. The lane label is at the top-left inside, horizontal, in the machine's color.
- Choose the lane order so that each transfer, especially the main action's line, goes between neighboring lanes. Try the candidate orders on paper and count the lanes each line would cross; pick the order where the main line crosses none.
- The same thing on different machines is a separate box in each lane, in the same column, so the transfers are straight vertical lines.
- The main path is a straight sequence of things joined by action chips. Data-creating actions branch off it (rule 3).
- Places that are not lanes go in a side column to the right of the lanes: people's PCs, outside destinations, and services that only supply one thing to one step (a token issuer). Put each card next to the step it serves. Lines to a non-neighboring lane also run down this column.
- Instructions: an actor chip in the instructing place's color, connected to its lane edge by a solid line from a dot. From the chip, an arrow to the data it changes, or dotted trigger lines to what it starts (rule 5).

### Gate pattern (an approval or manual trigger that releases several steps)

```
[Person]        ●
                │
             (⑤ approve  manual  optional)
                ┆ trigger line (actor color)
[Service]  ┌────●─────────────── job name ┐
           │  ⑥ fetch → [thing] → ⑦ …     │   every chip of the job is inside
           └──────────────────────────────┘
```

The frame encloses every thing and chip of the released job. The trigger line ends on the frame's edge with a dot. No arrow that carries a thing ends on the frame.

### Request/response pattern (another place does the work and returns something)

```
[Requester lane]  [token A] ──⑧ exchange at X──▶ [token B]
                                  ┆ (reference: X checks its settings)
[X lane]                     [settings]
```

Keep both things in the requester's lane, name the performer in the chip, and connect the chip to the performer through the data it checks.

## Side processes

For processes that run beside the main flow (manual interrupts, data pulls, viewers):

- Reuse the step-flow lanes. Give each process its own column with a heading (the section name in the document) and light dashed dividers between columns.
- Put a process with no people involved in the leftmost column, so lines do not cross the people-lane label.
- Where a process feeds the main flow, draw the main-flow element it reaches with its step number (e.g. "② register" into the "waiting tasks" stack). Do not draw a box standing for the whole main flow.
- Each column should read like a small step flow: things, chips, and at most one emphasized main action.
