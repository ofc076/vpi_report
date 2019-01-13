#!/usr/bin/python3
# -*- coding: utf-8 -*-


import datetime, calendar
from vpi_settings import fields_f4, fields_f6, alias, totalName, orderList
from vpi_func import reportCompile, convToBytes, cleenArr, reqToMsm
from vpi_html import printSorted


def weekDate():
    lastSunday = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    lastSunday -= oneday

    while lastSunday.weekday() != calendar.SUNDAY:  # Monday is 0 and Sunday is 6.
        lastSunday -= oneday

    dateEnd = lastSunday.strftime("%d.%m.%y")
    Monday = lastSunday - datetime.timedelta(days=6)
    dateBgn = Monday.strftime("%d.%m.%y")
 #   print('From {} to {}'.format(dateBgn, dateEnd))
    return dateBgn, dateEnd


def prevMonthDate():
    today = datetime.date.today()
    first = today.replace(day=1)
    lastMonth = first - datetime.timedelta(days=1)
    dateEnd = lastMonth.strftime("%d.%m.%y")
    dateBgn = lastMonth.strftime("01.%m.%y")
    return dateBgn, dateEnd



def main():
    dateBgn, dateEnd = weekDate()
    arr = reqToMsm('4', dateBgn, dateEnd)
    for i in arr:
        i[0] = i[0].replace('Итого по АС ', '')
 #   for i in arr:
 #       print(i)
    result = {}
    for i in arr[1:-1]:
        result[i[0]] = {'alien': 0, 'alienSum': 0, 'total': 0, 'totalSum':0}
    head_f4 = arr[0]
    for k in fields_f4:
        for line in arr[1:-1]:
            indx = head_f4.index(k)
            result[line[0]][k] = line[indx]

    for realAS in alias:
        aliasArr = alias[realAS]
        for AS in result:
            if AS in aliasArr:
                for k in result[AS]:
                    result[realAS][k] = float(result[AS][k]) + float(result[realAS][k])

    allAlias = []
    for AS in alias:
        allAlias.extend(alias[AS])
    for AS in allAlias:
        del result[AS]
 #   print('*************************************************')

    for i in result:
        result[i]['totalSum'] = round(float(result[i]['По ведом#']) + float(result[i]['Комис.$']) + float(result[i]['Станц.$']), 2)
        result[i]['total'] = int(result[i]['Б-тов'])

    result[totalName] = {'alien': 0, 'alienSum': 0, 'total': 0, 'totalSum':0}

    result = cleenArr(result)

    arr = reqToMsm('6', dateBgn, dateEnd)
    for i in arr:
        i[0] = i[0].replace('Всего по ведомостям ', '')

    result6 = {}
    for i in arr[1:-1]:
        result6[i[0]]={}
    head_f6 = arr[0]
    for k in fields_f6:
        for line in arr[1:-1]:
            indx = head_f6.index(k)
            result6[line[0]][k] = line[indx]
    for k in result6:
        result[k]['alien'] = result6[k][' Оп.']
        result[k]['alienSum'] = result6[k]['Всего#']

    alien = 0
    alienSum = 0
    total = 0
    totalSum = 0
    for AS in result:
        alien += int(result[AS]['alien'])
        alienSum += float(result[AS]['alienSum'])
        total += int(result[AS]['total'])
        totalSum += float(result[AS]['totalSum'])
    result[totalName] = {'alien': round(alien), 'alienSum': round(alienSum,2), 'total': round(total), 'totalSum': round(totalSum,2)}

#    print('-*-*-*-*-*--*-*-*--*-*-*-*-*-*-*-*-*-*--*-*-*-*-*')
#    print(result6)

    printSorted(result, dateBgn, dateEnd)




if __name__ == '__main__':
    try:
        main()
    except:
        print('Сервер вернул некорректный набор данных или превышено время ожидания')
    exit()


