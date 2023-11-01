"""Script to generate civil twilight start and end times for multiple locations"""

from datetime import datetime
import ephem

class CivilTwilight:
    """Object for ephem library to handle multiple locations"""
    def __init__(self):
        self.sun = ephem.Sun()
        self.observer = ephem.Observer()
        self.observer.pressure = 0

    def __get_timestamp(self, time: ephem.Date):
        """Converts ephem.Date to time string"""
        return ephem.localtime(time).strftime("%H:%M:%S %p")

    def calculate(self, lat: str, lon: str):
        """Takes lat and lon coordinates and returns civil twilight start and end time in local time"""
        self.observer.lat = lat
        self.observer.lon = lon

        self.observer.date = datetime.today().replace(hour=12, minute=0, second=0)

        self.observer.horizon = '-6'
        twilight_start = self.observer.next_setting(self.sun, use_center=True)
        twilight_end = self.observer.next_rising(self.sun, use_center=True)

        return {
            "twilight_start": self.__get_timestamp(twilight_start),
            "twilight_end": self.__get_timestamp(twilight_end)
        }


def main():
    """Function to test if the script is working as it should"""

    location = {"name": "Clockhouse", "lat": "52.22753338139345", "long": "0.4987074201616557"}

    civil_twilight = CivilTwilight()
    data = civil_twilight.calculate(str(location['lat']), str(location['long']))

    print(location)
    print(data)

if __name__ == "__main__":
    main()
