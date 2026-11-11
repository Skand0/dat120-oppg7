"""d) Min, median and max wind for each month of the year, for one station.
All measurements in a given month are used, and the year is ignored."""
import matplotlib.pyplot as plt
from vaerdata import load_station, ask_station, group_by, valid, none_to_nan

MANEDER = ["jan", "feb", "mar", "apr", "mai", "jun",
           "jul", "aug", "sep", "okt", "nov", "des"]


def median(values):
    """Middle value of the sorted list. For an even length, the mean of the two in the middle."""
    s = sorted(values)
    n = len(s)
    mid = n // 2
    if n % 2 == 1:
        return s[mid]
    return (s[mid - 1] + s[mid]) / 2


def wind_stats_per_month(data):
    """Return {month number: (min, median, max)}. None if the month has no wind data."""
    groups = group_by(data, lambda r: r["dato"].month)
    result = {}
    for month in range(1, 13):
        wind = valid(groups.get(month, []), "vindmaks")
        result[month] = (min(wind), median(wind), max(wind)) if wind else None
    return result


def plot_wind_stats(stats, navn, save_as=None):
    months = range(1, 13)
    labels = ["Minimum", "Median", "Maksimum"]
    for i, label in enumerate(labels):
        values = none_to_nan([stats[m][i] if stats[m] else None for m in months])
        plt.plot(months, values, marker="o", label=label)
    plt.xticks(months, MANEDER)
    plt.ylabel("Middelvind (m/s)")
    plt.title(f"{navn}, vindstyrke per måned (alle år)")
    plt.grid(True)
    plt.legend()
    if save_as:
        plt.savefig(save_as)
    plt.show()


def main():
    navn = ask_station()
    data = load_station(navn)
    plot_wind_stats(wind_stats_per_month(data), navn)


if __name__ == "__main__":
    main()
