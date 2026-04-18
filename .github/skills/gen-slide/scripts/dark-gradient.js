#!/usr/bin/env node
/** dark-gradient.js — Dark background with gradient accents, tech/startup vibe */
const { pptxgen, parseArgs, readInput, savePresentation, buildSlides } = require("./slide-utils");

const STYLE = {
  colors: { primary: "6366F1", accent: "22D3EE", bg: "0F172A", textDark: "0F172A", textLight: "F1F5F9" },
  fonts: { heading: "Inter", body: "Inter" },
  shapes: { accentBarWidth: 0.25 }
};

async function main() {
  const { input, output } = parseArgs();
  const data = readInput(input);
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  const count = buildSlides(pres, data, STYLE);
  await savePresentation(pres, output, "dark-gradient", count);
}
main().catch(e => { console.error(e); process.exit(1); });
