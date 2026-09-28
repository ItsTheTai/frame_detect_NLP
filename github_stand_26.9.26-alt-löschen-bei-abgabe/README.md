# frame_detect_NLP

## Hintergrund, Daten und Vorannahmen
Unterschiedliche politische Lager framen News häufig unterschiedlich.
Freie Meinungsbildung erfordert transparenz.
in den USA: GroundNews --> Sichtbar machen von Themen und Frames entlang der politischen Lager, Identifikation von Blindspots
in DEU: bislang nichts vergleichbares für deutsche Medienlandschaft
Vorhaben: Entwicklung eines Prototypen, Framing in deutschen Medien auf Basis von Titeln sichtbar macht

### Vorannahme
Wichtige Frames werden bereits im Titel transportiert

### Datengrundlage
--> SemEval Task 3: Frame-Erkennung in verschiedenen sprachen, mit verschiedenen Modellen, Wettbewerb
--> Datensätze für verschiedene Sprachen, auf Volltexten annotiert
--> wir wollen DE Medienartikel verarbeiten, bei Betrachtung von Titeln jedoch im Vergleich zu Volltexten informationsverlust, kleiner DE Datensatz wird insofern noch kleiner
--> um mehr Daten zu haben auch EN, IT, FR, PO da Annahme: ähnliche Themen (-kultur)

## Annotationsstudie
Annotationsstudie um zu prüfen, ob Frame Zuordnung auch auf Basis von Titeln möglich ist.
Dazu Stichprobe (15%) aus Datengrundlage (Volltextzuordnung) und manuelle Annotation entsprechend Codebook durch menschliche Annotatoren und LLMs

### Erwartete Erkenntnisse:
Konsistenz Frames-Zuordnung Titel menschliche Annotatoren vs. LLms
Leistung Frames Erkennung Titel vs. Volltext (LLM vs. Mensch)

