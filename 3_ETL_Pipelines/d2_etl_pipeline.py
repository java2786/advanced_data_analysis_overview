import pandas as pd  
import sqlite3  
from datetime import datetime  
  
def extract(filepath):  
    """E - Read the raw file exactly as it arrived."""  
    df = pd.read_csv(filepath)  
    print(f"Extracted {len(df)} raw rows")  
    return df  
  
def transform(df):  
    """T - Clean and standardize."""  
    # 1. Remove duplicate orders (same order_id appearing twice)  
    df = df.drop_duplicates(subset="order_id")  
  
    # 2. Fix city names: strip spaces, proper case -> ' pune  ' becomes 'Pune'  
    df["city"] = df["city"].str.strip().str.title()  
  
    # 3. Handle missing ratings: fill with the median rating  
    df["customer_rating"] = df["customer_rating"].fillna(df["customer_rating"].median())  
  
    # 4. Add the revenue column (same formula as Session 1 - our single truth)  
    df["revenue"] = df["quantity"] * df["unit_price"] * (1 - df["discount_percent"] / 100)  
  
    # 5. Stamp when this pipeline processed the row (audit trail)  
    df["processed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
  
    print(f"Transformed down to {len(df)} clean rows")  
    return df  
  
def load(df, db_name="swiftkart.db"):  
    """L - Save clean data into a SQLite database."""  
    conn = sqlite3.connect(db_name)  
    df.to_sql("clean_sales", conn, if_exists="append", index=False)  
    conn.close()  
    print(f"Loaded {len(df)} rows into {db_name} -> table clean_sales")  
  
if __name__ == "__main__":  
    raw = extract("daily_sales_raw.csv")  
    clean = transform(raw)  
    load(clean)  
    print("ETL pipeline finished successfully")