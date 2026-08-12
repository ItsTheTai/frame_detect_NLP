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
Ausgabe ChatGPT+: Der Titel sollte so codiert werden:
Legality, constitutionality and jurisprudence: 2 (primär)
Political: 1 (zusätzlich einschlägig)
Alle übrigen Frames: 0
Warum: Im Mittelpunkt stehen die Mueller-Untersuchung und die Weigerung, einen Plädoyervertrag zu unterzeichnen. Ein solcher „plea deal“ ist Bestandteil eines juristischen Verfahrens und fällt nach dem Codebook primär unter Legality, constitutionality and jurisprudence.
Political ist zusätzlich einschlägig, weil Jerome Corsi und Roger Stone eng mit dem politisch geprägten Mueller-Komplex verbunden sind. Dieser politische Kontext ist im Titel erkennbar, aber weniger dominant als das Rechtsverfahren.
Crime and punishment würde ich nicht vergeben: Der Titel nennt weder eine konkrete Straftat noch Verhaftung, Verurteilung oder Bestrafung. Auch Public opinion passt nicht, da Corsis individuelles „Feiern“ laut Codebook noch keine öffentliche Meinung darstellt.
Ausgabe Claude: 1. Jerome Corsi / Mueller-Untersuchung / Plädoyervertrag
Codierung: Legality (2), Political (1)
Ein "Plädoyervertrag" (plea deal) ist ein Instrument des Gerichtsverfahrens — die Weigerung, ihn zu unterschreiben, ist ein Akt innerhalb eines laufenden Ermittlungs-/Gerichtsprozesses. Das Codebook ordnet Verfahrenselemente wie "pleads guilty", "plea talks" explizit der Legality-Dimension zu (siehe Beispiel im Codebook selbst: "Kaczynski plea talks crumble" → Legality). [likely, per Analogieschluss aus dem Codebook-Beispiel]
"Ende der Mueller-Untersuchung" ist ebenfalls primär eine Aussage über den Status eines rechtlichen Ermittlungsverfahrens, nicht in erster Linie über Parteipolitik.
Political (1) als Sekundärcode, weil Corsi als Stone-Mitarbeiter Teil eines politisch aufgeladenen Kontexts ist (Trump-Russland-Ermittlung) und "feiert" eine parteipolitisch interpretierbare Reaktion zeigt.
Meine Unsicherheit hier [likely, nicht certain]: Man könnte argumentieren, dass Political stattdessen primär sein sollte, weil die gesamte Mueller-Affäre im Kern eine parteipolitische Auseinandersetzung ist und "feiert" ein politisches Framing signalisiert, nicht nur ein juristisches. Das Codebook selbst warnt bei "Crime and Punishment vs. Political Factors", dass bei politisch verorteten Sanktionen (z.B. Kongress-Zensur) die politische Einbettung den Ausschlag geben kann. Wenn du eine strengere Linie willst — "jede Nennung einer politischen Figur/Partei-Konfliktlinie = Political primär" — wäre Political(2)/Legality(1) hier ebenso vertretbar. Ich habe mich für Legality primär entschieden, weil der Nachrichtenkern (Plädoyervertrag-Weigerung, Ende der Untersuchung) verfahrensrechtlich ist, nicht wahlpolitisch.

Promt: Brasilianischer Waffenhändler in den USA festgenommen
AusgabeChat GPT+: Die passende Codierung lautet:
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
Ausgabe Claude: Codierung: Crime and Punishment (2), Security and Defense (1)
"Festgenommen" (arrested) ist laut Codebook der Kernindikator für Crime and Punishment: Verhaftungen, Gesetzesverstöße, Strafverfolgung fallen explizit in diese Dimension. [certain — direkte Übereinstimmung mit Codebook-Beispielen wie "DNA leading to the arrest of suspects... Crime and Punishment"]
Security and Defense als Sekundärcode, weil Waffenhandel im internationalen Kontext (Brasilianer, USA) potenziell eine Bedrohungsdimension berührt — allerdings schwächer, da die Headline keine Bedrohungsabwehr (Grenzsicherung, Prävention) beschreibt, sondern eine bereits erfolgte Festnahme, also retrospektiv.
Meine Unsicherheit hier [Guessing]: Ohne Artikeltext weiß ich nicht, warum er festgenommen wurde — illegaler Waffenhandel, Schmuggel, fehlende Lizenz? Das würde die Sekundärcodes verschieben: bei grenzüberschreitendem Schmuggel wäre External Regulation and Reputation denkbar, bei reiner Vertriebslizenzfrage eher Legality. Ich habe mich für die minimalinvasive Lesart entschieden (Verhaftung = Kernfakt), aber das ist bei so kurzen Headlines mit Unsicherheit behaftet, die ich nicht wegdiskutieren will.
