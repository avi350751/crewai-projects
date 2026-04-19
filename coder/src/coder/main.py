#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from coder.crew import Coder
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """
    inputs = {
        'assignment': 'Write a Python program to calculate the first 20 numbers of the series\
       and multiplyting the total by 5: 3-5+7-9+11-.',
    }

    result = Coder().crew().kickoff(inputs=inputs)
    print(result.raw)


if __name__ == "__main__":
    run()