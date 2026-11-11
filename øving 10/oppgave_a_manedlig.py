"""a) Monthly aggregation and plot for the whole time series.

Per month: max snow depth, total precipitation, max and min mean temperature,
max wind. Precipitation counts as OK only if the month has more than 20 valid days.
"""
from datetime import datetime
import matplotlib.pyplot as plt
from vaerdata import load_station, ask_station, group_by, valid, none_to_nan

MIN_NEDBOR_DAGER = 20  # need MORE than this many valid days to trust the total


def monthly_stats(data):
    """Return a list with one dict per month, in date order."""
    groups = group_by(data, lambda r: (r["dato"].year, r["dato"].month))
    result = []
    for (year, month), rows in groups.items():
        snow = valid(rows, "snodybde")
        rain = valid(rows, "nedbor")
        temp = valid(rows, "tmid")
        wind = valid(rows, "vindmaks")
        result.append({
            "dato": datetime(year, month, 1),
            "snow_max": max(snow) if snow else None,
            "rain_total": sum(rain) if len(rain) > MIN_NEDBOR_DAGER else None,
            "temp_max": max(temp) if temp else None,
            "temp_min": min(temp) if temp else None,
            "wind_max": max(wind) if wind else None,
        })
    return result


def plot_monthly(stats, navn, save_as=None):
    dates = [m["dato"] for m in stats]

    def column(key):
        return none_to_nan([m[key] for m in stats])

    fig, axes = plt.subplots(4, 1, sharex=True, figsize=(11, 10))
    axes[0].plot(dates, column("snow_max"))
    axes[0].set_ylabel("Maks snødybde (cm)")
    axes[1].plot(dates, column("rain_total"))
    axes[1].set_ylabel("Total nedbør (mm)")
    axes[2].plot(dates, column("temp_max"), label="Maks middeltemp.")
    axes[2].plot(dates, column("temp_min"), label="Min middeltemp.")
    axes[2].set_ylabel("Temperatur (°C)")
    axes[2].legend()
    axes[3].plot(dates, column("wind_max"))
    axes[3].set_ylabel("Maks middelvind (m/s)")
    for ax in axes:
        ax.grid(True)
    axes[0].set_title(f"{navn}, månedlige verdier")
    fig.autofmt_xdate()
    fig.tight_layout()
    if save_as:
        fig.savefig(save_as)
    plt.show()


def main():
    navn = ask_station()
    data = load_station(navn)
    plot_monthly(monthly_stats(data), navn)


if __name__ == "__main__":
    main()
