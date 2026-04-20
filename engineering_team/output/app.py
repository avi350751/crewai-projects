import gradio as gr
from accounts import Account, get_share_price
from datetime import datetime

accounts = {}

def create_account(user_id):
    if user_id in accounts:
        return "Account already exists."
    accounts[user_id] = Account(user_id)
    return f"Account created for user_id '{user_id}'."

def deposit_funds(user_id, amount):
    if user_id not in accounts:
        return "No account found. Create an account first.", ""
    try:
        amount = float(amount)
        accounts[user_id].deposit(amount)
        balance = accounts[user_id].get_balance()
        return f"Deposited ${amount:.2f} successfully.", f"${balance:.2f}"
    except Exception as e:
        return str(e), ""

def withdraw_funds(user_id, amount):
    if user_id not in accounts:
        return "No account found. Create an account first.", ""
    try:
        amount = float(amount)
        accounts[user_id].withdraw(amount)
        balance = accounts[user_id].get_balance()
        return f"Withdrew ${amount:.2f} successfully.", f"${balance:.2f}"
    except Exception as e:
        return str(e), ""

def check_balance(user_id):
    if user_id not in accounts:
        return "No account found. Create an account first."
    balance = accounts[user_id].get_balance()
    return f"Current Balance: ${balance:.2f}"

def buy_stock(user_id, symbol, quantity):
    if user_id not in accounts:
        return "No account found. Create an account first.", ""
    try:
        quantity = int(quantity)
        symbol = symbol.upper()
        accounts[user_id].buy_stock(symbol, quantity)
        portfolio = accounts[user_id].get_portfolio()
        return f"Bought {quantity} shares of {symbol}.", str(portfolio)
    except Exception as e:
        return str(e), ""

def sell_stock(user_id, symbol, quantity):
    if user_id not in accounts:
        return "No account found. Create an account first.", ""
    try:
        quantity = int(quantity)
        symbol = symbol.upper()
        accounts[user_id].sell_stock(symbol, quantity)
        portfolio = accounts[user_id].get_portfolio()
        return f"Sold {quantity} shares of {symbol}.", str(portfolio)
    except Exception as e:
        return str(e), ""

def view_portfolio(user_id):
    if user_id not in accounts:
        return "No account found. Create an account first."
    portfolio = accounts[user_id].get_portfolio()
    if not portfolio:
        return "Portfolio is empty."
    portfolio_text = "Current Portfolio:\n" + str(portfolio)
    return portfolio_text

def transaction_history(user_id):
    if user_id not in accounts:
        return "No account found. Create an account first.", []
    history = accounts[user_id].get_transaction_history()
    if not history:
        return "No transactions found.", []
    rows = []
    for txn in history:
        ttype = txn["type"].capitalize()
        amount = txn["amount"]
        symbol = txn["symbol"] if txn["symbol"] else "-"
        quantity = txn["quantity"] if txn["quantity"] else "-"
        bal_after = txn["balance_after"]
        ts = datetime.fromtimestamp(txn["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
        rows.append([ts, ttype, symbol, str(quantity), f"${amount:.2f}", f"${bal_after:.2f}"])
    return "Transaction History:", rows

def activity_report(user_id):
    if user_id not in accounts:
        return "No account found. Create an account first."
    report = accounts[user_id].generate_activity_report()
    lines = [
        f"Total Deposits: ${report['total_deposits']:.2f}",
        f"Total Withdrawals: ${report['total_withdrawals']:.2f}",
        f"Total Trades (Buy + Sell): {report['total_trades']}",
        f"Net Invested (Deposits - Withdrawals): ${report['net_invested']:.2f}"
    ]
    return "\n".join(lines)

with gr.Blocks() as demo:
    gr.Markdown("# Trading Simulation Account Management")
    with gr.Row():
        with gr.Column():
            user_id_in = gr.Textbox(label="User ID", placeholder="Enter user ID")
            create_acc_btn = gr.Button("Create Account")
            create_acc_out = gr.Textbox(label="Account Creation Result", interactive=False)
        
            deposit_amt = gr.Number(label="Deposit Amount", precision=2)
            deposit_btn = gr.Button("Deposit")
            deposit_out = gr.Textbox(label="Deposit Result", interactive=False)
            balance_after_deposit = gr.Textbox(label="Balance After Deposit", interactive=False)
        
            withdraw_amt = gr.Number(label="Withdraw Amount", precision=2)
            withdraw_btn = gr.Button("Withdraw")
            withdraw_out = gr.Textbox(label="Withdraw Result", interactive=False)
            balance_after_withdraw = gr.Textbox(label="Balance After Withdraw", interactive=False)
        
            balance_btn = gr.Button("Check Balance")
            balance_out = gr.Textbox(label="Current Balance", interactive=False)
        
        with gr.Column():
            stock_symbol_buy = gr.Textbox(label="Buy Stock Symbol", placeholder="e.g. AAPL")
            stock_qty_buy = gr.Number(label="Quantity to Buy", precision=0)
            buy_btn = gr.Button("Buy Stock")
            buy_out = gr.Textbox(label="Buy Result", interactive=False)
            portfolio_view_buy = gr.Textbox(label="Portfolio After Buy", interactive=False)
            
            stock_symbol_sell = gr.Textbox(label="Sell Stock Symbol", placeholder="e.g. TSLA")
            stock_qty_sell = gr.Number(label="Quantity to Sell", precision=0)
            sell_btn = gr.Button("Sell Stock")
            sell_out = gr.Textbox(label="Sell Result", interactive=False)
            portfolio_view_sell = gr.Textbox(label="Portfolio After Sell", interactive=False)

            portfolio_btn = gr.Button("View Portfolio")
            portfolio_out = gr.Textbox(label="Current Portfolio", interactive=False)
            
            txn_btn = gr.Button("Transaction History")
            txn_out_label = gr.Textbox(label="History Status", interactive=False)
            txn_out_table = gr.DataFrame(headers=["Date & Time","Type","Symbol","Qty","Amount","Balance After"],interactive=False)
            
            report_btn = gr.Button("Activity Report")
            report_out = gr.Textbox(label="Activity Report", interactive=False)

    create_acc_btn.click(fn=create_account, inputs=user_id_in, outputs=create_acc_out)
    deposit_btn.click(fn=deposit_funds, inputs=[user_id_in, deposit_amt], outputs=[deposit_out, balance_after_deposit])
    withdraw_btn.click(fn=withdraw_funds, inputs=[user_id_in, withdraw_amt], outputs=[withdraw_out, balance_after_withdraw])
    balance_btn.click(fn=check_balance, inputs=user_id_in, outputs=balance_out)
    buy_btn.click(fn=buy_stock, inputs=[user_id_in, stock_symbol_buy, stock_qty_buy], outputs=[buy_out, portfolio_view_buy])
    sell_btn.click(fn=sell_stock, inputs=[user_id_in, stock_symbol_sell, stock_qty_sell], outputs=[sell_out, portfolio_view_sell])
    portfolio_btn.click(fn=view_portfolio, inputs=user_id_in, outputs=portfolio_out)
    txn_btn.click(fn=transaction_history, inputs=user_id_in, outputs=[txn_out_label, txn_out_table])
    report_btn.click(fn=activity_report, inputs=user_id_in, outputs=report_out)

if __name__ == "__main__":
    demo.launch()