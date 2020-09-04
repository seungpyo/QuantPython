import requests
import config
import os
import pickle
import zipfile
import xml.etree.ElementTree as elemTree
from utils import debugPrint


def loadCorpCodesCached():
    corpCode = None
    if os.path.exists(config.corpCodePklPath):
        with open(config.corpCodePklPath, 'rb') as f:
            corpCode = pickle.load(f)
    return corpCode


def loadCorpCodes():
    # Check if pickle already exists
    corpCode = loadCorpCodesCached()
    if corpCode is not None:
        debugPrint('loadCorpCodes', 'corpCode cache hit!')
        return corpCode

    # Fetch Zipped XML from OPEN DART
    baseUrl = 'https://opendart.fss.or.kr/api/corpCode.xml'
    params = {'crtfc_key': config.crtfc_key}
    res = requests.get(baseUrl, params=params)
    debugPrint('loadCorpCodes', 'Downloading corpcode zip file...')
    if res.status_code != 200:
        debugPrint('loadCorpCodes', '{0} returned status code {1}'.
              format(baseUrl, res.status_code))
        return None
    debugPrint('loadCorpCodes', 'Downloaded corpcode zip file')

    # Save zip file
    debugPrint('loadCorpCodes', 'Saving corpcode zip file...')
    if not os.path.exists(config.dataPath):
        os.mkdir(config.dataPath)
    with open(config.corpCodeZipPath, 'wb') as f:
        for chunk in res.iter_content(chunk_size=128):
            f.write(chunk)
    debugPrint('loadCorpCodes', 'Saved corpcode zip file')

    # Extract zip file and save it as an XML file
    debugPrint('loadCorpCodes', 'Extracting corpcode zip file...')
    with zipfile.ZipFile(config.corpCodeZipPath) as zf:
        zf.extractall(config.dataPath)
    debugPrint('loadCorpCodes', 'Extracted corpcode zip file')

    # Transfrom XML as an dictionary
    debugPrint('loadCorpCodes', 'Transforming XML into dictionary...')
    corpCode = dict()
    tree = elemTree.parse(config.corpCodeXmlPath)
    for elem in tree.iter('list'):
        code = elem.find('corp_code').text
        name = elem.find('corp_name').text
        corpCode[name] = code
    debugPrint('loadCorpCodes', 'Transformed XML into dictionary')

    # Cache the dictionary as a pickle object
    debugPrint('loadCorpCodes', 'Saving dictonary as a pickle object...')
    with open(config.corpCodePklPath, 'wb') as f:
        pickle.dump(corpCode, f)
    debugPrint('loadCorpCodes', 'Saved dictonary as a pickle object')

    return corpCode


if __name__ == '__main__':
    corpCode = loadCorpCodes()
    print(corpCode['다코'], corpCode['일산약품'])
    print(corpCode['삼성전자'])