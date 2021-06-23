import argparse

import lib
from lib import logging

parser = argparse.ArgumentParser()
parser.add_argument('-a', help='Only download actas para envío al JEE', action='store_true')
parser.add_argument('-n', help='Download specific acta(s)')
parser.add_argument('-v', help='Download specific vuelta (v1, v2, or url base)', default='v2')
parser.add_argument('-b', help='Backend to use', default='ONPEClient', choices=[ 'ONPEClient', 'ONPEClientParallel' ])
args = parser.parse_args()

toGet = None
if args.a:
    logging.info('Building list of JEE actas...')
    toGet = lib.actasJEE()
elif args.n is not None:
    toGet = [ int(x) for x in args.n.split(',') ]
else:
    toGet = lib.lackingActas()

if len(toGet) > 0:
    logging.info('running')

    c = eval('lib.' + args.b)(args.v, args.a)

    try:
        c.getList(toGet)
    finally:
        del c

    logging.info('Finished')
