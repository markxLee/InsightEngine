#!/usr/bin/env node
/**
 * gen_slide.js — Main entry point for PPTX generation.
 *
 * Routes to the appropriate template script based on --template flag.
 * Accepts JSON data and outputs a .pptx file.
 *
 * Usage:
 *   node gen_slide.js --input data.json --output output.pptx --template corporate-blue
 *   node gen_slide.js --input data.json --output output.pptx --template dark-neon
 *   node gen_slide.js --list   # List all available templates
 */

const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");

const SCRIPTS_DIR = __dirname;

// Map of template name → script filename
const TEMPLATES = {
  "corporate-blue": "corporate-blue.js",
  "corporate-red": "corporate-red.js",
  "academic-serif": "academic-serif.js",
  "minimal-white": "minimal-white.js",
  "minimal-gray": "minimal-gray.js",
  "dark-gradient": "dark-gradient.js",
  "dark-neon": "dark-neon.js",
  "creative-gradient": "creative-gradient.js",
  "creative-warm": "creative-warm.js",
  "tech-modern": "tech-modern.js",
};

// Style aliases → default template
const STYLE_ALIASES = {
  corporate: "corporate-blue",
  academic: "academic-serif",
  minimal: "minimal-white",
  dark: "dark-gradient",
  "dark-modern": "dark-gradient",
  creative: "creative-gradient",
  tech: "tech-modern",
};

function parseArgs() {
  const args = process.argv.slice(2);
  const parsed = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--input" && args[i + 1]) parsed.input = args[++i];
    else if (args[i] === "--output" && args[i + 1]) parsed.output = args[++i];
    else if (args[i] === "--template" && args[i + 1]) parsed.template = args[++i];
    else if (args[i] === "--list") parsed.list = true;
    else if (args[i] === "--help" || args[i] === "-h") parsed.help = true;
  }
  return parsed;
}

function printUsage() {
  console.log(`Usage: node gen_slide.js --input <json> --output <pptx> --template <name>

Options:
  --input <path>      Path to JSON data file (required)
  --output <path>     Output .pptx file path (required)
  --template <name>   Template name or style alias (required)
  --list              List all available templates
  --help              Show this help

Templates: ${Object.keys(TEMPLATES).join(", ")}
Aliases:   ${Object.entries(STYLE_ALIASES).map(([k, v]) => `${k} → ${v}`).join(", ")}`);
}

function listTemplates() {
  console.log("Available PPTX templates:");
  console.log("─".repeat(50));
  for (const [name, file] of Object.entries(TEMPLATES)) {
    console.log(`  ${name.padEnd(22)} → ${file}`);
  }
  console.log("\nStyle aliases:");
  for (const [alias, target] of Object.entries(STYLE_ALIASES)) {
    console.log(`  ${alias.padEnd(22)} → ${target}`);
  }
}

function main() {
  const args = parseArgs();

  if (args.help) {
    printUsage();
    process.exit(0);
  }

  if (args.list) {
    listTemplates();
    process.exit(0);
  }

  if (!args.input || !args.output || !args.template) {
    console.error("Error: --input, --output, and --template are required.");
    printUsage();
    process.exit(1);
  }

  // Resolve template name (alias or direct)
  let templateName = args.template.toLowerCase();
  if (STYLE_ALIASES[templateName]) {
    templateName = STYLE_ALIASES[templateName];
  }

  const scriptFile = TEMPLATES[templateName];
  if (!scriptFile) {
    console.error(`Error: Unknown template "${args.template}".`);
    console.error(`Available: ${Object.keys(TEMPLATES).join(", ")}`);
    console.error(`Aliases: ${Object.keys(STYLE_ALIASES).join(", ")}`);
    process.exit(1);
  }

  // Verify input file exists
  if (!fs.existsSync(args.input)) {
    console.error(`Error: Input file not found: ${args.input}`);
    process.exit(1);
  }

  const scriptPath = path.join(SCRIPTS_DIR, scriptFile);
  if (!fs.existsSync(scriptPath)) {
    console.error(`Error: Template script not found: ${scriptPath}`);
    process.exit(1);
  }

  // Execute the template script with the same arguments
  try {
    const result = execFileSync("node", [scriptPath, "--input", args.input, "--output", args.output], {
      encoding: "utf-8",
      stdio: ["pipe", "pipe", "pipe"],
    });
    process.stdout.write(result);
  } catch (err) {
    console.error(`Error running template "${templateName}":`, err.stderr || err.message);
    process.exit(1);
  }
}

main();
