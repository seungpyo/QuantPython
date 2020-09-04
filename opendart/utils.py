import config


def debugPrint(func, msg, minimumVerbosity=1):
    log = '{0}: {1}'.format(func, msg)
    if config.debugVerbosity >= minimumVerbosity:
            print(log)
    else:
        pass
    

def commasToInt(s):
    return int(s.replace(',', ''))


def intToCommas(i):
    return '{:,}'.format(i)
    

if __name__ == '__main__':
    print(commasToInt('123,456,789,000') + 100)
    print(intToCommas(1234567890))