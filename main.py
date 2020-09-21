'''
See https://alerts.weather.gov/ for complete zone list
'''
from nws_alerts import NWS
from nws_alerts import Subscription

nws = NWS()


# Subscribe to alerts in North Carolina with severity "Moderate" or "Severe"
# @nws.alert(state='NC', severity='Severe')
# @nws.alert(state='NC', severity='Moderate')
# def MyStateAlert(entry):
#     print('MyStateAlert(', entry.severity, entry.title)


# Subscribe to events in my "zone" with severity
# @nws.alert(zone='NCC101', urgency='Immediate')  # See https://alerts.weather.gov/ for complete zone list
# def MyZoneAlert(entry):
#     print('MyZoneAlert(', entry.urgency, entry.title)


# You can also create a subscription and updated it synchronously
sub = Subscription(state='NC', severity='Moderate')
entries = sub.Update()
print('entries=', entries)

# nws_alerts.NowAlerts() will return any event happening now. It will not return future or past events.
# Only events from states/zones you have subscribed to with @nws_alerts.alert will be included.
# This will return all events regardless of severity, certainty, or urgency
nowAlerts = nws.NowAlerts()

for entry in nowAlerts:
    print(entry.severity, entry.title)

print('end main.py')
