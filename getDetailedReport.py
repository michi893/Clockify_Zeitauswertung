import requests
from datetime import datetime, timedelta


def get_detailed_report(
    API_KEY, WORKSPACE_ID, USER_ID, headers, start_date, end_date, show_output
):

    url = (
        f"https://reports.api.clockify.me/v1/"
        f"workspaces/{WORKSPACE_ID}/reports/detailed"
    )

    start = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%SZ")
    end = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%SZ")

    all_entries = []

    current = start

    while current <= end:

        day_start = current.strftime("%Y-%m-%dT00:00:00Z")
        day_end = current.strftime("%Y-%m-%dT23:59:59Z")

        payload = {
            "dateRangeStart": day_start,
            "dateRangeEnd": day_end,
            "detailedFilter": {"users": [USER_ID]},
            "page": 1,
            "pageSize": 50,
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 200:
            print(response.text)
            return 0

        report = response.json()

        entries = report.get("timeentries", [])

        if entries:
            print(current.strftime("%Y-%m-%d"), ":", len(entries), "Einträge")

        all_entries.extend(entries)

        current += timedelta(days=1)

    print()
    print("Gesamte Einträge:", len(all_entries))

    if all_entries:

        print("Ältester:", min(e["timeInterval"]["start"] for e in all_entries))

        print("Neuester:", max(e["timeInterval"]["start"] for e in all_entries))

    tracked_seconds = 0

    if show_output:
        print("Gefundene Zeiteinträge:")

    for entry in all_entries:

        if entry["userId"] != USER_ID:
            continue

        duration = entry["timeInterval"]["duration"]

        tracked_seconds += duration

        if show_output:
            print(
                f"{entry['userName']} | "
                f"{entry['timeInterval']['start']} | "
                f"{duration/3600:.2f}h"
            )

    return tracked_seconds / 3600
