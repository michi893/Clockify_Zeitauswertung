import requests
from datetime import datetime, timedelta


def get_detailed_report(
    WORKSPACE_ID, USERNAME, headers, start_date, end_date, show_output
):

    url = (
        f"https://reports.api.clockify.me/v1/"
        f"workspaces/{WORKSPACE_ID}/reports/detailed"
    )

    start = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%SZ")
    end = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%SZ")

    all_entries = []
    all_booked_vacation_hours = []
    print(f"\nBerechne Zeit", end="")

    # Zeitraum größer als 1 Monat?
    if (end.year - start.year) * 12 + (end.month - start.month) > 0:

        current = start.replace(day=1, hour=0, minute=0, second=0)

        while current <= end:
            print(".", end="")
            # Monatsende bestimmen
            if current.month == 12:
                next_month = current.replace(year=current.year + 1, month=1)
            else:
                next_month = current.replace(month=current.month + 1)

            month_end = next_month - timedelta(seconds=1)

            # Begrenzung auf gewünschten Zeitraum
            period_start = max(current, start)
            period_end = min(month_end, end)

            # print(f"\nMonatlicher Zeitraum: " f"{period_start} - {period_end}")

            entries = fetch_entries(url, headers, period_start, period_end, USERNAME)
            all_entries.extend(entries)
            current = next_month

    else:
        all_entries = fetch_entries(url, headers, start, end, USERNAME)

    # print("\nGesamte Einträge:", len(all_entries))

    # if show_output:
    #     print("Gefundene Zeiteinträge:")

    #     for entry in all_entries:
    #         duration = entry["timeInterval"]["duration"]

    # if entry["userName"] == USERNAME:
    #     print(
    #         f"{entry['userName']} | "
    #         f"{entry['timeInterval']['start']} | "
    #         f"{entry['projectName']} | "
    #         f"{duration/3600:.2f}h"
    #     )
    tracked_seconds = sum(
        e["timeInterval"]["duration"] for e in all_entries if e["userName"] == USERNAME
    )
    tracked_vacation_hours = sum(
        e["timeInterval"]["duration"]
        for e in all_entries
        if e.get("userName", "").strip() == USERNAME.strip()
        and e.get("projectName", "") == "Ferien"
    )
    tracked_bankHoliday_hours = sum(
        e["timeInterval"]["duration"]
        for e in all_entries
        if e.get("userName", "").strip() == USERNAME.strip()
        and e.get("projectName", "") == "Feiertag"
    )

    return (
        tracked_seconds / 3600,
        tracked_vacation_hours / 3600,
        tracked_bankHoliday_hours / 3600,
    )


def fetch_entries(url, headers, start, end, USERNAME):
    """Lädt alle Einträge eines Zeitraums.
    Falls >=50 Einträge zurückkommen, wird der Zeitraum halbiert.
    """
    # all_entries = []

    payload = {
        "dateRangeStart": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "dateRangeEnd": end.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "detailedFilter": {"users": [USERNAME]},
        "page": 1,
        "pageSize": 50,
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        raise RuntimeError(response.text)

    entries = response.json().get("timeentries", [])

    # Zeitraum vollständig
    if len(entries) < 50:
        # print(
        #     f"{payload['dateRangeStart']} - {payload['dateRangeEnd']} : {len(entries)}"
        # )
        return entries

    # Zeitraum halbieren
    mid = start + (end - start) / 2

    left = fetch_entries(url, headers, start, mid, USERNAME)
    right = fetch_entries(url, headers, mid + timedelta(milliseconds=1), end, USERNAME)

    return left + right
