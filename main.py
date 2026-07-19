from getApiKey import get_api_key
from getWorkspaceID import get_workspace_id
from getDateRange import get_date_range
from getDetailedReport import get_detailed_report
from getExpectedWorkingHours import expected_working_hours

def main():
    API_KEY, PENSUM = get_api_key()

    headers = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
    }
    
    WORKSPACE_ID, USER_ID = get_workspace_id(API_KEY, headers)
    start_date, end_date = get_date_range()
    #print (f"Startdatum: {start_date}")
    #print (f"Enddatum: {end_date}")
    tracked_hours = get_detailed_report(API_KEY, WORKSPACE_ID, USER_ID, headers, start_date, end_date)
    expected_hours = expected_working_hours(start_date, end_date)

    # -----------------------------------
    # Saldo
    # -----------------------------------
    balance = (tracked_hours - expected_hours)
    print(f"Stundensaldo: {balance:+.2f} Stunden")

    #print(f"API_KEY: {API_KEY}")1
    #print(f"WORKSPACE_ID: {WORKSPACE_ID}")
    #print(f"USER_ID: {USER_ID}")

if __name__ == "__main__":
    main()