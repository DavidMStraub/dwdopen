import requests
from .constants import URL_POLLEN, FMT_NEXT_UPDATE
from datetime import datetime


class HttpClient(object):
    def __init__(self, uri):
        self.uri = uri

    def get_json(self):
        r = requests.get(self.uri)
        return r.json()


class Pollen(object):
    def __init__(self):
        """Initialize the instance."""
        self._client = HttpClient(uri=URL_POLLEN)
        self._data = None
        self._regions = None
        self._pollen = None
        self._nextupdate = None
        self._day_dict = {0: 'today', 1: 'tomorrow', 2: 'dayafter_to'}
        self._value_dict = {'0': 0, '0-1': 0.5, '-1': 0.5, '1': 1,
                            '1-2': 1.5, '2': 2, '2-3': 2.5, '3': 3}

    @property
    def data(self):
        """Return the data dictionary (using the cached one if it exists)."""
        if self._data is None or self._update_due():
            self.update_data()
        return self._data

    @property
    def regions(self):
        """Return the regions dictionary (using the cached one if it exists)."""
        if self._regions is None or self._update_due():
            self.update_data()
        return self._regions

    @property
    def pollen(self):
        """Return the pollen set (using the cached one if it exists)."""
        if self._pollen is None or self._update_due():
            self.update_data()
        return self._pollen

    def update_data(self):
        """Fetch new data."""
        d = self._client.get_json()
        self._process_data(d)
        self._nextupdate = datetime.strptime(d.get('next_update'),
                                             FMT_NEXT_UPDATE)

    def _process_data(self, data):
        """Process that data into a useful form."""
        content = data.get('content', None)
        data_dict = {}
        region_dict = {}
        pollen_set = set()
        for el in content:
            region_dict[el['partregion_id']] = el['partregion_name']
            data_dict[el['partregion_id']] = el['Pollen']
            pollen_set.update(el['Pollen'].keys())
        self._regions = region_dict
        self._data = data_dict
        self._pollen = pollen_set
        try:
            self._nextupdate = datetime.strptime(data['next_update'],
                                                 FMT_NEXT_UPDATE)
        except (KeyError, ValueError):
            self._nextupdate = None

    def _update_due(self):
        """Checks if the next_update time has passed."""
        if self._nextupdate is None:
            return True
        elif datetime.now() >= self._nextupdate:
            return True
        else:
            return False

    def report(self, region, pollen, forecast=0):
        """Return the value of the pollen forecast.

        Parameters:

        - `region`: id of the region (use `regions` method to display possible
          values)
        - `pollen`: tuple of pollen types (string; use `pollen` method to
          display possible values)
        - forecast: 0 for today, 1 for tomorrow, 2 for day after tomorrow

        The number returned will be between 0 (no pollution) and 7 (high
        pollution). If `pollen` contains several elements, the maximum
        value will be returned.
        """
        value = []
        try:
            data = self.data[region]
        except KeyError:
            raise ValueError("Region {} not found in data. Use regions method to display possible values.".format(region))
        try:
            day_key = self._day_dict[forecast]
        except KeyError:
            raise ValueError("forecast should be 0 (today), 1 (tomorrow), or 2 (day after tomorrow)")
        if isinstance(pollen, str):
            raise ValueError("`pollen` should be a tuple!")
        for k in pollen:
            try:
                value.append(self._value_dict[data[k][day_key]])
            except KeyError:
                pass
        if not value:
            return None
        return max(value)
