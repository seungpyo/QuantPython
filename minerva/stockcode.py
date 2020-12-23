import pandas as pd
import sqlite3 as sl
import config
import os
import sys


def createStockCodeTable():
    df = pd.read_html(
        'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download',
        header=0)
    df = df[0][['회사명', '종목코드']]
    df = df.rename(columns={'회사명': 'corp_name', '종목코드': 'stock_code'})
    df = df.astype({'stock_code': str})
    df['stock_code'] = df['stock_code'].apply(
        lambda x: x.zfill(config.stockCodeLen))

    try:
        dbPath = os.path.join(config.dataPath, config.dbName)
        with sl.connect(dbPath) as con:
            con.execute('''
                CREATE TABLE IF NOT EXISTS STOCK_CODE (
                    corp_name TEXT NOT NULL PRIMARY KEY,
                    stock_code TEXT NOT NULL
                );
            ''')
            df.to_sql('STOCK_CODE', con, if_exists='replace')
    except sl.OperationalError as e:
        print('Failed to open database file at: {0}'.format(config.dbName))
        print(e)
        sys.exit(1)


def getStockCode(corpName, marketCode='KS'):
    assert marketCode in ['KS', 'KQ'], \
        'Expected "KS" (KOSPI) or "KQ" (KOSDAQ), got "{0}"'.format(marketCode)

    with sl.connect(config.dbName) as con:
        res = con.execute('''
            SELECT stock_code
            FROM STOCK_CODE
            WHERE corp_name='{0}';
        '''.format(corpName)
        )
        fetched = res.fetchone()
        if fetched is None:
            return config.noSuchStockCode
        return "{0}.{1}".format(fetched[0], marketCode)


def describeStockCode():
    with sl.connect(config.dbName) as con:
        res = con.execute('''
            pragma table_info('STOCK_CODE');
        ''')
        for row in res:
            print(row)


if __name__ == '__main__':
    # populateStockCode()
    # describeStockCode()
    print(getStockCode('교보메리츠'))
    print(getStockCode('삼성전자'))

