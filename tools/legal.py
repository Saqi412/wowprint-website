# -*- coding: utf-8 -*-
"""Rechtstexte (Vorlagen). Vor Livegang vom Kunden bzw. einer Fachperson prüfen lassen.
Platzhalter in [eckigen Klammern] ersetzen und SHOW_NOTICE auf False setzen."""
from content import COMPANY as C

SHOW_NOTICE = True
STAND = "Oktober 2026"


def notice():
    if not SHOW_NOTICE:
        return ""
    return ('<p class="notice"><strong>Vorlage:</strong> Dieser Text ist ein Entwurf und ersetzt keine Rechtsberatung. '
            'Bitte Angaben in [eckigen Klammern] ergänzen und vor der Veröffentlichung prüfen lassen.</p>')


def addr():
    return f'{C["name"]}<br>{C["street"]}<br>{C["zip"]} {C["city"]}<br>{C["country"]}'


def impressum(p):
    return f"""{notice()}
<h2>Kontaktadresse</h2>
<p>{addr()}</p>
<p>Telefon: <a class="link-u" href="tel:{C["phone_href"]}">{C["phone"]}</a><br>E-Mail: <a class="link-u" href="mailto:{C["email"]}">{C["email"]}</a></p>

<h2>Vertretungsberechtigte Person</h2>
<p>[Vorname Name], Inhaber</p>

<h2>Unternehmensangaben</h2>
<p>Rechtsform: [Einzelunternehmen / GmbH]<br>
Handelsregister: [Handelsregisteramt des Kantons St. Gallen]<br>
Unternehmens-Nr. (UID): [CHE-000.000.000]<br>
MWST-Nr.: [CHE-000.000.000 MWST]</p>

<h2>Haftungsausschluss</h2>
<p>Wir prüfen die Inhalte dieser Website sorgfältig, übernehmen aber keine Gewähr für Richtigkeit, Vollständigkeit und Aktualität der Informationen. Haftungsansprüche wegen Schäden materieller oder immaterieller Art, die aus dem Zugriff auf die veröffentlichten Informationen, durch Missbrauch der Verbindung oder durch technische Störungen entstanden sind, werden ausgeschlossen, soweit gesetzlich zulässig.</p>
<p>Alle Angebote sind unverbindlich. Wir behalten uns vor, Teile der Seiten oder das gesamte Angebot ohne Ankündigung zu verändern, zu ergänzen, zu löschen oder die Veröffentlichung zeitweise oder endgültig einzustellen.</p>

<h2>Haftung für Links</h2>
<p>Verweise und Links auf Websites Dritter liegen ausserhalb unseres Verantwortungsbereichs. Der Zugriff und die Nutzung solcher Websites erfolgen auf eigene Gefahr der Nutzerin oder des Nutzers.</p>

<h2>Urheberrechte</h2>
<p>Die Urheber- und alle anderen Rechte an Inhalten, Bildern, Fotos oder anderen Dateien auf dieser Website gehören ausschliesslich {C["name"]} oder den speziell genannten Rechteinhabern. Für die Reproduktion jeglicher Elemente ist die schriftliche Zustimmung der Urheberrechtsträger im Voraus einzuholen.</p>

<h2>Bildnachweis</h2>
<p>Ein Teil der Bilder auf dieser Website wurde mit Hilfe von KI (Higgsfield) erstellt. [Weitere Quellen ergänzen]</p>

<h2>Konzept & Umsetzung</h2>
<p>[Name / Agentur der Webentwicklung]</p>
"""


