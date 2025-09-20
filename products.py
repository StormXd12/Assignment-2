import pandas as pd
import numpy as np
# Products table
products = pd.DataFrame({
    "product_id": [101, 102, 103, 104],
    "product_name": ["Laptop", "Mobile", "Tablet", "Headphones"],
    "category": ["Electronics", "Electronics", "Electronics", "Accessories"],
    "cost": [40000, 12000, 10000, 1500]
})
# Orders table (each row = order line)
orders = pd.DataFrame({
    "order_id": [1,1,2,3,3,4,5,5,6],
    "date": pd.to_datetime([
        "2024-01-05","2024-01-05","2024-01-10","2024-02-01",
        "2024-02-01","2024-02-20","2024-03-01","2024-03-01","2024-03-15"
    ]),
    "product_id": [101,104,102,101,103,103,102,104,101],
    "price": [50000,2000,18000,48000,16000,14500,17500,2200,47000],
    "quantity": [1,2,1,1,2,1,1,3,2],
    "customer": ["A","A","B","C","C","D","E","E","F"]
})
# Returns (some orders returned partially)
returns = pd.DataFrame({
    "order_id": [3,5],
    "product_id": [103,104],
    "returned_qty": [1, 1]
})
print(products)
print(orders)
#how to generate revenue per order line and total revenue per order
orders = orders.copy()
orders["revenue"] = orders["price"] * orders["quantity"]
order_revenue = orders.groupby("order_id", as_index=False) ["revenue"].sum().rename(columns={"revenue":"order_revenue"})
print(order_revenue)
#join product info into orders
order_pro = orders.merge(products,on="product_id", how="left")
print(order_pro[["order_id","product_id","product_name","category","price","quantity"]])
#how to genarate profit per line and total profit by category
order_pro["x"] = order_pro["price"] - order_pro["cost"]
order_pro["line_profit"] = order_pro["x"] * order_pro["quantity"]
pro_cat = order_pro.groupby("category",as_index=False)["line_profit"].sum()
print(pro_cat)
#for each produt, genarate month-over-month sales (quantity) ?
orders_ts = order_pro.set_index("date")
monthly_qty = orders_ts.groupby("product_id") ["quantity"].resample("M").sum().unstack(level=0).fillna(0)
print(monthly_qty)
#create pivot table product * month total revenue with margin
final_pivot = (
    order_pro.groupby(['product_name', pd.Grouper(key='date', freq='M')])
    .agg(
        revenue=('revenue', 'sum'),
        profit=('line_profit', 'sum')
    )
    .assign(margin=lambda df: df['profit'] / df['revenue'])
    .unstack(level=1)
    .fillna(0)
)
final_pivot = final_pivot.swaplevel(0, 1, axis=1).sort_index(axis=1)
print(final_pivot)