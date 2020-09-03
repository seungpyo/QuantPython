import config
import corpcode
import requests
import json

reportCode = {'1Q': '11013', '2Q': '11012', '3Q': '11014', '4Q': '11011'}


def assertReprtCode(reprt_code):
    assert(reprt_code in ['11013', '11012', '11014', '11011'])


def getAccountJSON(corp_code, bsns_year, reprt_code):
    assertReprtCode(reprt_code)

    url = 'https://opendart.fss.or.kr/api/fnlttSinglAcnt.json'
    params = {'crtfc_key': config.crtfc_key,
              'corp_code': corp_code,
              'bsns_year': bsns_year,
              'reprt_code': reprt_code}
    print('getAccountJSON: Connecting to {0}...'.format(url))
    res = requests.get(url, params=params)
    if res.status_code != 200:
        print('getAccountJSON: {0} returned status code {1}'.format(url, res.status_code))
        return None
    print('getAccountJSON: Downloaded account as a JSON format')
    # print(str(res.content, 'utf-8'))
    accountJson = json.loads(res.content)
    print('getAccountJSON: Transformed into a JSON object')
    return accountJson


def parseFinStat(rawJSON):
    accounts = rawJSON['list']
    for account in accounts:
        pass


if __name__ == '__main__':
    corpCodes = corpcode.loadCorpCodes()
    code = corpCodes['삼성전자']
    aj = getAccountJSON(code, 2019, reportCode['1Q'])
    for item in aj['list']:
        print(item)