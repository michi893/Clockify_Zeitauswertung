import os
import sys
import re
from dotenv import load_dotenv

def get_api_key():
    env_found = load_dotenv()
    API_KEY = os.getenv("API_KEY")
    PENSUM = os.getenv("PENSUM")

    # Test: Wurde die '.env'-Datei gefunden/geladen?
    if not env_found:
        print("FEHLER: Keine '.env'-Datei gefunden!")
        print(f"Gesucht wurde im Verzeichnis: {os.getcwd()}")
        print(f"Speichere die Datei '.env' (Darf nicht umbenannt werden)im selben Verzeichnis wie 'main.py' und füge den persönlichen API-Key hinzu.")
        sys.exit(1)

    # Test: Wurde der API-Key geladen?
    if not API_KEY:
        print("FEHLER: Der API_KEY wurde nicht gefunden.")
        print(f"Trage deinen persönlichen API-Key in der Datei '.env' ein.")
        print(f"Überprüfe, dass deine Eingabe auf derselben Zeile wie 'API_KEY=' steht.")
        sys.exit(1)

    # Test: Der API-Key enthält keine Leerzeichen,Tabulatoren oder Zeilenumbrüche?
    if re.search(r"\s", API_KEY):
        print("FEHLER: Der API_KEY enthält Leerzeichen oder andere Whitespace-Zeichen.")
        print(f"Eintrag lautet nicht exakt 'API_KEY=<dein_api_key>'. Achtung:Keine Leerzeichen (Auch um das Gleichheitszeichen)!")
        sys.exit(1)

    # Test: Wurde das Pensum geladen?
    if PENSUM is None:
        print("FEHLER: Das PENSUM wurde nicht gefunden.")
        print("Trage dein Pensum in der Datei '.env' ein.")
        print("Beispiel: PENSUM=80")
        sys.exit(1)

    # Test: Pensum ist eine Zahl
    try:
        PENSUM = int(PENSUM)

    except ValueError:
        print("FEHLER: Das PENSUM muss eine Zahl sein.")
        print("Beispiel: PENSUM=80")
        sys.exit(1)

    # Test: Pensum zwischen 0 und 100
    if PENSUM < 1 or PENSUM > 100:
        print("FEHLER: Das PENSUM muss zwischen 0 und 100 liegen.")
        print("Beispiel: PENSUM=80")
        sys.exit(1)

    print("✓ API_KEY erfolgreich geladen.")
    print(f"✓ PENSUM erfolgreich geladen: {PENSUM}%")
    return API_KEY, PENSUM