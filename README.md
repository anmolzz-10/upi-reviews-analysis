# UPI App Reviews Analysis

**Which complaint themes cost UPI apps the most rating points, and which fix is worth the most?**

> Status: work in progress. Findings, the live app link and the dashboard will be added as each phase is finished. Progress and decisions are tracked openly in [`docs/decision-log.md`](docs/decision-log.md).

## The business problem

UPI apps compete on trust and reliability. A failed payment or a stuck refund shows up first in public reviews, long before it shows up in a company report. This project turns public Play Store reviews for five UPI apps into a ranked list of what to fix first.

**Apps studied:** PhonePe, Google Pay, Paytm, CRED, BHIM

## Data

- **Source:** public Google Play Store reviews, Indian store, English interface setting.
- **Window:** the last 60 days before collection, 28 Aug to 26 Oct 2026, collected on 27 Oct 2026. A fixed window is used so apps can be compared fairly.
- **Size:** 66,475 reviews (PhonePe 29,959, Paytm 21,951, Google Pay 8,559, BHIM 4,257, CRED 1,749).
- **Privacy:** reviewer names and profile pictures are never stored. The raw file is kept out of this repository because review text can contain personal details. In the processed file, reviews with contact details are fully redacted, reference numbers are masked, and review text is kept only for the roughly 14,000 reviews used in theme analysis. Every review keeps its rating, date and helper columns.
- **Reproducing it:** the raw reviews are not in the repo. Running `notebooks/01_collect.ipynb` collects a fresh 60-day window counted back from the run date, so numbers will differ from those in this README.

More detail is in [`data/raw/collection_note.md`](data/raw/collection_note.md).

## Approach

1. **Collect** 60 days of reviews for five apps (done).
2. **Clean, profile and protect:** profile duplicates and low-information text, redact reviews that contain contact details, mask reference numbers, and log every issue and decision.
3. **Tag complaint themes** on the detailed reviews (most reviews are only a word or two) using an open-weight LLM, saved as structured fields.
4. **Validate** the tags against a labelled sample of about 150 reviews and a classical TF-IDF + logistic regression baseline.
5. **Analyse** theme share by app, trends across time and app versions, and a regression of rating on themes to rank which problems cost the most rating points.
6. **Deliver** a live Streamlit app, an Excel stakeholder summary, and a Power BI dashboard.

## Progress

- [x] Environment and repo setup
- [x] Phase 1: collect reviews (66,475 reviews, 60-day window)
- [x] Phase 2: clean, profile and protect (see [`docs/data-quality-log.md`](docs/data-quality-log.md))
- [ ] Phase 3: LLM theme tagging
- [ ] Phase 4: validation
- [ ] Phase 5: analysis and findings
- [ ] Phase 6: Streamlit live app
- [ ] Phase 7: Excel summary
- [ ] Phase 8: Power BI dashboard

## Findings

_To be added after the analysis phase._

## Recommendations

_To be added after the analysis phase._

## Tools

Python (pandas, scikit-learn, statsmodels, plotly), Streamlit, Jupyter, an open-weight LLM via Hugging Face, Excel, Power BI Desktop, Git/GitHub.

## Repository structure

```
upi-reviews-analysis/
├── data/
│   ├── raw/          # collection note only; the raw reviews are kept private
│   ├── interim/      # intermediate files
│   └── processed/    # protected, analysis-ready table (text kept only for tagging candidates)
├── notebooks/        # numbered notebooks, run in order
├── app/              # Streamlit app
├── excel/            # stakeholder summary workbook
├── powerbi/          # Power BI file and screenshots
├── docs/             # decision log and data-quality log
├── requirements.txt
└── environment.yml
```

## How to run it

You need Git and either Miniforge, Miniconda or Anaconda installed.

```
git clone https://github.com/anmolzz-10/upi-reviews-analysis.git
cd upi-reviews-analysis
conda create -n upi-reviews -c conda-forge --override-channels python=3.11
conda activate upi-reviews
pip install -r requirements.txt
```

Open the folder in VS Code, choose the `upi-reviews` interpreter, and run the notebooks in the `notebooks/` folder in numeric order. Start with `01_collect.ipynb`, since the raw data is not included.

## Limitations

- There is no revenue data, so impact is measured in rating points and complaint share, not rupees.
- Public reviews skew toward very happy or very unhappy users and do not represent all users.
- The data is a 60-day snapshot, collected with English interface settings, so it can miss Hindi-language reviews and anything outside the window.
- Many reviews are very short and repeated (about 56% repeat the text of another review for the same app, ignoring case and punctuation), so theme analysis relies on the smaller set of detailed reviews.
- A regression shows association, not proof of cause.
- Theme tags come from an LLM and are checked against a labelled sample. They are not perfect.
- Redaction and masking reduce personal-data risk but cannot guarantee anonymity. Some people type their own name as a review, and a few names inside longer reviews can remain.

## How I built this

I use Claude, an AI assistant, for most of the implementation: code, analysis and drafting. I set the question, scope and tools, review the results, and make the final call on each decision. [`docs/decision-log.md`](docs/decision-log.md) records every decision and whose idea it was, including AI suggestions I accepted and ideas I rejected. How the validation sample was labelled will be described in this repo once that phase is done.

## Author

Anmol Singh Bhatia, [LinkedIn](https://linkedin.com/in/anmols2003), [GitHub](https://github.com/anmolzz-10)
