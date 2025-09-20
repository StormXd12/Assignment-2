import pandas as pd
import numpy as np
# Simulated Stock Data
stock_data = pd.DataFrame({
    "Symbol": ["RELI", "TCS", "HDFCB", "INFO"],
    "CompanyName": ["Reliance Industries", "Tata Consultancy", "HDFC Bank", "Infosys"],
    "CurrentPrice": [2950, 3800, 1520, 1610] 
})
print("--- Mini Stock Exchange ---\nAvailable Securities:")
print(stock_data, "\n" + "-"*30) 
transaction_log = []
print("\n--- Start Trading ---")
# User Interaction Loop
while True:
    trade_type = input("Enter trade type (BUY/SELL) or 'DONE' to finish: ").strip().upper()
    if trade_type == "DONE":
        break
    if trade_type not in ["BUY", "SELL"]:
        print("Invalid trade type.")
        continue
# Validate stock symbol
    stock_symbol = input(f"Enter symbol for {trade_type} order: ").strip().upper()
    if stock_symbol not in stock_data['Symbol'].values:
        print(f"Error: Symbol '{stock_symbol}' not found.\n")
        continue
# Validate and log the trade
    share_quantity = int(input(f"Enter quantity for {stock_symbol}: "))
    stock_price = stock_data.loc[stock_data["Symbol"] == stock_symbol, "CurrentPrice"].iloc[0]
    # Log the transaction
    transaction_log.append({
        "Symbol": stock_symbol, "Type": trade_type, 
        "Quantity": share_quantity, "ExecPrice": stock_price
    })
    print(f"Success! Logged {trade_type} of {share_quantity} {stock_symbol} at ₹{stock_price}.\n")

if transaction_log:
    transactions_df = pd.DataFrame(transaction_log)
    
    transactions_df['P/L'] = np.where(
        transactions_df['Type'] == 'SELL', 
        (transactions_df['ExecPrice'] - transactions_df['ExecPrice']) * transactions_df['Quantity'], 
        0
    )
    print("\n--- Full Transaction History with P/L ---")
    print(transactions_df)
# Summarize total shares traded and P/L by symbol
    final_summary = transactions_df.groupby("Symbol").agg(
        TotalSharesTraded=('Quantity', 'sum'),
        TotalPL=('P/L', 'sum')
    ).reset_index()
    print("\n--- Portfolio Summary by Symbol ---")
    print(final_summary)
else:
    print("\nNo trades were made.")