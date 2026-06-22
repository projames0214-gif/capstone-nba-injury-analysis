# Project Management Plan — NBA Player Injury & Performance Analysis

## Timeline Overview
- **Assigned:** June 19, 2026
- **Due:** July 2, 2026
- **Total time:** ~2 weeks

---

## Tasks

### Phase 1: Setup & Planning ✅ (June 19–22)
| Task | Est. Time | Target Date | Status |
|---|---|---|---|
| Create GitHub repo | 30 min | June 22 | ✅ Done |
| Write working plan + 10 questions | 1 hr | June 22 | ✅ Done |
| Download and commit datasets | 30 min | June 22 | ✅ Done |
| Write project management plan | 30 min | June 22 | ✅ Done |

### Phase 2: Exploratory Data Analysis (June 23–24)
| Task | Est. Time | Target Date | Status |
|---|---|---|---|
| EDA on injury stats dataset | 2 hrs | June 23 | ⬜ |
| EDA on player stats/injuries dataset | 2 hrs | June 23 | ⬜ |
| Identify data quality issues | 1 hr | June 24 | ⬜ |
| Document findings in notebook | 1 hr | June 24 | ⬜ |

### Phase 3: Database Design & ETL (June 24–26)
| Task | Est. Time | Target Date | Status |
|---|---|---|---|
| Design ERD and write DDL | 2 hrs | June 24 | ⬜ |
| Set up PostgreSQL schema | 1 hr | June 24 | ⬜ |
| Write data cleaning scripts (Pandas) | 3 hrs | June 25 | ⬜ |
| Build Airflow DAG for ETL pipeline | 3 hrs | June 25 | ⬜ |
| Load cleaned data into PostgreSQL | 1 hr | June 26 | ⬜ |
| Document ETL process | 1 hr | June 26 | ⬜ |

### Phase 4: Analysis & Visualization (June 26–28)
| Task | Est. Time | Target Date | Status |
|---|---|---|---|
| Write SQL queries to answer 10 questions | 3 hrs | June 26 | ⬜ |
| Sketch dashboard layout | 1 hr | June 27 | ⬜ |
| Build Dash app | 4 hrs | June 27 | ⬜ |
| Add charts and filters to dashboard | 2 hrs | June 28 | ⬜ |

### Phase 5: ML Model — Optional (June 28–29)
| Task | Est. Time | My Target Date | Status |
|---|---|---|---|
| Select features for injury risk model | 1 hr | June 28 | ⬜ |
| Train/test split and model training | 2 hrs | June 29 | ⬜ |
| Evaluate model performance | 1 hr | June 29 | ⬜ |
| Write predictions to database | 1 hr | June 29 | ⬜ |

### Phase 6: Finalization & Presentation (June 29 – July 2)
| Task | Est. Time | Target Date | Status |
|---|---|---|---|
| Polish README | 1 hr | June 30 | ⬜ |
| Write technical report | 2 hrs | June 30 | ⬜ |
| Build slide deck | 2 hrs | July 1 | ⬜ |
| Rehearse presentation | 1 hr | July 1 | ⬜ |
| Live presentation | — | July 2 | ⬜ |

---

## Datasets
- **Primary:** NBA Player Injury Stats 1951–2023
  - Source: kaggle.com/datasets/loganlauton/nba-injury-stats-1951-2023
  - Accessed: June 22, 2026
- **Supplementary:** NBA Player Stats & Injuries 2013–2023
  - Source: kaggle.com/datasets/icliu30/nba-player-stats-and-injured-data-from-13-to-23
  - Accessed: June 22, 2026
- **Non-CSV:** NBA API (nba_api Python package)
  - Source: github.com/swar/nba_api
  - Accessed: June 22, 2026

---

## Technologies
- Python, Pandas
- PostgreSQL
- Apache Airflow
- Dash
- scikit-learn 
- GitHub