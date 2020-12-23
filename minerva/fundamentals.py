import stockcode
import quotes
import corpcode
import finstat
import config
import utils


def PER(corpName, )


if __name__ == '__main__':
    stockCode = stockCode.getStockCode('삼성전자')
    corpCodes = corpcode.loadCorpCodes()
    finStat = finstat.FinStat('삼성전자', corpCodes['삼성전자'], 2019, finstat.reportCode['4Q'])
    