---
name: daily-news-digest
description: Create or adapt recurring curated news digest workflows for a topic or industry, including authoritative source selection, headline cleaning, importance ranking, local Markdown/TXT/PDF archives, readable HTML email delivery, SMTP setup, and scheduled daily automation. Use when the user asks to build daily news emails, morning briefings, industry digests, topic monitors, local news archives, or reusable news-push workflows.
---

# Daily News Digest

Use this skill to build a repeatable daily news digest workflow like the AI industry briefing: curated sources, local archives, readable email, and a scheduled automation.

## Workflow

1. Clarify the digest contract:
   - Topic and subcategories.
   - Time zone, run time, and lookback window.
   - Recipient email and sender SMTP provider.
   - Source policy: preferred outlets, blocked outlets, official feeds/accounts.
   - Output formats and local archive layout.

2. Scaffold the workflow:
   - Create a project folder such as `<workspace>/<topic>_news_digest/`.
   - Copy or adapt `scripts/digest_template.py`.
   - Add `.env.example`, `requirements.txt`, `run_digest.ps1`, `test_email.py`, and `check_setup.py`.
   - Never write real SMTP passwords or API keys into repo-visible files unless the user explicitly accepts that risk.

3. Implement source policy:
   - Prefer source allowlists over open web searches.
   - Query by `topic terms x source domains`.
   - Resolve Google News RSS links to original article URLs when possible.
   - Filter decoded URLs by allowed domains.
   - Keep aggregator links only as traceability metadata, not as the main source.

4. Generate readable output:
   - Put a category-by-category Chinese summary list at the top.
   - Use numbered news items under each category.
   - Clean summary text: remove timestamps, newsletter labels, “早报/周报/快讯”, and wire prefixes.
   - Translate English headlines into Chinese for the opening list, while keeping English titles in detailed sections.
   - Rank each category by importance using source authority, recency, and impact terms.

5. Archive locally:
   - Save every run, do not overwrite.
   - Use timestamped filenames.
   - Recommended layout:
     - `output/markdown/ai-news-digest-YYYY-MM-DD-HHMMSS.md`
     - `output/txt/ai-news-digest-YYYY-MM-DD-HHMMSS.txt`
     - `output/pdf/ai-news-digest-YYYY-MM-DD-HHMMSS.pdf`

6. Email:
   - Send the complete HTML body, not a truncated preview.
   - Attach PDF only unless the user asks for more attachments.
   - Keep Markdown/TXT/PDF locally.
   - Support provider-specific SMTP settings, especially SSL 465 vs STARTTLS 587.

7. Schedule:
   - Use the Codex automation tool when available.
   - For local cron automation, state that the computer must be on, online, and Codex/local environment available.

## Source Quality Rules

- Use authoritative allowlists per digest topic.
- Include official account feeds only when a stable API/RSSBridge/RSSHub feed is configured.
- Avoid generic repost sites, content farms, and low-signal aggregators.
- If a category has no qualified news, say so rather than filling with weak matches.

## Importance Ranking Heuristic

Score each item using:

- Source authority.
- Freshness inside the lookback window.
- Core entity mentions.
- Direct relevance to the category.
- Impact signals: regulation, funding, product launch, chips, model releases, major partnerships, safety/security issues.

Sort descending by score within each category. Do not expose the numeric score unless the user asks.

## Reusable Resources

- Start from `scripts/digest_template.py` when creating a new topic workflow.
- Use `references/checklist.md` as a compact implementation checklist.

