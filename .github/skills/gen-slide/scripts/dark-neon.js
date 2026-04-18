#!/usr/bin/env node
/** dark-neon.js — Dark slate with neon cyan/magenta accents */
const { pptxgen, parseArgs, readInput, savePresentation, buildSlides } = require("./slide-utils");

const STYLE = {
  colors: { primary: "00E5FF", accent: "FF4081", bg: "121212", textDark: "121212", textLight: "E0E0E0" },
  fonts: { heading: "Inter", body: "Inter" },
  shapes: { accentBarWidth: 0.2 }
};

async function main() {
  const { input, output } = parseArgs();
  const data = readInput(input);
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  const count = buildSlides(pres, data, STYLE);
  await savePresentation(pres, output, "dark-neon", count);
}
main().catch(e => { console.error(e); process.exit(1); });
