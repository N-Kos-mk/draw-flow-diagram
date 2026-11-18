# Review checklist (run on the rendered PNG)

Open the PNG with the Read tool and check each item. Fix, re-render, and look again until everything passes.

## Meaning

- [ ] Every box is a thing (data, image, queue, list, database, machine). No action or whole process is drawn as a box.
- [ ] Every action is a chip on a line, tagged auto or manual. Steps that only happen when configured also carry the optional tag.
- [ ] Scope frames enclose every chip and thing of their scope, and no arrow ends on a frame.
- [ ] Each instruction shows what it starts: an arrow to the data it changes, or trigger lines to the chips or frame it starts.
- [ ] Each thing → thing arrow is a real transformation. Data-creating actions branch off the main path.
- [ ] An action that produces two outputs branches into both.
- [ ] Different kinds of things have different shapes. The ledger, the queue and the database do not look alike.
- [ ] Places and things that are a specific product (GitHub, Cloudflare, a Python package, a smartphone…) carry that product's icon. Generic icons appear only where no product icon exists.
- [ ] No box holds two things ("A and B"). No two chips carry the same number.
- [ ] For every transfer, the machine that drives it is clear (actor chip where a passive place seems to act).
- [ ] The main processing step is the only emphasized action.
- [ ] Numbers match the other diagrams in the set and the real operations (one script or button = one number).
- [ ] Every flow was checked against the code.

## Text

- [ ] Boxes carry names only. No paths, tool names, ports or settings unless the user asked for them.
- [ ] Few or no caption sentences.
- [ ] Labels use the user's wording and the document's glossary. Nothing renamed silently.
- [ ] Lane and zone labels are horizontal.
- [ ] Multi-line labels break at meaningful points.

## Geometry

- [ ] No text overflows its box or chip.
- [ ] No line runs over a box or chip (crossing other lines is fine).
- [ ] No chip touches a neighboring box. There is a visible gap on both sides of every line squeezed between elements.
- [ ] Dotted reference lines are connected, branch clearly, and end at their target chips with a dot.
- [ ] Return arrows bend at most once.
- [ ] The main action's line crosses no lane it has nothing to do with. Other lines that reach distant lanes run in the side column, not through the contents of other lanes.
- [ ] Services that only supply one thing to one step are cards in the side column, not lanes.
- [ ] Lane labels are not crossed by lines.
- [ ] Inside/outside boundaries are visible (zone frame, dashed outside parties).
- [ ] The overall size suits embedding in the document (about 900–1300 px wide), with no large empty areas left by an old layout.
