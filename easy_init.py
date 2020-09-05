import minerva.config
import minerva.corpcode
import minerva.finstat
import minerva.quotes
import minerva.stockcode
from minerva.utils import *


if __name__ == '__main__':
    debugPrint('easy_init', 'Loading corporation codes...')
    minerva.corpcode.loadCorpCodes()
    debugPrint('easy_init', 'Creating and populating the STOCK_CODE table...')
    minerva.stockcode.createStockCodeTable()
    debugPrint('easy_init', 'Creating the QUOTES table...')
    minerva.quotes.createQuotesTable()
    # debugPrint('easy_init', 'Populating the QUOTES table...')
    debugPrint('easy_init', 'Initialization complete!', 0)
    