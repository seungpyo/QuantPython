import config
import inspect
import sys

def debugPrint(msg, minimumVerbosity=1):
    # func = inspect.stack()[1].function
    func = sys._getframe(1).f_code.co_name
    log = '{0}: {1}'.format(func, msg)
    if config.debugVerbosity >= minimumVerbosity:
            print(log)
    else:
        pass
    

def commasToInt(s):
    return int(s.replace(',', ''))


def intToCommas(i):
    return '{:,}'.format(i)
    

def dpStub():
    debugPrint('hey there')
    
if __name__ == '__main__':
    print(commasToInt('123,456,789,000') + 100)
    print(intToCommas(1234567890))
    dpStub()