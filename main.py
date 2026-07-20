# import datetime
import calendar
from datetime import datetime

from getApiKey import get_api_key
from getWorkspaceID import get_workspace_id
from getDateRange import get_date_range
from getDetailedReport import get_detailed_report
from getExpectedWorkingHours import expected_working_hours
from getVacationEntries import get_vacation_entries


def main():
    API_KEY, PENSUM = get_api_key()

    headers = {"X-Api-Key": API_KEY, "Content-Type": "application/json"}

    # Gleitzeitsaldo für den eingegebenen Datumsbereichs berechnen
    WORKSPACE_ID, USER_ID = get_workspace_id(API_KEY, headers)
    start_date, end_date = get_date_range()
    tracked_hours = get_detailed_report(
        API_KEY, WORKSPACE_ID, USER_ID, headers, start_date, end_date, show_output=True
    )
    print(f"\nErgebniss Auswertung\nGetrackte Zeit: {tracked_hours:.2f} Stunden")
    expected_hours = expected_working_hours(start_date, end_date, PENSUM)
    print(f"Sollzeit: {expected_hours:.2f} Stunden")

    balance = tracked_hours - expected_hours
    print(f"Saldo: {balance:+.2f} Stunden")

    # Gleitzeitsaldo für das Vorjahr des eingegebenen Datumsbereichs berechnen
    start = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%SZ")
    previous_year = start.year - 1
    tracked_hours_sum = 0
    expected_hours_sum = 0
    booked_vacation_hours_sum = 0

    # Aufsummieren der einzelnen Monate da unser Abo diese Zeitspanne nicht erlaubt auf einmal abfragen
    for month in range(1, 13):
        # Erster Tag des Monats
        month_start = datetime(previous_year, month, 1, 0, 0, 0).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )

        # Letzter Tag des Monats
        last_day = calendar.monthrange(previous_year, month)[1]
        month_end = datetime(previous_year, month, last_day, 23, 59, 59).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )

        tracked_hours = get_detailed_report(
            API_KEY,
            WORKSPACE_ID,
            USER_ID,
            headers,
            month_start,
            month_end,
            show_output=False,
        )
        expected_hours = expected_working_hours(month_start, month_end, PENSUM)
        tracked_hours_sum += tracked_hours
        expected_hours_sum += expected_hours

        # Ferienbuchungen für den eingegebenen Datumsbereich berechnen
        booked_vacation_hours = get_vacation_entries(
            API_KEY, WORKSPACE_ID, USER_ID, headers, month_start, month_end
        )
        booked_vacation_hours_sum += booked_vacation_hours["total_hours"]

    hours_balance = tracked_hours_sum - expected_hours_sum
    vacation_balance = 5 * 42 * PENSUM / 100 - booked_vacation_hours_sum
    print(f"Jahr {previous_year} Saldo: {hours_balance:+.2f} Stunden")
    print(f"Jahr {previous_year} Feriensaldo: {vacation_balance:+.2f} Stunden")


if __name__ == "__main__":
    main()
