import pandas as pd
#  Data Setup with New Theme and Values
# Supplier catalog DataFrame
supplier_catalog_df = pd.DataFrame({
    "supplier_id": [771, 772, 773, 774, 775],
    "supplier_name": ["SteelCraft Inc.", "Global Logistics", "Tech-Solutions", "Nexus Parts", "Quantum Fab"],
    "credit_limit": [150000, 200000, 350000, 80000, 500000]
})
# Purchase Orders DataFrame
purchase_orders_df = pd.DataFrame({
    "po_number": [901, 901, 902, 903, 903, 904, 905, 905, 906],
    "po_date": pd.to_datetime([
        "2025-04-10", "2025-04-10", "2025-04-15", "2025-05-02",
        "2025-05-02", "2025-05-21", "2025-06-05", "2025-06-05", "2025-06-18"
    ]),
    "supplier_id": [771, 774, 772, 771, 773, 773, 772, 774, 771],
    "unit_price": [7500, 300, 22000, 7200, 1900, 1850, 21500, 350, 6900],
    "quantity_ordered": [10, 50, 5, 12, 30, 20, 8, 100, 15],
    "project_code": ["P-1", "P-1", "P-2", "P-3", "P-3", "P-4", "P-5", "P-5", "P-6"]
})
# Shipment Returns DataFrame
shipment_returns_df = pd.DataFrame({
    "po_number": [903, 905],
    "supplier_id": [773, 774],
    "returned_units": [2, 5]
})
print("--- Supplier Catalog ---")
print(supplier_catalog_df)
print("\n--- Purchase Orders ---")
print(purchase_orders_df)
print("-" * 40)
#  Calculate Total Value per PO 
purchase_orders_df = purchase_orders_df.assign(
    line_total=lambda df: df['unit_price'] * df['quantity_ordered']
)
po_value_summary = purchase_orders_df.groupby("po_number", as_index=False)["line_total"].sum()
po_value_summary = po_value_summary.rename(columns={"line_total": "total_po_value"})
print("\n--- Summary of Total Value per PO ---")
print(po_value_summary)
print("-" * 40)
# Merge PO Data with Supplier Info 
merged_po_data = pd.merge(
    purchase_orders_df, 
    supplier_catalog_df, 
    on="supplier_id", 
    how="left"
)
print("\n--- Merged PO and Supplier Data (Sample Columns) ---")
print(merged_po_data[["po_number", "supplier_name", "unit_price", "quantity_ordered"]])
print("-" * 40)
total_spend_by_supplier = (
    merged_po_data.groupby('supplier_name')['line_total']
    .sum()
    .reset_index()
    .rename(columns={'line_total': 'total_spend'})
)
print("\n--- Total Spend by Supplier ---")
print(total_spend_by_supplier)
print("-" * 40)
# Generate month-over-month order quantity for each supplier
monthly_quantity = (
    merged_po_data.groupby(['supplier_name', pd.Grouper(key='po_date', freq='M')])['quantity_ordered']
    .sum()
    .unstack(level=0, fill_value=0)
)
print("\n--- Month-Over-Month Order Quantity by Supplier ---")
print(monthly_quantity)
print("-" * 40)