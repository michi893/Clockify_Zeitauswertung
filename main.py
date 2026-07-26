import streamlit as st

st.set_page_config(
    page_title="Clockify Zeitauswertung", page_icon="cevi-logo.png", layout="centered"
)
st.logo("cevi-logo.png")
st.title("Clockify Zeitauswertung")

from getApiKey import get_api_key
from getWorkspaceID import get_workspace_id
from getDateRange import get_date_range
from getDetailedReport import get_detailed_report
from getExpectedHours import expected_hours


def main():
    default_PENSUM, headers, WORKSPACE_ID, USERNAME = load_config()

    PENSUM = st.number_input(
        "Pensum (%)", min_value=10, max_value=100, value=default_PENSUM
    )
    start_date, end_date = get_date_range()

    if st.button("Auswertung starten"):
        with st.spinner("Berechne Zeit..."):
            (
                tracked_hours,
                target_hours,
                balance_tracked_hours,
                tracked_vacation_hours,
                tracked_bankHoliday_hours,
                target_vacation_hours,
                balance_vacation_hours,
                target_bankHoliday_hours,
                balance_bankHoliday_hours,
            ) = run_calculation(
                WORKSPACE_ID, USERNAME, headers, start_date, end_date, PENSUM
            )

        show_results(
            tracked_hours, target_hours, balance_tracked_hours, "Ergebnis erfasste Zeit"
        )

        show_results(
            tracked_vacation_hours,
            target_vacation_hours,
            balance_vacation_hours,
            "Ergebnis Ferien",
        )

        show_results(
            tracked_bankHoliday_hours,
            target_bankHoliday_hours,
            balance_bankHoliday_hours,
            "Ergebnis Feiertage",
        )

    # print(f"\nErgebniss Auswertung\nErfasste Zeit: {tracked_hours:.2f} Stunden")
    # print(f"Sollzeit: {target_hours:.2f} Stunden")
    # print(f"Saldo: {balance_tracked_hours:+.2f} Stunden")

    # # Feriensaldo für den eingegebenen Datumsbereichs berechnen
    # print(f"\nDavon erfasste Ferienzeit: {tracked_vacation_hours:.2f} Stunden")
    # print(f"Sollzeit Ferien (pro Jahr): {target_vacation_hours:.2f} Stunden")
    # print(f"Saldo: {balance_vacation_hours:+.2f} Stunden")

    # # Feiertagensaldo für den eingegebenen Datumsbereichs berechnen
    # print(f"\nDavon erfasste Feiertage-Zeit: {tracked_bankHoliday_hours:.2f} Stunden")
    # print(f"Sollzeit Feiertage: {target_bankHoliday_hours:.2f} Stunden")
    # print(f"Saldo: {balance_bankHoliday_hours:+.2f} Stunden")

    # print(f"Jahr {previous_year} Feriensaldo: {balance_vacation_hours:+.2f} Stunden")


def load_config():
    API_KEY, default_PENSUM = get_api_key()
    headers = {"X-Api-Key": API_KEY, "Content-Type": "application/json"}
    WORKSPACE_ID, USERNAME = get_workspace_id(API_KEY, headers)
    USERNAME = "Katja "
    # Usernames: David Niklaus, Katja , leana.leimer, Personaladmin  ACHTUNG: DER BENUTZTERNAME KATJA HAT EIN LEERZEICHEN AM ENDE!
    return default_PENSUM, headers, WORKSPACE_ID, USERNAME


def run_calculation(WORKSPACE_ID, USERNAME, headers, start_date, end_date, PENSUM):
    tracked_hours, tracked_vacation_hours, tracked_bankHoliday_hours = (
        get_detailed_report(
            WORKSPACE_ID,
            USERNAME,
            headers,
            start_date,
            end_date,
        )
    )

    target_hours, target_bankHoliday_hours = expected_hours(
        start_date, end_date, PENSUM
    )

    balance_tracked_hours = tracked_hours - target_hours
    target_vacation_hours = 5 * 42 * PENSUM / 100
    balance_vacation_hours = target_vacation_hours - tracked_vacation_hours
    balance_bankHoliday_hours = tracked_bankHoliday_hours - target_bankHoliday_hours
    return (
        tracked_hours,
        target_hours,
        balance_tracked_hours,
        tracked_vacation_hours,
        tracked_bankHoliday_hours,
        target_vacation_hours,
        balance_vacation_hours,
        target_bankHoliday_hours,
        balance_bankHoliday_hours,
    )


def show_results(tracked, target, balance, title):
    st.divider()
    st.subheader(title)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Erfasste Zeit", f"{tracked:.2f} h")

    with col2:
        st.metric("Sollzeit", f"{target:.2f} h")

    with col3:
        st.metric(
            "Saldo",
            f"{balance:+.2f} h",
            delta=f"{balance:+.2f} h",
        )


if __name__ == "__main__":
    main()
