# Flow Map Design System

## Recommended tokens

```css
:root {
  --bg: #050816;
  --surface: rgba(11, 18, 39, .82);
  --surface-strong: #0b1227;
  --border: rgba(148, 163, 184, .24);
  --text: #e8f0ff;
  --muted: #8fa4c7;
  --accent: #22d3ee;
  --secondary: #9b7bff;
  --success: #31e6a1;
  --warning: #ffca62;
  --danger: #ff6482;
  --radius: 18px;
}
```

## Semantic states

- Read or evidence: cyan
- Automatic and verified: green
- Approval-gated: amber
- Human-only, blocked, or destructive: red
- Inactive infrastructure: desaturated blue-gray

Never rely on color alone. Pair state colors with text, icons, or badges.

## Layout

- Use a stable world coordinate system, typically 1200 by 760.
- Fit the world into the viewport on first render and window resize.
- Keep nodes at least 150 by 72 pixels in world coordinates.
- Separate clusters with generous whitespace.
- Keep controls outside the transformed world layer.

## Interaction

- Pointer drag pans the map.
- Wheel or explicit controls zoom around the pointer or viewport center.
- Selecting a node opens details without changing the map unexpectedly.
- Scenario playback highlights one edge and one node at a time.
- Escape closes temporary panels.
- Space may start playback only when focus is not in an input control.

## Motion

- Prefer 180 to 300 ms interface transitions.
- Use one-second pulses only for active execution states.
- Animate a small data particle along the active edge rather than animating every edge continuously.
- Disable or drastically reduce motion under `prefers-reduced-motion`.

## Content

Each node should define:

- concise name
- role or lifecycle stage
- one-sentence purpose
- responsibilities
- guardrails or limitations
- semantic risk/status

Each view should define:

- title and subtitle
- node coordinates
- directed edges
- group boundaries
- simulation path
