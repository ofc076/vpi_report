#!/usr/bin/python3
# -*- coding: utf-8 -*-


import datetime
from vpi_settings import totalName, orderList


def printSorted(arr, dateBgn, dateEnd):
    print('<!DOCTYPE html><html><head>')
    print('<meta charset="utf-8"> <title>Отчет (чужие)</title>')
    print('<style> table, th, td {border: 1px solid black; border-collapse: collapse; } </style> ')
    print('</head><body>')
    print('<h2 style="text-align: center;">Відсоток віддаленого продажу за період (операції гостей)</h2>')
    print('<h3 style="text-align: center;">{} - {}</h3>'.format(dateBgn, dateEnd))
    print('<table cellpadding="7px" style="width: 100%;">')
    print('<tr style="text-align: center;">')
    print('<td>Автостанція</td> <td>к-ть відд.</td> <td>к-ть всього</td> <td>к-ть %</td> <td>сума відд.</td> <td>сума всього</td> <td>сума %</td>')
    print('</tr>')
    for i in orderList:
        print('<tr style="text-align: right;">')
        for AS in arr:
            if AS == i:
                try:
                    prc = float(arr[AS]['alien']) / float(arr[AS]['total']) * 100
                except:
                    prc = 0
                try:
                    prcSum = float(arr[AS]['alienSum']) / float(arr[AS]['totalSum']) * 100
                except:
                    prcSum = 0

                print('<td style="text-align: left;">{}</td>'.format(AS).replace(totalName,''))
                print('<td>{}</td> <td>{}</td> <td>{:.2f}%</td>'.format( arr[AS]['alien'], arr[AS]['total'], prc).replace(',',' '))
                print('<td>{:,.2f}</td> <td>{:,.2f}</td> <td>{:.2f}%</td>'.format(float(arr[AS]['alienSum']), arr[AS]['totalSum'], prcSum).replace(',',' '))
        print('</tr>')
    print('</table>')
    print('<p style="text-align: right;">Generated: {}</p>'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    print('</body></html>')