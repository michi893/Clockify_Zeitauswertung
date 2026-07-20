import requests

def get_detailed_report(API_KEY, WORKSPACE_ID, USER_ID, headers, start_date, end_date, show_output):
        
    url = (
        f"https://reports.api.clockify.me/v1/"
        f"workspaces/{WORKSPACE_ID}/reports/detailed"
    )

    payload = {
        "dateRangeStart": start_date,
        "dateRangeEnd": end_date,

        "detailedFilter": {
            "users": [
                USER_ID
            ]
        },
        "page": 1,
        "pageSize": 100
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        print("Fehler:", response.status_code)
        print(response.text)
        exit()

    report = response.json()

    # -----------------------------------
    # Zusammentragung erfasste Zeit
    # -----------------------------------

    tracked_seconds = 0

    if show_output:
        print(f"Gefundende Zeiteinräge:")

    for entry in report["timeentries"]:
        # Nur den ausgewählten Benutzer berücksichtigen
        if entry["userId"] != USER_ID:
            continue
        
        user = entry["userName"]
        duration = entry["timeInterval"]["duration"]
        working_date = entry["timeInterval"]["start"].split("T")[0]

        if show_output:
            print(f"Person: {user} | Datum: {working_date} | Dauer: {duration / 3600:.2f} Stunden")

        tracked_seconds += duration

    tracked_hours = tracked_seconds / 3600

    return tracked_hours