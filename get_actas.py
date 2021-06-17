import time
import json
import pickle
import logging
import argparse

import lib

parser = argparse.ArgumentParser()
parser.add_argument('-a', help='Only download actas para envío al JEE', action='store_true')
args = parser.parse_args()

logging.basicConfig(level=logging.INFO)

i = lib.nextI()
if args.a or i is not None:
    logging.info('running')

    toGet = None
    if args.a:
        logging.info('Building list of JEE actas...')
        toGet = lib.actasJEE()
    else:
        toGet = lib.ID_RANGE[lib.ID_RANGE.index(i):]
    errors = 0

    c = lib.ONPEClient()

    try:
        for i in toGet:
            try:
                ad = c.getActa(i)
                if 'generalPre' in ad['procesos']:
                    # we got data
                    errors = 0
                    if (args.a and 'JEE' not in ad['procesos']['generalPre']['presidencial']['OBSERVACION_TXT']) or (not args.a):
                        fn = lib.fnForI(i)
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
    finally:
        del c

    logging.info('Finished')
