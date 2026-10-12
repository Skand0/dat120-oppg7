"""e) Days with ski conditions (snow depth >= 20 cm) in one ski season.

Season for year Y: 1 November Y-1 to 31 May Y.
"""
from vaerdata import load_data, ask_year


def ski_days(data, year):
    """Return (days with ski conditions, days in the season with no snow reading)."""
    count = 0
    missing = 0
    for r in data:
        d = r["dato"]
        in_season = (d.year == year - 1 and d.month >= 11) or \
                    (d.year == year and d.month <= 5)
        if not in_season:
            continue
        if r["snodybde"] is None:
            missing += 1
        elif r["snodybde"] >= 20:
            count += 1
    return count, missing


def main():
    data = load_data()
    year = ask_year(data)
    count, missing = ski_days(data, year)
    print(f"Skisesongen {year - 1}/{year}: {count} dager med skiføre.")
    if missing > 0:
        print(f"Advarsel: {missing} dager i sesongen mangler snødybde og er ikke talt med.")


if __name__ == "__main__":
    main()
