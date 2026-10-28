# UPI App Reviews Analysis

**Which complaint themes cost UPI apps the most rating points, and which fix is worth the most?**

> Status: work in progress. Findings, the live app link and the dashboard will be added as each phase is finished.

## The business problem

UPI apps compete on trust and reliability. A failed payment or a stuck refund shows up first in public reviews, long before it shows up in a company report. This project turns thousands of public Play Store reviews for five UPI apps into a ranked list of what to fix first.

**Apps studied:** PhonePe, Google Pay, Paytm, CRED, BHIM

## Approach

1. **Collect** public Play Store reviews (rating, text, date, app version). Reviewer names are not stored.
2. **Clean and profile** the data, with a data-quality log of every issue and decision.
3. **Tag complaint themes** (payment failure, refund delay, login/KYC, crashes, support, fraud/security, rewards, UI) using an open-source LLM, saved as structured fields.
4. **Validate** the tags against 150 hand-labelled reviews and a classical TF-IDF + logistic regression baseline.
5. **Analyse** theme share by app, trends across time and app versions, and a regression of rating on themes to rank which problems cost the most rating points.
6. **Deliver** a live Streamlit app, an Excel stakeholder summary, and a Power BI dashboard.

## Progress

- [x] Environment and repo setup
- [ ] Phase 1: collect reviews
- [ ] Phase 2: clean and profile
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
│   ├── raw/          # collected reviews, untouched
│   ├── interim/      # intermediate files
│   └── processed/    # final analysis-ready tables
├── notebooks/        # numbered notebooks, run in order
├── app/              # Streamlit app
├── excel/            # stakeholder summary workbook
├── powerbi/          # Power BI file and screenshots
├── docs/             # data-quality log and notes
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

Open the folder in VS Code, choose the `upi-reviews` interpreter, and run the notebooks in the `notebooks/` folder in numeric order.

## Limitations

- There is no revenue data, so impact is measured in rating points and complaint share, not rupees.
- Public reviews skew toward very happy or very unhappy users and do not represent all users.
- A regression shows association, not proof of cause.
- Theme tags come from an LLM and are checked against a hand-labelled sample. They are not perfect.

## How AI was used

AI assistants helped with code and planning. Every query, measure and finding in this repo has been checked and can be explained by the author. The LLM theme-tagging step is validated against hand-labelled data, as described above.

## Author

Anmol Singh Bhatia, [LinkedIn](https://linkedin.com/in/anmols2003), [GitHub](https://github.com/anmolzz-10)
