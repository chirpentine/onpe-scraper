import os
import json
import time
import pickle
import logging
import threading

from selenium import webdriver

logging.basicConfig(level=logging.INFO)

DATA_DIR = 'data'
ID_RANGE = list(range(1, 83381)) + list(range(900001, 903109))

def fmtId(i):
    return str(i).rjust(6, '0')

def dataFiles():
    return sorted(os.listdir(DATA_DIR))

def haveI():
    return [ iForFn(x) for x in dataFiles() ]

def fnForI(i):
    return os.path.join(DATA_DIR, fmtId(i) + '.p')

def iForFn(fn):
    return int(fn.split('.')[0])

def lackingActas():
    return list(set(ID_RANGE).difference(set(haveI())))

def readActa(fn):
    with open(fn, 'rb') as f:
        d = pickle.load(f)['procesos']['generalPre']
    return d

def actasJEE():
    return [ i for i in haveI() if 'JEE' in readActa(fnForI(i))['presidencial']['OBSERVACION_TXT'] ]

def chunks(l, n):
    for i in range(n):
        yield l[i::n]

class ONPEClient:
    def __init__(self, baseUrl='v2', onlyJEE=False):
        self.setBaseUrl(baseUrl)
        self.onlyJEE = onlyJEE
        self.d = None

        logging.debug('ONPEClient(%s) initted', id(self))

    def getActa(self, i):
        self.d.get(self.baseUrl + ('%s?name=param' % fmtId(i)))
        return json.loads(self.d.find_element_by_tag_name('body').text)

    def setBaseUrl(self, baseUrl):
        urlmap = { 'v1': 'https://resultadoshistorico.onpe.gob.pe/v1/EG2021/mesas/detalle/',
                   'v2': 'https://api.resultadossep.eleccionesgenerales2021.pe/mesas/detalle/' }
        self.baseUrl = baseUrl if baseUrl not in urlmap else urlmap[baseUrl]

    def setupWebdriver(self):
        fp = webdriver.FirefoxProfile()
        fp.set_preference('', False)
        self.d = webdriver.Firefox(firefox_profile=fp)

    def getList(self, l):
        logging.debug('ONPEClient(%s).getList(%s)', id(self), l[:5])
        if self.d is None:
            self.setupWebdriver()

        logging.debug('ONPEClient(%s).getList(%s) webdriver setup complete, going to run', id(self), l[:5])
        errors = 0
        for i in l:
            try:
                ad = self.getActa(i)
                if 'generalPre' in ad['procesos']:
                    # we got data
                    errors = 0
                    if (self.onlyJEE and 'JEE' not in ad['procesos']['generalPre']['presidencial']['OBSERVACION_TXT']) or (not self.onlyJEE):
                        fn = fnForI(i)
                        pickle.dump(ad, open(fn, 'wb'))
                        logging.info('Wrote %s', fn)
            except json.decoder.JSONDecodeError:
                errors += 1
                if errors == 5:
                    logging.error('Exiting due to excess errors')
                    break
                else:
                    logging.error('JSONDecodeError, sleeping 1s')
                    time.sleep(1)

    def __del__(self):
        if self.d is not None:
            self.d.quit()


class ONPEClientParallel:
    def __init__(self, *args, **kwargs):
        self.args   = args
        self.kwargs = kwargs

    def getList(self, l, workers=2):
        wp = []
        wt = []
        for ll in chunks(l, workers):
            wp.append(ONPEClient(*self.args, **self.kwargs))
            wt.append(threading.Thread(target=wp[-1].getList, args=(ll,)))
            wt[-1].start()
        [ t.join() for t in wt ]
