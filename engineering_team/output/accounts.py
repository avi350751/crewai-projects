import time
from typing import Dict, List, Optional

def get_share_price(symbol: str) -> float:
    # Placeholder implementation; in real scenario, this would fetch live prices.
    prices = {
        "AAPL": 150.0,
        "GOOG": 2800.0,
        "TSLA": 700.0,
        "AMZN": 3400.0,
        "MSFT": 300.0,
    }
    if symbol not in prices:
        raise ValueError(f"Share price for symbol '{symbol}' not available.")
    return prices[symbol]

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
        self.user_id = user_id
        self.balance = 0.0
        self.portfolio: Dict[str, int] = {}
        self.transactions: List[Dict] = []

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
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")
        self.balance += amount
        self._record_transaction(
            txn_type="deposit",
            amount=amount,
            symbol=None,
            quantity=None,
            balance_after=self.balance,
        )

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
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")
        if self.balance <= 0:
            raise RuntimeError("Cannot withdraw: account balance is zero or negative.")
        if amount > self.balance:
            raise RuntimeError("Insufficient balance for withdrawal.")
        self.balance -= amount
        self._record_transaction(
            txn_type="withdrawal",
            amount=amount,
            symbol=None,
            quantity=None,
            balance_after=self.balance,
        )

    def get_balance(self) -> float:
        """
        Get the current cash balance.

        Returns:
            float: Current available cash balance.
        """
        return self.balance

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
        if quantity <= 0:
            raise ValueError("Quantity to buy must be greater than zero.")
        price = get_share_price(symbol)
        cost = price * quantity
        if self.balance < cost:
            raise RuntimeError("Insufficient funds to buy stock.")
        self.balance -= cost
        self.portfolio[symbol] = self.portfolio.get(symbol, 0) + quantity
        self._record_transaction(
            txn_type="buy",
            amount=cost,
            symbol=symbol,
            quantity=quantity,
            balance_after=self.balance,
        )

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
        if quantity <= 0:
            raise ValueError("Quantity to sell must be greater than zero.")
        if symbol not in self.portfolio or self.portfolio[symbol] < quantity:
            raise RuntimeError("Insufficient shares in portfolio to sell.")
        price = get_share_price(symbol)
        proceeds = price * quantity
        self.portfolio[symbol] -= quantity
        if self.portfolio[symbol] == 0:
            del self.portfolio[symbol]
        self.balance += proceeds
        self._record_transaction(
            txn_type="sell",
            amount=proceeds,
            symbol=symbol,
            quantity=quantity,
            balance_after=self.balance,
        )

    def get_portfolio(self) -> Dict[str, int]:
        """
        Get the current holdings portfolio.

        Returns:
            Dict[str, int]: Mapping stock symbol to quantity owned.
        """
        return dict(self.portfolio)

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
        return list(self.transactions)

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
        total_deposits = 0.0
        total_withdrawals = 0.0
        total_trades = 0
        for txn in self.transactions:
            ttype = txn['type']
            if ttype == "deposit":
                total_deposits += txn['amount']
            elif ttype == "withdrawal":
                total_withdrawals += txn['amount']
            elif ttype in ("buy", "sell"):
                total_trades += 1
        net_invested = total_deposits - total_withdrawals
        return {
            "total_deposits": total_deposits,
            "total_withdrawals": total_withdrawals,
            "total_trades": total_trades,
            "net_invested": net_invested,
        }

    def _record_transaction(self, txn_type: str, amount: float, symbol: Optional[str], quantity: Optional[int], balance_after: float) -> None:
        timestamp = time.time()
        record = {
            "type": txn_type,
            "amount": amount,
            "symbol": symbol,
            "quantity": quantity,
            "balance_after": balance_after,
            "timestamp": timestamp,
        }
        self.transactions.append(record)