# -*- coding: utf-8 -*-
"""Baut den minimalistischen Entwurf: python3 entwurf-minimal/build.py"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
import content as c  # noqa: E402

LIVE = "https://wow-print.ch"

ICONS = {
    "vehicle": '<path d="M6 31v-6l4-9h22l7 9h3a2 2 0 0 1 2 2v4h-4"/><path d="M14 31h16"/><circle cx="11" cy="32" r="3.5"/><circle cx="34" cy="32" r="3.5"/><path d="M11 25h26M20 16v9"/>',
    "windows": '<path d="M6 40V12h36v28"/><path d="M4 40h40"/><path d="M6 12l3-5h30l3 5"/><path d="M11 18h26v16H11z"/><path d="M24 18v16"/>',
    "textile": '<path d="M17 7l-9 5 3 8 4-2v22h18V18l4 2 3-8-9-5c-1 3-3.5 5-7 5s-6-2-7-5z"/>',
    "print": '<path d="M14 18V6h20v12"/><path d="M10 18h28a3 3 0 0 1 3 3v12h-7"/><path d="M14 33H7V21a3 3 0 0 1 3-3"/><path d="M14 28h20v14H14z"/><path d="M18 33h12M18 37h8"/>',
    "signage": '<path d="M8 10h32v16H8z"/><path d="M24 26v16M17 42h14"/><path d="M14 16h12M14 20h20"/>',
    "design": '<path d="M24 6l10 18-10 18-10-18z"/><circle cx="24" cy="24" r="3"/><path d="M24 6v15"/>',
    "digital": '<path d="M6 9h36v24H6z"/><path d="M18 41h12M24 33v8"/><path d="M6 28h36"/>',
    "wowlab": '<path d="M14 6h20l-3 12H17z"/><path d="M24 18v18"/><path d="M16 42h16"/><path d="M24 36l-6 6M24 36l6 6"/>',
}

STEP_TEXT = {s[0]: s for s in c.PROCESS}

PROJECTS = [
    ("project-vehicle.jpg", "Fahrzeuge | Design", "Fahrzeugbranding",
     "Ein Kleinwagen wird zur rollenden Visitenkarte: Layout auf die Karosserie geplant, gedruckt, geplottet und sauber bis in die Kanten verklebt.",
     "fahrzeugbeschriftung"),
    ("project-windows.jpg", "Schaufenster | Folien", "Schaufenstergrafik",
     "Grosse Buchstaben, viel Glas, klare Wirkung. Eine Schaufensterbeschriftung, die Passanten stehen bleiben lässt.",
     "schaufenster"),
    ("project-signage.jpg", "Schilder | Licht", "Ladenbeschilderung",
     "Leuchtende Acrylschrift für den Eingangsbereich. Damit man Sie findet und sich an Sie erinnert.",
     "signaletik"),
    ("project-textile.jpg", "Textil | Druck", "Teamwear",
     "Shirts und Hoodies, die nicht nach Werbeshirt aussehen, sondern nach Marke. Bedruckt oder bestickt.",
     "textildruck"),
]


def logo():
    svg = open(os.path.join(HERE, "..", "tools", "logo.svg"), encoding="utf-8").read()
    svg = re.sub(r"<\?xml[^>]*>\s*", "", svg)
    return svg.replace("<svg ", '<svg class="logo" role="img" aria-label="WOW PRINT" ', 1)


def cards():
    out = []
    for i, s in enumerate(c.SERVICES):
        short = s["short"]
        if s["key"] == "wowlab":
            short = "Interior Design und Möbelbau. Räume und Objekte, die in Erinnerung bleiben."
        out.append(
            f'        <a class="card rv" data-d="{i % 4}" href="{LIVE}/leistungen/{s["slug"]}/">'
            f'<svg viewBox="0 0 48 48" aria-hidden="true">{ICONS[s["key"]]}</svg>'
            f'<h3 class="caps">{s["title"]}</h3>'
            f'<div class="more"><p>{short}</p><span>Mehr erfahren</span></div></a>'
        )
    return "\n".join(out)


def projects():
    out = []
    for i, (img, tag, title, text, slug) in enumerate(PROJECTS):
        flip = " flip" if i % 2 else ""
        out.append(
            f'      <article class="proj{flip}">'
            f'<div class="pimg rv"><img loading="lazy" src="assets/img/{img}" alt="{title} von WOW PRINT"></div>'
            f'<div class="ptxt rv" data-d="1"><p class="tag">{tag}</p><h3 class="caps">{title}</h3><p>{text}</p>'
            f'<a class="btn btn-soft" href="{LIVE}/leistungen/{slug}/">Details</a></div></article>'
        )
    return "\n".join(out)


def steps():
    return "\n".join(
        f'        <div class="step rv" data-d="{i}"><div class="ring">{n}</div><h3 class="caps">{t}</h3><p>{d}</p></div>'
        for i, (n, t, d) in enumerate(c.PROCESS)
    )


def links():
    return "\n".join(
        f'        <a href="{LIVE}/leistungen/{s["slug"]}/">{s["sub"] if s["key"] != "wowlab" else "WOW LAB · Interior"}</a>'
        for s in c.SERVICES
    )


src = open(os.path.join(HERE, "index.src.html"), encoding="utf-8").read()
html = (src.replace("{{LOGO}}", logo()).replace("{{CARDS}}", cards())
        .replace("{{PROJECTS}}", projects()).replace("{{STEPS}}", steps()).replace("{{LINKS}}", links()))
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(html)
print("ok", len(html))
