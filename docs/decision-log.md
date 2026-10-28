# Decision log

A running record of the project's decisions, kept as the work happens. Each row says what was decided, what else was considered, why, and **whose idea it was**.

**Source labels**
- **Mine:** my idea or my constraint
- **AI, accepted:** suggested by the AI assistant, and I agreed
- **AI, rejected:** suggested by the AI assistant, and I said no
- **Joint:** shaped by back-and-forth

> Draft written from our planning conversation. Rows marked **[confirm]** are my best reading of what happened. Edit any label or wording that isn't accurate before pushing.

## Decisions

| # | Phase | Decision | Options considered | Why | Source |
|---|---|---|---|---|---|
| 1 | Planning | Use real, self-collected data | Synthetic data generator; Olist (Kaggle); scraped reviews | Insights from synthetic data are programmed in. Olist is on thousands of portfolios. | Joint: AI raised the synthetic-data problem; I rejected Olist as overused |
| 2 | Planning | Drop dbt and heavy SQL engineering | dbt marts; plain SQL; pandas | Too much engineering for an analyst role, and Python is my strongest skill | Mine (AI agreed) |
| 3 | Planning | Include Power BI as one part of the project, not the whole | Skip it; make it the main tool | Most requested BI tool in job postings, but not the centre of the work | Mine |
| 4 | Planning | Live link via Streamlit; Power BI shown with `.pbix`, screenshots and a video | Publish Power BI online | Personal accounts usually can't publish Power BI online | Joint [confirm] |
| 5 | Planning | Domain: UPI / fintech apps | Quick-commerce apps; government data; football | BFSI leads analyst hiring in the sources checked (directional only); fills a finance gap on my CV | AI, accepted (I asked it to choose from job-market evidence) |
| 6 | Planning | Keep LLM tagging; no agentic AI or RAG; validate against hand labels | Drop the LLM; add agents | I want to avoid GenAI depth, but LLM extraction is a current analyst skill | Joint: I set the boundary, AI added the validation step |
| 7 | Planning | Free and open-source tools only | Paid APIs; cloud services | Must be reproducible by a fresher at no cost | Mine |
| 8 | Setup | conda-forge environment plus `requirements.txt`, tested on a fresh environment | `environment.yml` only; default Anaconda channels | Terms-of-service prompt blocked the default channels on this PC | AI, accepted |
| 9 | Setup | Public repo; raw review file kept out of Git | Commit the raw CSV | Review text can contain phone numbers or UPI IDs | AI, accepted [confirm] |
| 10 | Phase 1 | Fixed 60-day window for every app | 5,000 reviews per app | First run gave windows from 10 to 151 days, so apps weren't comparable | AI spotted it from my output; I re-ran with the fix |
| 11 | Phase 1 | Never store reviewer names or pictures | Keep them and drop later | Privacy by default | AI, accepted |
| 12 | Phase 2 | Keep every row for rating analysis; tag only detailed reviews for themes | Tag everything; delete duplicates | 65% of reviews are two words or fewer; the rest carry the complaint text | **Pending: decide in Phase 2** |
| 13 | Later | Optional weekly refresh (GitHub Actions) | No automation | The data source is live, so a monitor has a real purpose. Needs a test run first. | **Pending: raised by me, decide after Phase 6** |

## Phase notes

For each phase, three short lines written at the end of the phase, in my own words.

### Phase 1: Collect
- **What I did:** ran the scraper twice. The first run capped at 5,000 reviews per app, and the second used a 60-day window. Collected 66,475 reviews.
- **What I checked myself:** _fill in (for example: that app totals add up, that rating mixes sum to 100%)_
- **What surprised me:** BHIM's recent reviews average 2.77 against 4.47 on its Play Store page, and CRED 3.36 against 4.76. About 53% of reviews repeat another review's text for the same app, mostly one or two words.

### Phase 2: Clean, profile and mask
- **What I did:** _fill in_
- **What I checked myself:** _fill in_
- **What surprised me:** _fill in_

_(Add a section per phase as we go.)_

## Habit

After each phase, spend two minutes: add any new rows above, and write the three lines. Edit what the AI drafts so it is accurate and sounds like you.
