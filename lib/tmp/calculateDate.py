import datetime, calendar

lastSunday = datetime.date.today()
oneday = datetime.timedelta(days=1)
lastSunday -= oneday

while lastSunday.weekday() != calendar.SUNDAY:  # Monday is 0 and Sunday is 6.
    lastSunday -= oneday

dateEnd = lastSunday.strftime("%d.%m.%y")
Monday = lastSunday - datetime.timedelta(days=6)
dateBgn = Monday.strftime("%d.%m.%y")
print('{} - {}'.format(dateBgn, dateEnd))
