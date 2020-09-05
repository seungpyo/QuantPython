import pandas as pd
import matplotlib.pyplot as plt

# Does goormide support GUI plotting?
def plotQuotes(q, column='close'):
    assert column in ['open', 'high', 'low', 'close']
    plt.plot(q['date'], q[column])
    plt.show()