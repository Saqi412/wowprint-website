# -*- coding: utf-8 -*-
"""Erzeugt die statischen HTML-Seiten der WOW PRINT Website nach ./site.

    python3 tools/build.py            # für Netlify (saubere URLs)
    python3 tools/build.py --preview  # Links auf index.html, für lokale Vorschau
"""
import hashlib
import json, os, re
import sys
from html import escape

sys.path.insert(0, os.path.dirname(__file__))
from content import COMPANY, HOURS, SERVICES, PROJECTS, PROCESS, WOWLAB, UPDATED  # noqa: E402
_MONATE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
UPDATED_TEXT = f"{int(UPDATED[8:10])}. {_MONATE[int(UPDATED[5:7]) - 1]} {UPDATED[:4]}"

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site")
PREVIEW = "--preview" in sys.argv
OUT = ROOT if "--out" not in sys.argv else sys.argv[sys.argv.index("--out") + 1]

C = COMPANY
with open(os.path.join(os.path.dirname(__file__), "logo.svg"), encoding="utf-8") as _f:
    LOGO = _f.read().replace('xmlns:xlink="http://www.w3.org/1999/xlink" ', "").strip()
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
        base = "/assets/" if self.absolute and not PREVIEW else "../" * self.depth + "assets/"
        return base + p + version(p)

    def form_action(self, target):
        return "/" + target if not PREVIEW else self.url(target)


def version(p):
    """Cache-Busting: ?v=<Hash> ändert sich, sobald sich die Datei ändert."""
    f = os.path.join(ROOT, "assets", p)
    if p.startswith("fonts/") or not os.path.exists(f):
        return ""
    with open(f, "rb") as fh:
        return "?v=" + hashlib.md5(fh.read()).hexdigest()[:8]


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
    svg = LOGO.replace("<svg ", f'<svg class="logo-svg {cls}" role="img" aria-label="WOW PRINT" ', 1)
    return svg


def lines(*ls):
    return " ".join(f'<span class="line"><span>{l}</span></span>' for l in ls)


