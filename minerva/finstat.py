import requests
import json
import minerva.config as config
import minerva.corpcode as corpcode
from minerva.utils import debugPrint, commasToInt, intToCommas

reportCode = {'1Q': '11013', '2Q': '11012', '3Q': '11014', '4Q': '11011'}


class FinStat:
    def __init__(self, name, corp_code, bsns_year, reprt_code):
        self.name = name
        self.corp_code = corp_code
        self.bsns_year = bsns_year
        self.reprt_code = reprt_code

        self.rawJSON = self.getFinStatJSON()
        '''
        self.stockCode = 0
        self.corpCode = 0
        self.currentAsset = 0
        self.nonCurrentAsset = 0

        '''
        
        self.parseFinStat()

    def getFinStatJSON(self):
        assert(self.reprt_code in ['11013', '11012', '11014', '11011'])
        url = 'https://opendart.fss.or.kr/api/fnlttSinglAcnt.json'
        params = {'crtfc_key': config.crtfc_key,
                  'corp_code': self.corp_code,
                  'bsns_year': self.bsns_year,
                  'reprt_code': self.reprt_code}
        
        debugPrint('getFinStatJSON', 'Connecting to {0}...'.format(url))
        res = requests.get(url, params=params)
        if res.status_code != 200:
            print('getFinStatJSON: {0} returned status code {1}'.
                  format(url, res.status_code))
            return None
        debugPrint('getFinStatJSON', 'Downloaded account as a JSON format')
        # print(str(res.content, 'utf-8'))
        accountJson = json.loads(res.content)
        debugPrint('getFinStatJSON', 'Transformed into a JSON object')
        return accountJson

    def parseFinStat(self):
        accounts = self.rawJSON['list']
        self.stockCode = accounts[0]['stock_code']
        for account in accounts:
            # print('parseFinStat:' + account['account_nm'])
            if account['account_nm'] == '유동자산':
                self.currentAssets = commasToInt(account['thstrm_amount'])
            elif account['account_nm'] == '비유동자산':
                self.nonCurrentAssets = commasToInt(account['thstrm_amount'])
            elif account['account_nm'] == '자산총계':
                self.totalAssets = commasToInt(account['thstrm_amount'])
            elif account['account_nm'] == '유동부채':
                self.currentLiabilities = commasToInt(account['thstrm_amount'])
            elif account['account_nm'] == '비유동부채':
                self.nonCurrentLiabilities = commasToInt(account['thstrm_amount'])
            elif account['account_nm'] == '부채총계':
                self.totalLiabilities = commasToInt(account['thstrm_amount'])
            elif account['account_nm'] == '자본금':
                self.equityCapital = commasToInt(account['thstrm_amount'])
            elif account['account_nm'] == '이익잉여금':
                self.retainedEarnings = commasToInt(account['thstrm_amount'])
            elif account['account_nm'] == '자본총계':
                self.totalEquity = commasToInt(account['thstrm_amount'])
            elif account['account_nm'] == '매출액':
                self.revenues = commasToInt(account['thstrm_amount'])
            elif account['account_nm'] == '영업이익':
                self.incomeFromOperations = commasToInt(account['thstrm_amount'])
            elif account['account_nm'] == '법인세차감전 순이익':
                self.incomeBeforeTax = commasToInt(account['thstrm_amount'])
            elif account['account_nm'] == '당기순이익':
                self.netIncome = commasToInt(account['thstrm_amount'])
            else:
                debugPrint('parseFinStat', 'Unknown account_nm {0}'
                      .format(account['account_nm']))
            


if __name__ == '__main__':
    corpCodes = corpcode.loadCorpCodes()
    code = corpCodes['삼성전자']
    aj = FinStat('삼성전자', code, 2019, reportCode['1Q'])
    print(intToCommas(aj.currentAssets), intToCommas(aj.nonCurrentAssets))