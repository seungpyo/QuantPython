import shutil, os, sys


def clearData():
    path = os.path.join(os.path.dirname(__file__), 'data')
    if os.path.exists(path):
        shutil.rmtree() 
    
if __name__ == '__main__':
    
    sys.path.insert(1, os.path.join(os.path.dirname(__file__), 'minerva'))

    import minerva.config
    import minerva.corpcode
    import minerva.finstat
    import minerva.quotes
    import minerva.stockcode
    from minerva.utils import *
    
    debugPrint('Cleaning data...')
    clearData()
    
    debugPrint('Loading corporation codes...')
    minerva.corpcode.loadCorpCodes()
    debugPrint('Creating and populating the STOCK_CODE table...')
    minerva.stockcode.createStockCodeTable()
    debugPrint('Creating the QUOTES table...')
    minerva.quotes.createQuotesTable()
    # debugPrint('easy_init', 'Populating the QUOTES table...')
    debugPrint('Initialization complete!', 0)
    
