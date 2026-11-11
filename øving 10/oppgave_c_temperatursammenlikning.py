"""c) Yearly mean temperature for each station, in one plot.

A year counts only if the station has at least 300 days with a mean temperature.
"""
import matplotlib.pyplot as plt
from vaerdata import load_all, group_by, valid, NAN

MIN_DAGER = 300


def yearly_mean_temp(data):
    """Return {year: mean of the daily mean temperatures}, only for years with enough data."""
    groups = group_by(data, lambda r: r["dato"].year)
    result = {}
    for year, rows in groups.items():
        temps = valid(rows, "tmid")
        if len(temps) >= MIN_DAGER:
            result[year] = sum(temps) / len(temps)
    return result


def plot_yearly_means(all_means, save_as=None):
    """all_means is {station name: {year: mean}}."""
    plt.figure(figsize=(11, 6))
    for navn, means in all_means.items():
        if not means:
            continue
        # Use nan for years we skipped, so the line has a gap there
        years = range(min(means), max(means) + 1)
        plt.plot(years, [means.get(y, NAN) for y in years], label=navn)
    plt.xlabel("År")
    plt.ylabel("Gjennomsnittstemperatur (°C)")
    plt.title("Årlig gjennomsnittstemperatur")
    plt.grid(True)
    plt.legend()
    if save_as:
        plt.savefig(save_as)
    plt.show()


def main():
    stasjoner = load_all()
    all_means = {navn: yearly_mean_temp(data) for navn, data in stasjoner.items()}
    plot_yearly_means(all_means)


if __name__ == "__main__":
    main()
