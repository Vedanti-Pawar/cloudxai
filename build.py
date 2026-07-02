#!/usr/bin/env python3
"""CloudxAi static site generator.
Edit the partials + page bodies in pages/, then run:  python3 build.py
Outputs the assembled *.html files at the project root.
Do NOT hand-edit the generated root *.html files — edit here / in pages/."""

import os, pathlib

ROOT = pathlib.Path(__file__).parent
PAGES = ROOT / "pages"

# (slug, nav-label, page-title, meta-description). slug "index" => Home, not in nav bar.
NAV = [
    ("overview",      "Overview",     "CloudDIET Overview — Deeper Azure Optimizations | CloudxAi",
     "CloudDIET goes beyond spend dashboards: profiling billing, usage, and configuration to find the engineering, commercial, and architectural root causes of Azure waste."),
    ("how-it-works",  "How It Works", "How CloudDIET Works — Read-only Azure Profiling | CloudxAi",
     "Daily read-only profiling feeds Azure-specific analysis, prioritized actions, and measurable cost outcomes — with service-aware engineering intelligence."),
    ("platform",      "Dashboard",    "CloudDIET Dashboard Overview — Cost & Savings Tools | CloudxAi",
     "The command center for Azure spend visibility, savings discovery, and optimization tracking: dashboard, Cost Explorer, Savings Plan Designer, Resource Explorer, and SQL Visibility."),
    ("partners",      "Partners",     "Partner Value Proposition — Sell, Deliver, Grow | CloudxAi",
     "CloudDIET gives Systems Integrator partners a low-friction way to assess Azure, scope follow-on work, and turn one-time projects into managed FinOps services."),
    ("case-studies",  "Case Studies", "Customer Case Studies — Real Azure Savings | CloudxAi",
     "How CloudDIET uncovered $3.8M of hidden savings, Databricks startup waste, and data-residency inefficiency that native Azure tools missed."),
    ("security",      "Security",     "Security & Data Protection — Read-only by Design | CloudxAi",
     "How CloudDIET accesses, protects, and lets customers control Azure metadata: read-only RBAC, control-plane only, AES-256, and fully customer-revocable."),
    ("faq",           "FAQ",          "Frequently Asked Questions | CloudxAi · CloudDIET",
     "Key onboarding, authentication, and data-access answers for CloudDIET — Azure-only, no agents, Azure Entra ID SSO, read-only control-plane access."),
]
EXTRA = [
    ("index",        None, "CloudxAi — Azure Cloud Cost Optimization · Distributor for CloudDIET",
     "CloudxAi is the distributor for CloudDIET — Azure cloud cost optimization that goes from spend visibility to prioritized engineering action."),
    ("get-started",  None, "Get Started Free — CloudDIET Preview | CloudxAi",
     "Get started in minutes for free with CloudDIET. Profiling and analysis of up to 3 nominated Azure subscriptions, with a top-level dashboard within a week."),
]

LOGO_IMG = '<img class="brand-logo" src="assets/cloudxai-logo.png" alt="CloudxAi" width="160" height="42">'


def head(title, desc):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/styles.css">
<script>(function(){{try{{var t=localStorage.getItem('theme')||(window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}}})();</script>
</head>
<body>
"""


def header(active):
    def link(slug, label):
        cls = ' class="active"' if slug == active else ''
        return f'<a href="{slug}.html"{cls}>{label}</a>'
    links = "\n      ".join(link(slug, label) for slug, label, *_ in NAV)
    mlinks = "\n    ".join(f'<a href="{slug}.html">{label}</a>' for slug, label, *_ in NAV)
    return f"""<header class="nav">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="CloudxAi home">
      {LOGO_IMG}
    </a>
    <nav class="nav-links">
      {links}
    </nav>
    <div class="nav-cta">
      <a class="btn btn-primary" href="get-started.html">Get started free</a>
    </div>
    <button class="menu-btn" aria-label="Open menu"><span></span><span></span><span></span></button>
  </div>
</header>

<div class="mobile-menu">
  <div class="mm-top">
    <span class="brand brand-on-dark">{LOGO_IMG}</span>
    <button class="mm-close" aria-label="Close menu">&times;</button>
  </div>
  <nav>
    {mlinks}
  </nav>
  <a class="btn btn-grad" href="get-started.html">Get started free</a>
  <div class="mm-theme" role="group" aria-label="Color theme">
    <button class="mm-tbtn" data-set-theme="light"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg> Light</button>
    <button class="mm-tbtn" data-set-theme="dark"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8Z"/></svg> Dark</button>
  </div>
</div>

<div class="theme-toggle" role="group" aria-label="Color theme">
  <button data-set-theme="light" aria-label="Light mode" title="Light mode">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
  </button>
  <button data-set-theme="dark" aria-label="Dark mode" title="Dark mode">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8Z"/></svg>
  </button>
</div>
"""


FOOTER = """<footer class="footer">
  <div class="wrap">
    <div class="top">
      <div class="about">
        <span class="brand brand-on-dark"><img class="brand-logo" src="assets/cloudxai-logo.png" alt="CloudxAi" width="170" height="44"></span>
        <p>From spend visibility to prioritized engineering action.</p>
        <span class="cobrand on-dark" style="margin-top:18px">
          <span class="dist">Distributor for</span>
          <span class="cd-lockup">
            <img class="cd-icon" src="assets/clouddiet-icon.svg" alt="CloudDIET" width="46" height="30" style="height:30px">
            <span class="cd-words">
              <span class="cd-name" style="font-size:19px"><b>Cloud</b><span class="lite">DIET</span></span>
              <span class="cd-sub"><b>AZURE CLOUD</b> <span class="c">COST</span> OPTIMIZATION</span>
            </span>
          </span>
        </span>
      </div>
      <div class="cols">
        <div class="col">
          <h4>Product</h4>
          <a href="overview.html">Overview</a>
          <a href="how-it-works.html">How it works</a>
          <a href="platform.html">Platform</a>
          <a href="security.html">Security</a>
        </div>
        <div class="col">
          <h4>Company</h4>
          <a href="partners.html">Partners</a>
          <a href="case-studies.html">Case studies</a>
          <a href="faq.html">FAQ</a>
          <a href="get-started.html">Get started</a>
        </div>
        <div class="col">
          <h4>Contact</h4>
          <a href="mailto:amit@cloudxai.sg">amit@cloudxai.sg</a>
          <a href="https://www.cloudxai.sg" target="_blank" rel="noopener">www.cloudxai.sg</a>
          <p>Singapore</p>
        </div>
      </div>
    </div>
    <div class="bottom">
      <span>© 2026 CloudxAi. CloudDIET is a product of its respective owner.</span>
      <span>Azure Cloud Cost Optimization</span>
    </div>
  </div>
</footer>

<script src="js/main.js"></script>
</body>
</html>
"""


def build():
    count = 0
    for slug, label, title, desc in NAV + EXTRA:
        body_path = PAGES / f"{slug}.html"
        if not body_path.exists():
            print(f"  ! missing body: pages/{slug}.html (skipped)")
            continue
        body = body_path.read_text()
        active = slug if any(slug == s for s, *_ in NAV) else None
        out = head(title, desc) + header(active) + "\n" + body + "\n" + FOOTER
        (ROOT / f"{slug}.html").write_text(out)
        count += 1
        print(f"  ✓ {slug}.html")
    print(f"Built {count} pages.")


if __name__ == "__main__":
    build()
