#!/usr/bin/env node
/** academic-serif.js — Clean scholarly template with serif fonts */
const { pptxgen, parseArgs, readInput, savePresentation, buildSlides } = require("./slide-utils");

const STYLE = {
  colors: { primary: "2C3E50", accent: "2980B9", bg: "FFFFFF", textDark: "2C3E50", textLight: "FFFFFF" },
  fonts: { heading: "Georgia", body: "Calibri" },
  shapes: { accentBarWidth: 0.15 }
};

async function main() {
  const { input, output } = parseArgs();
  const data = readInput(input);
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  const count = buildSlides(pres, data, STYLE);
  await savePresentation(pres, output, "academic-serif", count);
}
main().catch(e => { console.error(e); process.exit(1); });
