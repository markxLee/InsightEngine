#!/usr/bin/env node
/** corporate-blue.js — Professional blue business template */
const { pptxgen, parseArgs, readInput, savePresentation, buildSlides } = require("./slide-utils");

const STYLE = {
  colors: { primary: "1F4E79", accent: "3498DB", bg: "FFFFFF", textDark: "2C3E50", textLight: "FFFFFF" },
  fonts: { heading: "Arial Black", body: "Arial" },
  shapes: { accentBarWidth: 0.3 }
};

async function main() {
  const { input, output } = parseArgs();
  const data = readInput(input);
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  const count = buildSlides(pres, data, STYLE);
  await savePresentation(pres, output, "corporate-blue", count);
}
main().catch(e => { console.error(e); process.exit(1); });
