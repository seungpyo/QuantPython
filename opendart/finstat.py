import config
import corpcode
import requests
import json

reportCode = {'1Q': '11013', '2Q': '11012', '3Q': '11014', '4Q': '11011'}


class FinStat:
    def __init__(self, name, corp_code, bsns_year, reprt_code):
        self.name = name
        self.corp_code = corp_code
        self.bsns_year = bsns_year
        self.reprt_code = reprt_code

        self.rawJSON = self.getFinStatJSON()

        self.stockCode = 0
        self.corpCode = 0
        self.currentAsset = 0
        self.nonCurrentAsset = 0

        self.parseFinStat()

    def getFinStatJSON(self):
        assert(self.reprt_code in ['11013', '11012', '11014', '11011'])
        url = 'https://opendart.fss.or.kr/api/fnlttSinglAcnt.json'
        params = {'crtfc_key': config.crtfc_key,
                  'corp_code': self.corp_code,
                  'bsns_year': self.bsns_year,
                  'reprt_code': self.reprt_code}
        print('getFinStatJSON: Connecting to {0}...'.format(url))
        res = requests.get(url, params=params)
        if res.status_code != 200:
            print('getFinStatJSON: {0} returned status code {1}'.
                  format(url, res.status_code))
            return None
        print('getFinStatJSON: Downloaded account as a JSON format')
        # print(str(res.content, 'utf-8'))
        accountJson = json.loads(res.content)
        print('getFinStatJSON: Transformed into a JSON object')
        return accountJson

    def parseFinStat(self):
        accounts = self.rawJSON['list']
        for account in accounts:
            if account['account_nm'] == '유동자산':
                self.currentAsset = account['thstrm_amount']
            if account['account_nm'] == '비유동자산':
                self.nonCurrentAsset = account['thstrm_amount']


if __name__ == '__main__':
    corpCodes = corpcode.loadCorpCodes()
    code = corpCodes['삼성전자']
    aj = FinStat('삼성전자', code, 2019, reportCode['1Q'])
    print(aj.currentAsset, aj.nonCurrentAsset)