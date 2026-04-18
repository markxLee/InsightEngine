#!/usr/bin/env node
/** minimal-white.js — Ultra-clean whitespace-focused template */
const { pptxgen, parseArgs, readInput, savePresentation, buildSlides } = require("./slide-utils");

const STYLE = {
  colors: { primary: "1A1A1A", accent: "999999", bg: "FAFAFA", textDark: "1A1A1A", textLight: "FFFFFF" },
  fonts: { heading: "Helvetica Neue", body: "Helvetica Neue" },
  shapes: { accentBarWidth: 0.08 }
};

async function main() {
  const { input, output } = parseArgs();
  const data = readInput(input);
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  const count = buildSlides(pres, data, STYLE);
  await savePresentation(pres, output, "minimal-white", count);
}
main().catch(e => { console.error(e); process.exit(1); });
