import sqlite3
import pandas as pd
import os

def setup_database(csv_path, db_path):
    print(f"Connecting to SQLite database at {db_path}...")
    conn = sqlite3.connect(db_path)
    
    print(f"Loading data from {csv_path} into database...")
    df = pd.read_csv(csv_path)
    
    # Write the dataframe to a SQL table named 'business_metrics'
    df.to_sql('business_metrics', conn, if_exists='replace', index=False)
    print("✅ Table 'business_metrics' successfully created and populated!")
    
    return conn

def run_sql_query(conn, query_path):
    with open(query_path, 'r') as file:
        query = file.read()
    
    print(f"\n--- Executing query from {query_path} ---")
    # pandas read_sql makes the SQL output look like a neat table
    result_df = pd.read_sql_query(query, conn)
    print(result_df)
    return result_df

if __name__ == "__main__":
    # Create a database folder if it doesn't exist
    os.makedirs('data/db', exist_ok=True)
    
    CSV_FILE = 'data/processed/cleaned_business_data.csv'
    DB_FILE = 'data/db/ecommerce.db'
    SQL_FILE_1 = 'sql/monthly_kpis.sql'
    SQL_FILE_2 = 'sql/anomaly_analysis.sql'
    
    # 1. Setup the database
    conn = setup_database(CSV_FILE, DB_FILE)
    
    # 2. Run the SQL queries
    if os.path.exists(SQL_FILE_1) and os.path.exists(SQL_FILE_2):
        run_sql_query(conn, SQL_FILE_1)
        run_sql_query(conn, SQL_FILE_2)
    else:
        print("❌ Please create the SQL files in the 'sql/' folder first!")
        
    conn.close()