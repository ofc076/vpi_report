#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os
from vpi_settings import WORKDIR
from shutil import copyfile


REPORT_LIST = ['week.html','month.html']


def reportCopy():
    for fileName in REPORT_LIST:
        fullName = os.path.join(WORKDIR, fileName)
        statinfo = os.stat(fullName)
#        print(statinfo.st_size)
        if statinfo.st_size > 2500:
            bkName = os.path.join(WORKDIR, 'bk_'+fileName)
            copyfile(fullName, bkName)





if __name__ == '__main__':
    try:
        reportCopy()
    except Exception as e:
        fullName = os.path.join(WORKDIR, 'backup_ERR.LOG')
        with open(fullName, "w") as f:
            f.write(e)
 #       pass
    exit()