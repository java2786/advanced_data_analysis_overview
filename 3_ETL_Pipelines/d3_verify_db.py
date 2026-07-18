import sqlite3, pandas as pd  
  
conn = sqlite3.connect("swiftkart.db")  
check = pd.read_sql("SELECT city, COUNT(*) AS orders, ROUND(SUM(revenue),2) AS revenue FROM clean_sales GROUP BY city", conn)  
print(check)  
conn.close() 