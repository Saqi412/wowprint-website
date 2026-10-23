# -*- coding: utf-8 -*-
"""Erzeugt die statischen HTML-Seiten der WOW PRINT Website nach ./site.

    python3 tools/build.py            # für Netlify (saubere URLs)
    python3 tools/build.py --preview  # Links auf index.html, für lokale Vorschau
"""
import os
import sys
from html import escape

sys.path.insert(0, os.path.dirname(__file__))
from content import COMPANY, HOURS, SERVICES, PROJECTS, PROCESS  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site")
PREVIEW = "--preview" in sys.argv
OUT = ROOT if "--out" not in sys.argv else sys.argv[sys.argv.index("--out") + 1]

C = COMPANY
ADDRESS = f'{C["street"]}, {C["zip"]} {C["city"]}'

# ---------------------------------------------------------------- helpers

class Page:
    def __init__(self, path, absolute=False):
        self.path = path            # z. B. "leistungen/print/"
        self.absolute = absolute    # 404.html braucht absolute Pfade

    @property
    def depth(self):
        return self.path.count("/")

    def url(self, target):
        """Link von dieser Seite zu `target` (z. B. "kontakt/")."""
        if self.absolute and not PREVIEW:
            return "/" + target
        rel = "../" * self.depth + target
        if PREVIEW and (target == "" or target.endswith("/")):
            rel += "index.html"
        return rel or "./"

    def asset(self, p):
        if self.absolute and not PREVIEW:
            return "/assets/" + p
        return "../" * self.depth + "assets/" + p

    def form_action(self, target):
        return "/" + target if not PREVIEW else self.url(target)


ARROW = '<svg class="arrow" viewBox="0 0 18 12" aria-hidden="true"><path d="M0 6h16M11 1l5 5-5 5" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>'
ARROW_DIAG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 19 19 5M8 5h11v11" fill="none" stroke="currentColor" stroke-width="2"/></svg>'
ARROW_DOWN = '<svg width="12" height="16" viewBox="0 0 12 16" aria-hidden="true"><path d="M6 0v14M1 9l5 5 5-5" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>'
STAR = '<svg class="star" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 0c.6 6.4 5.6 11.4 12 12-6.4.6-11.4 5.6-12 12-.6-6.4-5.6-11.4-12-12C6.4 11.4 11.4 6.4 12 0Z" fill="currentColor"/></svg>'
IG = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="17.4" cy="6.6" r="1.2" fill="currentColor"/></svg>'
FB = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.5 21v-7.6h2.6l.4-3h-3V8.5c0-.9.3-1.5 1.5-1.5H16.6V4.3c-.3 0-1.2-.1-2.3-.1-2.3 0-3.8 1.4-3.8 3.9v2.3H7.9v3h2.6V21h3Z" fill="currentColor"/></svg>'
MAIL = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="m3.5 6 8.5 7 8.5-7" fill="none" stroke="currentColor" stroke-width="1.8"/></svg>'
PHONE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 3.5h3l1.4 4.2-2 1.3a12 12 0 0 0 6 6l1.3-2 4.2 1.4v3c0 1-.8 1.8-1.8 1.8A16.5 16.5 0 0 1 4.8 5.3c0-1 .8-1.8 1.8-1.8Z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>'
UPLOAD = '<svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 16V4M7 9l5-5 5 5M4 16v4h16v-4" fill="none" stroke="currentColor" stroke-width="2"/></svg>'

FEATURE_ICONS = [
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2 14.6 9.4 22 12l-7.4 2.6L12 22l-2.6-7.4L2 12l7.4-2.6Z" fill="currentColor"/></svg>',
    '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="3.5" fill="currentColor"/></svg>',
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12.5 9.5 18 20 6" fill="none" stroke="currentColor" stroke-width="2.4"/></svg>',
]


def wordmark(cls=""):
    return (f'<span class="wordmark {cls}" aria-label="WOW PRINT"><span class="wm-wow" aria-hidden="true">WOW</span>'
            f'<span class="wm-print" aria-hidden="true">PRINT</span><span class="wm-r" aria-hidden="true">®</span></span>')


def lines(*ls):
    return "".join(f'<span class="line"><span>{l}</span></span>' for l in ls)


def socials():
    return (f'<div class="socials">'
            f'<a href="{C["instagram"]}" aria-label="Instagram" data-magnetic=".4">{IG}</a>'
            f'<a href="{C["facebook"]}" aria-label="Facebook" data-magnetic=".4">{FB}</a>'
            f'<a href="mailto:{C["email"]}" aria-label="E-Mail" data-magnetic=".4">{MAIL}</a>'
            f'<a href="tel:{C["phone_href"]}" aria-label="Telefon" data-magnetic=".4">{PHONE}</a>'
            f'</div>')


def hours_html():
    return '<div class="hours">' + "".join(f"<span>{d}</span><span>{h}</span>" for d, h in HOURS) + "</div>"


def marquee(items, pink=False, reverse=False):
    cls = "marquee marquee--pink" if pink else "marquee"
    inner = "".join(
        f'<span class="marquee-item{" is-outline" if i % 2 else ""}">{escape(t)} {STAR}</span>'
        for i, t in enumerate(items)
    )
    return (f'<div class="{cls}"{" data-reverse" if reverse else ""} aria-hidden="true"><div class="marquee-track">'
            f'<div class="marquee-group">{inner}{inner}</div></div></div>')


