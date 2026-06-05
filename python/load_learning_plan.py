"""
San's Learning Pipeline - Learning Plan Loader
Loads Learning Plan data from CSV into PostgreSQL staging table
"""

import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

# ============================================================
# CONFIGURATION
# ============================================================

# Database connection details
DB_USER = 'postgres'
DB_PASSWORD = 'ADD YOUR PASSWORD HERE'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'learning_tracker'

# Path to your CSV file — UPDATE THIS to your actual file location
CSV_FILE_PATH = r'D:\Work\DATA ANALYSIS\Training\Daily Practice\san_pipeline\learning_plan.csv'

# Target table in PostgreSQL
STAGING_TABLE = 'staging_benchmarks'

# ============================================================
# MAIN SCRIPT
# ============================================================

def load_learning_plan():
    """Read CSV file and load into PostgreSQL staging table."""
    
    print("=" * 50)
    print(f"SAN'S LEARNING PIPELINE - Learning Plan Loader")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    # --- STEP 1: Read the CSV file ---
    try:
        print("\n[STEP 1] Reading CSV file...")
        
        # Read CSV treating the first row as headers
        df = pd.read_csv(CSV_FILE_PATH)

        # Remove completely blank rows
        df = df.dropna(how='all')
        
        print(f"   Found {len(df)} rows in CSV file.")
        print(f"   Columns: {list(df.columns)}")
        print("\nPreview:")
        print(df.head())
        
    except FileNotFoundError:
        print("   ERROR: CSV file not found. Check the CSV_FILE_PATH setting.")
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
        print("\n[STEP 4] Data Quality Checks...")

        missing_topics = df['topic_name'].isna().sum()
        print(f"Missing topics: {missing_topics}")

        missing_objectives = df['learning_objective'].isna().sum()
        print(f"Missing objectives: {missing_objectives}")

        print("\nStatus Distribution:")
        print(df['status'].value_counts())

        duplicates = df.duplicated(
            subset=['topic_name', 'learning_objective']
        ).sum()

        print(f"Duplicate objectives: {duplicates}")

    except Exception as e:
        print(f"Quality check failed: {e}")

    # --- COMPLETE ---
    print("\n" + "=" * 50)
    print(f"Pipeline complete at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)


# ============================================================
# RUN THE SCRIPT
# ============================================================
if __name__ == "__main__":
    load_learning_plan()
