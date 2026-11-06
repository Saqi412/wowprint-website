// Wird von Netlify automatisch bei jeder neuen Formular-Anfrage aufgerufen
// (Kontakt + Offerte) und schickt sie per SMTP an info@wow-print.ch.
// Einstellungen kommen aus den Netlify-Umgebungsvariablen:
//   SMTP_HOST, SMTP_PORT (465 oder 587), SMTP_USER, SMTP_PASS, MAIL_TO (optional)
import nodemailer from "nodemailer";

const LABELS = {
  name: "Name", firma: "Firma", email: "E-Mail", telefon: "Telefon", ort: "Ort",
  thema: "Thema", nachricht: "Nachricht", leistung: "Leistung", beschreibung: "Beschreibung",
  menge: "Menge", termin: "Termin", budget: "Budget", design: "Design",
  kontaktweg: "Kontaktweg", datei1: "Datei 1", datei2: "Datei 2", datei3: "Datei 3",
};
const SKIP = new Set(["bot-field", "ip", "user_agent", "referrer", "datenschutz", "form-name"]);

const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

function value(v) {
  if (v == null || v === "") return null;
  if (Array.isArray(v)) return v.map(value).filter(Boolean).join(", ") || null;
  if (typeof v === "object") return v.url ? { url: v.url, name: v.filename || "Datei" } : JSON.stringify(v);
  return String(v);
}

export const handler = async (event) => {
  const env = process.env;
  if (!env.SMTP_HOST || !env.SMTP_PASS) {
    console.log("SMTP nicht eingerichtet – keine Mail verschickt.");
    return { statusCode: 200, body: "skipped" };
  }
  const { payload } = JSON.parse(event.body || "{}");
  const form = payload?.form_name || "formular";
  const data = payload?.data || {};

  const rows = [];
  for (const [key, raw] of Object.entries(data)) {
    if (SKIP.has(key)) continue;
    const v = value(raw);
    if (!v) continue;
    rows.push([LABELS[key] || key, v]);
  }
  const text = rows.map(([k, v]) => `${k}: ${typeof v === "object" ? `${v.name} – ${v.url}` : v}`).join("\n");
  const html = `<table cellpadding="6" style="font-family:Arial,sans-serif;font-size:14px;border-collapse:collapse">${rows
    .map(([k, v]) => `<tr><td style="vertical-align:top;color:#6d6b68"><b>${esc(k)}</b></td><td>${
      typeof v === "object" ? `<a href="${esc(v.url)}">${esc(v.name)}</a>` : esc(v).replace(/\n/g, "<br>")
    }</td></tr>`).join("")}</table>`;

  const title = form === "offerte" ? "Neue Offert-Anfrage" : "Neue Kontaktanfrage";
  const port = Number(env.SMTP_PORT || 465);
  const user = env.SMTP_USER || "info@wow-print.ch";
  const transporter = nodemailer.createTransport({
    host: env.SMTP_HOST, port, secure: port === 465, auth: { user, pass: env.SMTP_PASS },
  });
  await transporter.sendMail({
    from: `"WOW PRINT Website" <${user}>`,
    to: env.MAIL_TO || "info@wow-print.ch",
    replyTo: data.email || undefined,
    subject: `${title}${data.name ? " von " + data.name : ""}`,
    text: `${title} über wow-print.ch\n\n${text}`,
    html: `<p style="font-family:Arial,sans-serif"><b>${title}</b> über wow-print.ch</p>${html}`,
  });
  return { statusCode: 200, body: "ok" };
};
