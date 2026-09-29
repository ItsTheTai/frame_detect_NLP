1. # Annotationsstudie (Human vs. LLMs)



**Prompt 1:** Der folgende Prompt wurde den vier LLMs zusammen mit dem Codebook und der vollständigen Datei mit 210 Titeln übergeben:

“Lies das hochgeladene Policy Frames Codebook vollständig ein und annotiere anschließend alle Headlines in headlines\_dataset\_15sample\_LLM.xlsx. Verwende ausschließlich die Frame-Definitionen und Coding-Regeln des Codebooks als Grundlage. In den vorhandenen Frame-Spalten soll das passendste/primäre Frame mit 2 markiert werden, weitere einschlägige Frames mit 1 und nicht passende Frames mit 0. Wenn es keine einschlägigen Frames gibt, werden alle Frames mit 0 markiert. Behalte Filename, Headline\_GER und Language unverändert und liefere die fertig annotierte XLSX-Datei zurück. Prüfe die Datei nach dem Schreiben auf Vollständigkeit und gültige Werte.”



## 2\. Prompts der Datenerweiterung für das Fine-Tuning

## Annotation von SemEval und CHN
Prompt 1 and 2 sind bis auf das Ausgabeformat identisch. Prompt 1 verwendet dabei.xlsx während Prompt 2 .csv verlangt.


**Prompt 2:** “Lies das hochgeladene Policy Frames Codebook vollständig ein und annotiere anschließend alle Headlines in headlines\_dataset\_15sample\_LLM.csv. Verwende ausschließlich die Frame-Definitionen und Coding-Regeln des Codebooks als Grundlage. In den vorhandenen Frame-Spalten soll das passendste/primäre Frame mit 2 markiert werden, weitere einschlägige Frames mit 1 und nicht passende Frames mit 0. Wenn es keine einschlägigen Frames gibt, werden alle Frames mit 0 markiert. Behalte Filename, Headline\_GER und Language unverändert und liefere die fertig annotierte CSV-Datei zurück. Prüfe die Datei nach dem Schreiben auf Vollständigkeit und gültige Werte.”



## Annotation von MFC



**Prompt 3:** “Verarbeite den vollständigen Datensatz intern blockweise, um die Annotationsqualität und Konsistenz zu gewährleisten. Teile die CSV nicht als separate Dateien auf und gib keine Zwischenresultate aus.

* Verarbeite alle Zeilen des Datensatzes.
* Teile den Datensatz intern in geeignete Blöcke auf.
* Wende auf jeden Block exakt dieselben
* Frame-Definitionen und Coding-Regeln des hochgeladenen Policy Frames Codebooks an.
* Die Aufteilung in Blöcke darf die Coding-Entscheidungen nicht verändern.
* Behalte die ursprüngliche Reihenfolge der Zeilen bei.
* Führe nach der Blockverarbeitung sämtliche Blöcke wieder zu einer einzigen vollständigen CSV zusammen.
* Gib keine einzelnen Blockdateien zurück, sondern ausschließlich die finale zusammengeführte CSV.
* Prüfe die fertige Gesamtdatei nach dem Zusammenführen auf:

  * exakt dieselbe Anzahl an Datenzeilen wie die Eingabedatei,
  * keine verlorenen oder zusätzlich erzeugten Zeilen,
  * unveränderte Werte in Filename, Headline\_GER und Language,
  * unveränderte Spaltenstruktur,
  * ausschließlich gültige Frame-Werte 0, 1 oder 2,
  * höchstens ein primäres Frame (2) pro Headline,
  * korrekte Behandlung von Headlines ohne einschlägiges Frame (alle Frame-Spalten = 0).

Erst nach erfolgreicher Gesamtprüfung soll die finale CSV-Datei ausgegeben werden.”

