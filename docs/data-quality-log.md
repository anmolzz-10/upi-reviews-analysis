# Data-quality log

Source file: `data/raw/reviews_raw.csv` (66,475 reviews). Numbers below are produced by `notebooks/02_clean_and_mask.ipynb`.

| # | Issue | Rows affected | % of data | Decision |
|---|---|---|---|---|
| 1 | Duplicate review_id | 0 | 0.0% | None found. review_id is a safe unique key. |
| 2 | Missing or blank review text | 0 | 0.0% | None found. |
| 3 | Rating outside 1 to 5 | 0 | 0.0% | None found. |
| 4 | Missing app_version and review_version | 9,795 | 14.7% | Kept as missing. Version analysis in Phase 5 will use only rows that have a version, and will say so. |
| 5 | Personal detail found: EMAIL | 0 | 0.0% | Detected. The whole review text is replaced with [REDACTED]; rating and date are kept. |
| 6 | Personal detail found: URL | 0 | 0.0% | Masked in place with a placeholder. The raw text is not saved to the processed file. |
| 7 | Personal detail found: UPI_ID | 5 | 0.0% | Detected. The whole review text is replaced with [REDACTED]; rating and date are kept. |
| 8 | Personal detail found: HANDLE | 7 | 0.0% | Detected. The whole review text is replaced with [REDACTED]; rating and date are kept. |
| 9 | Personal detail found: PHONE | 2 | 0.0% | Detected. The whole review text is replaced with [REDACTED]; rating and date are kept. |
| 10 | Personal detail found: ID_NUMBER | 0 | 0.0% | Masked in place with a placeholder. The raw text is not saved to the processed file. |
| 11 | Personal detail found: LONG_NUMBER | 7 | 0.0% | Masked in place with a placeholder. The raw text is not saved to the processed file. |
| 12 | Reviews fully redacted (contact details found) | 14 | 0.0% | Text removed because names cannot be detected by patterns. Rating and date kept for rating analysis; excluded from theme tagging. |
| 13 | Still contains a run of 10+ digits after protection | 2 | 0.0% | Counts only, not printed. Spot-checked when this notebook was built: ticket numbers and gibberish. |
| 14 | Still contains an '@' after protection | 18 | 0.0% | Counts only, not printed. Spot-checked when this notebook was built: brand mentions, times and gibberish. Names inside other reviews cannot be caught, so the README says anonymity is not guaranteed. |
| 15 | Very short text (2 words or fewer) | 43,127 | 64.9% | Kept for rating and volume analysis. Not sent for theme tagging. |
| 16 | Emoji or symbol-only text (no letters) | 1,932 | 2.9% | Kept for ratings. Flagged has_letters = False and excluded from tagging. |
| 17 | Hindi (Devanagari) script | 692 | 1.0% | Kept and flagged. The LLM step can read it, but volume is small. |
| 18 | Review text repeats another review in the same app (extra copies) | 37,186 | 55.9% | Kept, not deleted. Short phrases like 'good' are repeated by real users. Flagged with text_repeat_count. |
| 19 | Possible copy-paste or spam (6+ words, repeated 3+ times) | 8 | 0.0% | Kept and flagged through text_repeat_count. Reviewed again in Phase 5. |
| 20 | Reviews selected for theme tagging (tag_candidate) | 13,933 | 21.0% | Flagged. Phase 3 tags only these, and removes repeated texts before tagging to save compute. |
| 21 | Review text not stored in the processed file (not needed for theme analysis) | 52,542 | 79.0% | Replaced with [not stored]. Reason: some reviews are just a person's name, which patterns cannot detect. Ratings, dates and helper columns are kept for these reviews. |

## Observations (not defects)

- Developer reply rates differ widely by app (BHIM 99.9%, Paytm 95.9%, CRED 44.2%, PhonePe 25.2%, Google Pay 8.6%). Ratings can change after a reply, so comparisons between apps need this caveat.
- PhonePe on 2026-09-18: 31% of 632 reviews were 1-star (app average 9%). To investigate in Phase 5. Cause not yet known.
- The first collection run capped each app at 5,000 reviews, which gave windows from 10 to 151 days. It was replaced by a fixed 60-day window for every app (see the collection note).
