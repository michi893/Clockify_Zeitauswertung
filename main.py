# import datetime
import calendar
from datetime import datetime

from getApiKey import get_api_key
from getWorkspaceID import get_workspace_id
from getDateRange import get_date_range
from getDetailedReport import get_detailed_report
from getExpectedHours import expected_hours


def main():
    API_KEY, PENSUM = get_api_key()

    headers = {"X-Api-Key": API_KEY, "Content-Type": "application/json"}

    # Gleitzeitsaldo für den eingegebenen Datumsbereichs berechnen
    WORKSPACE_ID, USERNAME = get_workspace_id(API_KEY, headers)
    USERNAME = "David Niklaus"
    # Usernames: David Niklaus, Katja , leana.leimer, Personaladmin  ACHTUNG: DER BENUTZTERNAME KATJA HAT EIN LEERZEICHEN AM ENDE!
    start_date, end_date = get_date_range()
    tracked_hours, tracked_vacation_hours, tracked_bankHoliday_hours = (
        get_detailed_report(
            WORKSPACE_ID, USERNAME, headers, start_date, end_date, show_output=True
        )
    )
    print(f"\nErgebniss Auswertung\nErfasste Zeit: {tracked_hours:.2f} Stunden")
    target_hours, target_bankHoliday_hours = expected_hours(
        start_date, end_date, PENSUM
    )
    print(f"Sollzeit: {target_hours:.2f} Stunden")

    balance_tracked_hours = tracked_hours - target_hours
    print(f"Saldo: {balance_tracked_hours:+.2f} Stunden")

    # Feriensaldo für den eingegebenen Datumsbereichs berechnen
    print(f"\nDavon erfasste Ferienzeit: {tracked_vacation_hours:.2f} Stunden")
    target_vacation_hours = 5 * 42 * PENSUM / 100
    print(f"Sollzeit Ferien (pro Jahr): {target_vacation_hours:.2f} Stunden")

    balance_vacation_hours = 5 * 42 * PENSUM / 100 - tracked_vacation_hours
    print(f"Saldo: {balance_vacation_hours:+.2f} Stunden")

    # Feiertagensaldo für den eingegebenen Datumsbereichs berechnen
    print(f"\nDavon erfasste Feiertage-Zeit: {tracked_bankHoliday_hours:.2f} Stunden")
    print(f"Sollzeit Feiertage: {target_bankHoliday_hours:.2f} Stunden")

    balance_bankHoliday_hours = tracked_bankHoliday_hours - target_bankHoliday_hours
    print(f"Saldo: {balance_bankHoliday_hours:+.2f} Stunden")

    # print(f"Jahr {previous_year} Feriensaldo: {balance_vacation_hours:+.2f} Stunden")


if __name__ == "__main__":
    main()
