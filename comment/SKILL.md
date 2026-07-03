---
name: comment
description: Write and deliver concise Chinese event commentaries for finance/market events, including factual verification, structured sections, market and investor feedback, asset and stock impact analysis, Markdown and Word outputs, and default HTML email delivery with Word attachment unless the user explicitly says not to email. Use when the user asks for 事件点评, market commentary, IPO/event analysis, A股/美股 impact notes, or asks to follow the prior event-commentary format.
---

# Comment

Use this skill to produce a polished Chinese event commentary in the user's established format.

## Required Workflow

1. Verify the event first.
   - Browse or query authoritative sources when facts may be recent or market-sensitive.
   - Prefer official disclosures, exchanges, regulators, company announcements, and major financial media.
   - Treat social platforms such as 雪球 as investor-sentiment inputs, not as primary fact sources.
   - If the user's event wording is not fully confirmed, state the precise confirmed status in natural Chinese. Do not overstate it.

2. Draft using the standard structure.
   - Read `references/event-commentary-standard.md` before drafting.
   - Keep the piece concise but not thin: usually 5 sections and about 800-1400 Chinese characters, longer when the user asks for fuller market feedback.
   - Bold the opening judgment sentence of each paragraph.
   - Do not let “市场反馈” repeat “事件概要”; it must add incremental market, media, investor, and trading information.

3. Create deliverables.
   - Save a Markdown file in the current workspace.
   - Generate a Word `.docx` with the same content and professional business-brief styling.
   - Use the Documents skill when creating Word files; render/QA when available. If LibreOffice/soffice is unavailable, perform structural checks and disclose this only if relevant to the user.

4. Email as a default part of event-commentary delivery unless the user explicitly says not to email.
   - Use the `daily-news-digest` email pattern: complete HTML body, not a preview.
   - Attach the Word file by default.
   - Reuse the user's SMTP configuration at `C:\Users\hexuh\Documents\Test\ai_news_digest\.env` unless the user specifies another source.
   - Send to the SMTP_TO recipient(s) from that `.env` file unless the user specifies a different recipient.
   - Never print or write SMTP passwords into deliverables.

## Non-Negotiable Output Rules

- Never expose raw API/database/interface fields in final prose or email, such as `currStatus`, `registeResult`, `stockAudit`, `projectType`, `updateDate`, or similar implementation fields.
- Convert internal verification into reader-facing Chinese, e.g. “项目已进入提交注册阶段，尚未披露最终注册结果”.
- Do not mention tool internals, scripts, schemas, JSON, or scraping details in the commentary.
- For sources, cite human-readable institutions and article/page names; do not cite raw query output.
- Include clickable source links in Markdown, Word, and email when stable public URLs are available.
- Avoid unnecessary language, slogans, and repetitive background.

## File Naming

Use descriptive snake_case filenames, for example:

- `meta_compute_event_commentary.md`
- `meta_compute_event_commentary.docx`
- `unitree_ipo_event_commentary.md`
- `unitree_ipo_event_commentary.docx`

## Quality Gate

Before final delivery or email:

- Check that all five standard sections exist.
- Check that paragraph-opening judgment sentences are bold.
- Check that “市场反馈” contains incremental market/investor information.
- Search the Markdown and Word text for forbidden technical fields.
- Confirm the Word file exists and contains the same headings and source section.
- Confirm source links are present in the Markdown/Word source section when public URLs are available.
- Confirm the email was sent successfully, or clearly report any delivery failure and the next action needed.


