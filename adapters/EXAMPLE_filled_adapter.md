# EXAMPLE adapter (moved from core/PRINCIPLES_MAX.md B1 for core purity)

## B1. Filled reference adapter — demo: kitten gallery website

A complete example of a filled adapter for a small `build`-type project. It is a
DEMO of adapter *shape* — deliberately toy, so nobody mistakes its values for
protocol defaults. Use the structure, never the values.

```md
## Source of truth
path: <PROJECT_ROOT>/content/   (kitten photos + profile texts; immutable; reasoning agents read-only)
read-only to reasoning agents: yes

## Domain adapter
item definition: one kitten profile card (photo set + short text), identified by a stable internal id, NOT by file path.
_index.tsv columns: id  name  status  needs_manual_review  last_processed_change_id
counts tracked: kittens_total, drafted, published
lifecycle statuses: raw, drafted, review_needed, published, archived
domain safety rules:
  - never delete/rename source photos without a dry-run manifest + explicit user confirm
  - photo file path is metadata, never identity
  - unverified facts about a kitten (age, breed, health) -> manual_review, never published as confirmed
output types: one site page per kitten; a gallery index page; a publishing checklist report
review triggers (review lane): site structure changes, page template logic, publishing criteria
review triggers (audit lane): any file-output/deploy step, image-processing scripts, bulk renames
language conventions: user-facing RU / agent-facing EN
lane_binding: implement=<agent>, review=<agent>, audit=<agent>
```
