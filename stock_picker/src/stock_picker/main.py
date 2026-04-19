#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from stock_picker.crew import StockPicker
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """
    inputs = {
        'sector': 'Pharmaceuticals',
    }

    result = StockPicker().crew().kickoff(inputs=inputs)
    print("Crew finished successfully!")
    print(result.raw)



if __name__ == "__main__":
    run()