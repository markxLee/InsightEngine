# reveal.js API Reference

Quick reference for reveal.js features used in InsightEngine HTML presentations.

## CDN Setup (v5.1.0)

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/theme/white.css">
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js"></script>
```

## Built-in Themes

| Theme | Style |
|-------|-------|
| `white` | Clean white background |
| `black` | Dark background with white text |
| `night` | Dark blue background |
| `moon` | Solarized dark |
| `simple` | Minimal, serif fonts |
| `league` | Gray gradient background |
| `beige` | Warm beige background |
| `sky` | Blue sky gradient |
| `serif` | Traditional serif fonts |
| `blood` | Dark with red accents |
| `solarized` | Solarized color scheme |

## Initialization Options

```javascript
Reveal.initialize({
  // Navigation
  hash: true,              // URL fragment for each slide
  slideNumber: true,       // Show slide numbers
  controls: true,          // Show navigation arrows
  progress: true,          // Show progress bar
  
  // Transitions
  transition: 'slide',     // none/fade/slide/convex/concave/zoom
  transitionSpeed: 'default', // default/fast/slow
  
  // Background
  backgroundColor: '#fff',
  parallaxBackgroundImage: 'url',
  parallaxBackgroundSize: '2560px 1440px',
  
  // Plugins
  plugins: [RevealNotes, RevealHighlight, RevealMath]
});
```

## Slide Backgrounds

```html
<!-- Solid color -->
<section data-background-color="#4d7e65">

<!-- Gradient -->
<section data-background-gradient="linear-gradient(to bottom, #283b95, #17b2c3)">

<!-- Image -->
<section data-background-image="bg.jpg" data-background-size="cover" data-background-opacity="0.5">

<!-- Video -->
<section data-background-video="bg.mp4" data-background-video-muted>

<!-- iframe -->
<section data-background-iframe="https://example.com">
```

## Speaker Notes

```html
<section>
  <h2>Slide Title</h2>
  <aside class="notes">
    Speaker notes go here. Only visible in speaker view (press 'S').
  </aside>
</section>
```

## Code Highlighting

```html
<pre><code data-trim data-noescape class="language-python">
def hello():
    print("Hello World")
</code></pre>
```

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Arrow keys | Navigate slides |
| Space | Next slide |
| Escape | Overview mode |
| F | Fullscreen |
| S | Speaker notes view |
| B | Blackout screen |
| O | Slide overview |
| ? | Show keyboard shortcuts |

## Fragments (Animations)

```html
<p class="fragment">Appears on click</p>
<p class="fragment fade-up">Fades up</p>
<p class="fragment highlight-red">Highlights red</p>
<p class="fragment fade-in-then-out">Appears then disappears</p>
```

## PDF Export

Append `?print-pdf` to URL, then use browser Print → Save as PDF.

```
http://localhost:8000/presentation.html?print-pdf
```
