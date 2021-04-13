# QuantPython
A simple project to use pykrx package and sqlite3 to manage Korean stock quote data

## Problems in Korean stock data
Both financial statements and quotes are important to analyze stocks. However, Korean market has two different sources for these data.
Korean Financial Supervisory Service supports DART, which is a service providing financial statements of companies in Korean equity market.
Meanwhile, Korea Exchange (KRX) provides quote data.

This project aims to merge these two heterogeneous, yet crucial dataset into a single RDBMS schema.
