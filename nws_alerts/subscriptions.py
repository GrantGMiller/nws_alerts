import datetime
import json
import os
from nwscapparser3 import NWSCAPParser


class Subscription:
    def __init__(self, callback=None, **kwargs):
        self._kwargs = dict((k.lower(), v.lower()) for k, v, in kwargs.items())
        self._callback = callback
        self._alertHistoryFilename = 'alert_history_'
        for k, v, in sorted(kwargs.items()):
            self._alertHistoryFilename += '{}_{}-'.format(k, v)
        self._alertHistoryFilename += '.json'
        self.cap = None

    def Update(self):
        if 'state' in self._kwargs:
            url = 'https://alerts.weather.gov/cap/{state}.php?x=0'.format(
                state=self._kwargs['state'].upper()
            )

        elif 'zone' in self._kwargs:
            url = 'https://alerts.weather.gov/cap/wwaatmget.php?x={zone}&y=0'.format(
                zone=self._kwargs['zone'].upper()
            )
        else:
            raise Exception('Unknown location "{}"'.format(self._kwargs))

        self.cap = NWSCAPParser(url=url)
        ret = []
        for ID, entry in self.cap.entries.items():
            for key in ['severity', 'certainty', 'urgency']:
                if key in self._kwargs:
                    value = getattr(entry, key)
                    value = str(value).lower()
                    if value != self._kwargs[key]:
                        break
            else:
                self._DoCallback(entry)
                ret.append(entry)
        return ret

    def _DoCallback(self, entry):
        if self._callback:
            if entry.id not in self._GetAlertHistory():
                self._callback(entry)
                self._LogAlert(entry)

    def _GetAlertHistory(self):
        if not os.path.exists(self._alertHistoryFilename):
            return {}

        with open(self._alertHistoryFilename, mode='rt') as file:
            return json.loads(file.read())

    def _LogAlert(self, entry):
        data = self._GetAlertHistory()
        data[str(entry.id)] = datetime.datetime.utcnow().isoformat()
        with open(self._alertHistoryFilename, mode='wt') as file:
            file.write(json.dumps(data, indent=2, sort_keys=True))
