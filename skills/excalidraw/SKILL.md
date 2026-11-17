---
name: excalidraw
description: Create, inspect, compare, and edit Excalidraw diagrams and .excalidraw or .excalidraw.json files. Use for editable sketches, whiteboard layouts, or an existing Excalidraw artifact; preserve the user's chosen notation and format for other diagram tasks.
---

# Excalidraw

Keep the diagram editable and make the requested visual change with minimal disruption to its existing content.

## Choose an approach

- Identify the requested operation and source artifact. Use an available Excalidraw editor or integration when it supports the task; otherwise work with the scene data and available local tools.
- Excalidraw JSON can be verbose. Inspect file size, element counts, labels, IDs, and relevant connections through bounded queries before loading a whole large scene. Retain geometry and bindings when they matter to the task; text alone cannot establish arrow direction or grouping.
- Small, focused inspections and edits can be handled directly. For large files, comparisons, or substantial layout work, the main agent may delegate a bounded task when authorized and useful. Follow project rules about who may delegate; a worker must not spawn another worker where only the lead may do so. If delegation is unavailable, use focused extraction and continue directly.
- Do not convert an existing diagram to another format, replace it with a raster image, or rebuild unrelated areas merely to simplify editing.

## Inspect, create, or edit

For an explanation or comparison, identify visible elements, arrows, labels, groups, and relevant differences. Distinguish visible relationships from inferred intent; check the rendered view when geometry affects the interpretation. Do not mutate the artifact for a read-only request.

For creation, use the requested content and level of detail. Select a clear reading direction, consistent shape meanings, enough spacing for labels, and a restrained palette. Return an editable scene file; add PNG or SVG exports when requested or needed for inspection.

For edits:

- Preserve unaffected element IDs, content, styles, stacking order, groups, frames, embedded image data, and scene settings. Add unique IDs for new elements.
- Update labels together with their text dimensions and container relationships. Keep arrow endpoints, bindings, and reciprocal bound-element references consistent when adding, moving, or removing connected shapes. Preserve image `fileId` links and their `files` entries.
- Use supported APIs or an existing valid scene's conventions for the installed version. A JSON object that parses is not necessarily a valid or usable Excalidraw scene. Do not regenerate the entire scene to change one label.
- When programmatic creation is useful, check the installed API and consult [element conversion](https://plus.excalidraw.com/docs/sdk/excalidraw/api/excalidraw-element-skeleton). `convertToExcalidrawElements` can create elements, text containers, and arrow bindings from skeletons. It regenerates IDs by default; use the installed version's ID-preservation option when retaining existing IDs matters. [Restore utilities](https://docs.excalidraw.com/docs/@excalidraw/excalidraw/api/utils/restore) and [export utilities](https://docs.excalidraw.com/docs/@excalidraw/excalidraw/api/utils/export) are available in supported versions; do not assume their signatures or the SDK are installed.

## Validate the outcome

- Parse changed scene JSON and inspect identifiers and changed relationships for duplicate or dangling references. Check that unrelated content and embedded assets remain present.
- Open the scene in a compatible Excalidraw renderer or export it using available tooling, then visually inspect the changed area and its surrounding connections. Check text fit, arrow direction, crossings, spacing, overlap, clipping, and legibility at the intended size.
- For an interactive edit, confirm that the scene remains editable and bound text and arrows behave as intended. Inspect the result after the change, not only a pre-edit screenshot.
- If a renderer is unavailable, state that only structural checks were performed and identify any remaining visual uncertainty. Do not call a scene visually verified from JSON checks alone.
- Deliver the requested artifact path or explanation, a concise change summary, and checks actually performed. Do not return a whole scene's raw JSON in chat unless requested.

## When delegating

The lead keeps ownership of scope and final verification. Specify the objective, source files, allowed edit paths or read-only scope, applicable rules, and the output needed: a short semantic summary or changed artifact paths, IDs needed for integration, checks performed, and remaining uncertainty. Request no raw full-scene JSON in the response. The lead reviews the actual artifact and evidence before accepting the result.
