"""d) Plot snow depth, precipitation, mean temperature and max wind for one year."""
import matplotlib.pyplot as plt
from vaerdata import load_data, rows_for_year, ask_year

NAN = float("nan")  # matplotlib leaves a gap where the value is nan


def plot_year(data, year, save_as=None):
    rows = rows_for_year(data, year)
    dates = [r["dato"] for r in rows]  # datetime objects -> nicely formatted x-axis

    series = [
        ("snodybde", "Snødybde (cm)"),
        ("nedbor", "Nedbør (mm)"),
        ("tmid", "Middeltemp. (°C)"),
        ("vindmaks", "Høyeste middelvind (m/s)"),
    ]
    fig, axes = plt.subplots(4, 1, sharex=True, figsize=(10, 9))
    for ax, (key, label) in zip(axes, series):
        values = [NAN if r[key] is None else r[key] for r in rows]
        ax.plot(dates, values)
        ax.set_ylabel(label)
        ax.grid(True)
    axes[0].set_title(f"Sirdal - Sinnes {year}")
    fig.autofmt_xdate()
    fig.tight_layout()
    if save_as:
        fig.savefig(save_as)
    plt.show()


def main():
    data = load_data()
    year = ask_year(data)
    plot_year(data, year)


if __name__ == "__main__":
    main()
