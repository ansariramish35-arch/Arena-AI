"""Build a coherent synthetic daily air-quality dataset for Lucknow.

Monthly climatological means are fixed; day-to-day variation is added with
pollutant-specific noise amplitudes so that inter-pollutant correlations fall
in the range typically reported for Indo-Gangetic Plain cities.
"""
import numpy as np

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Climatological monthly means (ug/m3 unless stated)
MEANS = {
    "PM25": [165, 132, 98, 82, 74, 62, 38, 33, 46, 88, 152, 172],
    "PM10": [235, 198, 165, 148, 138, 118, 72, 65, 88, 158, 228, 248],
    "NO2":  [62, 55, 44, 38, 34, 30, 22, 20, 26, 42, 58, 66],
    "SO2":  [12, 11, 9, 8, 7, 6, 5, 4, 5, 8, 11, 13],
    "CO":   [1.9, 1.7, 1.4, 1.2, 1.1, 0.9, 0.6, 0.5, 0.8, 1.3, 1.8, 2.1],
    "O3":   [42, 48, 58, 66, 72, 68, 52, 46, 50, 56, 48, 40],
}

# day-to-day relative variability of each pollutant
NOISE = {"PM25": 0.34, "PM10": 0.30, "NO2": 0.28,
         "SO2": 0.35, "CO": 0.26, "O3": 0.32}

DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def build(seed=2026):
    rng = np.random.default_rng(seed)
    date, month, dayofweek = [], [], []
    series = {k: [] for k in MEANS}

    n = 0
    for mi, (mname, nd) in enumerate(zip(MONTHS, DAYS)):
        # one common synoptic factor per day (weather) + pollutant-specific noise
        weather = rng.normal(0, 1, nd)
        for d in range(nd):
            date.append(f"{d + 1:02d}-{mname}")
            month.append(mname)
            dayofweek.append((n + 3) % 7)   # 1 Jan treated as Thursday
            for k, means in MEANS.items():
                seasonal = means[mi]
                common = 0.55 * weather[d] * seasonal * NOISE[k]
                own = rng.normal(0, 0.85) * seasonal * NOISE[k]
                v = seasonal + common + own
                series[k].append(max(v, seasonal * 0.22))
            n += 1

    data = {k: np.array(v) for k, v in series.items()}
    aqi = aqi_from(data)
    data["AQI"] = aqi
    data["month"] = np.array(month)
    data["dow"] = np.array(dayofweek)
    data["date"] = np.array(date)
    return data


# CPCB breakpoints (simplified) and sub-index ranges
BP = {
    "PM25": [(0, 30, 0, 50), (30, 60, 51, 100), (60, 90, 101, 200),
             (90, 120, 201, 300), (120, 250, 301, 400), (250, 500, 401, 500)],
    "PM10": [(0, 50, 0, 50), (50, 100, 51, 100), (100, 250, 101, 200),
             (250, 350, 201, 300), (350, 430, 301, 400), (430, 600, 401, 500)],
    "NO2":  [(0, 40, 0, 50), (40, 80, 51, 100), (80, 180, 101, 200),
             (180, 280, 201, 300), (280, 400, 301, 400), (400, 600, 401, 500)],
    "SO2":  [(0, 40, 0, 50), (40, 80, 51, 100), (80, 380, 101, 200),
             (380, 800, 201, 300), (800, 1600, 301, 400), (1600, 2400, 401, 500)],
    "CO":   [(0, 1.0, 0, 50), (1.0, 2.0, 51, 100), (2.0, 10, 101, 200),
             (10, 17, 201, 300), (17, 34, 301, 400), (34, 50, 401, 500)],
    "O3":   [(0, 50, 0, 50), (50, 100, 51, 100), (100, 168, 101, 200),
             (168, 208, 201, 300), (208, 748, 301, 400), (748, 1000, 401, 500)],
}


def sub_index(name, c):
    for lo, hi, ilo, ihi in BP[name]:
        if c <= hi:
            return ilo + (ihi - ilo) / (hi - lo) * (c - lo)
    return 500.0


def aqi_from(data):
    subs = np.vstack([np.array([sub_index(k, c) for c in data[k]])
                      for k in ["PM25", "PM10", "NO2", "SO2", "CO", "O3"]])
    return subs.max(axis=0)
