#!/usr/bin/env node
/** creative-gradient.js — Vibrant purple-to-amber gradient, event/marketing style */
const { pptxgen, parseArgs, readInput, savePresentation, buildSlides } = require("./slide-utils");

const STYLE = {
  colors: { primary: "8B5CF6", accent: "F59E0B", bg: "FFFBEB", textDark: "1E1B4B", textLight: "FFFFFF" },
  fonts: { heading: "Poppins", body: "Open Sans" },
  shapes: { accentBarWidth: 0.3 }
};

async function main() {
  const { input, output } = parseArgs();
  const data = readInput(input);
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  const count = buildSlides(pres, data, STYLE);
  await savePresentation(pres, output, "creative-gradient", count);
}
main().catch(e => { console.error(e); process.exit(1); });