def datenschutz(p):
    return f"""{notice()}
<p>Mit dieser Datenschutzerklärung informieren wir darüber, welche Personendaten wir im Zusammenhang mit dieser Website und unseren Leistungen bearbeiten. Wir richten uns nach dem schweizerischen Bundesgesetz über den Datenschutz (DSG) und der Datenschutzverordnung (DSV).</p>

<h2>1. Verantwortliche Stelle</h2>
<p>{addr()}<br>E-Mail: <a class="link-u" href="mailto:{C["email"]}">{C["email"]}</a></p>

<h2>2. Welche Daten wir bearbeiten</h2>
<p>Wir bearbeiten Personendaten, die Sie uns selbst mitteilen, zum Beispiel über das Kontakt- oder Offertenformular, per E-Mail, Telefon oder WhatsApp. Dazu gehören insbesondere Name, Firma, E-Mail-Adresse, Telefonnummer, Ort, Angaben zu Ihrem Projekt sowie Dateien, die Sie uns hochladen (z. B. Logos oder Fotos).</p>
<p>Ausserdem fallen beim Besuch der Website technische Daten an (siehe Ziffer 4).</p>

<h2>3. Zweck der Bearbeitung</h2>
<p>Wir verwenden Ihre Daten, um Anfragen zu beantworten, Offerten zu erstellen, Aufträge abzuwickeln und mit Ihnen zu kommunizieren. Ausserdem bearbeiten wir Daten, soweit dies für den sicheren Betrieb der Website oder zur Erfüllung gesetzlicher Pflichten nötig ist. Eine Verwendung für Werbezwecke findet nur mit Ihrer Einwilligung statt.</p>

<h2>4. Website, Hosting und Server-Logfiles</h2>
<p>Diese Website wird bei Netlify, Inc., San Francisco, USA, gehostet. Beim Aufruf der Website werden technisch notwendige Daten wie IP-Adresse, Datum und Uhrzeit, aufgerufene Seite, Browsertyp und Betriebssystem vorübergehend in Logfiles gespeichert. Diese Daten dienen der Sicherheit und Stabilität der Website und werden nicht mit anderen Daten zusammengeführt.</p>

<h2>5. Kontakt- und Offertenformular</h2>
<p>Wenn Sie uns über ein Formular kontaktieren, werden Ihre Angaben und allfällig hochgeladene Dateien über den Formulardienst von Netlify übermittelt und gespeichert und uns per E-Mail weitergeleitet. Wir verwenden diese Daten ausschliesslich zur Bearbeitung Ihrer Anfrage. Zum Schutz vor Spam verwenden wir ein unsichtbares Prüffeld.</p>

<h2>6. Bekanntgabe ins Ausland</h2>
<p>Durch den Einsatz von Netlify können Personendaten in die USA übermittelt werden. Die USA gelten für Unternehmen, die unter dem Swiss-U.S. Data Privacy Framework zertifiziert sind, als Land mit angemessenem Datenschutz. Wo dies nicht zutrifft, stützen wir uns auf Standardvertragsklauseln oder andere geeignete Garantien. [Zertifizierungsstatus von Netlify vor Livegang prüfen]</p>

<h2>7. Cookies, Tracking und lokale Speicherung</h2>
<p>Wir verwenden keine Tracking- oder Analyse-Cookies und keine Werbe-Tracker. Die Website speichert im Sitzungsspeicher Ihres Browsers lediglich einen technischen Hinweis, ob die Startanimation bereits angezeigt wurde. Dieser Eintrag enthält keine Personendaten und wird beim Schliessen des Browsers gelöscht.</p>

<h2>8. Schriften und externe Inhalte</h2>
<p>Alle Schriften und Skripte werden direkt von unserem Server geladen. Es werden keine Inhalte von Google Fonts oder ähnlichen Diensten nachgeladen.</p>

<h2>9. Links zu sozialen Netzwerken und Karten</h2>
<p>Unsere Website enthält einfache Links zu Instagram, Facebook und Google Maps. Erst wenn Sie einen solchen Link anklicken, werden Sie auf die Seite des jeweiligen Anbieters weitergeleitet, und es gelten dessen Datenschutzbestimmungen. Beim blossen Besuch unserer Website werden keine Daten an diese Anbieter übermittelt.</p>

<h2>10. Aufbewahrung</h2>
<p>Wir bewahren Personendaten nur so lange auf, wie es für die genannten Zwecke erforderlich ist oder gesetzliche Aufbewahrungspflichten bestehen (z. B. zehn Jahre für Geschäftsunterlagen). Anfragen, aus denen kein Auftrag entsteht, löschen wir in der Regel nach [12 Monaten].</p>

<h2>11. Datensicherheit</h2>
<p>Wir treffen angemessene technische und organisatorische Massnahmen, um Ihre Daten vor Verlust, Missbrauch und unbefugtem Zugriff zu schützen. Die Übertragung der Website erfolgt verschlüsselt (HTTPS).</p>

<h2>12. Ihre Rechte</h2>
<p>Sie haben im Rahmen des DSG das Recht auf Auskunft über Ihre Personendaten, auf Berichtigung, Löschung sowie auf Herausgabe oder Übertragung Ihrer Daten. Sie können einer Bearbeitung widersprechen und eine Einwilligung jederzeit widerrufen. Wenden Sie sich dafür an die oben genannte Adresse. Zudem können Sie sich beim Eidgenössischen Datenschutz- und Öffentlichkeitsbeauftragten (EDÖB) beschweren.</p>

<h2>13. Änderungen</h2>
<p>Wir können diese Datenschutzerklärung jederzeit anpassen. Es gilt die jeweils auf dieser Website veröffentlichte Fassung.</p>
<p class="muted">Stand: {STAND}</p>
"""


