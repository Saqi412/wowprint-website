# -*- coding: utf-8 -*-
"""Inhalte der WOW PRINT Website. Texte hier ändern, dann `python3 tools/build.py` ausführen."""

COMPANY = {
    "name": "WOW PRINT",
    "street": "Löwengartenstrasse 8",
    "zip": "9400",
    "city": "Rorschach",
    "country": "Schweiz",
    # TODO: echte Kontaktdaten eintragen, sobald vorhanden
    "phone": "+41 00 000 00 00",
    "phone_href": "+41000000000",
    "email": "info@wowprint.ch",
    "instagram": "#",
    "facebook": "#",
    "domain": "https://www.wowprint.ch",
    "maps": "https://www.google.com/maps/search/?api=1&query=L%C3%B6wengartenstrasse+8%2C+9400+Rorschach",
}

HOURS = [("Mo – Fr", "09:00 – 12:00"), ("", "14:00 – 17:00"), ("Sa – So", "geschlossen")]

SERVICES = [
    {
        "slug": "fahrzeugbeschriftung", "key": "vehicle", "num": "01", "title": "Vehicle",
        "sub": "Fahrzeugbeschriftung & Folierung", "img": "service-vehicle.jpg",
        "short": "Vom Firmenauto bis zur ganzen Flotte: Beschriftung, Teil- und Vollfolierung, die man nicht übersieht.",
        "intro": [
            "Ihr Fahrzeug ist die Werbefläche, die jeden Tag unterwegs ist. Wir machen daraus einen Auftritt, der im Kopf bleibt: auf dem Parkplatz, im Stau und an der Ampel.",
            "Von der Idee über das Layout bis zur Montage passiert alles bei uns. Wir planen jede Linie auf die Karosserie, drucken und plotten selbst und verkleben sauber bis in die Kanten.",
        ],
        "offers": [
            ("Vollfolierung & Farbwechsel", "Neue Farbe, neuer Look, ohne neu zu lackieren. Matt, Glanz, Satin oder Spezialeffekt."),
            ("Teilfolierung", "Gezielte Akzente, die das Fahrzeug zum Hingucker machen, mit kleinerem Budget."),
            ("Fahrzeugbeschriftung", "Logo, Kontaktdaten und Botschaft, gut lesbar und perfekt platziert."),
            ("Flottenbeschriftung", "Ein einheitlicher Auftritt für alle Fahrzeuge, egal ob drei oder dreissig."),
            ("Lackschutzfolie", "Transparenter Schutz vor Steinschlag und Kratzern für Front, Schweller und Kanten."),
        ],
        "why": [
            ("Design, das auffällt", "Wir gestalten für die Strasse: grosse Formen, starke Kontraste, klare Botschaften."),
            ("Alles aus einer Hand", "Gestaltung, Druck, Plot und Montage. Ein Ansprechpartner von Anfang bis Ende."),
            ("Präzise verarbeitet", "Hochwertige Markenfolien und saubere Kanten, damit die Folierung lange schön bleibt."),
        ],
        "faq": [
            ("Wie lange dauert eine Vollfolierung?", "In der Regel zwei bis vier Arbeitstage, je nach Fahrzeug und Design. Den genauen Termin stimmen wir mit Ihnen ab."),
            ("Schadet die Folie dem Lack?", "Nein, auf intaktem Originallack schützt die Folie sogar. Bei Nachlackierungen prüfen wir den Untergrund vorher."),
            ("Kann die Folierung wieder entfernt werden?", "Ja. Hochwertige Folien lassen sich innerhalb der Lebensdauer rückstandsfrei entfernen."),
            ("Brauchen Sie ein fertiges Design?", "Nein. Wir entwickeln das Layout mit Ihnen, auf Wunsch auch das ganze Branding."),
        ],
        "before_after": True,
    },
    {
        "slug": "schaufenster", "key": "windows", "num": "02", "title": "Windows",
        "sub": "Schaufenster & Sichtschutz", "img": "service-windows.jpg",
        "short": "Schaufenster, die stoppen. Sichtschutz, der gut aussieht. Glasflächen, die für Sie arbeiten.",
        "intro": [
            "Ihr Schaufenster ist der erste Eindruck, noch bevor jemand Ihr Geschäft betritt. Wir machen Glasflächen zu Bühnen für Ihre Marke.",
            "Ob Ladenlokal, Büro oder Praxis: Wir verbinden Werbung, Sichtschutz und Atmosphäre und montieren alles direkt vor Ort.",
        ],
        "offers": [
            ("Schaufensterbeschriftung", "Logo, Öffnungszeiten, Angebote, im Schnitt- oder Digitaldruck."),
            ("Sichtschutz & Milchglas", "Diskretion für Büros, Praxen und Sitzungszimmer, gerne mit Muster oder Logo."),
            ("Lochfolien", "Von aussen volle Werbefläche, von innen freie Sicht nach draussen."),
            ("Kampagnen & Saisonales", "Wechselnde Gestaltungen für Aktionen, Feiertage und Events."),
        ],
        "why": [
            ("Stopper-Effekt", "Gestaltung, die Passanten stehen bleiben lässt und in den Laden zieht."),
            ("Montage vor Ort", "Wir kommen zu Ihnen und arbeiten sauber, schnell und mit möglichst wenig Unterbruch."),
            ("Flexibel", "Folien lassen sich ersetzen, wenn sich Angebot oder Kampagne ändern."),
        ],
        "faq": [
            ("Kann man die Folien wieder entfernen?", "Ja, die meisten Folien lassen sich rückstandsfrei entfernen und durch neue Motive ersetzen."),
            ("Arbeiten Sie auch ausserhalb der Öffnungszeiten?", "Nach Absprache montieren wir auch frühmorgens oder abends, damit Ihr Betrieb weiterläuft."),
            ("Was kostet eine Schaufensterbeschriftung?", "Das hängt von Fläche, Material und Aufwand ab. Schicken Sie uns Masse oder Fotos, dann erhalten Sie eine Offerte."),
        ],
    },
    {
        "slug": "textildruck", "key": "textile", "num": "03", "title": "Textile",
        "sub": "Textildruck & Veredelung", "img": "service-textile.jpg",
        "short": "Workwear, Teamwear und Merch, die man gerne trägt. Bedruckt oder bestickt.",
        "intro": [
            "Kleidung ist Branding, das man trägt. Wir machen Textilien, die Ihr Team stolz trägt und Ihre Kundschaft gerne mitnimmt.",
            "Vom einzelnen Hoodie bis zur Teamausstattung beraten wir Sie zu Textilien, Veredelung und Platzierung.",
        ],
        "offers": [
            ("Workwear", "Robuste Arbeitskleidung mit Ihrem Logo, gemacht für den Alltag."),
            ("Teamwear & Vereine", "Einheitliche Outfits für Teams, Events und Vereine."),
            ("Merchandise", "Hoodies, Shirts, Caps und Taschen für Ihre Marke oder Ihre Fans."),
            ("Druck & Stick", "Flex-, Flock- und Transferdruck oder edle Stickerei, je nach Wirkung und Material."),
        ],
        "why": [
            ("Tragbares Design", "Wir gestalten Motive, die nicht nach Werbeshirt aussehen, sondern nach Marke."),
            ("Kleine & grosse Mengen", "Ob Einzelstück oder Serie, Sie bekommen dieselbe Qualität."),
            ("Beratung zu Textilien", "Wir helfen bei Schnitt, Material und Veredelung, damit alles zusammenpasst."),
        ],
        "faq": [
            ("Gibt es eine Mindestmenge?", "Je nach Verfahren drucken wir schon ab einem Stück. Für grössere Mengen erhalten Sie bessere Konditionen."),
            ("Kann ich eigene Textilien bringen?", "Gerne nach Absprache. Wir prüfen vorher, ob Material und Verfahren zusammenpassen."),
            ("Wie lange dauert die Produktion?", "Meist ein bis zwei Wochen ab Freigabe, abhängig von Menge und Verfügbarkeit der Textilien."),
        ],
    },
    {
        "slug": "print", "key": "print", "num": "04", "title": "Print",
        "sub": "Sticker · Folien · Printmedien", "img": "service-print.jpg",
        "short": "Sticker, Etiketten, Flyer, Plakate und Folien. Gedruckt, geplottet, geschnitten.",
        "intro": [
            "Print ist nicht tot, Print muss nur gut sein. Wir drucken Medien, die man anfasst, aufhebt und weitergibt.",
            "Vom Sticker in Sonderform bis zum Grossformat-Plakat produzieren wir schnell und in Top-Qualität.",
        ],
        "offers": [
            ("Sticker & Etiketten", "In jeder Form und Grösse, für Produkte, Verpackungen und Giveaways."),
            ("Flyer, Karten & Broschüren", "Geschäftsdrucksachen, die Ihre Marke konsequent weitertragen."),
            ("Plakate & Grossformat", "Von A3 bis zur Bauwand, in kräftigen Farben."),
            ("Folienplot", "Geschnittene Schriften und Logos für Wände, Glas und Fahrzeuge."),
        ],
        "why": [
            ("Kräftige Farben", "Farbtreue und Schärfe, die Ihre Gestaltung zur Geltung bringen."),
            ("Schnell", "Kurze Wege, eigene Produktion und klare Termine."),
            ("Datencheck inklusive", "Wir prüfen Ihre Druckdaten, bevor etwas in Produktion geht."),
        ],
        "faq": [
            ("Welche Druckdaten brauchen Sie?", "Am besten PDF mit Beschnitt und Schriften in Pfaden. Wir prüfen die Daten und melden uns, falls etwas fehlt."),
            ("Können Sie auch das Design übernehmen?", "Ja, unser Designteam gestaltet Ihre Drucksachen auf Wunsch von Grund auf."),
            ("Gibt es Muster?", "Gerne zeigen wir Ihnen Materialien und Muster direkt bei uns in Rorschach."),
        ],
    },
    {
        "slug": "signaletik", "key": "signage", "num": "05", "title": "Signage",
        "sub": "Schilder & Werbetafeln", "img": "service-signage.jpg",
        "short": "Firmenschilder, Werbetafeln und Wegweiser. Damit man Sie findet und sich an Sie erinnert.",
        "intro": [
            "Ein Schild sagt in einer Sekunde, wer Sie sind. Wir sorgen dafür, dass diese Sekunde zählt.",
            "Wir gestalten, produzieren und montieren Beschilderungen für Fassade, Eingang und Innenräume, ob einzeln oder als komplettes Leitsystem.",
        ],
        "offers": [
            ("Firmen- & Fassadenschilder", "Repräsentative Schilder aus Alu-Verbund, Acryl oder mit Leuchtwirkung."),
            ("Werbetafeln & Banner", "Grossflächige Werbung für Bauzäune, Events und Gebäude."),
            ("Leit- & Orientierungssysteme", "Wegweiser und Türschilder, die Ordnung und Stil in Räume bringen."),
            ("Roll-ups & Messe", "Mobile Displays für Messen, Events und Verkaufspunkte."),
        ],
        "why": [
            ("Wirkung auf Distanz", "Lesbarkeit, Kontrast und Grösse sind bei uns keine Nebensache."),
            ("Langlebig", "Wetterfeste Materialien, die auch nach Jahren noch gut aussehen."),
            ("Montage inklusive", "Wir montieren sicher und sauber, auch in der Höhe."),
        ],
        "faq": [
            ("Brauche ich eine Bewilligung?", "Für Aussenreklamen oft schon. Wir sagen Ihnen, welche Unterlagen Ihre Gemeinde braucht."),
            ("Welche Materialien gibt es?", "Alu-Verbund, Acryl, Forex, Blachen und mehr. Wir empfehlen das passende Material je nach Einsatz."),
            ("Montieren Sie auch?", "Ja, Montage gehört bei uns dazu, auf Wunsch inklusive Demontage alter Schilder."),
        ],
    },
    {
        "slug": "design", "key": "design", "num": "06", "title": "Design",
        "sub": "Grafik · Branding · Logo", "img": "service-design.jpg",
        "short": "Logos, Corporate Design und Kampagnen mit Haltung. Damit Ihre Marke nicht nach 0815 aussieht.",
        "intro": [
            "Gutes Design ist kein Dekor, es ist Ihre Haltung, sichtbar gemacht. Wir entwickeln Marken mit Charakter, die sich abheben.",
            "Weil wir selbst produzieren, gestalten wir immer mit Blick auf die Umsetzung: auf dem Auto, am Schaufenster, auf dem Shirt und im Netz.",
        ],
        "offers": [
            ("Logo & Markenzeichen", "Ein Zeichen, das einfach, eigenständig und vielseitig einsetzbar ist."),
            ("Corporate Design", "Farben, Schriften, Bildsprache und Regeln für einen starken Auftritt."),
            ("Grafik & Layout", "Drucksachen, Anzeigen, Verpackungen und Präsentationen."),
            ("Social Media Visuals", "Vorlagen und Kampagnen-Grafiken für Instagram, Facebook und Co."),
        ],
        "why": [
            ("Mut zur Eigenständigkeit", "Wir suchen die Idee, die Sie unterscheidet, nicht die, die alle haben."),
            ("Design trifft Produktion", "Wir wissen, wie Gestaltung auf Folie, Stoff und Papier wirkt."),
            ("Persönlich", "Kurze Wege, offene Gespräche und ehrliches Feedback."),
        ],
        "faq": [
            ("Wie läuft ein Logo-Projekt ab?", "Briefing, Ideen, Entwürfe, Feinschliff und Reinzeichnung. Sie sind in jedem Schritt dabei."),
            ("Was erhalte ich am Ende?", "Alle Logo-Dateien für Print und Web sowie auf Wunsch ein Manual mit den wichtigsten Regeln."),
            ("Können Sie ein bestehendes Logo modernisieren?", "Ja. Oft reicht ein gezielter Relaunch, der die Wiedererkennung behält."),
        ],
    },
    {
        "slug": "digital", "key": "digital", "num": "07", "title": "Digital",
        "sub": "Webdesign & Websites", "img": "service-digital.jpg",
        "short": "Websites, die so stark aussehen wie Ihr Auftritt auf der Strasse. Schnell, mobil, klar.",
        "intro": [
            "Ihre Website ist Ihr Schaufenster, das nie schliesst. Wir gestalten und bauen Websites, die Ihre Marke digital genauso stark machen wie analog.",
            "Modern, schnell und auf jedem Gerät gut bedienbar, mit Inhalten, die Besucher zu Kunden machen.",
        ],
        "offers": [
            ("Websites", "Individuell gestaltete Websites für Unternehmen, Geschäfte und Marken."),
            ("Landingpages", "Fokussierte Seiten für Kampagnen, Produkte und Aktionen."),
            ("Pflege & Updates", "Wir halten Ihre Website aktuell, sicher und schnell."),
            ("Sichtbarkeit", "Saubere Technik und Struktur, damit man Sie auch bei Google findet."),
        ],
        "why": [
            ("Ein Auftritt, überall", "Online und offline aus einem Guss, vom Auto bis zur Website."),
            ("Mobil zuerst", "Gebaut für das Smartphone, wo Ihre Kundschaft heute sucht."),
            ("Schnell & schlank", "Kurze Ladezeiten und moderne Technik ohne unnötigen Ballast."),
        ],
        "faq": [
            ("Wie lange dauert eine Website?", "Eine kompakte Website ist oft in wenigen Wochen online. Den Zeitplan legen wir gemeinsam fest."),
            ("Kann ich Inhalte selbst ändern?", "Je nach Lösung ja. Oder Sie lassen uns die Pflege übernehmen."),
            ("Kümmern Sie sich auch um Domain und Hosting?", "Ja, wir richten alles ein und beraten Sie zu Domain, E-Mail und Hosting."),
        ],
    },
]

