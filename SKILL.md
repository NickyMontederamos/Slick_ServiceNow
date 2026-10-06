---
name: interactive-flow-map-builder
description: Create or upgrade a standalone, dependency-free HTML application that visualizes architectures, workflows, agent systems, operational processes, or service journeys as interactive flow maps. Use when users request an interactive flow map, architecture command center, mission-control UI, workflow simulator, clickable process diagram, animated system map, or a polished standalone HTML visualization.
---

# Interactive Flow Map Builder

Create premium, implementation-ready, standalone HTML flow-map experiences. The final artifact must work by opening one local `.html` file and must not require a server, package installation, CDN, external font, or network request.

## Primary workflow

1. Extract the minimum complete brief from the conversation:
   - map purpose and audience
   - required views or scenarios
   - nodes, groups, edges, and decision gates
   - risk or status model
   - desired visual direction
   - technical and accessibility constraints
2. Reuse prior approved design decisions. Do not ask the user to repeat information already supplied.
3. Start from `assets/flow-map-template.html` when its command-center interaction model fits.
4. Replace domain-specific labels, layouts, scenarios, detail-panel copy, and simulation paths with the user's content.
5. Preserve a single-file architecture: inline CSS, inline JavaScript, and inline SVG only.
6. Validate the artifact using `scripts/validate_flow_map.py`.
7. Return the final `.html` file and a concise list of implemented interactions and validation performed.

## Required interaction baseline

Unless the user requests a simpler artifact, include:

- at least two switchable map views when the content supports them
- pan, wheel zoom, zoom controls, and fit-to-view
- selectable nodes with a detail panel
- visible edge relationships
- scenario playback or active-path highlighting
- status or risk legend when applicable
- responsive behavior for desktop and narrow screens
- keyboard focus indicators and accessible button labels
- reduced-motion handling

## Data model

Represent the system with plain JavaScript objects:

```js
const nodes = {
  intake: {
    label: 'Intake Agent',
    icon: 'IN',
    status: 'read',
    description: 'Normalizes incoming work.',
    responsibilities: ['Parse inputs', 'Detect missing fields'],
    guardrails: ['Schema validation', 'No write access']
  }
};

const views = {
  architecture: {
    title: 'System Architecture',
    nodes: { intake: [100, 200], policy: [400, 200] },
    edges: [['intake', 'policy']],
    groups: [['Control plane', 70, 160, 520, 180]],
    runPath: ['intake', 'policy']
  }
};
```

Keep content separate from rendering logic so future edits require changing data rather than DOM code.

## Visual system rules

- Establish clear hierarchy before adding glow or motion.
- Use a restrained dark or light system with one primary accent and semantic state colors.
- Keep node labels readable at default fit-to-view scale.
- Use glass effects sparingly and maintain sufficient contrast.
- Avoid generic gradients, excessive neon, and decorative animation that competes with the map.
- Use spatial grouping, labels, and edge routing to explain the architecture.
- Do not use programmatic image generation for backgrounds. Prefer CSS surfaces and inline SVG.

See `references/design-system.md` for tokens and interaction guidance.

## Safety and governance defaults

For operational, enterprise, or agentic systems:

- label simulated metrics as illustrative unless connected to verified data
- visually distinguish automatic, approval-gated, read-only, and human-only actions
- prevent a demo from implying that production actions are actually executed
- avoid embedding secrets, tokens, tenant URLs, customer data, or credentials
- treat imported labels and record content as untrusted text
- use `textContent` for dynamic user-controlled content rather than raw `innerHTML`

## Accessibility acceptance criteria

- every interactive control is keyboard reachable
- visible focus indicator is present
- controls have accessible names
- selected and pressed states use semantic attributes where applicable
- text and meaningful UI meet WCAG 2.2 AA contrast targets
- layouts remain usable at 200% zoom
- motion respects `prefers-reduced-motion`
- map meaning is also exposed through labels and detail content, not color alone

## Technical acceptance criteria

- exactly one final `.html` artifact unless the user asks for source packaging
- no external `src` or `href` dependencies
- no build step or web server required
- JavaScript parses successfully
- major views render from structured data
- no console-breaking references in initialization code
- mobile panels can be opened and dismissed
- production or destructive controls are clearly simulated or gated

## Validation

Run:

```bash
python /home/oai/skills/interactive-flow-map-builder/scripts/validate_flow_map.py path/to/output.html
```

If installed elsewhere, run the script from this skill package's `scripts` directory.

The validator checks:

- HTML shell and viewport metadata
- inline style and script presence
- absence of external dependencies
- JavaScript syntax when Node.js is available
- baseline interaction and accessibility markers

Also inspect the file manually in a browser when browser tooling is available. Never claim browser validation if it was not actually performed.

## Output style

State:

1. artifact name and purpose
2. implemented views and interactions
3. validation evidence
4. any remaining human review, especially visual, keyboard, screen-reader, performance, and browser testing

Do not provide a long design plan when the user asked for the file. Build the artifact first.
