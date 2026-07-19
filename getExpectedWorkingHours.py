from datetime import date, datetime, timedelta

def expected_working_hours(start_date, end_date):
    # -----------------------------------
    # Sollzeit berechnen
    # Beispiel: 8h pro Arbeitstag
    # -----------------------------------

    working_days = 0

    #for day in range(1,last_day + 1):

    start = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%SZ")
    end = datetime.strptime(end_date,"%Y-%m-%dT%H:%M:%SZ")

    for day_offset in range((end.date() - start.date()).days + 1):
        current_date = start + timedelta(days=day_offset)
        
        weekday = date(
            current_date.year,
            current_date.month,
            current_date.day
        ).weekday()

        # Montag-Freitag
        if weekday < 5:
            working_days += 1


    TARGET_HOURS_PER_DAY = 8

    target_hours = (
        working_days *
        TARGET_HOURS_PER_DAY
    )

    print(
        f"Sollzeit: {target_hours:.2f} Stunden"
    )
    return target_hours


