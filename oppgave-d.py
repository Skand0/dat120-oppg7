import csv
from datetime import datetime
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt


DATA_FILE = Path(__file__).resolve().parent / "sinnes_2014_2025.csv"
DATE_COLUMN = "Tid(norsk normaltid)"
MEASUREMENTS = (
    ("Snødybde", "Snødybde (cm)"),
    ("Nedbør (døgn)", "Nedbør (mm)"),
    ("Middeltemperatur (døgn)", "Middeltemperatur (°C)"),
    ("Høyeste middelvind (døgn)", "Høyeste middelvind (m/s)"),
)


def parse_measurement(value: str) -> float | None:
    value = value.strip()
    if not value or value == "-":
        return None
    return float(value.replace(",", "."))


def main() -> None:
    try:
        year = int(input("Skriv inn et årstall: "))
    except ValueError:
        print("Du må skrive inn et gyldig årstall.")
        return

    dates: list[datetime] = []
    values: dict[str, list[float | None]] = {
        column: [] for column, _ in MEASUREMENTS
    }

    with DATA_FILE.open(encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=";")
        for row in reader:
            date_text = (row.get(DATE_COLUMN) or "").strip()
            if not date_text:
                continue

            date = datetime.strptime(date_text, "%d.%m.%Y")
            if date.year != year:
                continue

            dates.append(date)
            for column, _ in MEASUREMENTS:
                values[column].append(parse_measurement(row[column]))

    if not dates:
        print(f"Fant ingen målinger for {year}.")
        return

    figure, axes = plt.subplots(
        nrows=len(MEASUREMENTS),
        ncols=1,
        sharex=True,
        figsize=(12, 10),
    )
    for axis, (column, label) in zip(axes, MEASUREMENTS):
        axis.plot(dates, values[column], linewidth=1)
        axis.set_ylabel(label)
        axis.grid(True, alpha=0.3)

    date_locator = mdates.AutoDateLocator()
    axes[-1].xaxis.set_major_locator(date_locator)
    axes[-1].xaxis.set_major_formatter(mdates.ConciseDateFormatter(date_locator))
    axes[-1].set_xlabel("Dato")
    figure.suptitle(f"Værdata for {year} – Sirdal, Sinnes")
    figure.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()