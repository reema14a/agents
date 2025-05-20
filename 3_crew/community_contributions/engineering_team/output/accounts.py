
# accounts.py

from typing import Dict, List, Tuple, Optional
from datetime import datetime

def get_share_price(symbol: str) -> float:
    """
    Retrieves the current price of a share.

    Args:
        symbol: The stock symbol (e.g., 'AAPL').

    Returns:
        The current price of the share.
    """
    # Test implementation (can be replaced with a real API call)
    if symbol == 'AAPL':
        return 170.0
    elif symbol == 'TSLA':
        return 250.0
    elif symbol == 'GOOGL':
        return 2700.0
    else:
        raise ValueError(f"Share price for symbol '{symbol}' not found.")

class InsufficientFundsError(Exception):
    """Custom exception for insufficient funds."""
    pass

class InsufficientSharesError(Exception):
    """Custom exception for insufficient shares."""
    pass


class Transaction:
    """
    Represents a single transaction in the account.
    """
    def __init__(self, timestamp: datetime, type: str, symbol: str, quantity: int, price: float):
        """
        Initializes a new Transaction object.

        Args:
            timestamp: The date and time of the transaction.
            type: The type of transaction ('buy', 'sell', 'deposit', 'withdraw').
            symbol: The stock symbol (if applicable, otherwise None).
            quantity: The number of shares bought or sold (if applicable, otherwise None).
            price: The price per share at the time of the transaction (if applicable, otherwise None).
        """
        self.timestamp = timestamp
        self.type = type
        self.symbol = symbol
        self.quantity = quantity
        self.price = price

    def __repr__(self):
        return f"Transaction(timestamp={self.timestamp}, type='{self.type}', symbol='{self.symbol}', quantity={self.quantity}, price={self.price})"



class Account:
    """
    Represents a user's trading account.
    """

    def __init__(self, account_id: str, initial_deposit: float = 0.0):
        """
        Initializes a new Account object.

        Args:
            account_id: A unique identifier for the account.
            initial_deposit: The initial deposit amount (default: 0.0).
        """
        self.account_id = account_id
        self.balance = initial_deposit
        self.holdings: Dict[str, int] = {}  # {symbol: quantity}
        self.transactions: List[Transaction] = []
        self._record_transaction(datetime.now(), 'deposit', None, None, initial_deposit)


    def deposit(self, amount: float) -> None:
        """
        Deposits funds into the account.

        Args:
            amount: The amount to deposit.

        Raises:
            ValueError: If the amount is not positive.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self._record_transaction(datetime.now(), 'deposit', None, None, amount)


    def withdraw(self, amount: float) -> None:
        """
        Withdraws funds from the account.

        Args:
            amount: The amount to withdraw.

        Raises:
            ValueError: If the amount is not positive.
            InsufficientFundsError: If there are insufficient funds.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if self.balance < amount:
            raise InsufficientFundsError("Insufficient funds for withdrawal.")
        self.balance -= amount
        self._record_transaction(datetime.now(), 'withdraw', None, None, amount)

    def buy_shares(self, symbol: str, quantity: int) -> None:
        """
        Buys shares of a given stock.

        Args:
            symbol: The stock symbol.
            quantity: The number of shares to buy.

        Raises:
            ValueError: If the quantity is not positive.
            InsufficientFundsError: If there are insufficient funds.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")

        price_per_share = get_share_price(symbol)
        total_cost = price_per_share * quantity

        if self.balance < total_cost:
            raise InsufficientFundsError("Insufficient funds to buy shares.")

        self.balance -= total_cost
        self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
        self._record_transaction(datetime.now(), 'buy', symbol, quantity, price_per_share)


    def sell_shares(self, symbol: str, quantity: int) -> None:
        """
        Sells shares of a given stock.

        Args:
            symbol: The stock symbol.
            quantity: The number of shares to sell.

        Raises:
            ValueError: If the quantity is not positive.
            InsufficientSharesError: If there are insufficient shares.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")

        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            raise InsufficientSharesError("Insufficient shares to sell.")

        price_per_share = get_share_price(symbol)
        total_revenue = price_per_share * quantity

        self.balance += total_revenue
        self.holdings[symbol] -= quantity
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        self._record_transaction(datetime.now(), 'sell', symbol, quantity, price_per_share)


    def get_portfolio_value(self) -> float:
        """
        Calculates the total value of the portfolio (holdings + cash balance).

        Returns:
            The total portfolio value.
        """
        portfolio_value = self.balance
        for symbol, quantity in self.holdings.items():
            portfolio_value += get_share_price(symbol) * quantity
        return portfolio_value

    def get_profit_loss(self) -> float:
        """
        Calculates the profit or loss from the initial deposit.

        Returns:
            The profit or loss.
        """
        initial_deposit = next((t.price for t in self.transactions if t.type == 'deposit'), 0.0) #Gets initial deposit from transactions, defaults to zero.
        return self.get_portfolio_value() - initial_deposit

    def get_holdings(self) -> Dict[str, int]:
        """
        Returns the current holdings of the account.

        Returns:
            A dictionary where keys are stock symbols and values are the number of shares held.
        """
        return self.holdings.copy()

    def get_transactions(self) -> List[Transaction]:
        """
        Returns a list of all transactions in the account.

        Returns:
            A list of Transaction objects.
        """
        return self.transactions.copy()

    def _record_transaction(self, timestamp: datetime, type: str, symbol: Optional[str], quantity: Optional[int], price: float) -> None:
        """
        Records a transaction in the account's history.

        Args:
            timestamp: The date and time of the transaction.
            type: The type of transaction ('buy', 'sell', 'deposit', 'withdraw').
            symbol: The stock symbol (if applicable).
            quantity: The number of shares bought or sold (if applicable).
            price: The price per share (if applicable, otherwise the deposit/withdrawal amount).
        """
        self.transactions.append(Transaction(timestamp, type, symbol, quantity, price))
