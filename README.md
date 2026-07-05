# Hacker News Top Stories Pipeline

This is a standalone proof-of-concept for fetching Hacker News top stories,
extracting linked story content, running a basic quality check, generating
summaries, ranking positive/negative comments, and fetching comments from the
official Hacker News API.

## What It Does

1. Fetches the current top story IDs from Hacker News.
2. Takes the top N stories, defaulting to 10.
3. Fetches each story's metadata from the HN API.
4. Extracts story content using multiple methods:
   - HN inline text, for Ask HN/text posts
   - PDF text extraction, when the URL is a PDF
   - `trafilatura`, if installed
   - `readability-lxml`, if installed
   - `lxml` main/article/body text extraction
   - meta description fallback
5. Runs a basic extraction-health check on extracted text.
6. Fetches comments from HN using each story's `kids` comment IDs.
7. Automatically asks OpenAI to verify extraction only when the basic check
   finds an issue, or when forced through configuration.
8. Summarizes each story using OpenAI.
9. Ranks the top 5 positive and top 5 negative comments using batched OpenAI
   sentiment analysis.
10. Saves full debug output and clean final output as JSON and Markdown.

See [pipeline_flow_diagram.md](pipeline_flow_diagram.md) for a visual flow
diagram of the program.

## Run

Install this sample project's dependencies if needed:

```bash
python -m pip install -r artifacts/news_ycombinator/requirements.txt
```

From the repository root:

```bash
uv run python artifacts/news_ycombinator/main.py
```

Create your local `.env` from the template, then set `OPENAI_API_KEY` before
running the full pipeline, because summary generation and sentiment analysis use
OpenAI by default:

```bash
cp artifacts/news_ycombinator/.env.example artifacts/news_ycombinator/.env
```

Runtime values are configured in `.env`:

```text
STORY_LIMIT=10
MAX_COMMENTS_PER_STORY=100
REPLY_DEPTH=2
CONCURRENCY=25
MAX_CONTENT_CHARS=25000
LOG_LEVEL=INFO
SUMMARY_ENABLED=true
SENTIMENT_ENABLED=true
LLM_VERIFY_ENABLED=false
AUTO_LLM_VERIFY_ON_QUALITY_ISSUE=true
LLM_MAX_INPUT_CHARS=8000
LLM_WEB_SEARCH_TOOL=web_search
```

By default, LLM verification runs only when the basic extraction-health check is
`partial` or `failed`. Set `LLM_VERIFY_ENABLED=true` to force verification for
every story.

The Hacker News API base URL is also configured in `.env`:

```text
HN_BASE_URL=https://hacker-news.firebaseio.com/v0
```

Web search modes:

```text
off         never use web search
suspicious  use web search only for low-confidence quality checks
always      use web search for every LLM verification
```

## Outputs

Generated files are written to:

```text
artifacts/news_ycombinator/final_report.json
artifacts/news_ycombinator/final_report.md
artifacts/news_ycombinator/outputs/raw_debug_output.json
artifacts/news_ycombinator/outputs/raw_debug_output.md
```

Use `final_report.md` or `final_report.json` as the clean submission output
with only the heading, summary, top positive comments, and top negative comments
for each story. Use `outputs/raw_debug_output.json` as the full debug/archive
output.

## Structure

```text
main.py                   main runner
utils/hn_api.py           Hacker News API calls
utils/extractors.py       article/PDF/GitHub extraction
utils/comments.py         comment fetching
utils/content_checks.py   basic quality check and optional OpenAI verification
utils/sentiment.py        comment sentiment ranking
utils/summarizer.py       story summary generation
utils/models.py           dataclasses
utils/text_utils.py       text helpers
utils/http_client.py      HTTP helpers
utils/report_writer.py    JSON and Markdown output
```

## Notes

The Hacker News API gives reliable access to story metadata and comments. The
external article content is less predictable because every story can link to a
different website. That is why extraction, basic quality checking, and optional
LLM verification are separate steps.

Comment fetching defaults to reply depth 2. This captures top-level comments,
replies, and replies-to-replies while still avoiding unlimited recursive comment
fetching.
