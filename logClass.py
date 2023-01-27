import numpy
import datetime
from dataclasses import dataclass
import matplotlib.pyplot as plt
import folium
from geopy.distance import geodesic



def str_to_longtitude(str_long):
    tmp = int(str_long[:2]) + int(str_long[2:7]) / 10**3 / 60
    # tmp = int(str_long[:-1]) / 10**5
    if str_long[-1] == "S":
        tmp *= -1
    return tmp

def str_to_latitude(str_lati):
    tmp = int(str_lati[:3]) + int(str_lati[3:8]) / 10**3 / 60
    # tmp = int(str_lati[:-1]) / 10**5
    if str_lati[-1] == "W":
        tmp *= -1
    return tmp

def line_analysis(line):
    log_time = line[1:7]
    log_time = datetime.datetime.strptime(log_time, '%H%M%S')
    longtitude = str_to_longtitude(line[7:15])
    latitude = str_to_latitude(line[15:24])
    press_alt = int(line[25:30])
    gps_alt = int(line[30:35])
    return Log_second(log_time, longtitude, latitude, press_alt, gps_alt)

@dataclass
class Log_second:
    time: datetime.time
    longtitude: float
    latitude: float
    press_alt: int
    gps_alt: int

class Log:
    def __init__(self, logs, metadata):
        self.logs = logs
        self.metadata = metadata
        self.gps_alts = [log.gps_alt for log in logs]
        self.times = [log.time for log in logs]
        self.longtitudes = [log.longtitude for log in logs]
        self.latitudes = [log.latitude for log in logs]
        self.loc = [(log.longtitude, log.latitude) for log in logs]

    def print_stats(self):
        max_alt = 0
        max_rate =-float('inf')
        min_rate = float('inf')
        max_rate_in_3 =-float('inf')
        min_rate_in_3 = float('inf')
        tmp = self.gps_alts[0]
        for i, alt in enumerate(self.gps_alts):
            if i != 0:
                tmp = (self.gps_alts[i] - self.gps_alts[i - 1] ) /(self.times[i].timestamp() - self.times[i - 1].timestamp())
                if tmp > max_rate:
                    max_rate = tmp
                if tmp < min_rate:
                    min_rate = tmp
            if i >= 3:
                tmp = (self.gps_alts[i] - self.gps_alts[i - 3] ) /(self.times[i].timestamp() - self.times[i - 3].timestamp())
                if tmp > max_rate_in_3:
                    max_rate_in_3 = tmp
                if tmp < min_rate_in_3:
                    min_rate_in_3 = tmp
            if alt > max_alt:
                max_alt = alt
        print(max_alt, max_rate, min_rate, max_rate_in_3, min_rate_in_3)

    def plot_alititude(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.times, self.gps_alts)
        plt.xlabel("time", fontsize=20)
        plt.ylabel("altitude", fontsize=20)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=15)
        plt.show()

    def plot_velocity(self):
        velocity = [geodesic(self.loc[i], self.loc[i-1]).km for i in range(1, len(self.loc))]
        plt.figure(figsize=(10, 6))
        plt.plot(self.times[1:], velocity)
        plt.xlabel("time", fontsize=20)
        plt.ylabel("altitude", fontsize=20)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=15)
        plt.show()