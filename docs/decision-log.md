# Decision log

A running record of the project's decisions, kept as the work happens. Each row says what was decided, what else was considered, why, and **whose idea it was**.

**Source labels**
- **Mine:** my idea or my constraint
- **AI, accepted:** suggested by the AI assistant, and I agreed
- **AI, rejected:** suggested by the AI assistant, and I said no
- **Joint:** shaped by back-and-forth

**Division of work:** I direct the project and make the final call on each decision. Claude (an AI assistant) does most of the implementation, analysis and drafting, and explains each step so I can defend it. The labels above record whose idea each decision was.

## Decisions

| # | Phase | Decision | Options considered | Why | Source |
|---|---|---|---|---|---|
| 1 | Planning | Use real, self-collected data | Synthetic data generator; Olist (Kaggle); scraped reviews | Insights from synthetic data are programmed in. Olist is on thousands of portfolios. | Joint: AI raised the synthetic-data problem; I rejected Olist as overused |
| 2 | Planning | Drop dbt and heavy SQL engineering | dbt marts; plain SQL; pandas | Too much engineering for an analyst role, and Python is my strongest skill | Mine (AI agreed) |
| 3 | Planning | Include Power BI as one part of the project, not the whole | Skip it; make it the main tool | Most requested BI tool in job postings, but not the centre of the work | Mine |
| 4 | Planning | Live link via Streamlit; Power BI shown with `.pbix`, screenshots and a video | Publish Power BI online | Personal accounts usually can't publish Power BI online | Joint: I required a live link; AI proposed Streamlit for it |
| 5 | Planning | Domain: UPI / fintech apps | Quick-commerce apps; government data; football | BFSI leads analyst hiring in the sources checked (directional only); fills a finance gap on my CV | AI, accepted (I asked it to choose from job-market evidence) |
| 6 | Planning | Keep LLM tagging; no agentic AI or RAG; validate against a labelled sample | Drop the LLM; add agents | I want to avoid GenAI depth, but LLM extraction is a current analyst skill | Joint: I set the boundary, AI added the validation step |
| 7 | Planning | Free and open-source tools only | Paid APIs; cloud services | Must be reproducible by a fresher at no cost | Mine |
| 8 | Setup | conda-forge environment plus `requirements.txt`, tested on a fresh environment | `environment.yml` only; default Anaconda channels | Terms-of-service prompt blocked the default channels on this PC | AI, accepted |
| 9 | Setup | Public repo; raw review file kept out of Git | Commit the raw CSV | Review text can contain phone numbers or UPI IDs | AI, accepted |
| 10 | Phase 1 | Fixed 60-day window for every app | 5,000 reviews per app | First run gave windows from 10 to 151 days, so apps weren't comparable | AI spotted it from my output; I re-ran with the fix |
| 11 | Phase 1 | Never store reviewer names or pictures | Keep them and drop later | Privacy by default | AI, accepted |
| 12 | Phase 2 | Keep every row for rating analysis; tag only reviews with enough text: letters, and either 6+ words or rating 1-2 with 3+ words (13,933 reviews) | Tag everything; delete duplicates | 65% of reviews are two words or fewer; the rest carry the complaint text. The rating 1-2 rule keeps short complaints like "payment failed again". | AI proposed from the data profile; I accepted |
| 13 | Later | Optional weekly refresh (GitHub Actions) | No automation | The data source is live, so a monitor has a real purpose. Needs a test run first. | **Pending: raised by me, decide after Phase 6** |
| 14 | Phase 2 | Contact details (phone, UPI ID, email, @handle) cause the whole review text to be redacted; reference numbers are masked in place | Mask only the matched pattern | People who paste contact details often sign with a name, and patterns cannot catch names | AI proposed during Phase 2; accepted when I ran the notebook and sent back the results |
| 15 | Phase 2 | Keep review text in the processed file only for the tagging candidates | Keep all text | Some reviews are just a person's name. The scan found them, and patterns cannot detect names. Rating analysis does not need the text. | AI proposed after the scan found names typed as reviews; accepted when I ran the notebook and sent back the results |
| 16 | Process | AI carries out the implementation and drafting; I direct, review and decide. The README describes this accurately. | Doing every step myself | Productivity, and I can still explain and defend each step | Mine |

## Phase notes

For each phase, three short lines written at the end of the phase (drafted by Claude, reviewed by me).

### Phase 1: Collect
- **What I did:** ran the scraper twice. The first run capped at 5,000 reviews per app, and the second used a 60-day window. Collected 66,475 reviews.
- **What I checked myself:** asked what changed between the two runs (the short-window warnings disappeared) and had the totals, rating mixes and app IDs cross-checked. The cross-check found the collection note still said 12 months, which was corrected.
- **What surprised me:** BHIM's recent reviews average 2.77 against 4.47 on its Play Store page, and CRED 3.36 against 4.76. About 53% of reviews repeat another review's exact text for the same app (56% ignoring case and punctuation), mostly one or two words.

### Phase 2: Clean, profile and protect
- **What I did:** profiled the 66,475 reviews, found no duplicate IDs, blank text or invalid ratings, protected personal details, and flagged 13,933 reviews for theme tagging.
- **What I checked myself:** ran the notebook locally and sent the outputs back for comparison. Every log number and the 13,933 tagging candidates matched the reference run.
- **What surprised me:** only 21 reviews contained personal details, but some people simply type their own name as the review. About 56% of reviews repeat another review's text (ignoring case and punctuation). Developer reply rates range from 8.6% (Google Pay) to 99.9% (BHIM). PhonePe had one day (18 Sep) where 31% of 632 reviews were 1-star against a 9% average.

_(Add a section per phase as we go.)_

## Habit

After each phase, Claude adds any new rows above and drafts the three lines. I read them and correct anything that is not accurate.
