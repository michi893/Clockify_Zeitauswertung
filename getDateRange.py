import streamlit as st
import calendar
from datetime import datetime, date


def get_date_range():
    # while True:
    #     print("\nZeitraum auswählen:")
    #     print("1 - Auswertung über individuellen Zeitraum")
    #     print("2 - Auswertung über einen Monat")
    #     print("3 - Auswertung über ein Jahr")
    #     print(
    #         "4 - Total Gleit- und Ferienzeit bis zum aktuellen Datum (Startdatum 01.01.2025)"
    #     )

    #     choice = input("Auswahl (1-4): ")

    #     if choice == "1":
    #         return get_custom_range()

    #     elif choice == "2":
    #         return get_month_range()

    #     elif choice == "3":
    #         return get_year_range()

    #     elif choice == "4":
    #         return get_range()

    #     else:
    #         print("FEHLER: Bitte 1 oder 2 auswählen.")

    choice = st.selectbox(
        "Zeitraum",
        [
            "Individueller Zeitraum",
            "Monat",
            "Jahr",
            "Total Gleit- und Ferienzeit bis zum aktuellen Datum (Startdatum 01.01.2025)",
        ],
    )

    if choice == "Individueller Zeitraum":
        return get_custom_range()

    elif choice == "Monat":
        return get_month_range()

    elif choice == "Jahr":
        return get_year_range()

    elif (
        choice
        == "Total Gleit- und Ferienzeit bis zum aktuellen Datum (Startdatum 01.01.2025)"
    ):
        return get_range()

    # else:
    #     print("FEHLER: Bitte 1 oder 2 auswählen.")


def get_custom_range():
    today = date.today()
    # while True:
    # try:
    # start_input = input("Startdatum eingeben (YYYY-MM-DD): ")
    # end_input = input("Enddatum eingeben (YYYY-MM-DD): ")

    # start = datetime.strptime(start_input, "%Y-%m-%d").date()
    # end = datetime.strptime(end_input, "%Y-%m-%d").date()

    start = st.date_input("Startdatum auswählen", value=date.today())
    end = st.date_input("Enddatum auswählen", value=date.today())

    start_date = datetime.combine(start, datetime.min.time()).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    end_date = datetime.combine(end, datetime.max.time()).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Test: Jahre vor 2025 nicht erlaubt
    if start.year < 2025:
        # print("FEHLER: Es existieren keine Daten vor 2025.")
        st.error("FEHLER: Es existieren keine Daten vor 2025.")
        # continue

    # Test: Startdatum nach Enddatum
    if start > end:
        # print("FEHLER: Startdatum liegt nach Enddatum.")
        st.error("FEHLER: Startdatum liegt nach Enddatum.")
        # continue

    # Prüfen, ob ein Datum in der Zukunft liegt
    if start > today or end > today:
        # print("FEHLER: Eine Auswertung für die Zukunft ist nicht möglich.")
        st.error("FEHLER: Eine Auswertung für die Zukunft ist nicht möglich.")
        # continue

    # start_date = f"{start_input}T00:00:00Z"
    # end_date = f"{end_input}T23:59:59Z"

    return start_date, end_date

    # except ValueError:
    #     print(
    #         "FEHLER: Ungültiges Datum."
    #         "Prüfe Monat (1-12), gültige Tage des Monats und Format YYYY-MM-DD."
    #     )


def get_month_range():
    today = date.today()
    # Jahr abfragen
    # while True:
    #     try:
    # year = int(input("Jahr eingeben (YYYY): "))
    year = st.number_input("Jahr", 2024, today.year, today.year)

    # Test, ob das gewählte Jahr in der Zukunft liegt
    if year > today.year:
        # print("FEHLER: Eine Auswertung für die Zukunft ist nicht möglich.")
        st.error("FEHLER: Eine Auswertung für die Zukunft ist nicht möglich.")
        # continue

    # Test, ob das gewählte Jahr zu weit in der Vergangenheit liegt
    if year < 2024:
        # print("FEHLER: Ungültiges Jahr." "Es existieren keine Daten vor 2024.")
        st.error("FEHLER: Ungültiges Jahr." "Es existieren keine Daten vor 2024.")
        # continue
        # break

        # except ValueError:
        #     print("FEHLER: Ungültige Eingabe.")

    # Monat abfragen
    # while True:
    #     try:
    # month = int(input("Monat eingeben (1-12): "))
    month = st.number_input("Monat", 1, 12, today.month)

    # Test, ob der Monat zwischen 1 und 12 liegt
    if month < 1 or month > 12:
        # print("FEHLER: Monat muss zwischen 1 und 12 liegen.")
        st.error("FEHLER: Monat muss zwischen 1 und 12 liegen.")
        # continue

    # Test, ob der gewählte Monat in der Zukunft liegt
    if year == today.year and month > today.month:
        # print("FEHLER: Eine Auswertung für die Zukunft ist nicht möglich.")
        st.error("FEHLER: Eine Auswertung für die Zukunft ist nicht möglich.")
        # continue
        # break

        # except ValueError:
        #    print("FEHLER: Ungültige Eingabe.")

    start_date = f"{year}-{month:02d}-01T00:00:00Z"
    last_day = calendar.monthrange(year, month)[1]
    end_date = f"{year}-{month:02d}-{last_day}T23:59:59Z"
    return start_date, end_date


def get_year_range():
    today = date.today()
    # while True:
    #     try:
    # year = int(input("Jahr eingeben (YYYY): "))
    year = st.number_input("Jahr", 2024, today.year, today.year)

    if year == today.year:
        end_date = f"{today.strftime('%Y-%m-%d')}T23:59:59Z"
    else:
        end_date = f"{year}-12-31T23:59:59Z"

    # Test, ob das gewählte Jahr in der Zukunft liegt
    if year > today.year:
        # print("FEHLER: Eine Auswertung ist nur für abgeschlossene Jahre möglich.")
        st.error("FEHLER: Eine Auswertung ist nur für abgeschlossene Jahre möglich.")
        # continue

    # Test, ob das gewählte Jahr zu weit in der Vergangenheit liegt
    if year < 2024:
        # print("FEHLER: Ungültiges Jahr." "Es existieren keine Daten vor 2024.")
        st.error("FEHLER: Ungültiges Jahr." "Es existieren keine Daten vor 2024.")
        #         continue
        #     break

        # except ValueError:
        #     print("FEHLER: Ungültige Eingabe.")

    start_date = f"{year}-01-01T00:00:00Z"
    return start_date, end_date


def get_range():
    start_date = f"2025-01-01T00:00:00Z"
    end_date = f"{date.today().strftime('%Y-%m-%d')}T23:59:59Z"
    return start_date, end_date
