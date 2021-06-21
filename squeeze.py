import os
import csv
import argparse

import lib

parser = argparse.ArgumentParser()
parser.add_argument('-v', help='Data dir, default "data"', default='data')
args = parser.parse_args()

partyMap = { 'TOTAL VOTOS VALIDOS':                            'validos',
             'VOTOS EN BLANCO':                                'blancos',
             'VOTOS NULOS':                                    'nulos',
             'VOTOS IMPUGNADOS':                               'impug',
             'TOTAL VOTOS EMITIDOS':                           'emit',

             'ACCION POPULAR':                                 'ap',
             'ALIANZA PARA EL PROGRESO':                       'app',
             'AVANZA PAIS - PARTIDO DE INTEGRACION SOCIAL':    'avp',
             'DEMOCRACIA DIRECTA':                             'pdd',
             'EL FRENTE AMPLIO POR JUSTICIA, VIDA Y LIBERTAD': 'fa',
             'FUERZA POPULAR':                                 'fp',
             'JUNTOS POR EL PERU':                             'jp',
             'PARTIDO DEMOCRATICO SOMOS PERU':                 'sp',
             'PARTIDO MORADO':                                 'pm',
             'PARTIDO NACIONALISTA PERUANO':                   'pnp',
             'PARTIDO POLITICO NACIONAL PERU LIBRE':           'pl',
             'PARTIDO POPULAR CRISTIANO - PPC':                'ppc',
             'PERU PATRIA SEGURA':                             'pps',
             'PODEMOS PERU':                                   'pp',
             'RENACIMIENTO UNIDO NACIONAL':                    'runa',
             'RENOVACION POPULAR':                             'rp',
             'UNION POR EL PERU':                              'upp',
             'VICTORIA NACIONAL':                              'vn' }

rows = []
for fn in os.listdir(args.v):
    d = lib.readActa(os.path.join(args.v, fn))
    aut = {}
    for e in d['votos']:
        aut[e['AUTORIDAD']] = e['congresal']
    row = { 'mesa':          lib.iForFn(fn),
            'dpto':          d['presidencial']['DEPARTAMENTO'],
            'provincia':     d['presidencial']['PROVINCIA'],
            'distrito':      d['presidencial']['DISTRITO'],
            'local':         d['presidencial']['TNOMB_LOCAL'],
            'direcc':        d['presidencial']['TDIRE_LOCAL'],
            'electores.hab': d['presidencial']['NNUME_HABILM'],
            'votantes':      d['presidencial']['TOT_CIUDADANOS_VOTARON'],
            'estado.acta':   d['presidencial']['OBSERVACION_TXT'] }
    for p, v in aut.items():
        if p in partyMap:
            row['votos.%s' % partyMap[p]] = v
    rows.append(row)

with open('actas.csv', 'w') as csvfile:
    csvwriter = csv.DictWriter(csvfile, fieldnames=list(rows[0].keys()))
    csvwriter.writeheader()
    for row in rows:
        csvwriter.writerow(row)
