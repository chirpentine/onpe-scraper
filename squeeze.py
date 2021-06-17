import csv

import lib

fieldnames = [ 'mesa',
               'dpto',
               'provincia',
               'distrito',
               'local',
               'direcc',
               'electores.hab',
               'votantes',
               'estado.acta',
               'votos.validos',
               'votos.blancos',
               'votos.nulos',
               'votos.impug',
               'votos.fp',
               'votos.pl',
               'votos.emit' ]

with open('actas.csv', 'w') as csvfile:
    csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
    csvwriter.writeheader()
    for i in lib.ID_RANGE:
        d = lib.readActa(lib.fnForI(i))
        aut = {}
        for e in d['votos']:
            aut[e['AUTORIDAD']] = e['congresal']
        csvwriter.writerow({ 'mesa':          i,
                             'dpto':          d['presidencial']['DEPARTAMENTO'],
                             'provincia':     d['presidencial']['PROVINCIA'],
                             'distrito':      d['presidencial']['DISTRITO'],
                             'local':         d['presidencial']['TNOMB_LOCAL'],
                             'direcc':        d['presidencial']['TDIRE_LOCAL'],
                             'electores.hab': d['presidencial']['NNUME_HABILM'],
                             'votantes':      d['presidencial']['TOT_CIUDADANOS_VOTARON'],
                             'estado.acta':   d['presidencial']['OBSERVACION_TXT'],
                             'votos.validos': aut['TOTAL VOTOS VALIDOS'],
                             'votos.blancos': aut['VOTOS EN BLANCO'],
                             'votos.nulos':   aut['VOTOS NULOS'],
                             'votos.impug':   aut['VOTOS IMPUGNADOS'],
                             'votos.fp':      aut['FUERZA POPULAR'],
                             'votos.pl':      aut['PARTIDO POLITICO NACIONAL PERU LIBRE'],
                             'votos.emit':    aut['TOTAL VOTOS EMITIDOS'] })
