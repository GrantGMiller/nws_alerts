'''
See https://alerts.weather.gov/ for complete zone list

The ATOM and CAP feeds are updated about every two minutes.
'''
import datetime
import time

from nws import NWS

nws = NWS()


@nws.alert(state='NC', severity='Moderate')
def MyStateAlertSevere(entry):
    print('MyStateAlertSevere(', entry)


@nws.alert(zone='NCC101', severity='Severe')
def MyZoneAlert(entry):
    print('MyZoneAlert(', entry)


print('nowAlerts=')
nowAlerts = nws.NowAlerts()  # only returns events you have subscribed to with @nws.alert
for entry in nowAlerts:
    print('now entry=', entry)
    print('urgency=', entry.severity)
    print('urgency=', entry.urgency)
    print('urgency=', entry.certainty)

    if entry.severity == 'Severe':
        print('!!!!!!!!!!!!!!!!!!!!!!!! SEVERE !!!!!!!!!!!!!!!!!!!!!!!!!!!!')

print('end main.py')
