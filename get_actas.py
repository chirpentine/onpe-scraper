import time
import json
import pickle
import logging
import argparse

import lib

parser = argparse.ArgumentParser()
parser.add_argument('-a', help='Only download actas para envío al JEE', action='store_true')
parser.add_argument('-n', help='Download specific acta(s)')
parser.add_argument('-v', help='Download specific vuelta (v1, v2, or url base)', default='v2')
args = parser.parse_args()

logging.basicConfig(level=logging.INFO)

i = lib.nextI()
if args.a or args.n is not None or i is not None:
    logging.info('running')

    toGet = None
    if args.a:
        logging.info('Building list of JEE actas...')
        toGet = lib.actasJEE()
    elif args.n is not None:
        toGet = [ int(x) for x in args.n.split(',') ]
    else:
        toGet = lib.ID_RANGE[lib.ID_RANGE.index(i):]
    errors = 0

    c = lib.ONPEClient(args.v)

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
