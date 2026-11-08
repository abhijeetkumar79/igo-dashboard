# IGO Market Intelligence Dashboard — 2026

India ke ride-hailing aur logistics market (Rapido, Uber, Ola, Porter) ka data analysis,
jisse IGO decide kar sake ki kis city mein focus karna chahiye aur kaunsa segment
(bike, auto, cab, logistics) sabse zyada opportunity de sakta hai.

---

## Objective

IGO ko 6 major Indian cities mein expansion/focus plan karna hai. Is project ka goal:

1. Har city ka fare benchmark (per-km rate, base fare) samajhna
2. Har city ka demand proxy nikaalna
3. Dono ko combine karke ek City Opportunity Score banana
4. Manager ke liye ek interactive dashboard dena

---

## Cities Analyzed

| City | Type |
|---|---|
| Bengaluru | Silicon Hub |
| Delhi NCR | Metro (High Volume) |
| Mumbai | Metro (High Fare) |
| Hyderabad | Silicon Hub (Verified Demand) |
| Pune | Silicon Hub |
| Chennai | Metro |

---

## Platforms Analyzed

- Rapido — Bike taxi + Auto (India ka largest bike taxi player)
- Uber — Go (cab) + Moto (bike)
- Ola — Mini (cab) + Auto
- Porter — Intra-city logistics (2W / 3W / Tata Ace)

---

## Data Sources

### 1. 2026 Fare Benchmark (igo_fare_benchmark_2026.csv)
- 49 data points, 6 cities, 4 platforms
- Sources: 2026 public fare guides, published rate cards
- Confidence column:
  - verified = city-specific source se liya gaya (16 rows)
  - estimate = national range ka midpoint (33 rows)

### 2. Rapido 2025 Actual Dataset (rapido_city_summary_2025.csv)
- 30,000 bookings, July 2025
- 5 cities, 2 vehicle types (Bike, Auto)
- Important: Ye dataset synthetic hai (Kaggle par clearly mention hai).
  Iska use sirf analysis pipeline test karne ke liye kiya gaya hai.
  Real data aane par same code chalega.
- Metrics extracted:
  - City-wise total bookings, completed, cancelled, incomplete
  - Completion rate
  - Per-km rate (mean + median)
  - TAT (Vehicle + Customer turnaround time)
  - Peak hour distribution
  - Incomplete ride reasons

### 3. City Opportunity Score (igo_city_opportunity_score_v3.csv)
- 6 cities ranked
- Formula (balanced weights):
  Score = 0.60 * Demand Score
        + 0.25 * Fare Score
        + 0.15 * Logistics Score
        + Verified Bonus (+15 if actual demand data available)

---

## Key Results

| Rank | City | Score | Key Insight |
|---|---|---|---|
| 1 | Hyderabad | 63.7 | Verified demand (Rapido 1M+ rides/day), supply gap (82.01% completion) |
| 2 | Mumbai | 58.9 | Highest fare headroom (Rs 10+/km), intense competition |
| 3 | Bengaluru | 56.6 | Strong demand, but Rapido ka home market |
| 4 | Delhi NCR | 53.9 | Largest volume, regulatory complexity |
| 5 | Chennai | 37.9 | Lower demand proxy |
| 5 | Pune | 37.9 | Lower demand proxy |

### Recommendation
- Hyderabad — pilot start karo (supply gap fill karo)
- Mumbai — premium segment test karo
- Bengaluru / Delhi NCR — phase 2
- Chennai / Pune — deprioritize

---

## Dashboard (Streamlit)

### Features
5 interactive tabs:

1. City Ranking — Opportunity score bar chart + top city metric
2. Rapido 2025 (Actual) — Real bookings, completion %, cancellation %, per-km rate, TAT
3. 2026 Fare Estimates — Platform-wise per-km comparison
4. 2025 vs 2026 Comparison — Actual vs estimate side-by-side
5. Raw Data — Saare CSV tables

### Filters (Sidebar)
- City multi-select
- Platform multi-select

---

## Tech Stack

| Layer | Tool |
|---|---|
| Data Processing | Python, Pandas, NumPy |
| Visualization | Plotly Express |
| Dashboard | Streamlit |
| Data Storage | CSV |

---

## How to Run (Local)

### 1. Install dependencies
pip install streamlit pandas plotly

### 2. Run dashboard
python -m streamlit run dashboard_v2.py

### 3. Open browser
http://localhost:8501

---

## Project Structure

IGO_project/
  igo_fare_benchmark_2026.csv        -> 2026 public fare estimates
  rapido_city_summary_2025.csv       -> Rapido 2025 synthetic data summary
  igo_city_opportunity_score_v3.csv  -> Final city ranking
  generate_csv.py                    -> Creates 2026 fare CSV
  analyze_rapido_data.py             -> Analyzes Rapido dataset
  opportunity_score_v3.py            -> City scoring script
  dashboard_v2.py                    -> Streamlit dashboard
  README.md                          -> This file

---

## Limitations (Honest Disclosure)

1. Rapido raw data publicly available nahi hai. Jo dataset use kiya wo
   Kaggle par synthetic hai. Real booking data ke liye IGO ka internal data
   ya paid market reports chahiye.

2. 2026 fare estimates public guides se hain, live platform rates nahi.
   Live rates ke liye Apify scraper ($5/1000 results) ya manual sampling
   recommended hai.

3. Synthetic data ki nishaniyan:
   - Peak hours uniform hain (3 AM peak dikh raha hai — real mein nahi hota)
   - TAT sab cities mein same
   - Incomplete reasons barabar hain

   Isliye peak hour analysis aur TAT analysis ko manager ko
   decision-making ke liye use nahi karna chahiye.

---

## Next Steps

1. IGO ka internal data pull karo — app booking/search data
2. Hyderabad mein 1-month pilot — 50 drivers, supply gap fill
3. Apify se real-time fares — Rapido + Uber + Ola
4. Dashboard update — real data integration

---

## Author

IGO Data Science Team
Project: Market Intelligence & Demand-Supply Optimization
Year: 2026

---

## License

Internal use only — IGO company.
