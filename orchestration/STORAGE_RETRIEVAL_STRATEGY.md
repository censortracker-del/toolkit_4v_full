# STORAGE_RETRIEVAL_STRATEGY.md - Optional Retrieval Strategy

Agent_Wiki is the control plane and durable project memory. RAG/indexed
retrieval is optional evidence retrieval for large or search-heavy corpora.

## Default

Use Agent_Wiki/Markdown for:

- human-readable memory;
- manual handoff;
- decisions, reports, summaries, adapters;
- changelog, cursors, inboxes;
- small and medium projects.

## Use RAG/Index When

- files are too numerous to inspect manually;
- semantic search across a large corpus is needed;
- evidence retrieval matters;
- raw sources are many PDFs/docs/emails/tables/logs;
- corpus size is large or huge.

## Hybrid Pattern

```text
raw source corpus
-> index/RAG/full-text search
-> retrieved evidence
-> Agent_Wiki summaries, decisions, changelog, adapters
```

RAG answers: where is the relevant evidence?

Agent_Wiki answers: what did we decide, what changed, what is current state?

## Huge Corpus Rule

For hundreds of GB or around 1 TB:

- do not read all files;
- do not upload everything into chat;
- do not summarize everything at once;
- do not run normal document analysis.

First produce a project-local `CORPUS_INTAKE_PLAN.md` with:

1. inventory approach;
2. file type and size distribution;
3. sample strategy;
4. dedup/hash strategy;
5. sensitive data check;
6. extraction/OCR requirements;
7. indexing strategy;
8. retrieval validation strategy;
9. human confirmation before heavy processing.

## Schema Hint

`SOURCE_INVENTORY_SCHEMA.json` carries:

- `corpus_profile`
- `retrieval_strategy`
- `large_corpus_controls`
