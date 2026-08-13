###create a data set, but it will be product data set

import pandas as pd

# 1. Create a Product Dataset
product_data = {
    "PID": [2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010],
    "Product_Name": ["Laptop", "Smartphone", "Tablet", "Monitor", "Keyboard", "Mouse", "Headphones", "Smartwatch", "Printer", "Router"],
    "Category": ["Electronics", "Electronics", "Electronics", "Accessories", "Accessories", "Accessories", "Audio", "Wearables", "Office", "Networking"],
    "Cost_Price": [800, 400, 250, 150, 30, 15, 60, 120, 100, 50],
    "Selling_Price": [1100, 550, 320, 210, 45, 25, 90, 180, 140, 75],
    "Units_Sold": [120, 340, 210, 150, 450, 600, 380, 290, 80, 190],
    "Supplier": ["TechCorp", "GlobalDist", "TechCorp", "DisplayMax", "KeyIn", "KeyIn", "SoundWave", "GlobalDist", "PrintCom", "NetLink"],
    "Support_Email": ["support@techcorp.com", "info@globaldist.com", "support@techcorp.com", "sales@displaymax.com", "help@keyin.com", "help@keyin.com", "service@soundwave.com", "info@globaldist.com", "support@printcom.com", "tech@netlink.com"],
    "Warehouse_Code": ["W001", "W002", "W003", "W004", "W005", "W006", "W007", "W008", "W009", "W010"]
}

print("--- Original Dictionary ---")
print(product_data)

# 2. Initialize DataFrame
df = pd.DataFrame(product_data)
print("\n--- Initial DataFrame ---")
print(df)

# 3. Standardize Data Types
df["Cost_Price"] = df["Cost_Price"].astype(int)
df["Selling_Price"] = df["Selling_Price"].astype(int)
df["Units_Sold"] = df["Units_Sold"].astype(int)

# 4. Calculate Summary Columns (Business Metrics)
df["Unit_Profit"] = df["Selling_Price"] - df["Cost_Price"]
df["Total_Revenue"] = df["Selling_Price"] * df["Units_Sold"]
df["Total_Profit"] = df["Unit_Profit"] * df["Units_Sold"]
df["Profit_Margin_Pct"] = round((df["Unit_Profit"] / df["Selling_Price"]) * 100, 2)

# 5. Rank and Sort Products by Total Profit
df["Rank"] = (
    df["Total_Profit"].rank(ascending=False, method="dense").astype(int)
)
df = df.sort_values(by="Rank")
print("\n--- Final DataFrame with Rank ---")
print(df)

# Filtering Exercises
filtered_revenue = df[df['Total_Revenue'] > 50000]
print('\nProducts with Total_Revenue > 50,000:')
print(filtered_revenue)

filtered_margin = df[df["Profit_Margin_Pct"] > 30]
print("\nProducts with Profit Margin > 30%:")
print(filtered_margin)

filtered_supplier = df[df["Supplier"].str.upper() == "TECHCORP"]
print("\nProducts from Supplier 'TechCorp':")
print(filtered_supplier)

filtered_rank = df[df["Rank"] <= 3]
print("\nTop 3 Ranked Profitable Products:")
print(filtered_rank)

# 6. Export Results
df.to_csv("products.csv", index=False)
print("\nData saved to products.csv")

# 7. GUI Display using Tkinter & PandasTable
import tkinter as tk
from pandastable import Table

root = tk.Tk()
root.title("Product Inventory Tracker")
frame = tk.Frame(root)
frame.pack(fill="both", expand=True)
pt = Table(frame)
pt.model.df = pd.read_csv('products.csv')
pt.show()
# root.mainloop()  # Uncomment this line when running on your computer to open the GUI window

# 8. Interactive Plotly Charts
import plotly.express as px
import webbrowser

# Bar Chart: Total Profit
fig = px.bar(
    df,
    x='Product_Name',
    y='Total_Profit',
    color='Product_Name',
    text='Total_Profit',
    title='Total Profit by Product'
)
fig.update_layout(xaxis_title='Product Name', yaxis_title='Total Profit ($)')
fig.write_html("product_total_profit.html")
webbrowser.open("product_total_profit.html")

# Bar Chart: Profit Margin categorized by Category
fig = px.bar(
    df,
    x='Product_Name',
    y='Profit_Margin_Pct',
    color='Category',
    text='Profit_Margin_Pct',
    title='Profit Margin % of Products'
)
fig.write_html("product_profit_margin.html")
webbrowser.open("product_profit_margin.html")

# Bar Chart: Top 3 items
top3 = df[df['Rank'] <= 3]
fig = px.bar(
    top3,
    x='Product_Name',
    y='Total_Profit',
    color='Rank',
    text='Rank',
    title='Top 3 Ranked Products'
)
fig.write_html("top3_products.html")
webbrowser.open("top3_products.html")

# Grouped Bar Chart: Cost Price vs Selling Price (Using Melt)
price_df = df.melt(
    id_vars='Product_Name',
    value_vars=['Cost_Price', 'Selling_Price'],
    var_name='Price_Type',
    value_name='Amount'
)
fig = px.bar(
    price_df,
    x='Product_Name',
    y='Amount',
    color='Price_Type',
    barmode='group',
    title='Cost vs Selling Price Comparison'
)
fig.write_html("product_price_comparison.html")
webbrowser.open("product_price_comparison.html")

# Pie Chart: Revenue Distribution
fig = px.pie(
    df,
    names='Product_Name',
    values='Total_Revenue',
    title='Product Revenue Distribution Share'
)
fig.write_html('product_revenue_pie.html')
webbrowser.open('product_revenue_pie.html')


