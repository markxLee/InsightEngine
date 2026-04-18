/**
 * Shared utilities for PPTX template scripts.
 * Used by all template scripts in this directory.
 */
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

/**
 * Read JSON data from input file.
 * @param {string} inputPath - Path to JSON data file
 * @returns {object} Parsed JSON data
 */
function readInput(inputPath) {
  if (!fs.existsSync(inputPath)) {
    console.error(`Error: Input file not found: ${inputPath}`);
    process.exit(1);
  }
  return JSON.parse(fs.readFileSync(inputPath, "utf-8"));
}

/**
 * Parse CLI args: --input <file> --output <file>
 * @returns {{input: string, output: string}}
 */
function parseArgs() {
  const args = process.argv.slice(2);
  let input = "", output = "presentation.pptx";
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--input" && args[i + 1]) input = args[++i];
    else if (args[i] === "--output" && args[i + 1]) output = args[++i];
  }
  if (!input) {
    console.error("Usage: node <template>.js --input data.json --output output.pptx");
    process.exit(1);
  }
  return { input, output };
}

/**
 * Save presentation and print result.
 * @param {object} pres - pptxgenjs instance
 * @param {string} outputPath - Output file path
 * @param {string} templateName - Template name for logging
 * @param {number} slideCount - Number of slides
 */
async function savePresentation(pres, outputPath, templateName, slideCount) {
  const dir = path.dirname(outputPath);
  if (dir && !fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  await pres.writeFile({ fileName: outputPath });
  const stats = fs.statSync(outputPath);
  const sizeKB = (stats.size / 1024).toFixed(1);
  console.log(`✅ Saved: ${outputPath} (${sizeKB} KB, ${slideCount} slides, template: ${templateName})`);
}

/**
 * Add standard slide types from data.
 * @param {object} pres - pptxgenjs instance
 * @param {object} data - Slide data JSON
 * @param {object} style - Style config {colors, fonts, shapes}
 * @returns {number} Number of slides created
 */
function buildSlides(pres, data, style) {
  const slides = data.slides || [];
  let count = 0;

  for (const s of slides) {
    const slide = pres.addSlide();
    count++;

    switch (s.type) {
      case "title":
        addTitleSlide(slide, s, style, pres);
        break;
      case "section":
        addSectionSlide(slide, s, style, pres);
        break;
      case "content":
        addContentSlide(slide, s, style, pres);
        break;
      case "two-column":
        addTwoColumnSlide(slide, s, style, pres);
        break;
      case "image":
        addImageSlide(slide, s, style, pres);
        break;
      case "chart":
        addChartSlide(slide, s, style, pres);
        break;
      case "quote":
        addQuoteSlide(slide, s, style, pres);
        break;
      case "table":
        addTableSlide(slide, s, style, pres);
        break;
      case "closing":
        addClosingSlide(slide, s, style, pres);
        break;
      default:
        addContentSlide(slide, s, style, pres);
    }

    // Speaker notes — pass any "notes" field from JSON to PPTX
    if (s.notes) {
      slide.addNotes(s.notes);
    }
  }
  return count;
}

function addTitleSlide(slide, s, style, pres) {
  slide.background = { color: style.colors.bg };
  // Accent bar
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: style.shapes.accentBarWidth || 0.3, h: 7.5,
    fill: { color: style.colors.primary }
  });
  slide.addText(s.title || "", {
    x: 1.2, y: 2, w: 8, h: 1.5,
    fontSize: 36, bold: true, color: style.colors.textDark,
    fontFace: style.fonts.heading
  });
  if (s.subtitle) {
    slide.addText(s.subtitle, {
      x: 1.2, y: 3.8, w: 8, h: 0.8,
      fontSize: 18, color: style.colors.accent,
      fontFace: style.fonts.body
    });
  }
}

function addSectionSlide(slide, s, style, pres) {
  slide.background = { color: style.colors.primary };
  slide.addText(s.title || "", {
    x: 1, y: 2.5, w: 8, h: 2,
    fontSize: 32, bold: true, color: style.colors.textLight,
    fontFace: style.fonts.heading, align: "center", valign: "middle"
  });
  // Bottom accent line
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 4, y: 5, w: 2, h: 0.05,
    fill: { color: style.colors.accent }
  });
}

function addContentSlide(slide, s, style, pres) {
  slide.background = { color: style.colors.bg };
  // Accent bar
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 0.15, h: 7.5,
    fill: { color: style.colors.primary }
  });
  slide.addText(s.title || "", {
    x: 0.8, y: 0.3, w: 9, h: 0.8,
    fontSize: 24, bold: true, color: style.colors.primary,
    fontFace: style.fonts.heading
  });
  if (s.bullets && s.bullets.length > 0) {
    const textRows = s.bullets.map(b => ({
      text: b, options: { bullet: true, fontSize: 16, color: style.colors.textDark,
        fontFace: style.fonts.body, breakLine: true, paraSpaceAfter: 6 }
    }));
    slide.addText(textRows, { x: 1, y: 1.5, w: 8, h: 5 });
  } else if (s.text) {
    slide.addText(s.text, {
      x: 1, y: 1.5, w: 8, h: 5,
      fontSize: 16, color: style.colors.textDark, fontFace: style.fonts.body
    });
  }
}

