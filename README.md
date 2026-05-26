# San's Learning Pipeline

A personal Analytics Engineering portfolio project tracking daily learning progress against the Benner Model (Novice to Expert).

## Goal
Transition from Senior Nurse Leader to Healthcare Analytics Engineer by building and maintaining a mini ETL pipeline.

## Architecture
This project implements a 3-layer data warehouse pattern:
1. **Staging** (`staging_daily_log`): Raw data ingestion from CSV.
2. **Fact** (`fact_daily_log`): Cleaned, validated, and typed data.
3. **Mart** (`mart_learning_analytics`): Enriched data joined with dimensions (Date) and business logic.

## Tech Stack
- **Language:** Python 3.x
- **Database:** PostgreSQL
- **Tools:** Pandas, SQLAlchemy, Git/GitHub
- **Data Source:** Daily Learning Logs (CSV)

## How to Run
1. **Update Configuration:** Edit `load_data.py` with your database credentials and file paths.
2. **Install Dependencies:**
   ```bash
   pip install pandas sqlalchemy psycopg2-binary openpyxl
