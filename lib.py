import os
import json
import pickle

from selenium import webdriver

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

def nextI():
    df = dataFiles()
    if len(df) > 0:
        lastID = iForFn(df[-1])
        if lastID in ID_RANGE and ID_RANGE.index(lastID) + 1 < len(ID_RANGE):
            return ID_RANGE[ID_RANGE.index(lastID) + 1]
    else:
        return ID_RANGE[0]

def readActa(fn):
    with open(fn, 'rb') as f:
        d = pickle.load(f)['procesos']['generalPre']
    return d

def actasJEE():
    return [ i for i in haveI() if 'JEE' in readActa(fnForI(i))['presidencial']['OBSERVACION_TXT'] ]

class ONPEClient:
    def __init__(self):
        fp = webdriver.FirefoxProfile()
        fp.set_preference('', False)
        self.d = webdriver.Firefox(firefox_profile=fp)

    def getActa(self, i):
        self.d.get('https://api.resultadossep.eleccionesgenerales2021.pe/mesas/detalle/%s?name=param' % fmtId(i))
        return json.loads(self.d.find_element_by_tag_name('body').text)

    def __del__(self):
        self.d.quit()
