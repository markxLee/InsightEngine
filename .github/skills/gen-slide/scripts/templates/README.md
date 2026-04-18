# Templates Directory

This folder contains template-specific configurations for PPTX generation.

## Structure

Each template config is a JSON file that defines:
- Color scheme (primary, secondary, accent, background colors)
- Font pairing (heading font, body font)
- Spacing defaults (margins, padding, line heights)
- Slide layout preferences

## Available Configs

| Config | Template | Style Category |
|--------|----------|----------------|
| corporate-blue.json | corporate-blue.js | Light / Business |
| corporate-red.json | corporate-red.js | Light / Business |
| academic-serif.json | academic-serif.js | Light / Academic |
| minimal-white.json | minimal-white.js | Light / Minimal |
| minimal-gray.json | minimal-gray.js | Light / Minimal |
| dark-gradient.json | dark-gradient.js | Dark / Modern |
| dark-neon.json | dark-neon.js | Dark / Neon |
| creative-gradient.json | creative-gradient.js | Light / Creative |
| creative-warm.json | creative-warm.js | Light / Creative |
| tech-modern.json | tech-modern.js | Light / Tech |

## Usage

Template scripts in the parent `scripts/` directory import these configs
to define their visual identity. Each template script has its STYLE config
embedded, but these JSON files serve as the canonical reference for:
- Color values (exact hex codes)
- Font names (with fallback stacks)
- Spacing values (in inches)

These configs can be used by other tools (e.g., chart generators, document
builders) to maintain visual consistency across output formats.
