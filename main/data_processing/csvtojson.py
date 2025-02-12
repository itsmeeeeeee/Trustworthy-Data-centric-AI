import pandas as pd
import json

# Lade die CSV-Datei (Erneuter Datei-Upload erforderlich)
csv_path = "data/outputs/potato/text_summarisation_potato.csv"  # Falls Datei vorhanden, bitte den korrekten Pfad anpassen

# Konvertiere die CSV-Daten in das gewünschte JSON-Format
try:
    df = pd.read_csv(csv_path)

    json_data = []
    for _, row in df.iterrows():
        json_entry = {
            "id": row["id"],
            "original_input": row["original_input"],
            "gold_reference": row["gold_reference"],
            "bigscience/T0pp": row["bigscience/T0pp"],
            "text-davinci-003": row["text-davinci-003"],
            "gpt-3.5-turbo": row["gpt-3.5-turbo"],
            "label_annotations": {
                "RELEVANCE - gold reference": {"scale_": ""},
                "FLUENCY - gold reference": {"scale_": ""},
                "COHERENCE - gold reference": {"scale_": ""},
                "CONSISTENCY - gold reference": {"scale_": ""},
                "RELEVANCE - bigscience/T0pp": {"scale_": ""},
                "FLUENCY - bigscience/T0pp": {"scale_": ""},
                "COHERENCE - bigscience/T0pp": {"scale_": ""},
                "CONSISTENCY - bigscience/T0pp": {"scale_": ""},
                "RELEVANCE - text-davinci-003": {"scale_": ""},
                "FLUENCY - text-davinci-003": {"scale_": ""},
                "COHERENCE - text-davinci-003": {"scale_": ""},
                "CONSISTENCY - text-davinci-003": {"scale_": ""},
                "RELEVANCE - gpt-3.5-turbo": {"scale_": ""},
                "FLUENCY - gpt-3.5-turbo": {"scale_": ""},
                "COHERENCE - gpt-3.5-turbo": {"scale_": ""},
                "CONSISTENCY - gpt-3.5-turbo": {"scale_": ""}
            }
        }
        json_data.append(json_entry)

    # Speichere die konvertierte JSON-Datei
    json_path = "data/outputs/potato/text_summarisation_for_annotation.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)

    json_path

except FileNotFoundError:
    " Datei nicht gefunden. Bitte lade die CSV-Datei erneut hoch."
