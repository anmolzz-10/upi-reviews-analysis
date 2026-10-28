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
- **Privacy:** reviewer names and profile pictures are never stored. The raw file is kept out of this repository because review text can contain personal details. Personal details are masked before any text is shared or analysed.
- **Reproducing it:** the raw reviews are not in the repo. Running `notebooks/01_collect.ipynb` collects a fresh 60-day window counted back from the run date, so numbers will differ from those in this README.

More detail is in [`data/raw/collection_note.md`](data/raw/collection_note.md).

## Approach

1. **Collect** 60 days of reviews for five apps (done).
2. **Clean, profile and mask:** handle duplicates and low-information text, mask phone numbers, UPI IDs and similar personal details, and log every issue and decision.
3. **Tag complaint themes** on the detailed reviews (most reviews are only a word or two) using an open-weight LLM, saved as structured fields.
4. **Validate** the tags against about 150 hand-labelled reviews and a classical TF-IDF + logistic regression baseline.
5. **Analyse** theme share by app, trends across time and app versions, and a regression of rating on themes to rank which problems cost the most rating points.
6. **Deliver** a live Streamlit app, an Excel stakeholder summary, and a Power BI dashboard.

## Progress

- [x] Environment and repo setup
- [x] Phase 1: collect reviews (66,475 reviews, 60-day window)
- [ ] Phase 2: clean, profile and mask
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
│   └── processed/    # masked, analysis-ready tables
├── notebooks/        # numbered notebooks, run in order
├── app/              # Streamlit app
├── excel/            # stakeholder summary workbook
├── powerbi/          # Power BI file and screenshots
├── docs/             # decision log, data-quality log and notes
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
- Many reviews are very short and repeated (about 53% share their exact text with another review for the same app), so theme analysis relies on the smaller set of detailed reviews.
- A regression shows association, not proof of cause.
- Theme tags come from an LLM and are checked against a hand-labelled sample. They are not perfect.
- Masking removes common personal details but cannot guarantee full anonymity.

## How I built this

I use Claude, an AI assistant, throughout this project. It writes most of the code and helps with planning and debugging. I make the final call on every decision, and [`docs/decision-log.md`](docs/decision-log.md) records each one, including which ideas were mine, which were AI suggestions I accepted, and which I rejected. The theme definitions, the hand-labelled validation sample and the recommendations are my own work.

## Author

Anmol Singh Bhatia, [LinkedIn](https://linkedin.com/in/anmols2003), [GitHub](https://github.com/anmolzz-10)
