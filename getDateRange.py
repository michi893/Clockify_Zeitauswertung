import calendar
from datetime import datetime, date


def get_date_range():
    while True:
        print("\nZeitraum auswählen:")
        print("1 - Auswertung über einen Monat")
        print("2 - Auswertung über individuellen Zeitraum")

        choice = input("Auswahl (1/2): ")

        if choice == "1":
            return get_month_range()

        elif choice == "2":
            return get_custom_range()

        else:
            print("FEHLER: Bitte 1 oder 2 auswählen.")


def get_month_range():
    today = date.today()
    #Jahr abfragen
    while True:
        try:
            year = int(input("Jahr eingeben (YYYY): "))
            # Test, ob das gewählte Jahr in der Zukunft liegt
            if year > today.year:
                print("FEHLER: Eine Auswertung für die Zukunft ist nicht möglich.")
                continue
            
            # Test, ob das gewählte Jahr zu weit in der Vergangenheit liegt
            if year < 2024:
                print("FEHLER: Ungültiges Jahr." "Es existieren keine Daten vor 2024.")
                continue
            break
        
        except ValueError:
            print("FEHLER: Ungültige Eingabe.")

    #Monat abfragen
    while True:
        try:    
            month = int(input("Monat eingeben (1-12): "))
            #Test, ob der Monat zwischen 1 und 12 liegt
            if month < 1 or month > 12:
                print("FEHLER: Monat muss zwischen 1 und 12 liegen.")
                continue

            # Test, ob der gewählte Monat in der Zukunft liegt
            if month > today.month:
                print("FEHLER: Eine Auswertung für die Zukunft ist nicht möglich.")
                continue
            break

        except ValueError:
            print("FEHLER: Ungültige Eingabe.")
                
    start_date = f"{year}-{month:02d}-01T00:00:00Z"
    last_day = calendar.monthrange(year, month)[1]
    end_date = (f"{year}-{month:02d}-{last_day}T23:59:59Z")
    return start_date, end_date

def get_custom_range():
    today = date.today()
    while True:
        try:
            start_input = input("Startdatum eingeben (YYYY-MM-DD): ")
            end_input = input("Enddatum eingeben (YYYY-MM-DD): ")

            start = datetime.strptime(start_input,"%Y-%m-%d").date()
            end = datetime.strptime(end_input,"%Y-%m-%d").date()

            # Test: Jahre vor 2024 nicht erlaubt
            if start.year < 2024:
                print("FEHLER: Es existieren keine Daten vor 2024.")
                continue

            # Test: Startdatum nach Enddatum
            if start > end:
                print("FEHLER: Startdatum liegt nach Enddatum.")
                continue
            
            # Prüfen, ob ein Datum in der Zukunft liegt
            if start > today or end > today:
                print("FEHLER: Eine Auswertung für die Zukunft ist nicht möglich.")
                continue

            start_date = (f"{start_input}T00:00:00Z")
            end_date = (f"{end_input}T23:59:59Z")

            return start_date, end_date

        except ValueError:
            print(
                "FEHLER: Ungültiges Datum."
                "Prüfe Monat (1-12), gültige Tage des Monats und Format YYYY-MM-DD."
            )