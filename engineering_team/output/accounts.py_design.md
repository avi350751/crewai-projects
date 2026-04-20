```markdown
# Design for `accounts.py` module

## Overview
The `accounts.py` module implements an `Account` class that manages a simulated trading account for users on a trading simulation platform. It supports account creation (via constructor), funds deposit and withdrawal with safety checks, stock trading (buying and selling shares), portfolio tracking, transaction history, and activity reporting.

The module relies on an external function:
```python
def get_share_price(symbol: str) -> float:
    """Returns the current market price of the given stock symbol."""
    ...
```

## Module Contents

### Class: `Account`
Represents a single user's trading account.

#### Attributes:
- `user_id: str` — Unique identifier for the user/account.
- `balance: float` — Current cash balance in the account.
- `portfolio: Dict[str, int]` — Mapping of stock symbols to quantity of shares owned.
- `transactions: List[Dict]` — List of transaction records (deposits, withdrawals, trades).
  
#### Methods:

```python
class Account:
    def __init__(self, user_id: str):
        """
        Initialize a new trading account for a user.

        Args:
            user_id (str): Unique identifier for this account/user.

        Initializes:
            balance = 0.0
            portfolio = {}
            transactions = []
        """
```

```python
    def deposit(self, amount: float) -> None:
        """
        Deposit funds into the account.

        Args:
            amount (float): Amount to deposit. Must be > 0.

        Effects:
            - Increase balance by amount.
            - Record the deposit in transactions.

        Raises:
            ValueError: If amount <= 0.
        """
```

```python
    def withdraw(self, amount: float) -> None:
        """
        Withdraw funds from the account.

        Args:
            amount (float): Amount to withdraw. Must be > 0.

        Conditions:
            - User cannot withdraw if balance <= 0.
            - User cannot withdraw more than current balance.

        Effects:
            - Decrease balance by amount.
            - Record the withdrawal in transactions.

        Raises:
            ValueError: If amount <= 0.
            RuntimeError: If insufficient balance or balance is zero/negative.
        """
```

```python
    def get_balance(self) -> float:
        """
        Get the current cash balance.

        Returns:
            float: Current available cash balance.
        """
```

```python
    def buy_stock(self, symbol: str, quantity: int) -> None:
        """
        Purchase shares of a given stock.

        Args:
            symbol (str): Stock ticker symbol.
            quantity (int): Number of shares to buy (> 0).

        Process:
            - Get current price via get_share_price(symbol).
            - Calculate cost = price * quantity.
            - Check if sufficient balance.
            - Deduct cost from balance.
            - Add shares to portfolio.
            - Record trade in transactions.

        Raises:
            ValueError: If quantity <= 0.
            RuntimeError: If insufficient funds.
        """
```

```python
    def sell_stock(self, symbol: str, quantity: int) -> None:
        """
        Sell shares of a given stock.

        Args:
            symbol (str): Stock ticker symbol.
            quantity (int): Number of shares to sell (> 0).

        Process:
            - Check if portfolio has enough shares.
            - Get current price via get_share_price(symbol).
            - Calculate proceeds = price * quantity.
            - Remove shares from portfolio.
            - Increase balance by proceeds.
            - Record trade in transactions.

        Raises:
            ValueError: If quantity <= 0.
            RuntimeError: If insufficient shares.
        """
```

```python
    def get_portfolio(self) -> Dict[str, int]:
        """
        Get the current holdings portfolio.

        Returns:
            Dict[str, int]: Mapping stock symbol to quantity owned.
        """
```

```python
    def get_transaction_history(self) -> List[Dict]:
        """
        Get the list of all account transactions (deposits, withdrawals, trades).

        Each transaction record dict contains fields:
            - 'type': "deposit", "withdrawal", "buy", or "sell"
            - 'amount': float, cash value for deposits/withdrawals; total trade value for trades
            - 'symbol': present for trades (buy/sell), stock symbol
            - 'quantity': present for trades, number of shares bought/sold
            - 'balance_after': float, account balance after transaction
            - 'timestamp': timestamp of transaction
        
        Returns:
            List[Dict]: List of transaction records in chronological order.
        """
```

```python
    def generate_activity_report(self) -> Dict[str, float]:
        """
        Generate summary report on user activity.

        Returns:
            Dict[str, float] with keys:
              - 'total_deposits': sum of all deposited funds
              - 'total_withdrawals': sum of all withdrawn funds
              - 'total_trades': count of all buy and sell transactions
              - 'net_invested': total deposits - withdrawals (cash flow)
        """
```

---

## Example Transaction Record Format

For clarity, example of a transaction dictionary structure:

```python
{
    'type': 'buy' | 'sell' | 'deposit' | 'withdrawal',
    'amount': float,                # funds involved; for trades = price * quantity
    'symbol': Optional[str],        # stock symbol for trades, None otherwise
    'quantity': Optional[int],      # shares bought/sold for trades, None otherwise
    'balance_after': float,         # cash balance post transaction
    'timestamp': float              # Unix timestamp of transaction
}
```

---

## Summary

The `Account` class provides a self-contained interface to:
- create and track user accounts,
- manage deposits and withdrawals with error checks,
- buy and sell shares at current market prices,
- maintain detailed portfolios and transaction history, and
- generate activity summaries for reporting/analytics.

All operations guarantee internal consistency and basic error protection per requirements.  
This module can be extended with UI or API layers to interact with the `Account` class.
```