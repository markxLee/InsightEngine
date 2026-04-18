#!/usr/bin/env node
/** corporate-red.js — Bold red corporate template */
const { pptxgen, parseArgs, readInput, savePresentation, buildSlides } = require("./slide-utils");

const STYLE = {
  colors: { primary: "C0392B", accent: "E74C3C", bg: "FFFFFF", textDark: "2C3E50", textLight: "FFFFFF" },
  fonts: { heading: "Arial Black", body: "Calibri" },
  shapes: { accentBarWidth: 0.35 }
};

async function main() {
  const { input, output } = parseArgs();
  const data = readInput(input);
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  const count = buildSlides(pres, data, STYLE);
  await savePresentation(pres, output, "corporate-red", count);
}
main().catch(e => { console.error(e); process.exit(1); });
