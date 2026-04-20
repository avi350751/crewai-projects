import unittest
from unittest.mock import patch
import time

# We will embed the Account and get_share_price here to allow testing as standalone.

def get_share_price(symbol: str) -> float:
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
        self.user_id = user_id
        self.balance = 0.0
        self.portfolio = {}
        self.transactions = []

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")
        self.balance += amount
        self._record_transaction("deposit", amount, None, None, self.balance)

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")
        if self.balance <= 0:
            raise RuntimeError("Cannot withdraw: account balance is zero or negative.")
        if amount > self.balance:
            raise RuntimeError("Insufficient balance for withdrawal.")
        self.balance -= amount
        self._record_transaction("withdrawal", amount, None, None, self.balance)

    def get_balance(self) -> float:
        return self.balance

    def buy_stock(self, symbol: str, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity to buy must be greater than zero.")
        price = get_share_price(symbol)
        cost = price * quantity
        if self.balance < cost:
            raise RuntimeError("Insufficient funds to buy stock.")
        self.balance -= cost
        self.portfolio[symbol] = self.portfolio.get(symbol, 0) + quantity
        self._record_transaction("buy", cost, symbol, quantity, self.balance)

    def sell_stock(self, symbol: str, quantity: int) -> None:
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
        self._record_transaction("sell", proceeds, symbol, quantity, self.balance)

    def get_portfolio(self) -> dict:
        return dict(self.portfolio)

    def get_transaction_history(self) -> list:
        return list(self.transactions)

    def generate_activity_report(self) -> dict:
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

    def _record_transaction(self, txn_type: str, amount: float, symbol, quantity, balance_after: float) -> None:
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


class TestAccount(unittest.TestCase):
    def setUp(self):
        self.acc = Account("user1")

    def test_initial_state(self):
        self.assertEqual(self.acc.user_id, "user1")
        self.assertEqual(self.acc.get_balance(), 0.0)
        self.assertEqual(self.acc.get_portfolio(), {})
        self.assertEqual(self.acc.get_transaction_history(), [])

    def test_deposit_positive_amount(self):
        self.acc.deposit(100.0)
        self.assertEqual(self.acc.get_balance(), 100.0)
        txns = self.acc.get_transaction_history()
        self.assertEqual(len(txns), 1)
        self.assertEqual(txns[0]["type"], "deposit")
        self.assertEqual(txns[0]["amount"], 100.0)

    def test_deposit_zero_or_negative_raises(self):
        with self.assertRaises(ValueError):
            self.acc.deposit(0)
        with self.assertRaises(ValueError):
            self.acc.deposit(-10)

    def test_withdraw_valid(self):
        self.acc.deposit(200)
        self.acc.withdraw(50)
        self.assertEqual(self.acc.get_balance(), 150)
        txns = self.acc.get_transaction_history()
        self.assertEqual(txns[-1]["type"], "withdrawal")
        self.assertEqual(txns[-1]["amount"], 50)

    def test_withdraw_zero_or_negative_raises(self):
        with self.assertRaises(ValueError):
            self.acc.withdraw(0)
        with self.assertRaises(ValueError):
            self.acc.withdraw(-5)

    def test_withdraw_insufficient_funds_raises(self):
        with self.assertRaises(RuntimeError):
            self.acc.withdraw(10)
        self.acc.deposit(30)
        with self.assertRaises(RuntimeError):
            self.acc.withdraw(40)

    def test_buy_stock_success(self):
        self.acc.deposit(1000)
        self.acc.buy_stock("AAPL", 5)
        self.assertEqual(self.acc.get_portfolio()["AAPL"], 5)
        self.assertAlmostEqual(self.acc.get_balance(), 250)
        txns = self.acc.get_transaction_history()
        self.assertEqual(txns[-1]["type"], "buy")
        self.assertEqual(txns[-1]["symbol"], "AAPL")
        self.assertEqual(txns[-1]["quantity"], 5)

    def test_buy_stock_insufficient_funds_raises(self):
        self.acc.deposit(100)
        with self.assertRaises(RuntimeError):
            self.acc.buy_stock("GOOG", 1)

    def test_buy_stock_invalid_quantity_raises(self):
        with self.assertRaises(ValueError):
            self.acc.buy_stock("AAPL", 0)
        with self.assertRaises(ValueError):
            self.acc.buy_stock("AAPL", -3)

    def test_sell_stock_success(self):
        self.acc.deposit(2000)
        self.acc.buy_stock("TSLA", 2)
        self.acc.sell_stock("TSLA", 1)
        self.assertEqual(self.acc.get_portfolio()["TSLA"], 1)
        self.assertAlmostEqual(self.acc.get_balance(), 1300)
        txns = self.acc.get_transaction_history()
        self.assertEqual(txns[-1]["type"], "sell")
        self.assertEqual(txns[-1]["symbol"], "TSLA")
        self.assertEqual(txns[-1]["quantity"], 1)

    def test_sell_stock_all_shares_removes_symbol(self):
        self.acc.deposit(2000)
        self.acc.buy_stock("TSLA", 2)
        self.acc.sell_stock("TSLA", 2)
        self.assertNotIn("TSLA", self.acc.get_portfolio())

    def test_sell_stock_invalid_quantity_raises(self):
        with self.assertRaises(ValueError):
            self.acc.sell_stock("TSLA", 0)
        with self.assertRaises(ValueError):
            self.acc.sell_stock("TSLA", -1)

    def test_sell_stock_not_enough_shares_raises(self):
        self.acc.deposit(5000)
        self.acc.buy_stock("AAPL", 1)
        with self.assertRaises(RuntimeError):
            self.acc.sell_stock("AAPL", 2)
        with self.assertRaises(RuntimeError):
            self.acc.sell_stock("GOOG", 1)

    def test_get_transaction_history_order_and_fields(self):
        self.acc.deposit(500)
        self.acc.withdraw(100)
        self.acc.deposit(200)
        self.acc.buy_stock("MSFT", 1)
        history = self.acc.get_transaction_history()
        self.assertEqual(len(history), 4)
        for txn in history:
            self.assertIn("type", txn)
            self.assertIn("amount", txn)
            self.assertIn("balance_after", txn)
            self.assertIn("timestamp", txn)

    def test_generate_activity_report(self):
        self.acc.deposit(1000)
        self.acc.withdraw(200)
        self.acc.deposit(300)
        self.acc.buy_stock("AAPL", 2)
        self.acc.sell_stock("AAPL", 1)
        report = self.acc.generate_activity_report()
        self.assertEqual(report["total_deposits"], 1300)
        self.assertEqual(report["total_withdrawals"], 200)
        self.assertEqual(report["total_trades"], 2)
        self.assertEqual(report["net_invested"], 1100)

    def test_get_share_price_valid_and_invalid(self):
        self.assertEqual(get_share_price("AAPL"), 150.0)
        self.assertEqual(get_share_price("MSFT"), 300.0)
        with self.assertRaises(ValueError):
            get_share_price("INVALID")

if __name__ == '__main__':
    unittest.main()