import shutil, os, sys


def clearData():
    shutil.rmtree(os.path.join(os.path.dirname(__file__), 'data')) 
    
if __name__ == '__main__':
    
    sys.path.insert(1, os.path.join(os.path.dirname(__file__), 'minerva'))

    import minerva.config
    import minerva.corpcode
    import minerva.finstat
    import minerva.quotes
    import minerva.stockcode
    from minerva.utils import *
    
    debugPrint('easy_init', 'Loading corporation codes...')
    minerva.corpcode.loadCorpCodes()
    debugPrint('easy_init', 'Creating and populating the STOCK_CODE table...')
    minerva.stockcode.createStockCodeTable()
    debugPrint('easy_init', 'Creating the QUOTES table...')
    minerva.quotes.createQuotesTable()
    # debugPrint('easy_init', 'Populating the QUOTES table...')
    debugPrint('easy_init', 'Initialization complete!', 0)
    