"""f) Simplified plant growth: on a day with mean temperature above 5 degrees,
growth = temperature - 5. Colder days give 0."""
from vaerdata import load_data, rows_for_year, ask_year

MIN_TEMP = 5


def plant_growth(data, year):
    """Return (total growth, days with no temperature reading)."""
    total = 0
    missing = 0
    for r in rows_for_year(data, year):
        if r["tmid"] is None:
            missing += 1
        elif r["tmid"] > MIN_TEMP:
            total += r["tmid"] - MIN_TEMP
    return total, missing


def main():
    data = load_data()
    year = ask_year(data)
    total, missing = plant_growth(data, year)
    print(f"Total plantevekst i {year}: {total:.1f}")
    if missing > 0:
        print(f"Advarsel: {missing} dager mangler middeltemperatur og er ikke talt med.")


if __name__ == "__main__":
    main()
