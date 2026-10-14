"""Shared helpers: read the MET weather CSV into a list of dicts.

Every row is a dict with these keys:
    dato      datetime
    tmaks     max temperature (None if the file has no such column or value)
    tmid      mean temperature
    nedbor    precipitation (mm)
    vindmaks  highest mean wind (m/s)
    snodybde  snow depth (cm)
A missing value ("-" in the file) becomes None.
"""
import csv
import os
from datetime import datetime

# Default file. It has max temperature and all of 2025.
STANDARD_FIL = os.path.join(os.path.dirname(__file__), "data",
                            "sinnes_2014_2025_med_makstemperatur.csv")

# Column name in the file -> key in our dicts
KOLONNER = {
    "Maksimumstemperatur (døgn)": "tmaks",
    "Middeltemperatur (døgn)": "tmid",
    "Nedbør (døgn)": "nedbor",
    "Høyeste middelvind (døgn)": "vindmaks",
    "Snødybde": "snodybde",
}


def til_tall(tekst):
    """'1,4' -> 1.4 and '-' -> None."""
    tekst = tekst.strip()
    if tekst in ("", "-"):
        return None
    return float(tekst.replace(",", "."))


def load_data(filnavn=STANDARD_FIL):
    data = []
    # utf-8-sig removes the BOM at the start of the file
    with open(filnavn, encoding="utf-8-sig") as f:
        leser = csv.DictReader(f, delimiter=";")
        for rad in leser:
            tid = rad["Tid(norsk normaltid)"]
            # The last line of the file is a license note, not data
            if not tid[:2].isdigit():
                continue
            ny = {"dato": datetime.strptime(tid, "%d.%m.%Y")}
            for kolonne, nokkel in KOLONNER.items():
                ny[nokkel] = til_tall(rad[kolonne]) if kolonne in rad else None
            data.append(ny)
    # The rows are NOT in date order in the file, so sort them
    data.sort(key=lambda r: r["dato"])
    return data


def rows_for_year(data, year):
    return [r for r in data if r["dato"].year == year]


def ask_year(data):
    """Ask until the user gives a year that exists in the data."""
    forste = data[0]["dato"].year
    siste = data[-1]["dato"].year
    while True:
        svar = input(f"Årstall ({forste}-{siste}): ")
        if svar.strip().isdigit() and forste <= int(svar) <= siste:
            return int(svar)
        print("Ugyldig årstall, prøv igjen.")
