import pandas as pd
import matplotlib.pyplot as plt

# df = pd.read_csv("swiftkart_sales.csv")
df = pd.read_json("swiftkart_sales.json")

print("\t Shape")
print(df.shape)


print("\t Head")
print(df.head()) # initial 5 entries


print("\n============== Info ==============")
print(df.info())



# revenue = quantity * price * (1-discount/100)
df['revenue'] = df['quantity']*df['unit_price']*(1-df['discount_percent']/100)

print("\n============== Revenue ==============")
print(df[['order_id', 'category', 'quantity','unit_price','discount_percent','revenue']].head(4))


print("\n============== Data Exploration ==============")
print("Mean (average) of revenue: ",round(df['revenue'].mean(), 2))
print("Median (middle) of revenue: ",round(df['revenue'].median(), 2))
print("Median (most common category): ",df['category'].mode())

print("Describe: ",df['revenue'].describe())


print("\n============== GroupBy ==============")
city_revenue = df.groupby('city')['revenue'].sum().sort_values(ascending=False)
print(city_revenue.head())

pm_revenue = df.groupby('payment_mode')['revenue'].count().sort_values(ascending=False)
print(pm_revenue.head())

print(f"Q1. Total Revenue: {round(df['revenue'].sum(), 2)}")
print(f"Q2. Top City: {city_revenue.index[0]}")
print(f"Q3. Customer Rating: {round(df['customer_rating'].mean(), 2)} / 5")

# city_revenue.plot(kind="bar", title="SwiftKart Revenue by City")
# plt.ylabel("Rs. Revenue")
# plt.savefig("revenue_by_city.png")
# plt.tight_layout()
# plt.show()