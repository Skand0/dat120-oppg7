"""Shared helpers: read the MET weather CSV files into lists of dicts.

Every row is a dict with these keys:
    dato      datetime
    tmaks     max temperature
    tmid      mean temperature
    nedbor    precipitation (mm)
    vindmaks  highest mean wind (m/s)
    snodybde  snow depth (cm)
A missing value ("-" in the file) becomes None.
"""
import csv
import os
from datetime import datetime

DATA_MAPPE = os.path.join(os.path.dirname(__file__), "data")

# Station name -> file in the data folder
STASJONER = {
    "Oslo Blindern": "oslo_blindern_1954_2025_med_makstemperatur.csv",
    "Røros": "roeros_1954_2025_med_makstemperatur.csv",
    "Tromsø": "tromsoe_1954_2025_med_makstemperatur.csv",
    "Værnes": "vaernes_1954_2025_med_makstemperatur.csv",
    "Venabu": "venabu_1954_2025_med_makstemperatur.csv",
    "Sinnes": "sinnes_2014_2025_med_makstemperatur.csv",
}

# Column name in the file -> key in our dicts
KOLONNER = {
    "Maksimumstemperatur (døgn)": "tmaks",
    "Middeltemperatur (døgn)": "tmid",
    "Nedbør (døgn)": "nedbor",
    "Høyeste middelvind (døgn)": "vindmaks",
    "Snødybde": "snodybde",
}

NAN = float("nan")  # matplotlib leaves a gap in a line where the value is nan


def til_tall(tekst):
    """'1,4' -> 1.4 and '-' -> None."""
    tekst = tekst.strip()
    if tekst in ("", "-"):
        return None
    return float(tekst.replace(",", "."))


def load_data(filnavn):
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
    # Some files are NOT in date order, so sort them
    data.sort(key=lambda r: r["dato"])
    return data


def load_station(navn):
    return load_data(os.path.join(DATA_MAPPE, STASJONER[navn]))


def load_all():
    """Return {station name: data} for all stations."""
    return {navn: load_station(navn) for navn in STASJONER}


def group_by(data, key):
    """Group rows in a dict. key is a function that gives the group for a row.

    group_by(data, lambda r: r["dato"].year) -> {2014: [rows...], 2015: [rows...], ...}
    """
    groups = {}
    for r in data:
        groups.setdefault(key(r), []).append(r)
    return groups


def valid(rows, nokkel):
    """All values for one key in the rows, without the missing ones (None)."""
    return [r[nokkel] for r in rows if r[nokkel] is not None]


def none_to_nan(values):
    return [NAN if v is None else v for v in values]


def ask_station():
    """Let the user pick a station from a numbered list."""
    navn = list(STASJONER)
    for i, n in enumerate(navn, start=1):
        print(f"{i}. {n}")
    while True:
        svar = input("Velg stasjon (nummer): ")
        if svar.strip().isdigit() and 1 <= int(svar) <= len(navn):
            return navn[int(svar) - 1]
        print("Ugyldig valg, prøv igjen.")
