import csv
from datetime import date, datetime
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent / "sinnes_2014_2025.csv"
DATE_COLUMN = "Tid(norsk normaltid)"
SNOW_DEPTH_COLUMN = "Snødybde"
MINIMUM_SNOW_DEPTH_CM = 20


def parse_snow_depth(value: str) -> float | None:
    value = value.strip()
    if not value or value == "-":
        return None
    return float(value.replace(",", "."))


def main() -> None:
    try:
        season_year = int(input("Skriv inn året skisesongen slutter: "))
    except ValueError:
        print("Du må skrive inn et gyldig årstall.")
        return

    if not 2 <= season_year <= 9999:
        print("Årstallet må være mellom 2 og 9999.")
        return

    season_start = date(season_year - 1, 11, 1)
    season_end = date(season_year, 5, 31)
    season_length = (season_end - season_start).days + 1

    observed_dates: set[date] = set()
    days_with_snow_measurement = 0
    ski_days = 0

    with DATA_FILE.open(encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=";")
        for row in reader:
            date_text = (row.get(DATE_COLUMN) or "").strip()
            if not date_text:
                continue

            observation_date = datetime.strptime(date_text, "%d.%m.%Y").date()
            if not season_start <= observation_date <= season_end:
                continue

            observed_dates.add(observation_date)
            snow_depth = parse_snow_depth(row[SNOW_DEPTH_COLUMN])
            if snow_depth is None:
                continue

            days_with_snow_measurement += 1
            if snow_depth >= MINIMUM_SNOW_DEPTH_CM:
                ski_days += 1

    if not observed_dates:
        print(f"Fant ingen målinger for skisesongen {season_year - 1}/{season_year}.")
        return

    missing_dates = season_length - len(observed_dates)
    missing_snow_measurements = len(observed_dates) - days_with_snow_measurement
    print(
        f"Skisesongen {season_year - 1}/{season_year} hadde "
        f"{ski_days} dager med skiføre "
        f"(snødybde minst {MINIMUM_SNOW_DEPTH_CM} cm)."
    )

    if missing_dates or missing_snow_measurements:
        print(
            "Merk: Resultatet er basert på tilgjengelige målinger. "
            f"Mangler målinger for {missing_dates} datoer og "
            f"snødybdemåling for {missing_snow_measurements} datoer."
        )


if __name__ == "__main__":
    main()