NAV = [("projekte/", "Work"), ("leistungen/", "Services"), ("ueber-uns/", "About"), ("kontakt/", "Contact")]


def header(p, current=""):
    nav = "".join(
        f'<a class="link-u" href="{p.url(t)}"{" aria-current=page" if current == t else ""}>{label}</a>'
        for t, label in NAV
    )
    menu_links = "".join(
        f'<li><a href="{p.url(t)}"><small>0{i}</small>{label}</a></li>'
        for i, (t, label) in enumerate([("", "Home")] + NAV + [("offerte/", "Get a quote")], 1)
    )
    menu_services = "".join(f'<a href="{p.url("leistungen/" + s["slug"] + "/")}">{s["title"]}</a>' for s in SERVICES)
    return f"""
<a class="skip-link" href="#main">Zum Inhalt springen</a>
<div class="preloader" aria-hidden="true">
  <div class="preloader-word"><span>W</span><span>O</span><span>W</span></div>
  <div class="preloader-claim">We make you visible.</div>
  <div class="preloader-count">0</div>
</div>
<div class="page-transition" aria-hidden="true"><span></span><span></span></div>
<div class="cursor" aria-hidden="true"><div class="cursor-ring"><span></span></div><div class="cursor-dot"></div></div>

<header class="site-header">
  <div class="wrap">
    <a class="logo" href="{p.url("")}" aria-label="WOW PRINT Startseite">{wordmark()}</a>
    <nav class="nav" aria-label="Hauptnavigation">{nav}</nav>
    <div class="header-actions">
      <a class="btn btn--solid header-cta" href="{p.url("offerte/")}" data-magnetic=".25">Offerte {ARROW}</a>
      <button class="burger" type="button" aria-label="Menü öffnen" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>

<div class="menu" id="menu" aria-hidden="true">
  <div class="wrap">
    <nav aria-label="Menü"><ul class="menu-links">{menu_links}</ul></nav>
    <div class="menu-side">
      <div><h4>SERVICES</h4><div class="menu-services">{menu_services}</div></div>
      <div><h4>STUDIO</h4><p>{C["name"]}<br>{C["street"]}<br>{C["zip"]} {C["city"]}</p></div>
      <div><h4>KONTAKT</h4><p><a class="link-u" href="tel:{C["phone_href"]}">{C["phone"]}</a><br><a class="link-u" href="mailto:{C["email"]}">{C["email"]}</a></p></div>
      {socials()}
    </div>
  </div>
</div>
"""


def footer(p):
    svc = "".join(f'<li><a class="link-u" href="{p.url("leistungen/" + s["slug"] + "/")}">{s["title"]}</a></li>' for s in SERVICES)
    giant = "".join(f"<span>{ch}</span>" for ch in "WOWPRINT")
    return f"""
<footer class="site-footer on-dark">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        {wordmark()}
        <p>Fahrzeugbeschriftung, Werbetechnik, Textil, Print und Design aus Rorschach. We make you visible.</p>
        <div style="margin-top:26px">{socials()}</div>
      </div>
      <div><h4>STUDIO</h4><p>{C["name"]}<br>{C["street"]}<br>{C["zip"]} {C["city"]}<br>{C["country"]}</p>
        <p style="margin-top:12px"><a class="link-u" href="{C["maps"]}" target="_blank" rel="noopener">Route planen ↗</a></p></div>
      <div><h4>ÖFFNUNGSZEITEN</h4>{hours_html()}<p class="open-status" style="margin-top:14px"><i></i><span>Mo–Fr 09–12 / 14–17</span></p></div>
      <div><h4>SERVICES</h4><ul>{svc}</ul></div>
      <div><h4>KONTAKT</h4><ul>
        <li><a class="link-u" href="tel:{C["phone_href"]}">{C["phone"]}</a></li>
        <li><a class="link-u" href="mailto:{C["email"]}">{C["email"]}</a></li>
        <li><a class="link-u" href="{p.url("kontakt/")}">Kontaktformular</a></li>
        <li><a class="link-u" href="{p.url("offerte/")}">Offerte anfragen</a></li>
      </ul></div>
    </div>
    <div class="footer-giant" aria-hidden="true">{giant}</div>
    <div class="footer-bottom">
      <span>© <span data-year>2026</span> {C["name"]} · {C["city"]}, Switzerland</span>
      <nav aria-label="Rechtliches"><a class="link-u" href="{p.url("impressum/")}">Impressum</a><a class="link-u" href="{p.url("datenschutz/")}">Datenschutz</a><a class="link-u" href="{p.url("agb/")}">AGB</a></nav>
    </div>
  </div>
</footer>
"""


def cta_band(p, title_lines=("LET’S MAKE", "SOMETHING WOW.")):
    l1, l2 = title_lines
    return f"""
<section class="cta-band section">
  <div class="wrap">
    <h2 class="cta-title display" data-lines>{lines(l1)}<span class="line"><span><span class="fill" data-text="{escape(l2)}">{l2}</span></span></span></h2>
    <div class="cta-side">
      <p>Have a project?</p>
      <a class="btn" href="{p.url("kontakt/")}" data-magnetic=".3">Get in touch {ARROW}</a>
      <a class="btn btn--solid" href="{p.url("offerte/")}" data-magnetic=".3">Offerte anfragen {ARROW}</a>
    </div>
  </div>
</section>"""


