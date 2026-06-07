# Daily Digest Implementation Checklist

Use this checklist when adapting the workflow to a new topic.

## Contract

- Topic name.
- Categories.
- Time zone and run time.
- Lookback window.
- Recipient address.
- Sender SMTP provider.
- Output formats.
- Source allowlist and blocked sources.

## Local Files

- `requirements.txt`
- `.env.example`
- `run_digest.ps1`
- `test_email.py`
- `check_setup.py`
- Main digest script

## Output Layout

- `output/markdown/`
- `output/txt/`
- `output/pdf/`

Use timestamped filenames.

## Email

- Full HTML body.
- Plain text alternative.
- PDF attachment only by default.
- Never truncate body unless requested.

## Quality

- Clean labels such as timestamps, “早报”, “周报”, “快讯”.
- Use numbered lists.
- Translate English headlines for the opening summary.
- Keep English titles in detailed sections.
- Sort by importance inside each category.

