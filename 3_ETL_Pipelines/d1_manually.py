import pandas as pd  
  
df = pd.read_csv("swiftkart_sales.csv")  
  
# Take 20 orders and make them messy, like real daily files  
messy = df.sample(20, random_state=7).copy()  
messy["city"] = messy["city"].str.lower()          # pune, chennai...  
messy.loc[messy.index[:3], "customer_rating"] = None   # missing ratings  
messy = pd.concat([messy, messy.head(4)])          # duplicate rows  
messy["city"] = " " + messy["city"] + "  "         # extra spaces  
  
messy.to_csv("daily_sales_raw.csv", index=False)  
print("Messy daily file created:", messy.shape) 