def socials():
    return (f'<div class="socials">'
            f'<a href="{C["instagram"]}" aria-label="Instagram" target="_blank" rel="noopener" data-magnetic=".4">{IG}</a>'
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


NAV = [("projekte/", "Projekte"), ("leistungen/", "Leistungen"), ("ueber-uns/", "Über uns"), ("kontakt/", "Kontakt")]


def header(p, current=""):
    nav = "".join(
        f'<a class="link-u" href="{p.url(t)}"{" aria-current=page" if current == t else ""}>{label}</a>'
        for t, label in NAV
    )
    menu_links = "".join(
        f'<li><a href="{p.url(t)}"><small>0{i}</small>{label}</a></li>'
        for i, (t, label) in enumerate([("", "Start")] + NAV + [("offerte/", "Offerte anfragen")], 1)
    )
    menu_services = "".join(f'<a href="{p.url("leistungen/" + s["slug"] + "/")}">{s["title"]}</a>' for s in SERVICES)
    return f"""
<a class="skip-link" href="#main">Zum Inhalt springen</a>
<div class="preloader" aria-hidden="true">
  <div class="preloader-word"><span>W</span><span>O</span><span>W</span></div>
  <div class="preloader-claim">Wir machen Sie WOW.</div>
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
      <div><h4>LEISTUNGEN</h4><div class="menu-services">{menu_services}</div></div>
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
        <p>Fahrzeugbeschriftung, Werbetechnik, Textil, Print und Design aus Rorschach. Wir machen Sie WOW.</p>
        <div style="margin-top:26px">{socials()}</div>
      </div>
      <div><h4>STUDIO</h4><p>{C["name"]}<br>{C["street"]}<br>{C["zip"]} {C["city"]}<br>{C["country"]}</p>
        <p style="margin-top:12px"><a class="link-u" href="{C["maps"]}" target="_blank" rel="noopener">Route planen ↗</a></p></div>
      <div><h4>ÖFFNUNGSZEITEN</h4>{hours_html()}</div>
      <div><h4>LEISTUNGEN</h4><ul>{svc}</ul></div>
      <div><h4>KONTAKT</h4><ul>
        <li><a class="link-u" href="tel:{C["phone_href"]}">{C["phone"]}</a></li>
        <li><a class="link-u" href="mailto:{C["email"]}">{C["email"]}</a></li>
        <li><a class="link-u" href="{p.url("kontakt/")}">Kontaktformular</a></li>
        <li><a class="link-u" href="{p.url("offerte/")}">Offerte anfragen</a></li>
      </ul></div>
    </div>
    <div class="footer-giant" aria-hidden="true">{giant}</div>
    <div class="footer-bottom">
      <span>© <span data-year>2026</span> {C["name"]} · {C["city"]}, Schweiz</span>
      <nav aria-label="Rechtliches"><a class="link-u" href="{p.url("impressum/")}">Impressum</a><a class="link-u" href="{p.url("datenschutz/")}">Datenschutz</a><a class="link-u" href="{p.url("agb/")}">AGB</a></nav>
    </div>
  </div>
</footer>
"""


def fill_text(t):
    """Runder Punkt im Fill-Titel: bleibt mit dem letzten Wort auf derselben Zeile."""
    if not t.endswith("."):
        return t
    head, _, last = t.rstrip(".").rpartition(" ")
    return (head + " " if head else "") + f'<span class="nowrap">{last}{DOT}</span>'


def cta_band(p, title_lines=("Machen wir", "etwas WOW.")):
    l1, l2 = title_lines
    return f"""
<section class="cta-band section">
  <div class="wrap">
    <h2 class="cta-title display" data-lines>{lines(l1)} <span class="line"><span><span class="fill"><span class="fill-base">{fill_text(l2)}</span><span class="fill-top" aria-hidden="true">{fill_text(l2)}</span></span></span></span></h2>
    <div class="cta-side">
      <p>Haben Sie ein Projekt?</p>
      <a class="btn" href="{p.url("kontakt/")}" data-magnetic=".3">Kontakt aufnehmen {ARROW}</a>
      <a class="btn btn--solid" href="{p.url("offerte/")}" data-magnetic=".3">Offerte anfragen {ARROW}</a>
    </div>
  </div>
</section>"""


def fit_style(title_lines, vw=11.0):
    """Lange deutsche Wörter (z. B. SCHAUFENSTER.) passen sonst nicht in die Breite."""
    longest = max(len(t) for t in title_lines)
    size = min(vw, 78 / (longest * 0.9))
    return "" if size >= vw else f' style="font-size:clamp(34px, {size:.2f}vw, 190px)"'


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
    <h1 class="display"{fit_style(title_lines)}>{lines(*title_lines)}</h1>
    <div class="hero-bottom">
      {f'<p class="lead">{lead}</p>' if lead else '<span></span>'}
      <span class="eyebrow">{eyebrow}</span>
    </div>
    {extra}
  </div>
</section>"""


SITEMAP = []


def business_ld():
    return {
        "@context": "https://schema.org", "@type": "LocalBusiness", "@id": C["domain"] + "/#firma",
        "name": C["name"], "legalName": C["legal_name"], "url": C["domain"] + "/",
        "logo": C["domain"] + "/assets/img/wowprint-logo.svg", "image": C["domain"] + "/assets/img/hero-car.jpg",
        "description": "Werbetechnik und Design aus Rorschach: Fahrzeugbeschriftung und Folierung, Schaufenster, Textildruck, Print, Schilder, Grafikdesign und Websites.",
        "email": C["email"], "taxID": C["uid"],
        "telephone": C["phone_intl"],
        "address": {"@type": "PostalAddress", "streetAddress": C["street"], "postalCode": C["zip"],
                    "addressLocality": C["city"], "addressRegion": "SG", "addressCountry": "CH"},
        "areaServed": [{"@type": "City", "name": "Rorschach"}, {"@type": "City", "name": "St. Gallen"},
                       {"@type": "AdministrativeArea", "name": "Bodensee"}, {"@type": "AdministrativeArea", "name": "St. Galler Rheintal"},
                       {"@type": "AdministrativeArea", "name": "Thurgau"}, {"@type": "Country", "name": "Schweiz"}],
        "founder": {"@type": "Person", "name": C["owner"], "jobTitle": "Inhaberin"},
        **{k: C[k2] for k, k2 in (("foundingDate", "founded"), ("priceRange", "price_range")) if C.get(k2)},
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
             "opens": o, "closes": c} for o, c in (("09:00", "12:00"), ("14:00", "17:00"))],
        "sameAs": [C["instagram"]] + C.get("profiles", []),
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Leistungen", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": f'{s["title"]}: {s.get("seo_sub", s["sub"])}',
             "url": C["domain"] + "/leistungen/" + s["slug"] + "/"}} for s in SERVICES]},
    }


def strip_tags(t):
    return re.sub(r"<[^>]+>", "", t)


def service_ld(s):
    return [
        {"@context": "https://schema.org", "@type": "Service", "name": s.get("seo_sub", s["sub"]), "serviceType": s["title"],
         "description": s["short"], "provider": {"@id": C["domain"] + "/#firma"},
         "areaServed": {"@type": "Country", "name": "Schweiz"}, "url": C["domain"] + "/leistungen/" + s["slug"] + "/",
         "dateModified": UPDATED},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": strip_tags(q), "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}}
            for q, a in s["faq"]]},
    ][:2 if s["faq"] else 1]


def seo_files():
    """robots.txt, sitemap.xml und llms.txt (für Suchmaschinen und KI-Crawler)."""
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
        bots = ["OAI-SearchBot", "ChatGPT-User", "Claude-SearchBot", "Claude-User", "PerplexityBot", "Perplexity-User", "Bingbot", "Applebot", "Googlebot"]
        f.write("".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots)
                + "User-agent: *\nContent-Signal: search=yes, ai-input=yes\nAllow: /\n\n"
                + f"Sitemap: {C['domain']}/sitemap.xml\n")
    urls = "".join(f"  <url><loc>{u}</loc></url>\n" for u in dict.fromkeys(SITEMAP))
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    svc = "\n".join(f'- [{s["title"]}: {s.get("seo_sub", s["sub"])}]({C["domain"]}/leistungen/{s["slug"]}/): {strip_tags(s["short"])}' for s in SERVICES)
    hours = "Montag bis Freitag 09:00–12:00 und 14:00–17:00"
    phone = "" if "000 00 00" in C["phone"] else f"\n- Telefon: {C['phone']}"
    with open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8") as f:
        f.write(f"""# {C["name"]}

> {C["name"]} ({C["legal_name"]}) ist ein Werbetechnik- und Designstudio in {C["city"]} (Kanton St. Gallen, Schweiz). Fahrzeugbeschriftung und Folierung, Schaufenster- und Glasbeschriftung, Textildruck, Printmedien, Schilder, Grafikdesign und Websites: alles aus einer Hand, von der Idee bis zur Montage, für Kundschaft in der ganzen Schweiz.

## Kontakt
- Adresse: {C["street"]}, {C["zip"]} {C["city"]}, Schweiz
- E-Mail: {C["email"]}{phone}
- Öffnungszeiten: {hours}
- Instagram: {C["instagram"]}
- Offerte anfragen: {C["domain"]}/offerte/

## Leistungen
{svc}

## Seiten
- [Projekte]({C["domain"]}/projekte/)
- [Über uns]({C["domain"]}/ueber-uns/)
- [Kontakt]({C["domain"]}/kontakt/)
- [Impressum]({C["domain"]}/impressum/)

## Volltext
- [llms-full.txt]({C["domain"]}/llms-full.txt): alle Leistungen mit Angebot und FAQ
""")
    full = [f"# {C['name']}: Leistungen im Detail\n\n{C['name']} ({C['legal_name']}), {C['street']}, {C['zip']} {C['city']}, Schweiz. "
            f"Telefon {C['phone']}, E-Mail {C['email']}. Öffnungszeiten: {hours}. Stand: {UPDATED}.\n"]
    for s in SERVICES:
        sec = [f"## {s['title']}: {s.get('seo_sub', s['sub'])}", f"URL: {C['domain']}/leistungen/{s['slug']}/", "", strip_tags(s["short"])]
        if s.get("custom"):
            W = WOWLAB
            sec += [""] + W["hero"] + [""] + W["idea"] + ["", "### Angebot"]
            sec += [f"- **{t}** ({tag}) {' '.join(txt)}" for t, tag, txt in W["offers"]]
            sec += ["", "### Ablauf"] + [f"{n}. {t}: {d}" for n, t, d in W["process"]]
        else:
            sec += [""] + s["intro"] + ["", "### Angebot"] + [f"- **{t}:** {d}" for t, d in s["offers"]]
            sec += ["", "### Warum WOW PRINT"] + [f"- **{t}:** {d}" for t, d in s["why"]]
        if s["faq"]:
            sec += ["", "### Häufige Fragen"] + [f"**{strip_tags(q)}**\n{strip_tags(a)}\n" for q, a in s["faq"]]
        full.append("\n".join(sec) + "\n")
    with open(os.path.join(OUT, "llms-full.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(full))


def layout(p, title, desc, body, current="", og_img="hero-car.jpg", canonical=None, noindex=False, ld=None):
    canonical_url = C["domain"] + "/" + (p.path if canonical is None else canonical)
    if not noindex:
        SITEMAP.append(canonical_url)
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in [business_ld()] + (ld or []))
    robots = '<meta name="robots" content="noindex,follow">' if noindex else ""
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
{ld_html}<script>document.documentElement.classList.add('js')</script>
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


DOT = '<span class="dot" aria-hidden="true"></span>'
_UML = re.compile(r"[ÄÖÜäöü]")
_HEAD = re.compile(r"(<(h1|h2)\b[^>]*>)(.*?)(</\2>)", re.S)


def round_dots(html):
    """Punkte in Überschriften rund wie im Logo (Archivo hat eckige Punkte)."""
    def fix_inner(inner):
        parts = re.split(r"(<[^>]+>)", inner)
        return "".join(x if x.startswith("<") else x.replace(".", DOT) for x in parts)
    def mark_uml(m):
        open_tag, inner = m.group(1), fix_inner(m.group(3))
        if not _UML.search(re.sub(r"<[^>]+>", "", inner)):
            return open_tag + inner + m.group(4)
        if 'class="line"' in inner:
            # nur die Zeile mit Umlaut bekommt mehr Luft nach oben
            inner = re.sub(r'<span class="line">(<span>(?:(?!<span class="line">).)*?[ÄÖÜäöü])',
                           r'<span class="line uml">\1', inner, flags=re.S)
        else:
            open_tag = (open_tag.replace('class="', 'class="uml ', 1) if 'class="' in open_tag
                        else open_tag[:-1] + ' class="uml">')
        return open_tag + inner + m.group(4)
    return _HEAD.sub(mark_uml, html)


def write(p, html):
    html = round_dots(html)
    path = os.path.join(OUT, p.path, "index.html") if not p.path.endswith(".html") else os.path.join(OUT, p.path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("  ✓", os.path.relpath(path, OUT))


def img(p, name, alt, extra=""):
    return f'<img src="{p.asset("img/" + name)}" alt="{escape(alt)}" loading="lazy" decoding="async" {extra}>'

GALLERY_EXTRA = {}


def gallery_steps(p, s):
    caps = ["Schritt 01", "Schritt 02", "Schritt 03", "Ergebnis"]
    out = "".join(
        f'<figure data-reveal>{img(p, f"{s["slug"]}-step{i}.jpg", f"{s["title"]} – {c}")}<figcaption>{c}</figcaption></figure>'
        for i, c in enumerate(caps, 1))
    for n in range(GALLERY_EXTRA.get(s["slug"], 0)):
        out += f'<figure data-reveal>{img(p, f"{s["slug"]}-extra{n + 1}.jpg", s["title"])}</figure>'
    return out

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
        <span class="go"><span>{s.get("go", "Mehr")}</span>{ARROW}</span>
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
    <h1 class="display">{lines("Wir machen", "Sie WOW.")}</h1>
    <div class="hero-bottom">
      <p class="lead">Fahrzeugbeschriftung, Werbetechnik, Textil, Print und Design aus Rorschach. Für Marken, die nicht wie alle anderen aussehen wollen.</p>
      <a class="scroll-cue" href="#services">Scrollen {ARROW_DOWN}</a>
    </div>
  </div>
</section>

{marquee([s["title"] for s in SERVICES])}

<section class="section" id="services">
  <div class="wrap services-layout">
    <div class="services-intro">
      <span class="eyebrow">Leistungen</span>
      <h2 class="display d-l" style="margin-top:18px" data-lines>{lines("Was wir", "machen.")}</h2>
      <p class="lead" data-reveal>Acht Disziplinen, ein Ziel: Ihre Marke sichtbar machen. Von der ersten Skizze bis zur fertigen Montage, alles aus einer Hand.</p>
      <a class="btn" href="{p.url("leistungen/")}" data-magnetic=".3" data-reveal>Alle Leistungen {ARROW}</a>
    </div>
    <div class="services-grid">{service_cards(p)}
    </div>
  </div>
</section>

<section class="statement section">
  <div class="wrap">
    <span class="eyebrow" style="color:var(--pink)">Anders aus Prinzip</span>
    <p class="statement-text">Wir sind keine 0815-Agentur. Wir sind <em>kreative Artisten</em> mit einem Gespür für Ästhetik, einem Auge fürs Detail und der Leidenschaft, aus jeder Marke <em>etwas Einzigartiges</em> zu machen.</p>
    <div class="statement-foot">
      <p class="statement-claim"><span class="dots" aria-hidden="true"><i></i><i></i><i></i></span><span>Werbung können viele<span class="dot"></span> Kunst nicht<span class="dot"></span><span class="dot"></span><span class="dot"></span></span></p>
      <a class="btn btn--light" href="{p.url("ueber-uns/")}" data-magnetic=".3">Über uns {ARROW}</a>
    </div>
  </div>
</section>

<section class="projects" id="work">
  <div class="projects-pin">
    <div class="wrap section-head">
      <span class="eyebrow">Ausgewählte Arbeiten</span>
      <h2 class="display d-xl" data-lines>{lines("Projekte.")}</h2>
      <a class="btn" href="{p.url("projekte/")}" data-magnetic=".3">Alle Projekte {ARROW}</a>
    </div>
    <div class="projects-track">{projects}
      <div class="projects-end">
        <h3 class="display d-m">Ihr Projekt<br>ist das nächste.</h3>
        <a class="btn btn--solid" href="{p.url("offerte/")}" data-magnetic=".3">Projekt starten {ARROW}</a>
      </div>
    </div>
  </div>
</section>

<section class="process section">
  <div class="wrap process-grid">
    <div>
      <span class="eyebrow">Unser Ablauf</span>
      <h2 class="display d-l" style="margin-top:18px" data-lines>{lines("Einfach.")}</h2>
    </div>
    <div class="process-steps"><div class="process-line"><i></i></div>{steps}
    </div>
  </div>
</section>

{marquee(["Wir machen Sie WOW", "Rorschach", "Schweiz", "Seit Tag eins: WOW"], pink=True, reverse=True)}
{cta_band(p)}
"""
    write(p, layout(p, "WOW PRINT – Wir machen Sie WOW. | Werbetechnik Rorschach",
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
{page_hero(p, "Leistungen", ["Was wir", "machen."], "Acht Disziplinen unter einem Dach. Wir gestalten, produzieren und montieren und machen Ihre Marke überall sichtbar, wo man sie sehen soll.", [("", "Start"), (None, "Leistungen")])}
<section class="section">
  <div class="wrap">
    <div class="svc-list">{rows}
    </div>
  </div>
  <div class="hover-img" aria-hidden="true"><img src="" alt=""></div>
</section>
{marquee(["Design", "Druck", "Plot", "Produktion", "Montage", "Wow"])}
<section class="process section">
  <div class="wrap process-grid">
    <div><span class="eyebrow">Unser Ablauf</span><h2 class="display d-l" style="margin-top:18px" data-lines>{lines("Einfach.")}</h2></div>
    <div class="process-steps"><div class="process-line"><i></i></div>{"".join(f'<div class="step{" step--wow" if n == "04" else ""}"><span class="num">{n}</span><h3 class="display">{t}</h3><p>{d}</p></div>' for n, t, d in PROCESS)}</div>
  </div>
</section>
{cta_band(p)}
"""
    write(p, layout(p, "Leistungen – WOW PRINT Rorschach", "Fahrzeugbeschriftung, Schaufenster, Textildruck, Print, Schilder, Design und Websites von WOW PRINT in Rorschach.", body, current="leistungen/"))


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
    <div class="section-head"><span class="eyebrow">Vorher / Nachher</span><h2 class="display d-l" data-lines>{lines("Gleiches Auto.", "Neuer Auftritt.")}</h2><p class="muted">Ziehen Sie den Regler und sehen Sie, was eine Folierung aus einem Fahrzeug macht.</p></div>
    <div class="ba" data-reveal>
      {img(p, "vehicle-after.jpg", "Fahrzeug nach der Folierung")}
      <img class="ba-before" src="{p.asset("img/vehicle-before.jpg")}" alt="Fahrzeug vor der Folierung" loading="lazy">
      <span class="ba-label ba-label--l">Vorher</span><span class="ba-label ba-label--r">Nachher</span>
      <div class="ba-handle"></div>
      <input type="range" min="0" max="100" value="50" aria-label="Vorher-Nachher-Vergleich">
    </div>
  </div>
</section>"""
    body = f"""
{page_hero(p, s["sub"], [s["title"] + "."], s["short"], [("", "Start"), ("leistungen/", "Leistungen"), (None, s["title"])], bg_num=s["num"])}
<div class="media-band">{img(p, s["img"], s["title"] + " – " + s["sub"], 'data-parallax=".25"')}</div>
<section class="section">
  <div class="wrap split">
    <div><span class="eyebrow">{s["num"]} — {s["sub"]}</span><h2 class="display d-m" style="margin-top:18px" data-lines>{lines("Nicht zu", "übersehen.")}</h2></div>
    <div class="prose" data-reveal>{"".join(f"<p>{t}</p>" for t in s["intro"])}
      <a class="btn btn--solid" href="{p.url("offerte/")}?leistung={s["key"]}" data-magnetic=".3" style="margin-top:14px">Offerte für {s["title"]} {ARROW}</a>
    </div>
  </div>
</section>
<section class="section section--tight" style="padding-top:0">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Angebot</span><h2 class="display d-l" data-lines>{lines("Unser Angebot.")}</h2></div>
    <ul class="offer-list">{offers}</ul>
  </div>
</section>
{ba}
<section class="section bg-ink on-dark">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow" style="color:var(--pink)">Warum WOW</span><h2 class="display d-l" data-lines>{lines("Warum wir.")}</h2></div>
    <div class="cards-3">{why}</div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Galerie</span><h2 class="display d-l" data-lines>{lines("Im Einsatz.")}</h2></div>
    <div class="gallery gallery--steps">{gallery_steps(p, s)}</div>
  </div>
</section>
<section class="section bg-paper2">
  <div class="wrap split">
    <div><span class="eyebrow">FAQ</span><h2 class="display d-l" style="margin-top:18px" data-lines>{lines("Gute", "Fragen.")}</h2></div>
    <div class="faq">{faq}</div>
  </div>
</section>
<p class="wrap stand muted">Stand: {UPDATED_TEXT}</p>
<div class="next-wrap"><a class="next-link" href="{p.url("leistungen/" + nxt["slug"] + "/")}" data-cursor="Weiter"><div class="wrap"><span class="eyebrow">Nächste Leistung · {nxt["num"]}</span><span class="display d-xl" style="font-size:clamp(30px, {min(8.4, 80 / (len(nxt["title"]) * 0.82 + 0.9)):.2f}vw, 148px)">{nxt["title"]} {ARROW_DIAG}</span></div></a></div>
{cta_band(p)}
"""
    write(p, layout(p, f"{s['title']} – {s['sub']} | WOW PRINT Rorschach", s["short"], body, current="leistungen/", og_img=s["img"], ld=service_ld(s)))


def wowlab_page(i, s):
    p = Page(f"leistungen/{s['slug']}/")
    W = WOWLAB
    nxt = SERVICES[(i + 1) % len(SERVICES)]
    ask = f'{p.url("offerte/")}?leistung={s["key"]}'
    offers = "".join(f"""<li data-reveal><span class="num">{str(k + 1).zfill(2)}</span><div><h3 class="display">{t}</h3><p class="lab-tag">{tag}</p></div><div class="lab-text">{"".join(f"<p>{x}</p>" for x in txt)}</div></li>"""
                     for k, (t, tag, txt) in enumerate(W["offers"]))
    steps = "".join(f'<div class="step{" step--wow" if n == "05" else ""}"><span class="num">{n}</span><h3 class="display">{t}</h3><p>{d}</p></div>' for n, t, d in W["process"])
    gal = "".join(f'<figure class="lab-g{k + 1}" data-reveal>{img(p, f, c + " (Konzeptvisualisierung)")}<figcaption>{c}</figcaption></figure>'
                  for k, (f, c) in enumerate(W["gallery"]))
    related = [x for x in SERVICES if x["key"] in ("windows", "signage", "design")]
    rel = "".join(f'<a class="lab-rel" href="{p.url("leistungen/" + x["slug"] + "/")}"><span class="num">{x["num"]}</span><b class="display">{x["title"]}</b><small>{x["sub"]}</small>{ARROW}</a>' for x in related)
    body = f"""
{page_hero(p, "WOW PRINT presents", ["WOW LAB."], "Das kreative Design- und Entwicklungsstudio von WOW PRINT. Räume. Objekte. Erlebnisse.", [("", "Start"), ("leistungen/", "Leistungen"), (None, "WOW LAB")], bg_num=s["num"])}
<div class="media-band">{img(p, s["img"], "WOW LAB – kreativ eingerichteter Laden (Konzeptvisualisierung)", 'data-parallax=".25"')}</div>
<section class="section">
  <div class="wrap split">
    <div><span class="eyebrow">08 — WOW LAB</span><h2 class="display d-m" style="margin-top:18px" data-lines>{lines("Gewöhnlich", "kann jeder.")}</h2></div>
    <div class="prose" data-reveal>{"".join(f"<p>{t}</p>" for t in W["hero"])}
      <p class="lab-claim">Wir machen aus Räumen Erlebnisse.</p>
      <a class="btn btn--solid" href="{ask}" data-magnetic=".3" style="margin-top:6px">Projekt anfragen {ARROW}</a>
    </div>
  </div>
</section>
<section class="section section--tight" style="padding-top:0">
  <div class="wrap split">
    <div><span class="eyebrow">Die Idee</span></div>
    <div class="prose lab-idea" data-reveal>{"".join(f"<p>{t}</p>" for t in W["idea"])}<p class="lab-claim">WOW LAB – wir gestalten, was in Erinnerung bleibt.</p></div>
  </div>
</section>
{marquee(["Interior", "Retail", "Möbel", "Licht", "Engineering", "Wow"])}
<section class="section">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Angebot</span><h2 class="display d-l" data-lines>{lines("Was wir", "machen.")}</h2></div>
    <ul class="offer-list lab-offers">{offers}</ul>
  </div>
</section>
<section class="section bg-ink on-dark">
  <div class="wrap split">
    <div><span class="eyebrow" style="color:var(--pink)">Unsere Stärke</span><h2 class="display d-l lab-dme" style="margin-top:18px" data-lines>{lines("Design", "meets", "Engineering.")}</h2></div>
    <div class="prose" data-reveal>{"".join(f"<p>{t}</p>" for t in W["strength"])}<p class="lab-claim lab-claim--pink">We don’t think standard.</p></div>
  </div>
</section>
<section class="process section">
  <div class="wrap process-grid">
    <div><span class="eyebrow">Ablauf</span><h2 class="display d-l" style="margin-top:18px" data-lines>{lines("Von der Idee", "zum WOW.")}</h2></div>
    <div class="process-steps process-steps--5"><div class="process-line"><i></i></div>{steps}</div>
  </div>
</section>
<section class="section bg-paper2">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Möglichkeiten</span><h2 class="display d-l" data-lines>{lines("Was möglich", "ist.")}</h2><p class="muted">Konzeptvisualisierungen: So könnten WOW-LAB-Projekte aussehen. Es handelt sich nicht um realisierte Referenzprojekte.</p></div>
    <div class="gallery lab-gallery">{gal}</div>
  </div>
</section>
<section class="section lab-brand">
  <div class="wrap">
    <span class="eyebrow">WOW LAB</span>
    <h2 class="display d-xl" style="margin-top:18px" data-lines>{lines("Beyond", "ordinary.")}</h2>
    <div class="lab-brand-text" data-reveal>
      <p>Wir gestalten Räume, Möbel und Objekte, die Menschen begeistern. Mit Kreativität, Leidenschaft und technischem Know-how verwandeln wir gewöhnliche Ideen in aussergewöhnliche Erlebnisse.</p>
      <p class="lab-claim">Not just design. A WOW experience.</p>
      <small>WOW LAB – a creative division of WOW PRINT.</small>
    </div>
  </div>
</section>
<section class="section section--tight">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Passt dazu</span><h2 class="display d-m" data-lines>{lines("Alles aus", "einer Hand.")}</h2></div>
    <div class="lab-rels">{rel}</div>
  </div>
</section>
<p class="wrap stand muted">Stand: {UPDATED_TEXT}</p>
<div class="next-wrap"><a class="next-link" href="{p.url("leistungen/" + nxt["slug"] + "/")}" data-cursor="Weiter"><div class="wrap"><span class="eyebrow">Nächste Leistung · {nxt["num"]}</span><span class="display d-xl" style="font-size:clamp(30px, {min(8.4, 80 / (len(nxt["title"]) * 0.82 + 0.9)):.2f}vw, 148px)">{nxt["title"]} {ARROW_DIAG}</span></div></a></div>
<section class="cta-band section lab-cta">
  <div class="wrap">
    <h2 class="cta-title display" data-lines>{lines("Eine Idee?")} <span class="line"><span><span class="fill"><span class="fill-base">{fill_text("Wir machen sie WOW.")}</span><span class="fill-top" aria-hidden="true">{fill_text("Wir machen sie WOW.")}</span></span></span></span></h2>
    <div class="cta-side">
      <p>Ein Laden, der anders sein soll. Ein Möbelstück, das es nicht zu kaufen gibt. Ein Raum, der Menschen begeistert. Oder einfach eine verrückte Idee. Erzählen Sie uns davon.</p>
      <a class="btn btn--solid" href="{ask}" data-magnetic=".3">Projekt anfragen {ARROW}</a>
    </div>
  </div>
</section>
"""
    write(p, layout(p, "WOW LAB | Interior Design, Ladenbau & individuelle Möbel | WOW PRINT",
                    "WOW LAB by WOW PRINT – kreatives Interior Design, aussergewöhnlicher Ladenbau, individuelle Möbel und Sonderanfertigungen. Design trifft über 20 Jahre Konstruktionserfahrung.",
                    body, current="leistungen/", og_img=s["img"], ld=service_ld(s)))


def projects_page():
    p = Page("projekte/")
    chips = '<button class="chip is-active" data-filter="all" aria-pressed="true">Alle</button>' + "".join(
        f'<button class="chip" data-filter="{s["key"]}" aria-pressed="false">{s["title"]}</button>' for s in SERVICES if not s.get("custom"))
    cards = "".join(f"""
      <article class="work-card" data-cat="{pr["cat"]}" data-cursor="WOW" data-reveal>
        <div class="media">{img(p, pr["img"], pr["title"])}</div>
        <div class="info"><h3 class="display">{pr["title"]}</h3><small>{pr["meta"]} · {pr["label"]}</small></div>
      </article>""" for pr in PROJECTS)
    body = f"""
{page_hero(p, "Ausgewählte Arbeiten", ["Projekte."], "Eine Auswahl unserer Arbeiten: Fahrzeuge, Schaufenster, Textilien, Print und mehr. Jedes Projekt mit dem Ziel, aufzufallen.", [("", "Start"), (None, "Projekte")])}
<section class="section">
  <div class="wrap">
    <div class="filters" role="group" aria-label="Projekte filtern">{chips}</div>
    <div class="work-grid">{cards}
    </div>
  </div>
</section>
{cta_band(p, ("Ihr Projekt", "ist das nächste."))}
"""
    write(p, layout(p, "Projekte – WOW PRINT Rorschach", "Ausgewählte Projekte von WOW PRINT: Fahrzeugfolierungen, Schaufenster, Textil, Print und Design.", body, current="projekte/"))


def about_page():
    p = Page("ueber-uns/")
    body = f"""
{page_hero(p, "Über uns", ["Wir sind", "anders."], "Kein Standard, kein Copy-Paste. WOW PRINT ist für alle, die mit ihrem Auftritt auffallen wollen.", [("", "Start"), (None, "Über uns")])}
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
    <span class="eyebrow">Design mit Charakter.</span>
    <h2 class="display d-xl" data-lines>{lines("Die Kunst", "des Designs.")}</h2>
    <p>Gespür für Ästhetik, Proportion und Stil. Wir glauben, dass gutes Design Emotionen auslöst und dass auch Werbetechnik schön sein darf.</p>
  </div>
  <div class="ch on-dark">
    <span class="eyebrow" style="color:var(--pink)">Schweizer Qualität</span>
    <h2 class="display d-xl" data-lines>{lines("Schweizer", "Präzision.")}</h2>
    <p class="muted">Sauber geplant, exakt produziert, pünktlich montiert. Auf uns ist Verlass, bis in die letzte Folienkante.</p>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Werte</span><h2 class="display d-l" data-lines>{lines("Was uns antreibt.")}</h2></div>
    <div class="values">
      <div class="value" data-reveal><span class="num">01</span><h3 class="display">Mutig.</h3><p>Wir trauen uns, aufzufallen, und bringen Ideen ein, auf die andere nicht kommen.</p></div>
      <div class="value" data-reveal><span class="num">02</span><h3 class="display">Präzise.</h3><p>Hinter jedem WOW steckt Handwerk: genaue Planung, gute Materialien, saubere Arbeit.</p></div>
      <div class="value" data-reveal><span class="num">03</span><h3 class="display">Persönlich.</h3><p>Ein Ansprechpartner, kurze Wege, ehrliche Beratung. Wir nehmen uns Zeit für Ihr Projekt.</p></div>
    </div>
  </div>
</section>
{marquee(["Design", "Druck", "Plot", "Produktion", "Montage", "Alles aus einer Hand"], pink=True)}
<section class="section bg-ink on-dark">
  <div class="wrap split">
    <div><span class="eyebrow" style="color:var(--pink)">Rorschach · Bodensee</span></div>
    <div>
      <p class="big-quote" data-reveal>Am Bodensee zu Hause, für Kundinnen und Kunden in der ganzen Schweiz unterwegs.</p>
      <p class="muted" style="margin-top:26px" data-reveal>{ADDRESS}</p>
      <a class="btn btn--light" style="margin-top:22px" href="{C["maps"]}" target="_blank" rel="noopener" data-magnetic=".3" data-reveal>Route planen {ARROW}</a>
    </div>
  </div>
</section>
{cta_band(p)}
"""
    write(p, layout(p, "Über uns – WOW PRINT Rorschach", "WOW PRINT: Italienisches Designgefühl trifft Schweizer Präzision. Werbetechnik und Design aus Rorschach.", body, current="ueber-uns/"))


def contact_page():
    p = Page("kontakt/")
    body = f"""
{page_hero(p, "Kontakt", ["Reden wir."], "Sie haben eine Idee, ein Projekt oder einfach eine Frage? Schreiben Sie uns, rufen Sie an oder kommen Sie vorbei.", [("", "Start"), (None, "Kontakt")])}
<section class="section">
  <div class="wrap contact-layout">
    <div class="contact-info">
      <div><h4>TELEFON</h4><a class="big-link link-u" href="tel:{C["phone_href"]}">{C["phone"]}</a></div>
      <div><h4>E-MAIL</h4><a class="big-link link-u" href="mailto:{C["email"]}">{C["email"]}</a></div>
      <div><h4>STUDIO</h4><p>{C["name"]}<br>{C["street"]}<br>{C["zip"]} {C["city"]}</p><p style="margin-top:8px"><a class="link-u" href="{C["maps"]}" target="_blank" rel="noopener">Route planen ↗</a></p></div>
      <div><h4>ÖFFNUNGSZEITEN</h4>{hours_html()}</div>
      <div><h4>SOCIAL</h4>{socials()}</div>
    </div>
    <div>
      <h2 class="display d-m" data-lines>{lines("Schreiben Sie uns.")}</h2>
      <p class="muted" style="margin:14px 0 36px">Für eine konkrete Offerte mit Dateien nutzen Sie am besten unser <a class="link-u" style="color:var(--ink)" href="{p.url("offerte/")}">Offertenformular</a>.</p>
      <form name="kontakt" method="POST" action="{p.form_action("danke/")}" data-netlify="true" netlify-honeypot="bot-field">
        <input type="hidden" name="form-name" value="kontakt">
        <p class="hp" aria-hidden="true"><input name="bot-field" tabindex="-1" autocomplete="off"></p>
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
    write(p, layout(p, "Kontakt – WOW PRINT Rorschach", f"Kontakt zu WOW PRINT, {ADDRESS}. Öffnungszeiten Mo–Fr 09:00–12:00 und 14:00–17:00.", body, current="kontakt/"))


QUOTE_ICONS = {
    "beschriftung": '<path d="M3 15.5V12l2.2-4.6A2 2 0 0 1 7 6.3h7.6a2 2 0 0 1 1.6.8L19.5 11l1.3.5c.7.3 1.2 1 1.2 1.8v2.2h-2"/><path d="M3 15.5h2.2M10.8 15.5h4.4"/><circle cx="8" cy="16" r="2.2"/><circle cx="18" cy="16" r="2.2"/><path d="M6 11h13.3"/>',
    "schaufenster": '<path d="M3 21V10M21 21V10M2 21h20"/><path d="M2.5 6.5 4 3h16l1.5 3.5c0 1.6-1.3 2.8-2.8 2.8s-2.8-1.2-2.8-2.8c0 1.6-1.3 2.8-2.9 2.8S10 8.1 10 6.5c0 1.6-1.3 2.8-2.8 2.8s-2.9-1.2-2.9-2.8"/><rect x="6" y="13" width="7" height="5"/><path d="M16 21v-8h3v8"/>',
    "textildruck": '<path d="M8.5 3 3 6l2 4 2-.8V21h10V9.2l2 .8 2-4-5.5-3c-.5 1.5-1.9 2.5-3.5 2.5S9 4.5 8.5 3Z"/>',
    "werbetafeln": '<rect x="3" y="4" width="18" height="10" rx="1"/><path d="M7 14v7M17 14v7M7 8h7M7 11h10"/>',
    "print": '<path d="M7 8V3h10v5"/><rect x="3" y="8" width="18" height="9" rx="1.5"/><path d="M7 14h10v7H7z"/><circle cx="17.5" cy="11" r=".6" fill="currentColor"/>',
    "design": '<path d="m12 2 6 8-6 12L6 10Z"/><circle cx="12" cy="12" r="1.6"/><path d="M12 2v8.4"/>',
    "webdesign": '<rect x="2.5" y="4" width="19" height="15" rx="1.5"/><path d="M2.5 8h19"/><circle cx="5.5" cy="6" r=".5" fill="currentColor"/><circle cx="7.5" cy="6" r=".5" fill="currentColor"/><path d="m9 12-2.5 2.5L9 17M15 12l2.5 2.5L15 17"/>',
    "wowlab": '<path d="M12 2v4"/><path d="M6 13a6 6 0 0 1 12 0Z"/><path d="M10 13a2 2 0 0 0 4 0"/><path d="M5 21h14M8 21l1.5-5M16 21l-1.5-5"/>',
}

# Hauptleistung -> (Titel, Unteroptionen). "Ich brauche Beratung" kommt in jeder Gruppe automatisch dazu.
QUOTE_GROUPS = [
    ("beschriftung", "Beschriftung", "Beschriftung", ["Fahrzeugbeschriftung", "Schaufensterbeschriftung", "Fahrzeugfolierung", "Lochfolie fürs Fahrzeug"]),
    ("schaufenster", "Schaufenster", "Schaufenster", ["Schaufensterbeschriftung", "Milchglasfolie", "Sichtschutzfolie", "Sonnenschutzfolie", "Kleine Motive und Aufkleber"]),
    ("textildruck", "Textildruck", "Textildruck", ["T-Shirts", "Hoodies und Pullover", "Arbeitskleidung", "Jacken", "Vereinskleidung"]),
    ("werbetafeln", "Werbetafeln", "Werbetafeln", ["Firmenschild", "Bautafel", "Wegweiser", "Werbebanner", "Leuchtschild"]),
    ("print", "Print", "Print", ["Visitenkarten", "Flyer", "Aufkleber und Etiketten", "Plakate", "Verpackungen"]),
    ("design", "Design", "Design", ["Logo", "Branding", "Drucksachen gestalten", "Fahrzeug- oder Schaufenstergestaltung"]),
    ("webdesign", "Webdesign", "Webdesign", ["Neue Website", "Bestehende Website überarbeiten", "Landingpage"]),
    ("wowlab", "WOW LAB", "WOW LAB – Ladenbau & Interieur", ["Laden umbauen oder neu gestalten", "Interieurdesign", "Möbel nach Mass", "Individuelle Beleuchtung", "Sonderanfertigung aus Holz, Metall oder Plexiglas", "Messestand"]),
]

# Zusatzfrage: (id, Frage, Antworten, ausgelöst durch Optionen oder Hauptleistung)
QUOTE_DETAILS = [
    ("fahrzeug", "Welches Fahrzeug?", ["PW", "Transporter", "LKW", "Anhänger", "Anderes"], {"opts": ["Fahrzeugbeschriftung", "Fahrzeugfolierung", "Lochfolie fürs Fahrzeug"]}),
    ("fenster", "Wie viele Fenster?", ["1 Fenster", "2–3 Fenster", "4 oder mehr", "Noch offen"], {"opts": ["Schaufensterbeschriftung"]}),
    ("stueck", "Wie viele Stück ungefähr?", ["1–10", "11–25", "26–50", "Über 50", "Noch offen"], {"main": "textildruck"}),
]


def quote_page():
    p = Page("offerte/")
    CHECK = '<svg class="tick" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5 10 17.5 19 7" fill="none" stroke="currentColor" stroke-width="2.6"/></svg>'

    tiles = "".join(f"""
          <label class="q-tile"><input type="checkbox" data-main="{k}" value="{t}"><span><i class="q-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{QUOTE_ICONS[k]}</svg></i><b>{t}</b>{CHECK}</span></label>"""
                    for k, t, _, _ in QUOTE_GROUPS)

    def pill(o, attrs=""):
        return f'<label class="q-pill"><input type="checkbox" value="{o}" data-opt="{o}"{attrs}><span>{o}</span></label>'

    def detail(did, q, answers, trig):
        t = f' data-opts="{"|".join(trig["opts"])}"' if "opts" in trig else f' data-main-trigger="{trig["main"]}"'
        btns = "".join(f'<label class="q-pill q-pill--sm"><input type="radio" name="q-{did}" value="{a}"><span>{a}</span></label>' for a in answers)
        return f'<div class="q-detail" data-detail="{did}" data-label="{ {"fahrzeug": "Fahrzeug", "fenster": "Anzahl", "stueck": "Stückzahl"}[did]}"{t} hidden><p class="q-detail-q">{q} <span class="opt">optional</span></p><div class="q-pills">{btns}</div></div>'

    details = {d[0]: detail(*d) for d in QUOTE_DETAILS}
    groups = ""
    for k, t, head, opts in QUOTE_GROUPS:
        here = "".join(details[d[0]] for d in QUOTE_DETAILS
                       if ("opts" in d[3] and any(o in opts for o in d[3]["opts"]) and d[0] != "fenster") or d[3].get("main") == k)
        groups += f"""
          <div class="q-group" data-group="{k}" hidden>
            <h3 class="q-group-title"><i class="q-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{QUOTE_ICONS[k]}</svg></i>{head}</h3>
            <div class="q-pills">{"".join(pill(o) for o in opts)}{pill("Ich brauche Beratung", ' data-beratung')}</div>
            {here}<div class="q-slot"></div>
          </div>"""
    fenster = details["fenster"]

    def dz(n, label):
        return f"""<label class="dropzone"><input type="file" name="datei{n}" accept=".pdf,.ai,.eps,.svg,.png,.jpg,.jpeg,.heic,.zip"><span class="dz-ico">{UPLOAD}</span><span><strong>{label}</strong><small>Logo, Foto oder Skizze · PDF, AI, SVG, JPG, PNG oder ZIP</small></span></label>"""

    body = f"""
{page_hero(p, "Offerte", ["Machen wir", "es WOW."], "Stellen Sie Ihre Anfrage in wenigen Klicks zusammen. Ohne Beschreibung, Masse oder Fotos. Wir melden uns innert zwei Arbeitstagen.", [("", "Start"), (None, "Offerte")])}
<section class="section q-section">
  <div class="wrap" style="max-width:1160px">
    <form class="wizard qform" name="offerte" method="POST" action="{p.form_action("danke/")}" enctype="multipart/form-data" data-netlify="true" netlify-honeypot="bot-field" novalidate>
      <input type="hidden" name="form-name" value="offerte">
      <input type="hidden" name="leistung" value="">
      <textarea name="auswahl" hidden></textarea>
      <p class="hp" aria-hidden="true"><input name="bot-field" tabindex="-1" autocomplete="off"></p>
      <ol class="wizard-progress wizard-progress--2" aria-hidden="true"><li><span>01 Auswahl</span></li><li><span>02 Kontakt</span></li></ol>

      <fieldset data-require-main>
        <legend><span class="eyebrow">Schritt 1 von 2</span><h2 class="display d-m" style="margin-top:14px">Was möchten Sie umsetzen?</h2></legend>
        <p class="q-hint">Mehrfachauswahl möglich.</p>
        <div class="q-tiles">{tiles}
        </div>
        <div class="q-subs" aria-live="polite">
          <p class="q-subs-head" hidden><span class="eyebrow">Was genau brauchen Sie?</span><small>Alles optional. Sie können auch direkt weiter.</small></p>
          {groups}
          <div class="q-park" hidden>{fenster}</div>
        </div>
      </fieldset>

      <fieldset>
        <legend><span class="eyebrow">Schritt 2 von 2</span><h2 class="display d-m" style="margin-top:14px">Fast geschafft.</h2></legend>
        <div class="q-summary">
          <div class="q-summary-head"><span class="eyebrow">Ihre Auswahl</span><button type="button" class="q-edit link-u">Ändern</button></div>
          <ul class="q-summary-list"></ul>
        </div>
        <div class="form-grid">
          <div class="field"><label for="o-name">Vorname & Name</label><input id="o-name" name="name" autocomplete="name" required></div>
          <div class="field"><label for="o-mail">E-Mail</label><input id="o-mail" type="email" name="email" autocomplete="email" required></div>
          <div class="field"><label for="o-tel">Telefon <span class="opt">(optional)</span></label><input id="o-tel" type="tel" name="telefon" autocomplete="tel"></div>
          <div class="field"><label for="o-firma">Firma <span class="opt">(optional)</span></label><input id="o-firma" name="firma" autocomplete="organization"></div>
          <div class="field full"><span class="label">Dateien <span class="opt">(optional, max. 8 MB)</span></span><div class="uploads uploads--2" style="margin-top:6px">{dz(1, "Datei hochladen")}{dz(2, "Weitere Datei")}</div></div>
          <div class="field full"><label for="o-mehr">Möchten Sie noch etwas ergänzen? <span class="opt">(optional)</span></label><textarea id="o-mehr" name="ergaenzung" rows="3"></textarea></div>
          <p class="full q-legal">Mit dem Absenden akzeptieren Sie unsere <a class="link-u" href="{p.url("datenschutz/")}">Datenschutzerklärung</a> und <a class="link-u" href="{p.url("agb/")}">AGB</a>. Ihre Angaben verwenden wir nur für die Offerte.</p>
        </div>
      </fieldset>

      <p class="wizard-error" role="alert"></p>
      <div class="wizard-nav q-nav">
        <button type="button" class="back" hidden>← Zurück</button>
        <span class="q-count"></span>
        <button type="button" class="btn btn--solid next" data-magnetic=".3">Weiter {ARROW}</button>
        <button type="submit" class="btn btn--solid submit" hidden data-magnetic=".3">Offerte anfragen {ARROW}</button>
      </div>
    </form>
  </div>
</section>
"""
    write(p, layout(p, "Offerte anfragen – WOW PRINT", "Unverbindliche Offerte in wenigen Klicks: Beschriftung, Schaufenster, Textildruck, Werbetafeln, Print, Design, Webdesign oder WOW LAB.", body))


def thanks_page():
    p = Page("danke/")
    body = f"""
<section class="center-stage">
  <div class="hero-bgword" aria-hidden="true">WOW</div>
  <div style="position:relative">
    <span class="eyebrow">Nachricht erhalten</span>
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
    <span class="eyebrow">Fehler 404</span>
    <h1 class="display d-xxl" style="margin-top:20px">{lines("Hoppla.")}</h1>
    <p>Diese Seite ist leider nicht sichtbar. Ausnahmsweise. Alles andere finden Sie hier:</p>
    <a class="btn btn--solid" href="{p.url("")}" data-magnetic=".3">Zur Startseite {ARROW}</a>
  </div>
</section>"""
    write(p, layout(p, "Seite nicht gefunden – WOW PRINT", "Diese Seite existiert nicht.", body, noindex=True, canonical="404"))


def legal_page(slug, eyebrow, title, desc, inner):
    p = Page(slug + "/")
    body = f"""
{page_hero(p, eyebrow, [title], "", [("", "Start"), (None, eyebrow)])}
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
        if s.get("custom"):
            wowlab_page(i, s)
        else:
            service_page(i, s)
    projects_page()
    about_page()
    contact_page()
    quote_page()
    thanks_page()
    not_found()
    legal_page("impressum", "Impressum", "Impressum.", "Impressum von WOW PRINT, Rorschach.", impressum)
    legal_page("datenschutz", "Datenschutz", "Datenschutz.", "Datenschutzerklärung von WOW PRINT nach Schweizer Datenschutzgesetz (DSG).", datenschutz)
    legal_page("agb", "AGB", "AGB.", "Allgemeine Geschäftsbedingungen von WOW PRINT.", agb)
    seo_files()
    print("Fertig.")


if __name__ == "__main__":
    main()
