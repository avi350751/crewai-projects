#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from engineering_team.crew import EngineeringTeam
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


requirements = """
A simple account management system for a trading simulation platform.
The system should allow users to create accounts, deposit and withdraw funds, and view their account balance.
The system should also include basic error handling, such as preventing users from withdrawing more funds than they have in their account.
The The system should allow users to buy and sell stocks, and keep track of their portfolio.
The system should be able to generate reports on user activity, such as total deposits, withdrawals, and trades made.
The system should be able to list the transactions that the user has made over time.
The system should not allow the user to withdraw fund when the account balance is negative or zero.
The system has access to a function get_share_price(symbol) which returns the current price of a stock given its symbol."""

module_name = "accounts.py"
classname = "Account"



def run():
    """
    Run the crew.
    """
    inputs = {
        'requirements': requirements,
        'module_name': module_name,
        'classname': classname

    }

    try:
        EngineeringTeam().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


if __name__ == "__main__":
    run()