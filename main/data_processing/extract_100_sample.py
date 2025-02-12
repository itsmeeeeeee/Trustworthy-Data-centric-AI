import os
import json
import csv
import argparse

def parse_arguments():
    """Parst die Befehlszeilenargumente."""
    parser = argparse.ArgumentParser(description="Extrahiere und speichere Texte aus JSONL-Dateien basierend auf einer bestimmten Evaluationsaufgabe.")
    
    parser.add_argument(
        "--task",
        type=str,
        choices=[ "simplification", "summarisation"],
        required=True,
        help="Die Evaluationsaufgabe (gec, simplification, summarisation)."
    )
    
    parser.add_argument(
        "--folder_count",
        type=int,
        default=4,
        help="Anzahl der zu durchsuchenden Ordner (Standard: 4)."
    )
    
    parser.add_argument(
        "--folder_suffix",
        type=str,
        default="of_8",
        help="Suffix für die Ordner (z. B. 'of_8' oder 'of_4')."
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    
    base_dir = os.path.dirname(__file__)

    
    folder_prefix = f"{args.task}_evaluation_"
    
    
    unique_entries = {}

    
    for i in range(1, args.folder_count + 1):
        folder_name = f"{folder_prefix}{i}_{args.folder_suffix}"
        folder_path = os.path.join(base_dir, folder_name, "annotation_output")

        # Prüfen, ob das Verzeichnis existiert
        if os.path.exists(folder_path):
            # Suche nach Unterordnern in "annotation_output"
            for subfolder in os.listdir(folder_path):
                subfolder_path = os.path.join(folder_path, subfolder)
                jsonl_file_path = os.path.join(subfolder_path, "annotated_instances.jsonl")

                # Prüfen, ob die Datei existiert
                if os.path.isfile(jsonl_file_path):
                    # Datei öffnen und Inhalte auslesen
                    with open(jsonl_file_path, 'r', encoding='utf-8') as file:
                        for line_num, line in enumerate(file, start=1):
                            line = line.strip()

                            # Ignoriere leere Zeilen
                            if not line:
                                print(f"Leere Zeile in Datei {jsonl_file_path} bei Zeile {line_num} übersprungen.")
                                continue

                            try:
                                data = json.loads(line)
                            except json.JSONDecodeError as e:
                                print(f"JSON-Fehler in Datei {jsonl_file_path} bei Zeile {line_num}: {e}")
                                continue  # Überspringe die fehlerhafte Zeile

                            # Speichere nur valide Einträge ohne "attention_check"
                            if "displayed_text" in data and data.get("id") not in ["attention_check_1", "attention_check_2"]:
                                displayed_text = data["displayed_text"]

                                # Nur speichern, wenn dieser "displayed_text" noch nicht existiert
                                if displayed_text not in unique_entries:
                                    unique_entries[displayed_text] = {
                                        "id": data["id"],
                                        "displayed_text": displayed_text,
                                        "gold_reference": data.get("summary_1", "")  # Umbenennung von summary_1 in gold_reference
                                    }

    # Konvertiere das Dictionary in eine Liste für die CSV-Ausgabe
    filtered_entries = list(unique_entries.values())

    
    output_folder = os.path.join(base_dir, "..", "100_sample")  

    # Erstelle den Ordner, falls er nicht existiert
    os.makedirs(output_folder, exist_ok=True)

    
    output_filename = f"{args.task}_texts_1.csv"
    output_path = os.path.join(output_folder, output_filename)

    if filtered_entries:
        with open(output_path, 'w', encoding='utf-8', newline='') as csv_file:
            fieldnames = ["id", "displayed_text", "gold_reference"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # Schreibe Kopfzeile
            writer.writeheader()

            # Schreibe die Daten
            writer.writerows(filtered_entries)

        print(f"Eindeutige gefilterte Texte wurden in {output_path} gespeichert.")
    else:
        print("Keine passenden 'displayed_text'-Einträge gefunden.")


if __name__ == "__main__":
    main()
