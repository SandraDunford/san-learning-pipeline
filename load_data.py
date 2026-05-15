"""
San's Learning Pipeline - Loader Script
Loads daily log data from Excel into PostgreSQL staging table
"""

import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

# ============================================================
# CONFIGURATION
# ============================================================

# Database connection details
DB_USER = 'postgres'
DB_PASSWORD = 'REPLACE_WITH_YOUR_PASSWORD'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'learning_tracker'

# Path to your Excel file — UPDATE THIS to your actual file location
EXCEL_FILE_PATH = r'D:\Work\DATA ANALYSIS\Training\Daily Practice\san_pipeline\Daily Log.csv'

# Target table in PostgreSQL
STAGING_TABLE = 'staging_daily_log'

# ============================================================
# MAIN SCRIPT
# ============================================================

def load_data():
    """Read Excel file and load into PostgreSQL staging table."""
    
    print("=" * 50)
    print(f"SAN'S LEARNING PIPELINE - Loader Script")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    # --- STEP 1: Read the Excel file ---
        # --- STEP 1: Read the CSV file ---
    try:
        print("\n[STEP 1] Reading CSV file...")
        
        # Define the column names manually since the CSV has no header row
        col_names = ['log_date', 'topic', 'hours_spent', 'confidence_level', 'notes']
        
        # Read CSV without treating the first row as headers
        df = pd.read_csv(EXCEL_FILE_PATH, header=None, names=col_names)
        
        # Convert date column to proper datetime format
        df['log_date'] = pd.to_datetime(df['log_date'], errors='coerce')
        
        # Remove rows where the date is empty (blank rows at bottom)
        df = df.dropna(subset=['log_date'])
        
        print(f"   Found {len(df)} rows in CSV file.")
        print(f"   Columns: {list(df.columns)}")
        
    except FileNotFoundError:
        print("   ERROR: CSV file not found. Check the EXCEL_FILE_PATH setting.")
        return
    except Exception as e:
        print(f"   ERROR reading CSV: {e}")
        return

    # --- STEP 2: Connect to PostgreSQL ---
    try:
        print("\n[STEP 2] Connecting to PostgreSQL...")
        conn_str = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        engine = create_engine(conn_str)
        
        # Test the connection
        with engine.connect() as test_conn:
            print("   Connection successful!")
            
    except Exception as e:
        print(f"   ERROR connecting to database: {e}")
        print("   Check that PostgreSQL is running and credentials are correct.")
        return

    # --- STEP 3: Load data into staging table ---
    try:
        print(f"\n[STEP 3] Loading data into '{STAGING_TABLE}'...")
        
        df.to_sql(
            name=STAGING_TABLE,
            con=engine,
            if_exists='append',
            index=False
        )
        
        print(f"   Successfully loaded {len(df)} rows into {STAGING_TABLE}.")
        
    except Exception as e:
        print(f"   ERROR loading data: {e}")
        print("   Check that the staging table exists and column names match.")
        return

    # --- STEP 4: Run a quick data quality check ---
    try:
        print("\n[STEP 4] Running data quality check...")
        
        quality_query = """
        SELECT 
            COUNT(*) AS total_rows,
            SUM(CASE WHEN hours_spent < 0 THEN 1 ELSE 0 END) AS negative_hours,
            SUM(CASE WHEN confidence_level NOT BETWEEN 1 AND 6 THEN 1 ELSE 0 END) AS invalid_confidence,
            SUM(CASE WHEN log_date IS NULL THEN 1 ELSE 0 END) AS missing_dates
        FROM staging_daily_log;
        """
        
        quality_df = pd.read_sql(quality_query, engine)
        
        total = quality_df['total_rows'].iloc[0]
        neg_hours = quality_df['negative_hours'].iloc[0]
        bad_conf = quality_df['invalid_confidence'].iloc[0]
        miss_date = quality_df['missing_dates'].iloc[0]
        
        print(f"   Total rows in staging: {total}")
        print(f"   Negative hours: {neg_hours}")
        print(f"   Invalid confidence (outside 1-6): {bad_conf}")
        print(f"   Missing dates: {miss_date}")
        
        if neg_hours > 0 or bad_conf > 0 or miss_date > 0:
            print("   WARNING: Data quality issues detected! Review before promoting to fact table.")
        else:
            print("   All checks passed. Data looks clean.")
            
    except Exception as e:
        print(f"   Could not run quality check: {e}")

    # --- COMPLETE ---
    print("\n" + "=" * 50)
    print(f"Pipeline complete at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)


# ============================================================
# RUN THE SCRIPT
# ============================================================
if __name__ == "__main__":
    load_data()