PROJECTS = [
    {"title": "Vehicle Branding", "cat": "vehicle", "label": "Vehicle", "meta": "Project 001 — 2026", "img": "project-vehicle.jpg"},
    {"title": "Window Graphics", "cat": "windows", "label": "Windows", "meta": "Project 002 — 2026", "img": "project-windows.jpg"},
    {"title": "Textile", "cat": "textile", "label": "Textile", "meta": "Project 003 — 2026", "img": "project-textile.jpg"},
    {"title": "Printmedia", "cat": "print", "label": "Print", "meta": "Project 004 — 2026", "img": "project-print.jpg"},
    {"title": "Store Signage", "cat": "signage", "label": "Signage", "meta": "Project 005 — 2026", "img": "service-signage.jpg"},
    {"title": "Web Presence", "cat": "digital", "label": "Digital", "meta": "Project 006 — 2026", "img": "service-digital.jpg"},
]

PROCESS = [
    ("01", "Talk", "Erzählen Sie uns, was Sie brauchen. Persönlich, am Telefon oder per Offerte."),
    ("02", "Create", "Wir entwickeln das Design und zeigen Ihnen Entwürfe, bis es passt."),
    ("03", "Make", "Wir drucken, plotten, produzieren und montieren. Alles im eigenen Haus."),
    ("04", "Wow", "Bereit, gesehen zu werden. Ihr Auftritt ist da und fällt auf."),
]
