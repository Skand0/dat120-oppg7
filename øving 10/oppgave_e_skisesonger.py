"""e) Number of ski days (snow depth >= 20 cm) for every ski season, all stations in one plot.

Season for year Y: 1 November Y-1 to 31 May Y.
A season counts only if there are snow depth readings for at least half of the days in it.
"""
from datetime import datetime
import matplotlib.pyplot as plt
from vaerdata import load_all


def days_in_season(year):
    start = datetime(year - 1, 11, 1)
    end = datetime(year, 5, 31)
    return (end - start).days + 1


def ski_days_per_season(data):
    """Return {season (end year): ski days}, only for seasons with enough data."""
    seasons = {}  # season -> [days with a reading, ski days]
    for r in data:
        month = r["dato"].month
        if month >= 11:
            season = r["dato"].year + 1
        elif month <= 5:
            season = r["dato"].year
        else:
            continue  # June to October is not in any season
        if r["snodybde"] is None:
            continue
        if season not in seasons:
            seasons[season] = [0, 0]
        seasons[season][0] += 1
        if r["snodybde"] >= 20:
            seasons[season][1] += 1

    result = {}
    for season, (n_readings, n_ski) in seasons.items():
        if n_readings >= days_in_season(season) / 2:
            result[season] = n_ski
    return result


def plot_ski_seasons(all_seasons, save_as=None):
    """all_seasons is {station name: {season: ski days}}."""
    plt.figure(figsize=(11, 6))
    for navn, seasons in all_seasons.items():
        years = sorted(seasons)
        plt.plot(years, [seasons[y] for y in years], marker="o", markersize=3, label=navn)
    plt.xlabel("Sesong (sluttår, f.eks. 2020 = nov 2019 til mai 2020)")
    plt.ylabel("Dager med skiføre")
    plt.title("Skiføre per sesong")
    plt.grid(True)
    plt.legend()
    if save_as:
        plt.savefig(save_as)
    plt.show()


def main():
    stasjoner = load_all()
    all_seasons = {navn: ski_days_per_season(data) for navn, data in stasjoner.items()}
    plot_ski_seasons(all_seasons)


if __name__ == "__main__":
    main()
