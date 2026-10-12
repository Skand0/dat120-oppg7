"""h) Count summer days (>20), high summer days (>25) and tropical days (>30)
based on daily max temperature."""
from vaerdata import load_data, rows_for_year, ask_year


def count_hot_days(data, year):
    """Return (summer, high summer, tropical, days with no max temperature)."""
    summer = high = tropical = missing = 0
    for r in rows_for_year(data, year):
        t = r["tmaks"]
        if t is None:
            missing += 1
            continue
        if t > 20:
            summer += 1
        if t > 25:
            high += 1
        if t > 30:
            tropical += 1
    return summer, high, tropical, missing


def main():
    data = load_data()
    year = ask_year(data)
    summer, high, tropical, missing = count_hot_days(data, year)
    print(f"Sommerdager (over 20 grader):      {summer}")
    print(f"Høysommerdager (over 25 grader):   {high}")
    print(f"Tropedager (over 30 grader):       {tropical}")
    if missing > 0:
        print(f"Advarsel: {missing} dager mangler maksimumstemperatur.")


if __name__ == "__main__":
    main()
