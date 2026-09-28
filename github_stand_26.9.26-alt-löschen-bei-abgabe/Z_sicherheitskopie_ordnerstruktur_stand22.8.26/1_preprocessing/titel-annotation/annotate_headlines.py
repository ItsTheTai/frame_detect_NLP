import time
import json
import pandas as pd
from google import genai
from google.genai import types

# ==========================================
# 1. KONFIGURATION & API-KEY
# ==========================================
API_KEY = "AQ.Ab8RN6LUJlnJsXOPNB9TryOuLyef2gjD5ZYzK3kcRj6e4EfpoQ"  

CODEBOOK_PATH = "/Users/Familie/Documents/Uni_Regensburg/A_Digital_Humanities/2SE_SS26/Natural_Language_Engineering/projekt/frame_detect_NLP/Z_Policy_Frames_Codebook.pdf"
INPUT_FILE = "/Users/Familie/Documents/Uni_Regensburg/A_Digital_Humanities/2SE_SS26/Natural_Language_Engineering/projekt/frame_detect_NLP/1_preprocessing/headlines_dataset_full_LLM.xlsx"
OUTPUT_XLSX = "headlines_dataset_full_LLM_annotiert_gemini-3.7-flash.xlsx"


MODEL_NAME = "gemini-3.7-flash"

# Anzahl Headlines pro API-Request
BATCH_SIZE = 40

# Wie oft ein fehlgeschlagener Request wiederholt werden soll
MAX_RETRIES = 5

# Grundwartezeit für Retries
RETRY_WAIT_SECONDS = 10

# Pause zwischen erfolgreichen Batches
BATCH_WAIT_SECONDS = 4


# ==========================================
# 2. GEMINI CLIENT
# ==========================================

client = genai.Client(
    api_key=API_KEY
)


# ==========================================
# 3. FRAME-SPALTEN
# ==========================================

FRAME_COLUMNS = [
    "Economic",
    "Capacity and resources",
    "Morality",
    "Fairness and equality",
    "Legality, constitutionality and jurisprudence",
    "Policy prescription and evaluation",
    "Crime and punishment",
    "Security and defense",
    "Health and safety",
    "Quality of life",
    "Cultural identity",
    "Public opinion",
    "Political",
    "External regulation and reputation"
]


# ==========================================
# 4. JSON-SCHEMA
# ==========================================

batch_schema = {
    "type": "ARRAY",
    "description": (
        "Liste der annotierten Schlagzeilen "
        "aus dem Batch."
    ),

    "items": {
        "type": "OBJECT",

        "properties": {

            "row_id": {
                "type": "INTEGER",
                "description": (
                    "Exakte ID der ursprünglichen "
                    "DataFrame-Zeile."
                )
            },

            "Economic": {
                "type": "INTEGER"
            },

            "Capacity and resources": {
                "type": "INTEGER"
            },

            "Morality": {
                "type": "INTEGER"
            },

            "Fairness and equality": {
                "type": "INTEGER"
            },

            "Legality, constitutionality and jurisprudence": {
                "type": "INTEGER"
            },

            "Policy prescription and evaluation": {
                "type": "INTEGER"
            },

            "Crime and punishment": {
                "type": "INTEGER"
            },

            "Security and defense": {
                "type": "INTEGER"
            },

            "Health and safety": {
                "type": "INTEGER"
            },

            "Quality of life": {
                "type": "INTEGER"
            },

            "Cultural identity": {
                "type": "INTEGER"
            },

            "Public opinion": {
                "type": "INTEGER"
            },

            "Political": {
                "type": "INTEGER"
            },

            "External regulation and reputation": {
                "type": "INTEGER"
            }
        },

        "required": [
            "row_id"
        ] + FRAME_COLUMNS
    }
}


# ==========================================
# 5. SYSTEM-INSTRUKTION
# ==========================================

SYSTEM_INSTRUCTION = """
Lies das hochgeladene Policy Frames Codebook vollständig ein und annotiere anschließend alle Headlines in headlines_dataset_full_LLM.xlsx. Verwende ausschließlich die Frame-Definitionen und Coding-Regeln des Codebooks als Grundlage. In den vorhandenen Frame-Spalten soll das passendste/primäre Frame mit 2 markiert werden, weitere einschlägige Frames mit 1 und nicht passende Frames mit 0. Wenn es keine einschlägigen Frames gibt, werden alle Frames mit 0 markiert. Behalte Filename, Headline_GER und Language unverändert und liefere die fertig annotierte XLSX-Datei zurück. Prüfe die Datei nach dem Schreiben auf Vollständigkeit und gültige Werte.
"""


# ==========================================
# 6. EINEN BATCH AN GEMINI SENDEN
# ==========================================