def page_hero(p, eyebrow, title_lines, lead="", crumbs=None, bg_num="", extra=""):
    crumb_html = ""
    if crumbs:
        crumb_html = '<nav class="breadcrumb" aria-label="Brotkrümel">' + ' <span>/</span> '.join(
            f'<a href="{p.url(t)}">{escape(l)}</a>' if t is not None else f"<span>{escape(l)}</span>" for t, l in crumbs
        ) + "</nav>"
    return f"""
<section class="page-hero">
  {f'<div class="bg-num" aria-hidden="true">{bg_num}</div>' if bg_num else ''}
  <div class="wrap" style="position:relative">
    {crumb_html}
    <h1 class="display">{lines(*title_lines)}</h1>
    <div class="hero-bottom">
      {f'<p class="lead">{lead}</p>' if lead else '<span></span>'}
      <span class="eyebrow">{eyebrow}</span>
    </div>
    {extra}
  </div>
</section>"""


def layout(p, title, desc, body, current="", og_img="hero-car.jpg", canonical=None, noindex=False):
    canonical_url = C["domain"] + "/" + (p.path if canonical is None else canonical)
    robots = '<meta name="robots" content="noindex">' if noindex else ""
    return f"""<!doctype html>
<html lang="de-CH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
{robots}
<link rel="canonical" href="{canonical_url}">
<meta name="theme-color" content="#f5bdbe">
<meta property="og:type" content="website">
<meta property="og:locale" content="de_CH">
<meta property="og:site_name" content="WOW PRINT">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:image" content="{C["domain"]}/assets/img/{og_img}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{p.asset("img/favicon.svg")}" type="image/svg+xml">
<link rel="preload" href="{p.asset("fonts/archivo.woff2")}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{p.asset("fonts/inter.woff2")}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{p.asset("css/style.css")}">
<script>document.documentElement.classList.add('js')</script>
</head>
<body>
{header(p, current)}
<main id="main">
{body}
</main>
{footer(p)}
<script src="{p.asset("js/gsap.min.js")}" defer></script>
<script src="{p.asset("js/ScrollTrigger.min.js")}" defer></script>
<script src="{p.asset("js/lenis.min.js")}" defer></script>
<script src="{p.asset("js/main.js")}" defer></script>
</body>
</html>
"""


