#!/usr/bin/env node
/**
 * gen_previews.js — Generate preview .pptx files for all templates.
 *
 * Creates a sample presentation using each template so users can see
 * what each style looks like. Previews are saved to references/previews/.
 *
 * Usage:
 *   node gen_previews.js [--output-dir path]
 */

const path = require("path");
const { execFileSync } = require("child_process");
const fs = require("fs");

const SCRIPTS_DIR = path.join(__dirname);
const DEFAULT_OUTPUT = path.join(__dirname, "..", "references", "previews");

const TEMPLATES = [
  "corporate-blue", "corporate-red", "academic-serif",
  "minimal-white", "minimal-gray", "dark-gradient", "dark-neon",
  "creative-gradient", "creative-warm", "tech-modern",
];

const SAMPLE_DATA = {
  title: "Template Preview",
  slides: [
    { type: "title", title: "Template Preview", subtitle: "InsightEngine Presentation" },
    { type: "section", title: "Overview" },
    { type: "content", title: "Key Features", bullets: [
      "Professional slide layouts",
      "Consistent typography and colors",
      "Multiple slide types supported",
      "Charts, tables, and images",
    ]},
    { type: "two-column", title: "Comparison", left: ["Feature A", "Feature B"], right: ["Benefit 1", "Benefit 2"] },
    { type: "quote", text: "Design is intelligence made visible.", author: "Alina Wheeler" },
    { type: "table", title: "Sample Data", headers: ["Category", "Q1", "Q2"], rows: [["Revenue", "$1.2M", "$1.5M"], ["Growth", "12%", "18%"]] },
    { type: "closing", title: "Cảm ơn!", subtitle: "Questions?" },
  ],
};

function main() {
  const args = process.argv.slice(2);
  let outputDir = DEFAULT_OUTPUT;
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--output-dir" && args[i + 1]) outputDir = args[++i];
  }

  fs.mkdirSync(outputDir, { recursive: true });

  // Write sample data to temp file
  const tmpJson = path.join(outputDir, "_sample_data.json");
  fs.writeFileSync(tmpJson, JSON.stringify(SAMPLE_DATA, null, 2));

  console.log(`Generating previews for ${TEMPLATES.length} templates...`);
  console.log("─".repeat(50));

  let success = 0;
  for (const tmpl of TEMPLATES) {
    const outFile = path.join(outputDir, `preview-${tmpl}.pptx`);
    const script = path.join(SCRIPTS_DIR, `${tmpl}.js`);
    if (!fs.existsSync(script)) {
      console.log(`  ⚠️  ${tmpl}: script not found, skipping`);
      continue;
    }
    try {
      const result = execFileSync("node", [script, "--input", tmpJson, "--output", outFile], {
        encoding: "utf-8",
        stdio: ["pipe", "pipe", "pipe"],
      });
      console.log(`  ✅ ${tmpl}: ${result.trim()}`);
      success++;
    } catch (err) {
      console.log(`  ❌ ${tmpl}: ${err.stderr || err.message}`);
    }
  }

  // Clean up temp file
  fs.unlinkSync(tmpJson);

  console.log("─".repeat(50));
  console.log(`Done: ${success}/${TEMPLATES.length} previews generated in ${outputDir}`);
}

main();