def send_batch(pdf_file, batch_items):

    user_prompt = (
        "Annotiere die folgenden Headlines aus dem Datensatz "
        "gemäß dem hochgeladenen Policy Frames Codebook.\n\n"
        + json.dumps(
            batch_items,
            ensure_ascii=False,
            indent=2
        )
    )

    # ======================================
    # WICHTIG:
    #
    # KEINE thinking_config
    # KEIN thinking_level
    # ======================================

    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        response_mime_type="application/json",
        response_schema=batch_schema
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[
            pdf_file,
            user_prompt
        ],
        config=config
    )

    if not response.text:
        raise ValueError(
            "Gemini hat eine leere Antwort zurückgegeben."
        )

    results = json.loads(
        response.text
    )

    if not isinstance(results, list):
        raise ValueError(
            "Die Gemini-Antwort ist keine Liste."
        )

    return results


# ==========================================
# 7. BATCH MIT RETRY-MECHANISMUS
# ==========================================

def annotate_batch_with_retry(
    pdf_file,
    batch_items,
    batch_number,
    start_display,
    end_display
):

    for attempt in range(
        1,
        MAX_RETRIES + 1
    ):

        try:

            print(
                f"API-Request Versuch "
                f"{attempt}/{MAX_RETRIES}..."
            )

            results = send_batch(
                pdf_file,
                batch_items
            )

            print(
                "API-Request erfolgreich."
            )

            return results

        except Exception as e:

            error_text = str(e)

            print()
            print(
                f"Request fehlgeschlagen "
                f"(Versuch {attempt}/{MAX_RETRIES})."
            )

            print(
                f"Fehlertyp: {type(e).__name__}"
            )

            print(
                f"Fehler: {error_text}"
            )

            # ==================================
            # Prüfen, ob es ein 503-Fehler ist
            # ==================================

            is_503 = (
                "503" in error_text
                or "UNAVAILABLE" in error_text
                or "high demand" in error_text
            )

            if not is_503:

                print(
                    "Kein 503-Fehler. "
                    "Der Fehler wird nicht automatisch "
                    "wiederholt."
                )

                raise

            # ==================================
            # Letzter Versuch?
            # ==================================

            if attempt >= MAX_RETRIES:

                print()
                print(
                    f"Batch {batch_number} konnte nach "
                    f"{MAX_RETRIES} Versuchen nicht "
                    f"verarbeitet werden."
                )

                raise

            # ==================================
            # Exponentielles Warten
            # ==================================

            wait_time = (
                RETRY_WAIT_SECONDS
                * (2 ** (attempt - 1))
            )

            print()
            print(
                f"Gemini ist momentan ausgelastet."
            )

            print(
                f"Warte {wait_time} Sekunden "
                f"und versuche Batch "
                f"{batch_number} erneut..."
            )

            print()

            time.sleep(
                wait_time
            )


# ==========================================
# 8. HAUPTPROGRAMM
# ==========================================

pdf_file = None

