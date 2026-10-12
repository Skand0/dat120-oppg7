"""g) Longest unbroken period where daily precipitation is 0."""
from datetime import timedelta
from vaerdata import load_data


def longest_dry_period(data):
    """Return (length in days, start date, end date).

    data must be sorted by date (load_data does that).
    A missing precipitation value (None) ends the streak, since we don't know it was dry.
    """
    best_len, best_start, best_end = 0, None, None
    cur_len, cur_start, prev_date = 0, None, None
    for r in data:
        d = r["dato"]
        dry = r["nedbor"] == 0
        # A gap in the dates also ends the streak
        follows_prev = prev_date is not None and d - prev_date == timedelta(days=1)
        if dry:
            if cur_len > 0 and follows_prev:
                cur_len += 1
            else:
                cur_len, cur_start = 1, d
            if cur_len > best_len:
                best_len, best_start, best_end = cur_len, cur_start, d
        else:
            cur_len = 0
        prev_date = d
    return best_len, best_start, best_end


def main():
    data = load_data()
    length, start, end = longest_dry_period(data)
    print(f"Lengste periode uten nedbør: {length} dager")
    print(f"Startdato: {start:%d.%m.%Y}")
    print(f"Sluttdato: {end:%d.%m.%Y}")


if __name__ == "__main__":
    main()
