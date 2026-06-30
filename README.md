# CloudxAi · CloudDIET

Marketing site for **CloudxAi** — distributor for **CloudDIET** (Azure Cloud Cost Optimization).
From spend visibility to prioritized engineering action.

## Stack
Static **HTML / CSS / JS**. Pages are assembled by a small Python generator from shared
partials, so the nav, footer and logo stay consistent across every page.

- `pages/*.html` — page bodies (edit these)
- `build.py` — generator: header/footer/theme markup + page assembly
- `css/styles.css`, `js/main.js`, `assets/` — styles, interactions, logos
- Root `*.html` — **generated** output (do not hand-edit)

## Build & preview
```bash
python3 build.py          # regenerate the root *.html files
python3 -m http.server    # preview at http://localhost:8000
```

## Features
- Light / dark theme (purple-toned dark mode), persisted + system-aware
- Responsive desktop → tablet → phone, accessible contrast
- Sections mirror the CloudDIET partner deck (Overview, How It Works, Platform,
  Partners, Case Studies, Security, FAQ, Get Started)

## Contact
Amit Pawar · amit@cloudxai.sg · www.cloudxai.sg · Singapore
