# WOW PRINT – Website

Mehrseitige, statische Website für WOW PRINT (Rorschach). Kein Framework, kein Build auf Netlify nötig.

## Struktur
- `site/` – fertige Website (wird von Netlify veröffentlicht)
- `tools/content.py` – Firmendaten, Leistungen, Projekte, Prozess
- `tools/legal.py` – Impressum, Datenschutz, AGB (Vorlagen)
- `tools/build.py` – erzeugt alle HTML-Seiten aus den Inhalten
- `tools/placeholders.py` – Platzhalterbilder, bis die Higgsfield-Bilder da sind
- `HIGGSFIELD-PROMPTS.md` – Bildliste mit Prompts und Dateinamen

## Inhalte ändern
1. Texte in `tools/content.py` oder `tools/legal.py` anpassen
2. `python3 tools/build.py` ausführen
3. Committen und pushen, Netlify veröffentlicht automatisch

## Bilder ersetzen
Neue Bilder mit exakt dem Dateinamen aus `HIGGSFIELD-PROMPTS.md` nach `site/assets/img/` legen (JPG, ca. 80 % Qualität). Kein Build nötig.

## Formulare (Netlify Forms)
- `kontakt` und `offerte` (mit Datei-Upload, max. 8 MB pro Anfrage)
- Nach dem ersten Deploy in Netlify unter *Forms → Form notifications* eine E-Mail-Benachrichtigung einrichten.

## Vor dem Livegang
- Telefon und E-Mail in `tools/content.py` ersetzen, Social-Links eintragen
- Platzhalter `[...]` in den Rechtstexten ersetzen, `SHOW_NOTICE = False` in `tools/legal.py`
- Domain in `tools/content.py` (`domain`) prüfen
- Projekte durch echte Referenzen ersetzen

## Technik
GSAP + ScrollTrigger, Lenis (Smooth Scroll), Schriften Archivo und Inter lokal eingebunden (keine Google-Server, DSG-freundlich). Animationen respektieren `prefers-reduced-motion`.
