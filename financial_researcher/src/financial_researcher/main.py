#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from financial_researcher.crew import Financial_Researcher
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """
    inputs = {
        'company': 'Microsoft',
    }

    try:
        result = Financial_Researcher().crew().kickoff(inputs=inputs)
        print(result.raw)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
    
if __name__ == "__main__":
    run()
