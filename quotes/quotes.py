import sqlite3 as sl
import pandas as pd
import stockCodes
import config
import pandas_datareader.data as web


def createQuotesTable():
    con = sl.connect(config.dbName)
    with con:
        con.execute('''
            CREATE TABLE IF NOT EXISTS QUOTES (
                stock_code TEXT NOT NULL PRIMARY KEY,
                date TEXT,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume REAL,
                adj_close REAL,
                FOREIGN KEY(stock_code) REFERENCES STOCK_CODES(stock_code),
                CHECK(low < open AND low < high AND low < close
                AND high > open AND high > close)
            );
        ''')


def describeQuotes():
    with sl.connect(config.dbName) as con:
        res = con.execute('''
            pragma table_info('QUOTES');
        ''')
        for row in res:
            print(row)


def dropQuotes():
    with sl.connect(config.dbName) as con:
        con.execute('''
            DROP TABLE IF EXISTS QUOTES;
        ''')


def insertQuotes(stockCode, startDate, endDate, source='yahoo'):
    df = web.DataReader(stockCode, source, startDate, endDate)
    df['stock_code'] = stockCode
    df['date'] = df.index
    df = df.rename(columns={
        'High': 'high', 'Low': 'low', 'Open': 'open', 'Close': 'close',
        'Volume': 'volume', 'Adj Close': 'adj_close'})
    df = df[['stock_code', 'date',
            'open', 'high', 'low', 'close', 'volume', 'adj_close']]
    with sl.connect(config.dbName) as con:
        df.to_sql('QUOTES', con, if_exists='replace', index=False)


def getQuotes(stockCode, startDate, endDate):
    with sl.connect(config.dbName) as con:
        res = con.execute('''
            SELECT * FROM QUOTES
            WHERE stock_code='{0}' AND date BETWEEN '{1}' AND '{2}';
        '''.format(stockCode, startDate, endDate))
        cols = [column[0] for column in res.description]
        quotes = pd.DataFrame.from_records(data=res.fetchall(), columns=cols)
        return quotes


if __name__ == '__main__':
    dropQuotes()
    createQuotesTable()
    # describeQuotes()
    stockCode = stockCodes.getStockCode('삼성전자')
    insertQuotes(stockCode, '2020-01-01', '2020-09-02')
    ret = getQuotes(stockCode, '2020-01-17', '2020-04-02')
    print(ret)
