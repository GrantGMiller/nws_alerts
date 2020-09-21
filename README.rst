NWS_Alert
=========

A easy way to subscribe to National Weather Service (NWS) alerts.

Install
=======

::

    pip install nws_alert

Usage
=====

::


    from nws import NWS

    nws = NWS()


    # Subscribe to alerts in North Carolina with severity "Moderate" or "Severe"
    @nws.alert(state='NC', severity='Moderate')
    @nws.alert(state='NC', severity='Severe')
    def MyStateAlert(entry):
        print('MyStateAlert(', entry.severity, entry.title)


    # Subscribe to events in my "zone" with urgency "Immediate"
    @nws.alert(zone='NCC101', urgency='Immediate')  # See https://alerts.weather.gov/ for complete zone list
    def MyZoneAlert(entry):
        print('MyZoneAlert(', entry.urgency, entry.title)


    # nws.NowAlerts() will return any event happening now. It will not return future or past events.
    # Only events from states/zones you have subscribed to with @nws.alert will be included.
    # This will return all events regardless of severity, certainty, or urgency

    nowAlerts = nws.NowAlerts()
    for entry in nowAlerts:
        print('now entry=', entry)

Notes
=====

The @nws.alert decorator will only be triggered once per NWS alert.
The alerts are logged to a JSON file in the current directory so that the code will remember which alerts have already been triggered.

Event Attributes
================

See https://docs.oasis-open.org/emergency/cap/v1.2/CAP-v1.2-os.pdf for more detailed CAP info

SEVERITY:

* Severe: Significant threat to life or property
* Moderate: Possible threat to life or property
* Minor: Minimal to no known threat to life or property
* Unknown: Severity unknown

CERTAINTY:

* Observed: Determined to have occurred or to be ongoing
* Likely: Likely (p > ~50%)
* Possible: Possible but not likely (p <= ~50%)
* Unlikely: Not expected to occur (p ~ 0)
* Unknown: Certainty unknown

URGENCY:

* Immediate: Responsive action SHOULD be taken immediately
* Expected: Responsive action SHOULD be taken soon (within next hour)
* Future: Responsive action SHOULD be taken in the near future
* Past: Responsive action is no longer required
* Unknown: Urgency not known