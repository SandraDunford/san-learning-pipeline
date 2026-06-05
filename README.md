# San's Learning Pipeline

A personal Analytics Engineering portfolio project tracking daily learning progress against the Benner Model (Novice to Expert).

This project demonstrates an end-to-end analytics engineering workflow using a personal learning dataset.

Daily learning activities are recorded in Excel, exported to CSV, loaded into PostgreSQL using Python, validated through staging tables, transformed into analytical structures, and prepared for reporting and analysis.

## Goal
Develop skills that support a transition from Senior Nurse Leader to Healthcare Analytics/Data Engineer.

## Architecture
This project implements a 3-layer data warehouse pattern:
1. **Staging** (`staging_daily_log`): Raw data ingestion from CSV.
2. **Fact** (`fact_daily_log`): Cleaned, validated, and typed data.
3. **Mart** (`mart_learning_analytics`): Enriched data joined with dimensions (Date) and business logic.

## Tech Stack
- **Language:** Python 3.x
- **Database:** PostgreSQL
- **Tools:** Pandas, SQLAlchemy, Git/GitHub, Excel, VS Code
- **Data Source:** Daily Learning Logs (CSV) Benner Model (CSV)

## How to Run
1. **Update Configuration:** Edit `load_data.py` with your database credentials and file paths.
2. **Install Dependencies:**
   ```bash
   pip install pandas sqlalchemy psycopg2-binary openpyxl
