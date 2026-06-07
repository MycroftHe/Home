"""
Template for a local recurring news digest.

Copy this file into a workspace and customize:
- CATEGORIES
- SOURCE_GROUPS
- RELEVANCE_KEYWORDS
- SMTP/.env values

This template intentionally omits secrets.
"""

from __future__ import annotations

import datetime as dt
import email.message
import html
import os
import re
import smtplib
import ssl
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

import feedparser
import requests
from dotenv import load_dotenv
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import Paragraph, SimpleDocTemplate


TZ = ZoneInfo("Asia/Shanghai")
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"


CATEGORIES = {
    "Category A": ["topic keyword", "company keyword"],
    "Category B": ["policy keyword", "funding keyword"],
}

SOURCE_GROUPS = {
    "authoritative": ["reuters.com", "bloomberg.com", "bbc.com"],
}


@dataclass
class NewsItem:
    category: str
    title: str
    source: str
    link: str
    summary: str
    published: dt.datetime
    importance: int = 0
    chinese_sentence: str = ""
    english_title: str = ""


def google_news_rss(query: str) -> str:
    encoded = requests.utils.quote(query)
    return f"https://news.google.com/rss/search?q={encoded}%20when%3A1d&hl=en-US&gl=US&ceid=US%3Aen"


def clean_text(value: object) -> str:
    text = html.unescape(str(value or ""))
    text = re.sub(r"<[^>]+>", " ", text)
    return " ".join(text.split())


def strip_labels(text: str) -> str:
    value = text.strip()
    value = re.sub(r"^\d{1,2}:\d{2}(?::\d{2})?\s*", "", value)
    value = re.sub(r"^【[^】]*(?:早报|午报|晚报|快讯|周报)[^】]*】\s*", "", value)
    value = re.sub(r"^(?:早报|午报|晚报|快讯|周报)\s*[丨|｜:：-]\s*", "", value)
    return value.strip(" -|｜:：，,。")


def is_english(text: str) -> bool:
    letters = [c for c in text if c.isalpha()]
    return bool(letters) and sum(c.isascii() for c in letters) / len(letters) >= 0.8


def translate_title(text: str) -> str:
    if not is_english(text):
        return text
    try:
        response = requests.get(
            "https://translate.googleapis.com/translate_a/single",
            params={"client": "gtx", "sl": "en", "tl": "zh-CN", "dt": "t", "q": text},
            timeout=10,
        )
        data = response.json()
        return "".join(part[0] for part in data[0] if part and part[0]).strip() or text
    except Exception:
        return text


def write_pdf(markdown: str, path: Path) -> None:
    pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
    path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(path), pagesize=A4)
    style = ParagraphStyle("Body", fontName="STSong-Light", fontSize=10, leading=15)
    story = [Paragraph(html.escape(line or " "), style) for line in markdown.splitlines()]
    doc.build(story)


def send_email(subject: str, markdown: str, pdf_path: Path) -> None:
    host = os.getenv("SMTP_HOST")
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")
    sender = os.getenv("SMTP_FROM") or username
    recipient = os.getenv("SMTP_TO")
    if not all([host, username, password, sender, recipient]):
        print("SMTP not configured; skipped email.")
        return

    msg = email.message.EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient
    msg.set_content(markdown)
    msg.add_attachment(pdf_path.read_bytes(), maintype="application", subtype="pdf", filename=pdf_path.name)

    port = int(os.getenv("SMTP_PORT", "465"))
    use_ssl = os.getenv("SMTP_USE_SSL", "true").lower() == "true"
    context = ssl.create_default_context()
    smtp_cls = smtplib.SMTP_SSL if use_ssl else smtplib.SMTP
    with smtp_cls(host, port) as smtp:
        if os.getenv("SMTP_USE_TLS", "false").lower() == "true" and not use_ssl:
            smtp.starttls(context=context)
        smtp.login(username, password)
        smtp.send_message(msg)


def main() -> None:
    load_dotenv(BASE_DIR / ".env")
    now = dt.datetime.now(TZ)
    stamp = f"{now:%Y-%m-%d-%H%M%S}"
    markdown = "# Daily News Digest\n\nCustomize this template before use.\n"
    for folder, suffix in [("markdown", "md"), ("txt", "txt"), ("pdf", "pdf")]:
        (OUTPUT_DIR / folder).mkdir(parents=True, exist_ok=True)
    md_path = OUTPUT_DIR / "markdown" / f"digest-{stamp}.md"
    txt_path = OUTPUT_DIR / "txt" / f"digest-{stamp}.txt"
    pdf_path = OUTPUT_DIR / "pdf" / f"digest-{stamp}.pdf"
    md_path.write_text(markdown, encoding="utf-8")
    txt_path.write_text(markdown, encoding="utf-8")
    write_pdf(markdown, pdf_path)
    send_email(f"Daily News Digest {now:%Y-%m-%d}", markdown, pdf_path)


if __name__ == "__main__":
    main()
