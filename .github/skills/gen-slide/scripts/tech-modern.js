#!/usr/bin/env node
/** tech-modern.js — Modern tech company look with teal/blue tones */
const { pptxgen, parseArgs, readInput, savePresentation, buildSlides } = require("./slide-utils");

const STYLE = {
  colors: { primary: "0D9488", accent: "2563EB", bg: "F8FAFC", textDark: "1E293B", textLight: "FFFFFF" },
  fonts: { heading: "Inter", body: "Inter" },
  shapes: { accentBarWidth: 0.2 }
};

async function main() {
  const { input, output } = parseArgs();
  const data = readInput(input);
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  const count = buildSlides(pres, data, STYLE);
  await savePresentation(pres, output, "tech-modern", count);
}
main().catch(e => { console.error(e); process.exit(1); });
