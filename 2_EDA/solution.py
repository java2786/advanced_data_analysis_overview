import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv("swiftkart_sales.csv")

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


print("\n\n========================\n\n")
group_a = df[df['banner_shown']=="A"]['customer_rating']
group_b = df[df['banner_shown']=="B"]['customer_rating']

print(f"A Customer Rating: {round(group_a.mean(), 2)} / 5")
print(f"B Customer Rating: {round(group_b.mean(), 2)} / 5")

# A/B Testing

t_stats, value = stats.ttest_ind(group_a, group_b)
print("T statistics:", round(t_stats,2))
print("Values:", round(value, 4))

if(value < 0.05):
    print("Result: The difference is significant. Banner B is better.")
else:
    print("Result: Not significant, do not switch bussiness from A to B")