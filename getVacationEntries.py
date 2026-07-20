import requests
from datetime import datetime


def get_vacation_entries(
    API_KEY,
    WORKSPACE_ID,
    USER_ID,
    headers,
    start_date,
    end_date,
    vacation_keywords=None,
):
    """
    Gibt alle Ferienbuchungen aus Clockify zurück.

    vacation_keywords:
        Liste mit Suchbegriffen für Ferien.
        Beispiel:
        ["ferien", "vacation", "holiday"]

    Rückgabe:
        {
            "entries": [...],
            "total_hours": xx.xx
        }
    """

    if vacation_keywords is None:
        vacation_keywords = ["ferien", "vacation", "holiday"]

    url = (
        f"https://reports.api.clockify.me/v1/workspaces/"
        f"{WORKSPACE_ID}/reports/detailed"
    )

    payload = {
        "dateRangeStart": start_date,
        "dateRangeEnd": end_date,
        "users": {"ids": [USER_ID]},
        "detailedFilter": {"page": 1, "pageSize": 1000},
    }

    response = requests.post(url, headers=headers, json=payload)

    response.raise_for_status()

    data = response.json()

    vacation_entries = []
    total_seconds = 0

    for entry in data.get("timeentries", []):

        description = entry.get("description", "").lower()

        project_name = entry.get("projectName", "").lower()

        task_name = entry.get("taskName", "").lower()

        text = description + " " + project_name + " " + task_name

        if any(keyword.lower() in text for keyword in vacation_keywords):

            duration = entry.get("timeInterval", {}).get("duration", 0)

            total_seconds += duration

            vacation_entries.append(
                {
                    "date": entry.get("timeInterval", {}).get("start"),
                    "description": entry.get("description"),
                    "project": entry.get("projectName"),
                    "task": entry.get("taskName"),
                    "hours": round(duration / 3600, 2),
                }
            )

    return {"entries": vacation_entries, "total_hours": round(total_seconds / 3600, 2)}
