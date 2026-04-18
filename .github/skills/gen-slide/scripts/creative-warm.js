#!/usr/bin/env node
/** creative-warm.js — Warm earthy tones, friendly and inviting */
const { pptxgen, parseArgs, readInput, savePresentation, buildSlides } = require("./slide-utils");

const STYLE = {
  colors: { primary: "D97706", accent: "059669", bg: "FFFDF7", textDark: "3D2C1E", textLight: "FFFFFF" },
  fonts: { heading: "Poppins", body: "Open Sans" },
  shapes: { accentBarWidth: 0.25 }
};

async function main() {
  const { input, output } = parseArgs();
  const data = readInput(input);
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  const count = buildSlides(pres, data, STYLE);
  await savePresentation(pres, output, "creative-warm", count);
}
main().catch(e => { console.error(e); process.exit(1); });
