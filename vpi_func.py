#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from subprocess import Popen, PIPE, STDOUT
from vpi_settings import totalName, SERVER, WORKDIR


def reportCompile(num, dateBgn='01.01.18', dateEnd='31.12.18'):
    text = ''
    fileName = os.path.join(WORKDIR, num + '.report')
    with open(fileName, 'r', encoding='koi8-u') as f:
        for line in f:
            text += line.replace('<<DateStr>>', dateBgn).replace('<<DateEnd>>', dateEnd)
 #   print(text)
    return text


def convToBytes(num, text):
    byteText = b''
    fileName = os.path.join(WORKDIR, num + '.req.tmp')
    with open(fileName, 'w', encoding='koi8-r') as f:
        f.write(text)
    with open(fileName, 'rb') as f:
        byteText = f.read()
    return byteText



def cleenArr(arr):
    fieldsList = []
    newArr = {}
    for k in arr[totalName]:
        fieldsList.append(k)
    for AS in arr:
        newArr[AS] = {}
        for f in fieldsList:
            newArr[AS][f] = arr[AS][f]
    return newArr


# Обманка для запроса не от МСМ, а из лок.файла (.resp)
def pseudoReqToMsm(num):
    fileName = os.path.join(WORKDIR, num + '.resp')
    with open(fileName,'r',encoding='utf-8') as f:
        resp = f.read()
    arr = resp.split('\n')
    table = []
    for line in arr:
        current = line.strip().split(';')
        if len(current) < 2:
            continue
        table.append(current)
  #  for i in table:
  #      print(i)
  #  print('============================================')
    return table



def reqToMsm(num, dateBgn, dateEnd):
    text = reportCompile(num, dateBgn, dateEnd)
    aprMagic = convToBytes(num, text)
    cmdStr = '/var/vpi_report/Report.pl.ip -p {} -I'.format(SERVER)
    cmdArr = []
    cmdArr.append(cmdStr)
#    print('----------------started----------------------')
    p = Popen(cmdArr, shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    grep_stdout = p.communicate(input=aprMagic)[0]
    resp = grep_stdout.decode('koi8-u')
#    print(resp)
    arr = resp.split('\n')
    table = []
    for line in arr:
        current = line.strip().split(';')
        if len(current) < 2:
            continue
        table.append(current)
  #  for i in table:
  #      print(i)
  #  print('============================================')
    return table