def write(p, html):
    path = os.path.join(OUT, p.path, "index.html") if not p.path.endswith(".html") else os.path.join(OUT, p.path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("  ✓", os.path.relpath(path, OUT))


def img(p, name, alt, extra=""):
    return f'<img src="{p.asset("img/" + name)}" alt="{escape(alt)}" loading="lazy" decoding="async" {extra}>'

# ---------------------------------------------------------------- pages

def service_cards(p):
    cards = ""
    for s in SERVICES:
        cards += f"""
      <a class="service-card" href="{p.url("leistungen/" + s["slug"] + "/")}">
        <span class="num">{s["num"]}</span>
        <h3 class="display">{s["title"]}</h3>
        <p>{s["sub"]}</p>
        <div class="thumb">{img(p, s["img"], s["title"] + " – " + s["sub"])}</div>
        <span class="go"><span>Mehr</span>{ARROW}</span>
      </a>"""
    cards += f"""
      <a class="service-card service-card--cta" href="{p.url("offerte/")}">
        <span class="num">08</span>
        <span class="big">Your<br>idea?</span>
        <p>Etwas Besonderes vor? Erzählen Sie uns davon, wir finden einen Weg.</p>
        <span class="go"><span>Offerte</span>{ARROW}</span>
      </a>"""
    return cards


def home():
    p = Page("")
    projects = "".join(f"""
      <article class="project-card" data-cursor="WOW">
        {img(p, pr["img"], pr["title"])}
        <div class="project-meta"><div><h3 class="display">{pr["title"]}</h3><small>{pr["meta"]}</small></div><span class="tag">{pr["label"]}</span></div>
      </article>""" for pr in PROJECTS[:4])
    steps = "".join(f"""
        <div class="step{" step--wow" if n == "04" else ""}"><span class="num">{n}</span><h3 class="display">{t}</h3><p>{d}</p></div>""" for n, t, d in PROCESS)
    body = f"""
<section class="hero">
  <div class="hero-bgword" aria-hidden="true">WOW</div>
  <div class="hero-media">{img(p, "hero-car.jpg", "Sportwagen in Rosa, foliert mit WOW-Schriftzug", 'fetchpriority="high" loading="eager"')}</div>
  <div class="wrap hero-content">
    <h1 class="display">{lines("We make", "you visible.")}</h1>
    <div class="hero-bottom">
      <p class="lead">Fahrzeugbeschriftung, Werbetechnik, Textil, Print und Design aus Rorschach. Für Marken, die nicht wie alle anderen aussehen wollen.</p>
      <a class="scroll-cue" href="#services">Scroll {ARROW_DOWN}</a>
    </div>
  </div>
</section>

{marquee([s["title"] for s in SERVICES])}

<section class="section" id="services">
  <div class="wrap services-layout">
    <div class="services-intro">
      <span class="eyebrow">Services</span>
      <h2 class="display d-l" style="margin-top:18px" data-lines>{lines("What", "we do.")}</h2>
      <p class="lead" data-reveal>Sieben Disziplinen, ein Ziel: Ihre Marke sichtbar machen. Von der ersten Skizze bis zur fertigen Montage, alles aus einer Hand.</p>
      <a class="btn" href="{p.url("leistungen/")}" data-magnetic=".3" data-reveal>Alle Services {ARROW}</a>
    </div>
    <div class="services-grid">{service_cards(p)}
    </div>
  </div>
</section>

<section class="statement section">
  <div class="wrap">
    <span class="eyebrow" style="color:var(--pink)">Different by design</span>
    <p class="statement-text">Wir sind keine 0815-Agentur. Wir verbinden <em>italienisches Designgefühl</em> mit <em>Schweizer Präzision</em> und machen Marken sichtbar, die man nicht mehr vergisst.</p>
    <div class="statement-foot">
      <span class="eyebrow" style="color:var(--paper)"><span class="it-flag" aria-hidden="true"><i style="background:#2f9b55"></i><i style="background:#f6f5f1"></i><i style="background:#d6403a"></i></span>&nbsp;Design con passione · Made in Rorschach</span>
      <a class="btn btn--light" href="{p.url("ueber-uns/")}" data-magnetic=".3">About us {ARROW}</a>
    </div>
  </div>
</section>

<section class="projects" id="work">
  <div class="projects-pin">
    <div class="wrap section-head">
      <span class="eyebrow">Selected work</span>
      <h2 class="display d-xl" data-lines>{lines("Projects.")}</h2>
      <a class="btn" href="{p.url("projekte/")}" data-magnetic=".3">All projects {ARROW}</a>
    </div>
    <div class="projects-track">{projects}
      <div class="projects-end">
        <h3 class="display d-m">Your project<br>could be next.</h3>
        <a class="btn btn--solid" href="{p.url("offerte/")}" data-magnetic=".3">Projekt starten {ARROW}</a>
      </div>
    </div>
  </div>
</section>

<section class="process section">
  <div class="wrap process-grid">
    <div>
      <span class="eyebrow">Our process</span>
      <h2 class="display d-l" style="margin-top:18px" data-lines>{lines("Simple.")}</h2>
    </div>
    <div class="process-steps"><div class="process-line"><i></i></div>{steps}
    </div>
  </div>
</section>

{marquee(["We make you visible", "Rorschach", "Switzerland", "Since day one: WOW"], pink=True, reverse=True)}
{cta_band(p)}
"""
    write(p, layout(p, "WOW PRINT – We make you visible. | Werbetechnik Rorschach",
                    "WOW PRINT aus Rorschach: Fahrzeugbeschriftung, Schaufenster, Textildruck, Print, Schilder, Design und Websites. Alles aus einer Hand.", body))


def services_overview():
    p = Page("leistungen/")
    rows = "".join(f"""
    <a class="svc-row" href="{p.url("leistungen/" + s["slug"] + "/")}" data-img="{p.asset("img/" + s["img"])}" data-reveal>
      <span class="num">{s["num"]}</span>
      <h2 class="display">{s["title"]}</h2>
      <p>{s["sub"]}<br><span class="muted">{s["short"]}</span></p>
      <span class="circle">{ARROW}</span>
    </a>""" for s in SERVICES)
    body = f"""
{page_hero(p, "Services", ["What", "we do."], "Sieben Disziplinen unter einem Dach. Wir gestalten, produzieren und montieren und machen Ihre Marke überall sichtbar, wo man sie sehen soll.", [("", "Home"), (None, "Services")])}
<section class="section">
  <div class="wrap">
    <div class="svc-list">{rows}
    </div>
  </div>
  <div class="hover-img" aria-hidden="true"><img src="" alt=""></div>
</section>
{marquee(["Design", "Print", "Plot", "Produce", "Install", "Wow"])}
<section class="process section">
  <div class="wrap process-grid">
    <div><span class="eyebrow">Our process</span><h2 class="display d-l" style="margin-top:18px" data-lines>{lines("Simple.")}</h2></div>
    <div class="process-steps"><div class="process-line"><i></i></div>{"".join(f'<div class="step{" step--wow" if n == "04" else ""}"><span class="num">{n}</span><h3 class="display">{t}</h3><p>{d}</p></div>' for n, t, d in PROCESS)}</div>
  </div>
</section>
{cta_band(p)}
"""
    write(p, layout(p, "Services – WOW PRINT", "Fahrzeugbeschriftung, Schaufenster, Textildruck, Print, Schilder, Design und Websites von WOW PRINT in Rorschach.", body, current="leistungen/"))


def service_page(i, s):
    p = Page(f"leistungen/{s['slug']}/")
    nxt = SERVICES[(i + 1) % len(SERVICES)]
    offers = "".join(f'<li data-reveal><span class="num">{str(k + 1).zfill(2)}</span><h3 class="display">{t}</h3><p>{d}</p></li>' for k, (t, d) in enumerate(s["offers"]))
    why = "".join(f'<div class="feature" data-reveal><span class="ico">{FEATURE_ICONS[k % 3]}</span><h3 class="display">{t}</h3><p>{d}</p></div>' for k, (t, d) in enumerate(s["why"]))
    faq = "".join(f'<details><summary>{q}<span class="pm" aria-hidden="true"></span></summary><div class="answer"><p>{a}</p></div></details>' for q, a in s["faq"])
    ba = ""
    if s.get("before_after"):
        ba = f"""
<section class="section section--tight">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Before / After</span><h2 class="display d-l" data-lines>{lines("Same car.", "New story.")}</h2><p class="muted">Ziehen Sie den Regler und sehen Sie, was eine Folierung aus einem Fahrzeug macht.</p></div>
    <div class="ba" data-reveal>
      {img(p, "vehicle-after.jpg", "Fahrzeug nach der Folierung")}
      <img class="ba-before" src="{p.asset("img/vehicle-before.jpg")}" alt="Fahrzeug vor der Folierung" loading="lazy">
      <span class="ba-label ba-label--l">Before</span><span class="ba-label ba-label--r">After</span>
      <div class="ba-handle"></div>
      <input type="range" min="0" max="100" value="50" aria-label="Vorher-Nachher-Vergleich">
    </div>
  </div>
</section>"""
    body = f"""
{page_hero(p, s["sub"], [s["title"] + "."], s["short"], [("", "Home"), ("leistungen/", "Services"), (None, s["title"])], bg_num=s["num"])}
<div class="media-band">{img(p, s["img"], s["title"] + " – " + s["sub"], 'data-parallax=".25"')}</div>
<section class="section">
  <div class="wrap split">
    <div><span class="eyebrow">{s["num"]} — {s["sub"]}</span><h2 class="display d-m" style="margin-top:18px" data-lines>{lines("Make it", "impossible", "to ignore.")}</h2></div>
    <div class="prose" data-reveal>{"".join(f"<p>{t}</p>" for t in s["intro"])}
      <a class="btn btn--solid" href="{p.url("offerte/")}?leistung={s["key"]}" data-magnetic=".3" style="margin-top:14px">Offerte für {s["title"]} {ARROW}</a>
    </div>
  </div>
</section>
<section class="section section--tight" style="padding-top:0">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">What we offer</span><h2 class="display d-l" data-lines>{lines("Our scope.")}</h2></div>
    <ul class="offer-list">{offers}</ul>
  </div>
</section>
{ba}
<section class="section bg-ink on-dark">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow" style="color:var(--pink)">Why WOW</span><h2 class="display d-l" data-lines>{lines("Why us.")}</h2></div>
    <div class="cards-3">{why}</div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Gallery</span><h2 class="display d-l" data-lines>{lines("In action.")}</h2></div>
    <div class="gallery">
      <figure class="g1" data-reveal>{img(p, s["img"], s["title"])}</figure>
      <figure class="g2" data-reveal>{img(p, s["slug"] + "-2.jpg", s["title"] + " Detail")}<figcaption>Detail</figcaption></figure>
      <figure class="g3" data-reveal>{img(p, s["slug"] + "-3.jpg", s["title"] + " Produktion")}<figcaption>Production</figcaption></figure>
      <figure class="g4" data-reveal>{img(p, s["slug"] + "-4.jpg", s["title"] + " Ergebnis")}<figcaption>Result</figcaption></figure>
    </div>
  </div>
</section>
<section class="section bg-paper2">
  <div class="wrap split">
    <div><span class="eyebrow">FAQ</span><h2 class="display d-l" style="margin-top:18px" data-lines>{lines("Good", "questions.")}</h2></div>
    <div class="faq">{faq}</div>
  </div>
</section>
<div class="next-wrap"><a class="next-link" href="{p.url("leistungen/" + nxt["slug"] + "/")}" data-cursor="Next"><div class="wrap"><span class="eyebrow">Next service · {nxt["num"]}</span><span class="display d-xl">{nxt["title"]} {ARROW_DIAG}</span></div></a></div>
{cta_band(p)}
"""
    write(p, layout(p, f"{s['title']} – {s['sub']} | WOW PRINT Rorschach", s["short"], body, current="leistungen/", og_img=s["img"]))


def projects_page():
    p = Page("projekte/")
    chips = '<button class="chip is-active" data-filter="all" aria-pressed="true">Alle</button>' + "".join(
        f'<button class="chip" data-filter="{s["key"]}" aria-pressed="false">{s["title"]}</button>' for s in SERVICES)
    cards = "".join(f"""
      <article class="work-card" data-cat="{pr["cat"]}" data-cursor="WOW" data-reveal>
        <div class="media">{img(p, pr["img"], pr["title"])}</div>
        <div class="info"><h3 class="display">{pr["title"]}</h3><small>{pr["meta"]} · {pr["label"]}</small></div>
      </article>""" for pr in PROJECTS)
    body = f"""
{page_hero(p, "Selected work", ["Projects."], "Eine Auswahl unserer Arbeiten: Fahrzeuge, Schaufenster, Textilien, Print und mehr. Jedes Projekt mit dem Ziel, aufzufallen.", [("", "Home"), (None, "Work")])}
<section class="section">
  <div class="wrap">
    <div class="filters" role="group" aria-label="Projekte filtern">{chips}</div>
    <div class="work-grid">{cards}
    </div>
    <p class="note">Hinweis: Die gezeigten Projekte sind Platzhalter und werden durch echte Referenzen ersetzt.</p>
  </div>
</section>
{cta_band(p, ("Your project", "could be next."))}
"""
    write(p, layout(p, "Projects – WOW PRINT", "Ausgewählte Projekte von WOW PRINT: Fahrzeugfolierungen, Schaufenster, Textil, Print und Design.", body, current="projekte/"))


def about_page():
    p = Page("ueber-uns/")
    body = f"""
{page_hero(p, "About", ["We are", "different."], "Kein Standard, kein Copy-Paste. WOW PRINT ist für alle, die mit ihrem Auftritt auffallen wollen.", [("", "Home"), (None, "About")])}
<section class="section">
  <div class="wrap split">
    <div><span class="eyebrow">Manifest</span></div>
    <div class="prose" data-reveal>
      <p>Es gibt genug Agenturen, die alles ein bisschen gleich machen. Wir machen es lieber anders: mutiger, klarer, mit mehr Gefühl für Form und Farbe.</p>
      <p>WOW PRINT ist ein Studio für Werbetechnik und Design in Rorschach. Wir gestalten, drucken, plotten und montieren unter einem Dach. So bleibt die Idee vom ersten Strich bis zur letzten Kante in einer Hand.</p>
      <p>Unser Anspruch ist einfach: Wenn jemand Ihr Fahrzeug, Ihr Schaufenster oder Ihr Shirt sieht, soll er zweimal hinschauen.</p>
    </div>
  </div>
</section>
<section class="duo">
  <div class="it">
    <span class="eyebrow">Design con passione</span>
    <h2 class="display d-xl" data-lines>{lines("Italian", "design.")}</h2>
    <p>Gespür für Ästhetik, Proportion und Stil. Wir glauben, dass gutes Design Emotionen auslöst und dass auch Werbetechnik schön sein darf.</p>
  </div>
  <div class="ch on-dark">
    <span class="eyebrow" style="color:var(--pink)">Swiss made</span>
    <h2 class="display d-xl" data-lines>{lines("Swiss", "precision.")}</h2>
    <p class="muted">Sauber geplant, exakt produziert, pünktlich montiert. Auf uns ist Verlass, bis in die letzte Folienkante.</p>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Values</span><h2 class="display d-l" data-lines>{lines("What drives us.")}</h2></div>
    <div class="values">
      <div class="value" data-reveal><span class="num">01</span><h3 class="display">Bold.</h3><p>Wir trauen uns, aufzufallen, und bringen Ideen ein, auf die andere nicht kommen.</p></div>
      <div class="value" data-reveal><span class="num">02</span><h3 class="display">Precise.</h3><p>Hinter jedem WOW steckt Handwerk: genaue Planung, gute Materialien, saubere Arbeit.</p></div>
      <div class="value" data-reveal><span class="num">03</span><h3 class="display">Personal.</h3><p>Ein Ansprechpartner, kurze Wege, ehrliche Beratung. Wir nehmen uns Zeit für Ihr Projekt.</p></div>
    </div>
  </div>
</section>
{marquee(["Design", "Print", "Plot", "Produce", "Install", "All in one house"], pink=True)}
<section class="section bg-ink on-dark">
  <div class="wrap split">
    <div><span class="eyebrow" style="color:var(--pink)">Rorschach · Bodensee</span></div>
    <div>
      <p class="big-quote" data-reveal>Am Bodensee zu Hause, für Kundinnen und Kunden in der ganzen Ostschweiz unterwegs.</p>
      <p class="muted" style="margin-top:26px" data-reveal>{ADDRESS}</p>
      <a class="btn btn--light" style="margin-top:22px" href="{C["maps"]}" target="_blank" rel="noopener" data-magnetic=".3" data-reveal>Route planen {ARROW}</a>
    </div>
  </div>
</section>
{cta_band(p)}
"""
    write(p, layout(p, "About – WOW PRINT", "WOW PRINT: Italienisches Designgefühl trifft Schweizer Präzision. Werbetechnik und Design aus Rorschach.", body, current="ueber-uns/"))


def contact_page():
    p = Page("kontakt/")
    body = f"""
{page_hero(p, "Contact", ["Let’s talk."], "Sie haben eine Idee, ein Projekt oder einfach eine Frage? Schreiben Sie uns, rufen Sie an oder kommen Sie vorbei.", [("", "Home"), (None, "Contact")])}
<section class="section">
  <div class="wrap contact-layout">
    <div class="contact-info">
      <div><h4>TELEFON</h4><a class="big-link link-u" href="tel:{C["phone_href"]}">{C["phone"]}</a></div>
      <div><h4>E-MAIL</h4><a class="big-link link-u" href="mailto:{C["email"]}">{C["email"]}</a></div>
      <div><h4>STUDIO</h4><p>{C["name"]}<br>{C["street"]}<br>{C["zip"]} {C["city"]}</p><p style="margin-top:8px"><a class="link-u" href="{C["maps"]}" target="_blank" rel="noopener">Route planen ↗</a></p></div>
      <div><h4>ÖFFNUNGSZEITEN</h4>{hours_html()}<p class="open-status" style="margin-top:12px"><i></i><span>Mo–Fr 09–12 / 14–17</span></p></div>
      <div><h4>SOCIAL</h4>{socials()}</div>
    </div>
    <div>
      <h2 class="display d-m" data-lines>{lines("Write us.")}</h2>
      <p class="muted" style="margin:14px 0 36px">Für eine konkrete Offerte mit Dateien nutzen Sie am besten unser <a class="link-u" style="color:var(--ink)" href="{p.url("offerte/")}">Offertenformular</a>.</p>
      <form name="kontakt" method="POST" action="{p.form_action("danke/")}" data-netlify="true" netlify-honeypot="bot-field">
        <input type="hidden" name="form-name" value="kontakt">
        <p class="hp"><label>Nicht ausfüllen: <input name="bot-field"></label></p>
        <div class="form-grid">
          <div class="field"><label for="k-name">Name</label><input id="k-name" name="name" autocomplete="name" required></div>
          <div class="field"><label for="k-firma">Firma <span class="opt">(optional)</span></label><input id="k-firma" name="firma" autocomplete="organization"></div>
          <div class="field"><label for="k-mail">E-Mail</label><input id="k-mail" type="email" name="email" autocomplete="email" required></div>
          <div class="field"><label for="k-tel">Telefon <span class="opt">(optional)</span></label><input id="k-tel" type="tel" name="telefon" autocomplete="tel"></div>
          <div class="field full"><label for="k-thema">Thema</label>
            <select id="k-thema" name="thema"><option>Allgemeine Anfrage</option>{"".join(f"<option>{s['title']} – {s['sub']}</option>" for s in SERVICES)}</select></div>
          <div class="field full"><label for="k-msg">Nachricht</label><textarea id="k-msg" name="nachricht" required></textarea></div>
          <label class="check full"><input type="checkbox" name="datenschutz" value="akzeptiert" required><span>Ich habe die <a class="link-u" href="{p.url("datenschutz/")}">Datenschutzerklärung</a> gelesen und bin einverstanden, dass meine Angaben zur Bearbeitung der Anfrage verwendet werden.</span></label>
          <div class="full"><button class="btn btn--solid" type="submit" data-magnetic=".3">Nachricht senden {ARROW}</button></div>
        </div>
      </form>
    </div>
  </div>
</section>
"""
    write(p, layout(p, "Contact – WOW PRINT Rorschach", f"Kontakt zu WOW PRINT, {ADDRESS}. Öffnungszeiten Mo–Fr 09:00–12:00 und 14:00–17:00.", body, current="kontakt/"))


def quote_page():
    p = Page("offerte/")
    choices = "".join(f"""
          <label class="choice"><input type="checkbox" name="leistung[]" value="{s["key"]}"><span><em>{s["num"]}</em><b>{s["title"]}</b><small>{s["sub"]}</small></span></label>""" for s in SERVICES)
    choices += '<label class="choice"><input type="checkbox" name="leistung[]" value="anderes"><span><em>08</em><b>Other</b><small>Etwas anderes oder noch unklar</small></span></label>'

    def radio_group(name, opts):
        return "".join(f'<label class="choice"><input type="radio" name="{name}" value="{o}"{" required" if k == 0 else ""}><span><b>{o}</b></span></label>' for k, o in enumerate(opts))

    def dz(n, label):
        return f"""<label class="dropzone"><input type="file" name="datei{n}" accept=".pdf,.ai,.eps,.svg,.png,.jpg,.jpeg,.heic,.zip"><span class="dz-ico">{UPLOAD}</span><span><strong>{label}</strong><small>PDF, AI, EPS, SVG, JPG, PNG oder ZIP</small></span></label>"""

    body = f"""
{page_hero(p, "Get a quote", ["Let’s make", "it wow."], "In vier kurzen Schritten zur unverbindlichen Offerte. Wir melden uns innert zwei Arbeitstagen bei Ihnen.", [("", "Home"), (None, "Offerte")])}
<section class="section">
  <div class="wrap" style="max-width:1100px">
    <form class="wizard" name="offerte" method="POST" action="{p.form_action("danke/")}" enctype="multipart/form-data" data-netlify="true" netlify-honeypot="bot-field" novalidate>
      <input type="hidden" name="form-name" value="offerte">
      <p class="hp"><label>Nicht ausfüllen: <input name="bot-field"></label></p>
      <ol class="wizard-progress" aria-hidden="true"><li><span>01 Leistung</span></li><li><span>02 Projekt</span></li><li><span>03 Dateien</span></li><li><span>04 Kontakt</span></li></ol>

      <fieldset data-require-one>
        <legend><span class="eyebrow">Schritt 1 von 4</span><h2 class="display d-m" style="margin-top:14px">What do you need?</h2></legend>
        <div class="choice-grid">{choices}
        </div>
      </fieldset>

      <fieldset>
        <legend><span class="eyebrow">Schritt 2 von 4</span><h2 class="display d-m" style="margin-top:14px">Tell us more.</h2></legend>
        <div class="form-grid">
          <div class="field full"><label for="o-desc">Projektbeschreibung</label><textarea id="o-desc" name="beschreibung" required placeholder="Was soll entstehen? Z. B. Fahrzeugmodell, Fläche, Anzahl Shirts, Wunschtexte …"></textarea></div>
          <div class="field"><label for="o-menge">Menge / Masse <span class="opt">(optional)</span></label><input id="o-menge" name="menge" placeholder="z. B. 3 Fahrzeuge, 2 × 1.5 m, 50 Stück"></div>
          <div class="field"><label for="o-termin">Wunschtermin <span class="opt">(optional)</span></label><input id="o-termin" type="date" name="termin"></div>
          <div class="field full"><span class="label">Budgetrahmen <span class="opt">(optional)</span></span>
            <div class="choice-grid choice-grid--sm" style="margin-top:6px">
              {"".join(f'<label class="choice"><input type="radio" name="budget" value="{o}"><span><b>{o}</b></span></label>' for o in ["bis CHF 1’000", "CHF 1’000 – 3’000", "CHF 3’000 – 10’000", "über CHF 10’000", "Noch offen"])}
            </div></div>
          <div class="field full"><span class="label">Design vorhanden?</span>
            <div class="choice-grid choice-grid--sm" style="margin-top:6px">{radio_group("design", ["Ja, Druckdaten sind bereit", "Teilweise (Logo o. ä.)", "Nein, bitte gestalten"])}</div></div>
        </div>
      </fieldset>

      <fieldset>
        <legend><span class="eyebrow">Schritt 3 von 4</span><h2 class="display d-m" style="margin-top:14px">Upload files.</h2></legend>
        <p class="muted" style="margin:-10px 0 24px">Logo, Druckdaten, Fotos vom Fahrzeug oder Schaufenster, Skizzen. Alles hilft. Optional, max. 8 MB insgesamt.</p>
        <div class="uploads">{dz(1, "Datei 1 hochladen")}{dz(2, "Datei 2 hochladen")}{dz(3, "Datei 3 hochladen")}</div>
      </fieldset>

      <fieldset>
        <legend><span class="eyebrow">Schritt 4 von 4</span><h2 class="display d-m" style="margin-top:14px">Almost wow.</h2></legend>
        <div class="form-grid">
          <div class="field"><label for="o-name">Vorname & Name</label><input id="o-name" name="name" autocomplete="name" required></div>
          <div class="field"><label for="o-firma">Firma <span class="opt">(optional)</span></label><input id="o-firma" name="firma" autocomplete="organization"></div>
          <div class="field"><label for="o-mail">E-Mail</label><input id="o-mail" type="email" name="email" autocomplete="email" required></div>
          <div class="field"><label for="o-tel">Telefon</label><input id="o-tel" type="tel" name="telefon" autocomplete="tel" required></div>
          <div class="field full"><label for="o-ort">PLZ / Ort <span class="opt">(optional)</span></label><input id="o-ort" name="ort" autocomplete="address-level2"></div>
          <div class="field full"><span class="label">Bevorzugter Kontakt</span>
            <div class="choice-grid choice-grid--sm" style="margin-top:6px">{radio_group("kontaktweg", ["Anruf", "WhatsApp", "E-Mail"])}</div></div>
          <label class="check full"><input type="checkbox" name="datenschutz" value="akzeptiert" required><span>Ich habe die <a class="link-u" href="{p.url("datenschutz/")}">Datenschutzerklärung</a> und die <a class="link-u" href="{p.url("agb/")}">AGB</a> gelesen und bin einverstanden, dass meine Angaben für die Offerte verwendet werden.</span></label>
        </div>
      </fieldset>

      <p class="wizard-error" role="alert"></p>
      <div class="wizard-nav">
        <button type="button" class="back" hidden>← Zurück</button>
        <span></span>
        <button type="button" class="btn btn--solid next" data-magnetic=".3">Weiter {ARROW}</button>
        <button type="submit" class="btn btn--solid submit" hidden data-magnetic=".3">Offerte anfragen {ARROW}</button>
      </div>
    </form>
  </div>
</section>
"""
    write(p, layout(p, "Offerte anfragen – WOW PRINT", "Unverbindliche Offerte für Fahrzeugbeschriftung, Schaufenster, Textildruck, Print, Schilder, Design oder Website anfragen.", body))


def thanks_page():
    p = Page("danke/")
    body = f"""
<section class="center-stage">
  <div class="hero-bgword" aria-hidden="true">WOW</div>
  <div style="position:relative">
    <span class="eyebrow">Message received</span>
    <h1 class="display d-xxl" style="margin-top:20px">{lines("Wow!")}</h1>
    <p>Danke für Ihre Anfrage. Wir melden uns innert zwei Arbeitstagen bei Ihnen. Bis bald!</p>
    <a class="btn btn--solid" href="{p.url("")}" data-magnetic=".3">Zur Startseite {ARROW}</a>
  </div>
</section>"""
    write(p, layout(p, "Danke – WOW PRINT", "Vielen Dank für Ihre Anfrage.", body, noindex=True))


def not_found():
    p = Page("404.html", absolute=True)
    body = f"""
<section class="center-stage">
  <div class="hero-bgword" aria-hidden="true">404</div>
  <div style="position:relative">
    <span class="eyebrow">Error 404</span>
    <h1 class="display d-xxl" style="margin-top:20px">{lines("Oops.")}</h1>
    <p>Diese Seite ist leider nicht sichtbar. Ausnahmsweise. Alles andere finden Sie hier:</p>
    <a class="btn btn--solid" href="{p.url("")}" data-magnetic=".3">Zur Startseite {ARROW}</a>
  </div>
</section>"""
    write(p, layout(p, "Seite nicht gefunden – WOW PRINT", "Diese Seite existiert nicht.", body, noindex=True, canonical="404"))


def legal_page(slug, eyebrow, title, desc, inner):
    p = Page(slug + "/")
    body = f"""
{page_hero(p, eyebrow, [title], "", [("", "Home"), (None, eyebrow)])}
<section class="section">
  <div class="wrap"><div class="legal">{inner(p)}</div></div>
</section>"""
    write(p, layout(p, f"{eyebrow} – WOW PRINT", desc, body))


from legal import impressum, datenschutz, agb  # noqa: E402


def main():
    print("Baue WOW PRINT Website" + (" (Vorschau)" if PREVIEW else "") + " …")
    home()
    services_overview()
    for i, s in enumerate(SERVICES):
        service_page(i, s)
    projects_page()
    about_page()
    contact_page()
    quote_page()
    thanks_page()
    not_found()
    legal_page("impressum", "Impressum", "Imprint.", "Impressum von WOW PRINT, Rorschach.", impressum)
    legal_page("datenschutz", "Datenschutz", "Privacy.", "Datenschutzerklärung von WOW PRINT nach Schweizer Datenschutzgesetz (DSG).", datenschutz)
    legal_page("agb", "AGB", "Terms.", "Allgemeine Geschäftsbedingungen von WOW PRINT.", agb)
    print("Fertig.")


if __name__ == "__main__":
    main()
