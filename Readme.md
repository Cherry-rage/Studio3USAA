 # Banking Dive Fraud Intelligence

 _Credits: Gustavo Franco · Abhi Veerthineni · Nick Jones · Riya Vadadoria_

 ## Project Overview
 - Goal: surface fraud-facing signals from recent Banking Dive coverage to inform narrative storytelling and prioritization for DTSC 3602 deliverables.
 - Inputs:
   - `banking_dive_scraper.ipynb` for article harvesting.
   - `banking_dive_fraud_visualizations.ipynb` to explore the high-risk subset and prototype visuals.
   - `analysis.ipynb` (new “analysis” notebook) consolidates text mining and metrics referenced below.
   - CSV files under `data/` with full article corpus, fraud-augmented labels, and the fraud-only subset.

 ## Snapshot Metrics
 | Metric | Value |
 | --- | --- |
 | Articles scraped | 200 |
 | Fraud-flagged articles | 16 (8 Wire/Check Fraud, 8 Money Laundering) |
 | Risk mix | 8 High risk vs. 8 Low risk (no Medium flags in current sample) |
 | Distinct fraud categories detected | 2 |

 ## Key Findings
 1. **Wire + check fraud dominates** the current Banking Dive coverage, splitting evenly with money-laundering mentions and highlighting continued vulnerability in payments rails.
 2. **Legal and regulatory actions are the storytelling hook**: most fraud articles couple enforcement actions (CFPB, activist lawsuits) with governance failures, giving us ready-made narratives around compliance breakdowns.
 3. **Geographic and demographic specificity stands out**: repeated references to Chinese American employees, South Carolina cases, and branch-level schemes suggest readers respond to localized, people-forward framing.

 ## Common Trends Observed
 - Fraud stories cluster around merger-and-acquisition flashpoints (Comerica–Fifth Third, Fulton–Blue Foundry) where due diligence gaps are exposed.
 - Enforcement bodies (CFPB, state AGs, local prosecutors) drive momentum, creating clear timelines for storytelling.
 - Risk levels polarize: articles are either clearly high-risk enforcement events or low-risk governance notes—there is little middle ground, signaling that our pipeline should expect “spike” coverage rather than steady volume.

 ## Top 5 Keywords / Phrases
 - **Keywords (unigrams)**: Chinese, bank, check, said, employees.
 - **Phrases (bigrams)**: “Chinese American,” “Prosecutors said,” “Chinese Chinese,” “American employees,” “Plaintiffs said.”

 ## Top 3 Fraud Trends To Track
 1. **Wire & Check Fraud Rings** – Half of all flagged stories cite overlapping wire/check abuse, often tied to branch-level overrides or coerced employees.
 2. **Money-Laundering via Cross-Border Relationships** – The other half of the sample highlights laundering concerns, especially when international customer bases intersect with weak KYC controls.
 3. **Regulatory Settlements Targeting Membership / Fee Structures** – CFPB vs. MoneyLion and similar cases show regulators zeroing in on fee-based loopholes (membership dues, ancillary services) that mask true APRs.

 ## Next Steps
 - Expand scraping schedule to capture fresh Banking Dive posts weekly; rerun `analysis.ipynb` to refresh metrics.
 - Layer qualitative context (earnings transcripts, enforcement dockets) atop the existing timelines for better narrative pitches.

 ---
