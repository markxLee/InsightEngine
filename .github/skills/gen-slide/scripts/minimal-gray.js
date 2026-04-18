#!/usr/bin/env node
/** minimal-gray.js — Soft gray tones with generous spacing */
const { pptxgen, parseArgs, readInput, savePresentation, buildSlides } = require("./slide-utils");

const STYLE = {
  colors: { primary: "4A4A4A", accent: "B0B0B0", bg: "F5F5F5", textDark: "333333", textLight: "FFFFFF" },
  fonts: { heading: "Helvetica Neue", body: "Helvetica Neue" },
  shapes: { accentBarWidth: 0.1 }
};

async function main() {
  const { input, output } = parseArgs();
  const data = readInput(input);
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  const count = buildSlides(pres, data, STYLE);
  await savePresentation(pres, output, "minimal-gray", count);
}
main().catch(e => { console.error(e); process.exit(1); });