try:

    print("==========================================")
    print("POLICY FRAME ANNOTATION MIT GEMINI")
    print("==========================================")
    print()

    # ======================================
    # CODEBOOK HOCHLADEN
    # ======================================

    print(
        "Lade Policy Frames Codebook (PDF) hoch..."
    )

    pdf_file = client.files.upload(
        file=CODEBOOK_PATH
    )

    print(
        f"Codebook hochgeladen: {pdf_file.name}"
    )

    print()

    # ======================================
    # EXCEL EINLESEN
    # ======================================

    print(
        "Lese Excel-Datei (.xlsx) ein..."
    )

    df = pd.read_excel(
        INPUT_FILE
    )

    total_rows = len(df)

    print(
        f"Gesamtzeilen im Datensatz: {total_rows}"
    )

    print()

    # ======================================
    # EINGABESPALTEN PRÜFEN
    # ======================================

    required_input_columns = [
        "Headline_GER",
        "Filename",
        "Language"
    ]

    missing_columns = [
        col
        for col in required_input_columns
        if col not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            "Folgende benötigte Spalten fehlen "
            "in der Excel-Datei: "
            + ", ".join(missing_columns)
        )

    # ======================================
    # FRAME-SPALTEN ERSTELLEN
    # ======================================

    for col in FRAME_COLUMNS:

        if col not in df.columns:

            df[col] = 0

    # ======================================
    # BATCH-ANNOTATION
    # ======================================

    total_batches = (
        (total_rows + BATCH_SIZE - 1)
        // BATCH_SIZE
    )

    print(
        f"Starte Batch-Annotation mit "
        f"{MODEL_NAME}..."
    )

    print(
        f"Batch-Größe: {BATCH_SIZE}"
    )

    print(
        f"Anzahl Batches: {total_batches}"
    )

    print()

    processed_rows = 0

    # ======================================
    # BATCH LOOP
    # ======================================

    for i in range(
        0,
        total_rows,
        BATCH_SIZE
    ):

        batch_number = (
            i // BATCH_SIZE
        ) + 1

        batch_df = df.iloc[
            i:i + BATCH_SIZE
        ]

        start_display = i + 1

        end_display = min(
            i + BATCH_SIZE,
            total_rows
        )

        print(
            "------------------------------------------"
        )

        print(
            f"Batch {batch_number}/{total_batches}"
        )

        print(
            f"Verarbeite Zeilen "
            f"{start_display} bis "
            f"{end_display} "
            f"von {total_rows}..."
        )

        print(
            "------------------------------------------"
        )

        # ==================================
        # BATCH VORBEREITEN
        # ==================================

        batch_items = []

        for idx, row in batch_df.iterrows():

            # Headline
            headline = row["Headline_GER"]

            if pd.isna(headline):

                headline = ""

            # Filename
            filename = row["Filename"]

            if pd.isna(filename):

                filename = ""

            # Language
            language = row["Language"]

            if pd.isna(language):

                language = ""

            batch_items.append(
                {
                    "row_id": int(idx),

                    "Headline_GER": str(
                        headline
                    ),

                    "Filename": str(
                        filename
                    ),

                    "Language": str(
                        language
                    )
                }
            )

        # ==================================
        # BATCH SENDEN + RETRIES
        # ==================================

        results = annotate_batch_with_retry(
            pdf_file=pdf_file,
            batch_items=batch_items,
            batch_number=batch_number,
            start_display=start_display,
            end_display=end_display
        )

        # ==================================
        # IDS PRÜFEN
        # ==================================

        expected_ids = {
            item["row_id"]
            for item in batch_items
        }

        returned_ids = {
            item.get("row_id")
            for item in results
        }

        # Fehlende IDs
        missing_ids = (
            expected_ids - returned_ids
        )

        if missing_ids:

            raise ValueError(
                "Gemini hat keine Ergebnisse "
                "für folgende row_ids zurückgegeben: "
                f"{sorted(missing_ids)}"
            )

        # Unerwartete IDs
        unexpected_ids = (
            returned_ids - expected_ids
        )

        if unexpected_ids:

            raise ValueError(
                "Gemini hat unbekannte row_ids "
                "zurückgegeben: "
                f"{sorted(unexpected_ids)}"
            )

        # Anzahl prüfen
        if len(results) != len(batch_items):

            raise ValueError(
                f"Erwartet: {len(batch_items)} Ergebnisse. "
                f"Erhalten: {len(results)}."
            )

        # ==================================
        # ERGEBNISSE IN DATAFRAME SCHREIBEN
        # ==================================

        for item in results:

            r_id = int(
                item["row_id"]
            )

            if r_id not in df.index:

                raise ValueError(
                    f"row_id {r_id} existiert "
                    "nicht im DataFrame."
                )

            for col in FRAME_COLUMNS:

                value = int(
                    item[col]
                )

                if value not in (
                    0,
                    1,
                    2
                ):

                    raise ValueError(
                        f"Ungültiger Wert für "
                        f"row_id={r_id}, "
                        f"Frame='{col}': "
                        f"{value}. "
                        "Erlaubt sind nur 0, 1 oder 2."
                    )

                df.at[
                    r_id,
                    col
                ] = value

        # ==================================
        # FORTSCHRITT
        # ==================================

        processed_rows += len(results)

        print()
        print(
            f"Batch {batch_number} erfolgreich."
        )

        print(
            f"Verarbeitet: "
            f"{processed_rows}/{total_rows}"
        )

        # ==================================
        # PAUSE ZWISCHEN BATCHES
        # ==================================

        if end_display < total_rows:

            print(
                f"Warte {BATCH_WAIT_SECONDS} Sekunden "
                "vor dem nächsten Batch..."
            )

            time.sleep(
                BATCH_WAIT_SECONDS
            )

        print()

    # ======================================
    # ALLE BATCHES ERFOLGREICH
    # ======================================

    print("==========================================")
    print("ALLE BATCHES ERFOLGREICH VERARBEITET")
    print("==========================================")

    print(
        f"Verarbeitete Zeilen: "
        f"{processed_rows}/{total_rows}"
    )

    print()

    # ======================================
    # FINALE EXCEL-DATEI SPEICHERN
    # ======================================

    print(
        "Speichere finale Excel-Datei..."
    )

    df.to_excel(
        OUTPUT_XLSX,
        index=False
    )

    print()

    print(
        "=========================================="
    )

    print(
        "ERFOLG!"
    )

    print(
        "=========================================="
    )

    print(
        f"Datei gespeichert als:"
    )

    print(
        OUTPUT_XLSX
    )

    print()


# ==========================================
# 9. FEHLERBEHANDLUNG
# ==========================================

except Exception as e:

    print()

    print(
        "=========================================="
    )

    print(
        "FEHLER WÄHREND DER VERARBEITUNG"
    )

    print(
        "=========================================="
    )

    print(
        f"Fehlermeldung: {e}"
    )

    print(
        f"Fehlertyp: {type(e).__name__}"
    )

    print()

    print(
        "Die finale Excel-Datei wurde "
        "nicht gespeichert."
    )


# ==========================================
# 10. CODEBOOK LÖSCHEN
# ==========================================

finally:

    print()

    print(
        "Räume temporäres Codebook auf..."
    )

    if pdf_file is not None:

        try:

            client.files.delete(
                name=pdf_file.name
            )

            print(
                "Cleanup erfolgreich."
            )

        except Exception as cleanup_error:

            print(
                f"Cleanup-Fehler (ignoriert): "
                f"{cleanup_error}"
            )

    else:

        print(
            "Kein hochgeladenes PDF "
            "zum Löschen vorhanden."
        )

    print(
        "Fertig."
    )