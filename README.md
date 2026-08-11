# frame_detect_NLP

## Hintergrund
GroundNews --> Sichtbar machen von Themen und Frames für deutsche Medien auf Basis von Titeln

## Datengrundlage
--> SemEval
--> DE, EN, IT, FR, PO: wir wollen DE Medienartikel verarbeiten, um mehr Daten zu haben auch EN, IT, FR, PO da Annahme: ähnliche Themen (-kultur)

## Annotationsstudie
Annotationsstudie um zu prüfen, ob Frame Zuordnung auch auf Basis von Titeln möglich ist.
Dazu Stichprobe (15%) aus Datengrundlage (Volltextzuordnung) und manuelle Annotation entsprechend Codebook
--> Annotationen Menschen vs. LLM

### Erwartete Erkenntnisse:
Frames-Zuordnung Titel vs. Volltext (LLM vs. Mensch)
Frames-Zuordnung Titel (Mensch)
Frames-Zuordnung Titel (LLM)
Frames-Zuordnung Mensch vs. LLM


### Promt LLM
Lies das hochgeladene Policy Frames Codebook vollständig ein und annotiere anschließend alle Headlines in headlines_dataset_15sample_LLM.xlsx. 
Verwende ausschließlich die Frame-Definitionen und Coding-Regeln des Codebooks als Grundlage. 
In den vorhandenen Frame-Spalten soll das passendste/primäre Frame mit 2 markiert werden, weitere einschlägige Frames mit 1 und nicht passende Frames mit 0. 
Behalte Filename, Headline_GER und Language unverändert und liefere die fertig annotierte XLSX-Datei zurück. 
Prüfe die Datei nach dem Schreiben auf Vollständigkeit und gültige Werte.


### Detailausgabe LLM (ChatGPT+):
Promt: Jerome Corsi, Mitarbeiter von Roger Stone, feiert das Ende der Mueller-Untersuchung, nachdem er sich geweigert hat, einen Plädoyervertrag zu unterzeichnen
Ausgabe: Der Titel sollte so codiert werden:
Legality, constitutionality and jurisprudence: 2 (primär)
Political: 1 (zusätzlich einschlägig)
Alle übrigen Frames: 0
Warum: Im Mittelpunkt stehen die Mueller-Untersuchung und die Weigerung, einen Plädoyervertrag zu unterzeichnen. Ein solcher „plea deal“ ist Bestandteil eines juristischen Verfahrens und fällt nach dem Codebook primär unter Legality, constitutionality and jurisprudence.
Political ist zusätzlich einschlägig, weil Jerome Corsi und Roger Stone eng mit dem politisch geprägten Mueller-Komplex verbunden sind. Dieser politische Kontext ist im Titel erkennbar, aber weniger dominant als das Rechtsverfahren.
Crime and punishment würde ich nicht vergeben: Der Titel nennt weder eine konkrete Straftat noch Verhaftung, Verurteilung oder Bestrafung. Auch Public opinion passt nicht, da Corsis individuelles „Feiern“ laut Codebook noch keine öffentliche Meinung darstellt.

Promt: Brasilianischer Waffenhändler in den USA festgenommen
Ausgabe: Die passende Codierung lautet:
Crime and punishment: 2 (primär)
External regulation and reputation: 1 (zusätzlich)
alle übrigen Frames: 0
Begründung: Die Festnahme nach einem mutmaßlichen Gesetzesverstoß ist das zentrale Signal. Das Codebook ordnet Festnahmen und polizeiliche Maßnahmen eindeutig Crime and punishment zu.
External regulation and reputation ist zusätzlich vertretbar, weil ein brasilianischer Waffenhändler in den USA festgenommen wird und die Headline somit einen grenzüberschreitenden Kontext enthält. Dieser Aspekt ist jedoch deutlich schwächer als die Festnahme.
Nicht passend sind:
Security and defense: Waffen allein reichen nicht; es wird keine drohende Gefahr oder präventive Abwehrmaßnahme genannt.
Legality: Es fehlt ein Gericht, Rechtsstreit oder eine Entscheidung über die Rechtmäßigkeit.
Economic: „Händler“ bezeichnet nur die Person beziehungsweise Tätigkeit; finanzielle Auswirkungen oder Marktfragen werden nicht behandelt.
Bei sehr konservativer Codierung wäre auch ausschließlich Crime and punishment = 2 gut begründbar.
