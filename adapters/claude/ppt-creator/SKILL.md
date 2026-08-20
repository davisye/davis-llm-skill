---
name: ppt-creator
description: This skill should be used when the user asks to create a presentation, make slides, build a PPT deck, generate a pitch deck, or produce slide content. Trigger for requests like "make a presentation", "create a deck", "build slides", "PPT on X", or "presentation about Y".
allowed-tools: [Read, Write, Bash]
---

# PPT Creator

> **Goal**: Transform a simple topic into a presentation-ready, high-quality slide deck. When key information is missing, use the minimal intake form to gather context or apply safe defaults. Then follow the workflow to produce an outline, slide drafts, charts, and speaker notes. After generation, self-evaluate using the rubric; if the score is < 75, automatically refine up to 2 iterations until ≥ 75 before delivery.

## When to Use This Skill

Use this skill when the user requests:
- "Make a presentation/deck/PPT/slides" on any topic
- "Improve/optimize a presentation/pitch/demo"
- Converting scattered materials into a structured, persuasive slide deck
- Creating presentations with data visualization and speaker notes
- Building decks for business reviews, product pitches, educational content, or reports

## Quick Start

1. **Gather Intent**: If critical information is missing, ask the 10 Minimal Questions. If the user doesn't respond after 2 prompts, use safe defaults and note assumptions.

2. **Structure the Story**: Apply the Pyramid Principle to establish "one conclusion → 3-5 top-level reasons → supporting evidence." Each slide uses assertion-style headings (complete sentences), with body content providing evidence.

3. **Choose Charts**: Use chart selection guidelines to pick the most appropriate visualization for each point.

4. **Layout & Style**: Follow the style guide for font sizes, line spacing, white space, contrast ratios, color palettes, and accessibility (WCAG AA compliance).

5. **Speaker Notes**: Generate 45-60 second speaker notes for each slide, structured as: opening → core assertion → evidence explanation → transition.

6. **Self-Check & Score**: Score with the rubric. If total < 75, identify weakest 3 items and refine; repeat (max 2 iterations).

7. **Deliverables**:
   - `/output/slides.md`: Markdown slides, with assertion-style headings + bullet points/chart placeholders + notes
   - `/output/assets/*.png`: Generated charts (if applicable)
   - `/output/notes.md`: Full speaker notes and delivery outline
   - `/output/refs.md`: Citations and data sources
   - `/output/presentation.pptx`: If available, export to PPTX

## Core Principles

- **Information Organization**: Conclusion first, then evidence (Pyramid Principle). Each slide conveys only 1 core idea. Headings must be testable assertion sentences, not topic labels.
- **Evidence-First**: Use charts/tables/evidence blocks instead of long paragraphs; limit to 3-5 bullet points per slide.
- **Data Visualization**: Chart selection and labeling must comply with visualization standards.
- **Accessibility**: Color and text contrast must meet AA standards. Provide alt/readable descriptions for charts and images.
- **Reusability**: Use consistent naming, stable paths, reproducible output.
- **Safety & Dependencies**: Do not scrape the web without permission. Only run scripts when user provides data.

## Workflow Overview

**Stage 0 - Archive Input**: Record user's original request, defaults used, and assumptions.

**Stage 1 - Structure Goals**: Rewrite the goal into "who takes what action when" (clear CTA).

**Stage 2 - Storyline**: Use Pyramid Principle to define "one-sentence conclusion → 3-5 first-level reasons → evidence."

**Stage 3 - Outline & Slide Titles**: Create a 12-15 slide chapter skeleton. Each slide has one assertion-style heading.

**Stage 4 - Evidence & Charts**: Pick appropriate visualizations. If data is provided, generate charts; otherwise create placeholder + required field list.

**Stage 5 - Layout & Accessibility**: Apply style guide for font sizes, spacing, contrast ratios, color palettes.

**Stage 6 - Speaker Notes**: Generate 45-60 second notes per slide: opening → assertion → evidence explanation → transition.

**Stage 7 - Self-Check & Scoring**: Score with rubric. If < 75, focus on weakest 3 items, refine, re-score (max 2 iterations).

**Stage 8 - Package Deliverables**: Generate output directory with all files. Export PPTX if available.

**Stage 9 - Reuse Instructions**: Include a guide to replace data/colors for future use.
