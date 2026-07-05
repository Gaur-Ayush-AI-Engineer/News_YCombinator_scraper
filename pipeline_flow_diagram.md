# Hacker News Pipeline Flow

This diagram shows how `main.py` runs the project from configuration to final
outputs.

```mermaid
flowchart TD
    A[Start: python main.py] --> B[Load .env]
    B --> C[Build runtime config]
    C --> D[Create aiohttp session and concurrency semaphore]
    D --> E[Fetch top story IDs from HN API]
    E --> F[Fetch story metadata for top N stories]
    F --> G{For each story, run in parallel}

    G --> H[Extract linked story content]
    G --> I[Fetch HN comments up to reply depth]

    H --> H1[Try HN inline text]
    H1 --> H2[Try GitHub/PDF/html extractors]
    H2 --> H3[Return selected content and extraction attempts]

    I --> I1[Fetch top-level comments]
    I1 --> I2[Fetch replies until depth limit]
    I2 --> I3[Return cleaned comments]

    H3 --> J[Run basic extraction-health check]
    I3 --> K[Prepare comments for sentiment]

    J --> L{Should LLM verify content?}
    L -->|LLM_VERIFY_ENABLED=true| M[Run LLM content verification]
    L -->|status partial/failed and AUTO_LLM_VERIFY_ON_QUALITY_ISSUE=true| M
    L -->|No trigger| N[Skip LLM content verification]

    H3 --> O{SUMMARY_ENABLED=true?}
    O -->|Yes| P[Generate story summary with OpenAI]
    O -->|No| Q[Skip summary]

    K --> R{SENTIMENT_ENABLED=true?}
    R -->|Yes| S[Analyze comments with OpenAI]
    S --> T[Select top positive and negative comments]
    R -->|No| U[Skip sentiment]

    M --> V[Assemble story result]
    N --> V
    P --> V
    Q --> V
    T --> V
    U --> V

    V --> W[Combine all story results]
    W --> X[Write full debug JSON and Markdown]
    W --> Y[Write clean final JSON and Markdown]
    X --> Z[Print terminal summary]
    Y --> Z
```

## Simple Explanation

1. `main.py` loads settings from `.env`.
2. It fetches the current top Hacker News stories.
3. For each story, it does two main jobs at the same time:
   - extracts the linked article/post content
   - fetches comments from Hacker News
4. It runs a basic extraction-health check on the extracted content.
5. LLM content verification runs only when forced or when extraction looks
   problematic.
6. The summary step creates a story summary with OpenAI.
7. The sentiment step ranks the top positive and negative comments with OpenAI.
8. The project writes two output types:
   - full debug output with all details
   - clean final output for submission

## Output Files

```text
final_report.json
final_report.md
outputs/raw_debug_output.json
outputs/raw_debug_output.md
```