function addTwoColumnSlide(slide, s, style, pres) {
  slide.background = { color: style.colors.bg };
  slide.addText(s.title || "", {
    x: 0.5, y: 0.3, w: 9, h: 0.8,
    fontSize: 24, bold: true, color: style.colors.primary,
    fontFace: style.fonts.heading
  });
  // Left column
  const leftItems = (s.left || []).map(b => ({
    text: b, options: { bullet: true, fontSize: 14, color: style.colors.textDark,
      fontFace: style.fonts.body, breakLine: true, paraSpaceAfter: 4 }
  }));
  slide.addText(leftItems, { x: 0.5, y: 1.5, w: 4.5, h: 5 });
  // Right column
  const rightItems = (s.right || []).map(b => ({
    text: b, options: { bullet: true, fontSize: 14, color: style.colors.textDark,
      fontFace: style.fonts.body, breakLine: true, paraSpaceAfter: 4 }
  }));
  slide.addText(rightItems, { x: 5.3, y: 1.5, w: 4.5, h: 5 });
  // Divider line
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 5, y: 1.5, w: 0.02, h: 5,
    fill: { color: style.colors.accent }
  });
}

function addImageSlide(slide, s, style, pres) {
  slide.background = { color: style.colors.bg };
  slide.addText(s.title || "", {
    x: 0.5, y: 0.3, w: 9, h: 0.8,
    fontSize: 24, bold: true, color: style.colors.primary,
    fontFace: style.fonts.heading
  });
  if (s.image_path && fs.existsSync(s.image_path)) {
    slide.addImage({ path: s.image_path, x: 1.5, y: 1.5, w: 7, h: 5 });
  } else {
    // Placeholder
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 2, y: 1.5, w: 6, h: 4.5,
      fill: { color: "E0E0E0" }
    });
    slide.addText(s.caption || "[Image placeholder]", {
      x: 2, y: 3.2, w: 6, h: 1,
      fontSize: 14, color: "999999", align: "center",
      fontFace: style.fonts.body
    });
  }
  if (s.caption) {
    slide.addText(s.caption, {
      x: 1, y: 6.5, w: 8, h: 0.5,
      fontSize: 12, color: style.colors.accent, align: "center",
      fontFace: style.fonts.body, italic: true
    });
  }
}

function addChartSlide(slide, s, style, pres) {
  slide.background = { color: style.colors.bg };
  slide.addText(s.title || "", {
    x: 0.5, y: 0.3, w: 9, h: 0.8,
    fontSize: 24, bold: true, color: style.colors.primary,
    fontFace: style.fonts.heading
  });
  // If chart image path provided
  if (s.chart_image && fs.existsSync(s.chart_image)) {
    slide.addImage({ path: s.chart_image, x: 1, y: 1.5, w: 8, h: 5 });
  } else {
    // Placeholder for chart
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 1.5, y: 1.5, w: 7, h: 5,
      fill: { color: "F0F0F0" }, line: { color: style.colors.accent, width: 1 }
    });
    slide.addText("[Chart placeholder]", {
      x: 1.5, y: 3.5, w: 7, h: 1,
      fontSize: 14, color: "999999", align: "center",
      fontFace: style.fonts.body
    });
  }
}

function addQuoteSlide(slide, s, style, pres) {
  slide.background = { color: style.colors.bg };
  // Large quote mark
  slide.addText("\u201C", {
    x: 1, y: 1, w: 2, h: 2,
    fontSize: 72, color: style.colors.accent,
    fontFace: style.fonts.heading, bold: true
  });
  slide.addText(s.text || "", {
    x: 2, y: 2.5, w: 7, h: 2.5,
    fontSize: 22, color: style.colors.textDark, italic: true,
    fontFace: style.fonts.body
  });
  if (s.author) {
    slide.addText(`\u2014 ${s.author}`, {
      x: 2, y: 5.2, w: 7, h: 0.6,
      fontSize: 16, color: style.colors.accent,
      fontFace: style.fonts.body
    });
  }
}

function addTableSlide(slide, s, style, pres) {
  slide.background = { color: style.colors.bg };
  slide.addText(s.title || "", {
    x: 0.5, y: 0.3, w: 9, h: 0.8,
    fontSize: 24, bold: true, color: style.colors.primary,
    fontFace: style.fonts.heading
  });
  const headers = (s.headers || []).map(h => ({
    text: h, options: { bold: true, color: "FFFFFF", fill: { color: style.colors.primary },
      fontSize: 14, fontFace: style.fonts.body }
  }));
  const rows = (s.rows || []).map((row, idx) =>
    row.map(cell => ({
      text: String(cell), options: {
        fontSize: 13, color: style.colors.textDark,
        fontFace: style.fonts.body,
        fill: { color: idx % 2 === 0 ? "F5F5F5" : "FFFFFF" }
      }
    }))
  );
  const tableData = [headers, ...rows];
  slide.addTable(tableData, {
    x: 0.5, y: 1.5, w: 9, h: 5,
    border: { type: "solid", pt: 0.5, color: "DDDDDD" },
    colW: Array(headers.length).fill(9 / headers.length)
  });
}

function addClosingSlide(slide, s, style, pres) {
  slide.background = { color: style.colors.primary };
  slide.addText(s.title || "Cảm ơn!", {
    x: 1, y: 2, w: 8, h: 2,
    fontSize: 40, bold: true, color: style.colors.textLight,
    fontFace: style.fonts.heading, align: "center", valign: "middle"
  });
  if (s.subtitle) {
    slide.addText(s.subtitle, {
      x: 1, y: 4.2, w: 8, h: 1,
      fontSize: 20, color: style.colors.accent || style.colors.textLight,
      fontFace: style.fonts.body, align: "center"
    });
  }
}

module.exports = {
  pptxgen, fs, path,
  readInput, parseArgs, savePresentation, buildSlides,
  addTitleSlide, addSectionSlide, addContentSlide, addTwoColumnSlide,
  addImageSlide, addChartSlide, addQuoteSlide, addTableSlide, addClosingSlide
};
