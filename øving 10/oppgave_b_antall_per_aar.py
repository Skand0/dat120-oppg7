"""b) Count summer days (>20), high summer days (>25) and tropical days (>30)
for every year, and plot them with the year on the x-axis.

Years with a lot of missing data (for example the first and last year of Røros
and Venabu) give lower counts, since missing days can't be counted.
"""
import matplotlib.pyplot as plt
from vaerdata import load_station, ask_station


def count_hot_days_per_year(data):
    """Return {year: [summer days, high summer days, tropical days]}."""
    counts = {}
    for r in data:
        t = r["tmaks"]
        if t is None:
            continue
        year = r["dato"].year
        if year not in counts:
            counts[year] = [0, 0, 0]
        if t > 20:
            counts[year][0] += 1
        if t > 25:
            counts[year][1] += 1
        if t > 30:
            counts[year][2] += 1
    return counts


def plot_hot_days(counts, navn, save_as=None):
    years = sorted(counts)
    labels = ["Sommerdager (>20 °C)", "Høysommerdager (>25 °C)", "Tropedager (>30 °C)"]
    for i, label in enumerate(labels):
        plt.plot(years, [counts[y][i] for y in years], label=label)
    plt.xlabel("År")
    plt.ylabel("Antall dager")
    plt.title(navn)
    plt.grid(True)
    plt.legend()
    if save_as:
        plt.savefig(save_as)
    plt.show()


def main():
    navn = ask_station()
    data = load_station(navn)
    plot_hot_days(count_hot_days_per_year(data), navn)


if __name__ == "__main__":
    main()
