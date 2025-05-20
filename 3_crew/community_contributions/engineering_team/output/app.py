import gradio as gr
from accounts import Account, InsufficientFundsError, InsufficientSharesError
from datetime import datetime

# Initialize account
account = Account("user123")

def create_account(initial_deposit: float):
    global account
    account = Account("user123", initial_deposit)
    return f"Account created with initial deposit: {initial_deposit}"

def deposit(amount: float):
    try:
        account.deposit(amount)
        return f"Deposited {amount}. New balance: {account.balance}"
    except ValueError as e:
        return str(e)

def withdraw(amount: float):
    try:
        account.withdraw(amount)
        return f"Withdrew {amount}. New balance: {account.balance}"
    except ValueError as e:
        return str(e)
    except InsufficientFundsError as e:
        return str(e)

def buy_shares(symbol: str, quantity: int):
    try:
        account.buy_shares(symbol, quantity)
        return f"Bought {quantity} shares of {symbol}. New balance: {account.balance}"
    except ValueError as e:
        return str(e)
    except InsufficientFundsError as e:
        return str(e)

def sell_shares(symbol: str, quantity: int):
    try:
        account.sell_shares(symbol, quantity)
        return f"Sold {quantity} shares of {symbol}. New balance: {account.balance}"
    except ValueError as e:
        return str(e)
    except InsufficientSharesError as e:
        return str(e)

def get_balance():
    return f"Current balance: {account.balance}"

def get_portfolio_value():
    return f"Portfolio value: {account.get_portfolio_value()}"

def get_profit_loss():
    return f"Profit/Loss: {account.get_profit_loss()}"

def get_holdings():
    return str(account.get_holdings())

def get_transactions():
    transactions = account.get_transactions()
    transaction_strings = [str(t) for t in transactions]
    return "\n".join(transaction_strings)

with gr.Blocks() as demo:
    gr.Markdown("# Simple Trading Account")

    with gr.Accordion("Account Actions", open=False):
        initial_deposit_input = gr.Number(label="Initial Deposit")
        create_account_button = gr.Button("Create Account")
        create_account_output = gr.Textbox(label="Account Creation Status")
        create_account_button.click(create_account, inputs=initial_deposit_input, outputs=create_account_output)


        deposit_input = gr.Number(label="Deposit Amount")
        deposit_button = gr.Button("Deposit")
        deposit_output = gr.Textbox(label="Deposit Status")
        deposit_button.click(deposit, inputs=deposit_input, outputs=deposit_output)

        withdraw_input = gr.Number(label="Withdraw Amount")
        withdraw_button = gr.Button("Withdraw")
        withdraw_output = gr.Textbox(label="Withdraw Status")
        withdraw_button.click(withdraw, inputs=withdraw_input, outputs=withdraw_output)

        symbol_input = gr.Textbox(label="Stock Symbol")
        quantity_input = gr.Number(label="Quantity")

        buy_button = gr.Button("Buy Shares")
        buy_output = gr.Textbox(label="Buy Status")
        buy_button.click(buy_shares, inputs=[symbol_input, quantity_input], outputs=buy_output)

        sell_button = gr.Button("Sell Shares")
        sell_output = gr.Textbox(label="Sell Status")
        sell_button.click(sell_shares, inputs=[symbol_input, quantity_input], outputs=sell_output)

    with gr.Accordion("Account Information", open=False):
        balance_button = gr.Button("Get Balance")
        balance_output = gr.Textbox(label="Balance")
        balance_button.click(get_balance, outputs=balance_output)

        portfolio_button = gr.Button("Get Portfolio Value")
        portfolio_output = gr.Textbox(label="Portfolio Value")
        portfolio_button.click(get_portfolio_value, outputs=portfolio_output)

        profit_loss_button = gr.Button("Get Profit/Loss")
        profit_loss_output = gr.Textbox(label="Profit/Loss")
        profit_loss_button.click(get_profit_loss, outputs=profit_loss_output)

        holdings_button = gr.Button("Get Holdings")
        holdings_output = gr.Textbox(label="Holdings")
        holdings_button.click(get_holdings, outputs=holdings_output)

        transactions_button = gr.Button("Get Transactions")
        transactions_output = gr.Textbox(label="Transactions")
        transactions_button.click(get_transactions, outputs=transactions_output)


demo.launch()
