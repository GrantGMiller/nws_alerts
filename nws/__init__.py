import datetime
import os
from .subscriptions import Subscription
import threading

DEBUG = False

UPDATE_INTERVAL = 60 * 2 if DEBUG is False else 30  # Per https://alerts.weather.gov/ feeds are updated every 2 minutes

if DEBUG is True:
    for file in os.listdir():
        if file.startswith('alert_history'):
            print('deleting', file)
            os.remove(file)


class NWS:
    def __init__(self):
        self._subscriptions = []
        self._timer = None
        self.ResetTimer()

    def ResetTimer(self):
        '''

        :return:
        '''
        if self._timer and self._timer.is_alive():
            self._timer.cancel()
        self._timer = threading.Timer(UPDATE_INTERVAL, self.Update)
        self._timer.start()

    def alert(self, *a, **kwargs):
        kwargs = dict((k.lower(), v.lower()) for k, v, in kwargs.items())

        def NewFunc(*a, **k):
            sub = Subscription(kwargs=kwargs, callback=a[0])
            self._subscriptions.append(sub)
            sub.Update()

        return NewFunc

    def Update(self):
        for sub in self._subscriptions:
            sub.Update()
        self.ResetTimer()

    def NowAlerts(self, **k):
        nowDT = datetime.datetime.utcnow()
        nowDT = nowDT.replace(tzinfo=datetime.timezone.utc)
        ret = []
        for sub in self._subscriptions:
            if sub.cap:
                try:
                    sub.Update()
                except Exception as e:
                    print(e)
                    continue

            for ID, entry in sub.cap.entries.items():
                try:
                    effective = datetime.datetime.fromisoformat(str(entry.effective))
                    expires = datetime.datetime.fromisoformat(str(entry.expires))
                    if effective < nowDT < expires:
                        ret.append(entry)
                except Exception as e:
                    print(e)
                    continue

        return ret


'''
See https://docs.oasis-open.org/emergency/cap/v1.2/CAP-v1.2-os.pdf for more detailed CAP info

SEVERITY:
“Severe” - Significant threat to life or property 
“Moderate” - Possible threat to life or property 
“Minor” – Minimal to no known threat to life or property 
“Unknown” - Severity unknown 

CERTAINTY:
“Observed” – Determined to have occurred or to be ongoing 
“Likely” - Likely (p > ~50%) 
“Possible” - Possible but not likely (p <= ~50%) 
“Unlikely” - Not expected to occur (p ~ 0) 
“Unknown” - Certainty unknow

URGENCY:
“Immediate” - Responsive action SHOULD be taken immediately 
“Expected” - Responsive action SHOULD be taken soon (within next hour) 
“Future” - Responsive action SHOULD be taken in the near future 
“Past” - Responsive action is no longer required 
“Unknown” - Urgency not known
'''
