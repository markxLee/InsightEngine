# pptxgenjs API Reference

Quick reference for commonly used pptxgenjs features in InsightEngine templates.

## Core API

```javascript
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();

// Presentation settings
pres.defineSection({ title: "Section Name" });
pres.layout = "LAYOUT_16x9";  // or LAYOUT_4x3, LAYOUT_WIDE

// Add a slide
const slide = pres.addSlide();
const slide = pres.addSlide({ sectionTitle: "Section Name" });
```

## Slide Methods

### addText(text, options)
```javascript
slide.addText("Hello", {
  x: 0.5, y: 0.5, w: "90%", h: 1.0,
  fontSize: 24,
  fontFace: "Arial",
  color: "363636",        // NO # prefix!
  bold: true,
  italic: false,
  underline: false,
  align: "center",        // left, center, right
  valign: "middle",       // top, middle, bottom
  lineSpacingMultiple: 1.5,
});

// Multi-line with formatting
slide.addText([
  { text: "Bold ", options: { bold: true, fontSize: 18 } },
  { text: "and normal", options: { fontSize: 18 } },
], { x: 0.5, y: 2 });
```

### addTable(rows, options)
```javascript
const rows = [
  [{ text: "Header1", options: { bold: true, fill: { color: "1A365D" }, color: "FFFFFF" } }, ...],
  ["Cell1", "Cell2", "Cell3"],
];
slide.addTable(rows, {
  x: 0.5, y: 1.5, w: 9.0,
  border: { pt: 1, color: "CCCCCC" },
  colW: [3, 3, 3],
  fontSize: 14,
  autoPage: true,
});
```

### addImage(options)
```javascript
slide.addImage({
  path: "image.png",     // local path
  // or: data: "base64...",
  x: 1.0, y: 1.5, w: 4.0, h: 3.0,
  sizing: { type: "contain", w: 4, h: 3 },
});
```

### addChart(type, data, options)
```javascript
slide.addChart(pres.ChartType.bar, [
  { name: "Series 1", labels: ["A", "B"], values: [10, 20] },
], {
  x: 0.5, y: 1.5, w: 6, h: 4,
  showTitle: true,
  title: "Chart Title",
  showLegend: true,
});
```

### addShape(shape, options)
```javascript
slide.addShape(pres.ShapeType.rect, {
  x: 0, y: 0, w: "100%", h: 0.5,
  fill: { color: "1A365D" },
});
```

## Background
```javascript
// Solid color
slide.background = { fill: "0F172A" };  // NO # prefix!

// Gradient
slide.background = {
  fill: { type: "solid", color: "0F172A" },
};
```

## Color Rules

**CRITICAL: Never use # prefix with pptxgenjs!**
- ✅ `"FF5733"`
- ❌ `"#FF5733"`

## Save
```javascript
await pres.writeFile({ fileName: "output.pptx" });
// or
const buffer = await pres.write({ outputType: "nodebuffer" });
```

## Design Guidelines

### Font Pairing Best Practices
- Heading: Bold sans-serif (Arial Black, Inter Bold, Poppins Bold)
- Body: Regular weight (Arial, Calibri, Inter, Open Sans)
- Avoid more than 2 font families per presentation

### Color Ratio
- 60% background/neutral
- 30% primary brand color
- 10% accent for emphasis

### Spacing
- Minimum 0.5" margins on all sides
- Line spacing: 1.3-1.6x for readability
- 16-18pt body text for projection