def agb(p):
    return f"""{notice()}
<p>Diese Allgemeinen Geschäftsbedingungen (AGB) gelten für alle Leistungen von {C["name"]}, {C["street"]}, {C["zip"]} {C["city"]} (nachfolgend «WOW PRINT»), insbesondere Fahrzeugbeschriftung und -folierung, Schaufenster- und Glasbeschriftung, Textildruck, Druckprodukte, Schilder, Grafikdesign und Webdesign.</p>

<h2>1. Geltungsbereich</h2>
<p>Die AGB gelten für alle Verträge zwischen WOW PRINT und ihren Kundinnen und Kunden. Abweichende Bedingungen gelten nur, wenn WOW PRINT sie schriftlich bestätigt hat.</p>

<h2>2. Offerten und Vertragsabschluss</h2>
<p>Offerten sind während [30 Tagen] gültig, sofern nichts anderes angegeben ist. Ein Vertrag kommt mit der schriftlichen Auftragsbestätigung (auch per E-Mail) oder mit Beginn der Ausführung zustande. Änderungen nach Auftragserteilung können zu Mehrkosten und Terminverschiebungen führen.</p>

<h2>3. Preise und Zahlung</h2>
<p>Alle Preise verstehen sich in Schweizer Franken (CHF) [zuzüglich gesetzlicher Mehrwertsteuer]. Rechnungen sind innert [30 Tagen] netto zahlbar. WOW PRINT kann bei grösseren Aufträgen oder Neukunden eine Anzahlung von bis zu [50 %] verlangen. Bei Zahlungsverzug kann ein Verzugszins von 5 % pro Jahr erhoben werden.</p>

<h2>4. Gestaltung, Entwürfe und Druckdaten</h2>
<p>Die Kundin oder der Kunde ist für die Richtigkeit der gelieferten Inhalte, Texte und Daten verantwortlich und stellt sicher, dass dafür die nötigen Rechte vorliegen. Vor der Produktion erhält die Kundschaft einen Korrekturabzug oder eine Visualisierung zur Freigabe («Gut zur Ausführung»). Mit der Freigabe gehen die Verantwortung für Fehler im freigegebenen Entwurf auf die Kundschaft über.</p>
<p>Im Preis sind [zwei] Korrekturrunden enthalten. Weitere Änderungen werden nach Aufwand verrechnet.</p>

<h2>5. Nutzungsrechte</h2>
<p>Die Urheberrechte an Entwürfen und Gestaltungen verbleiben bei WOW PRINT. Mit vollständiger Bezahlung erhält die Kundschaft das Recht, die Gestaltungen für den vereinbarten Zweck zu nutzen. Offene Daten (z. B. Arbeitsdateien) werden nur nach Vereinbarung herausgegeben. WOW PRINT darf ausgeführte Arbeiten als Referenz zeigen, sofern nichts anderes vereinbart ist.</p>

<h2>6. Termine</h2>
<p>Liefer- und Montagetermine werden nach bestem Wissen vereinbart. Verzögerungen durch verspätete Daten oder Freigaben, Lieferengpässe, Witterung oder höhere Gewalt berechtigen nicht zu Schadenersatz oder Rücktritt.</p>

<h2>7. Fahrzeuge und Montage</h2>
<p>Fahrzeuge sind zum vereinbarten Termin sauber gewaschen, trocken und ohne Wachs- oder Versiegelungsrückstände zu übergeben. WOW PRINT haftet nicht für Schäden an nachlackierten oder vorgeschädigten Lackstellen, an nicht originalen Lacken oder für Lackablösungen beim späteren Entfernen von Folien. Für die Montage vor Ort stellt die Kundschaft einen freien Zugang, Strom und eine geeignete Arbeitsumgebung zur Verfügung. Für allfällige Bewilligungen (z. B. Aussenreklamen) ist die Kundschaft verantwortlich.</p>

<h2>8. Farben und Materialien</h2>
<p>Geringfügige Farbabweichungen zwischen Bildschirm, Proof und Endprodukt sowie zwischen verschiedenen Materialien und Produktionsserien sind technisch bedingt und stellen keinen Mangel dar.</p>

<h2>9. Mängelrüge und Gewährleistung</h2>
<p>Die Kundschaft prüft die Leistung sofort nach Erhalt oder Montage. Mängel sind innert [7 Tagen] schriftlich zu melden, versteckte Mängel sofort nach Entdeckung. Bei berechtigten Mängeln bessert WOW PRINT nach oder liefert Ersatz. Weitergehende Ansprüche sind ausgeschlossen, soweit gesetzlich zulässig. Für die Haltbarkeit von Folien gelten die Angaben der Hersteller bei sachgemässer Pflege.</p>

<h2>10. Haftung</h2>
<p>WOW PRINT haftet nur für Schäden, die vorsätzlich oder grobfahrlässig verursacht wurden. Die Haftung für leichte Fahrlässigkeit, Folgeschäden und entgangenen Gewinn ist ausgeschlossen, soweit gesetzlich zulässig.</p>

<h2>11. Eigentumsvorbehalt</h2>
<p>Gelieferte Waren bleiben bis zur vollständigen Bezahlung Eigentum von WOW PRINT.</p>

<h2>12. Websites und digitale Leistungen</h2>
<p>Für Websites und digitale Leistungen gelten ergänzend die im jeweiligen Angebot festgehaltenen Bedingungen, insbesondere zu Hosting, Domains, Wartung und Laufzeiten.</p>

<h2>13. Anwendbares Recht und Gerichtsstand</h2>
<p>Es gilt ausschliesslich schweizerisches Recht. Gerichtsstand ist [Rorschach], soweit gesetzlich zulässig.</p>
<p class="muted">Stand: {STAND}</p>
"""
