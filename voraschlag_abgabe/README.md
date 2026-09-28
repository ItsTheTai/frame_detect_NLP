# Automated Detection of Policy Frames in German News Headlines

This repository contains the codebase, weak supervision pseudo-labeling pipeline, model training scripts, evaluation benchmarks, and prototype application for detecting policy frames in German news headlines and comparing thematic coverage across media outlets.

## Project Overview
News headlines condense complex issues into key words that set the perspective (frame) through which events are interpreted. This project provides:
* **Transformer-Based Multi-Label Frame Classifier**: A fine-tuned `LSX-UniWue/ModernGBERT\_134M` model trained to detect 14 generic policy frames (plus a residual category) at the headline level.
* **Weak Supervision \& Pseudo-Labeling Pipeline**: An automated annotation strategy combining LLM annotations (GPT-5.6, Claude, Gemini/Mistral) with majority voting and article-reference matching across SemEval-2023, Media Frames Corpus (MFC), and Chinese News Framing Dataset (CHN).
* **Human-Annotated Gold Standard**: A manually curated benchmark set of 70 *Tagesschau* headlines for model evaluation against real-world media.
* **Ground-News-Inspired Prototype**: A BERTopic clustering and inference pipeline designed to group comparable news headlines across German news outlets (*Tagesschau*, *FAZ*, *taz*) and highlight frame distributions.

## Key Results
* **Full Dataset Mix**: Reached a **micro-$F\_1$ of 0.716** (macro-$F\_1$: 0.532) on the stratified multi-label test set.
* **Tagesschau Gold Benchmark**: Achieved a **micro-$F\_1$ of 0.588** (macro-$F\_1$: 0.379) on 70 independently annotated human benchmark headlines.

## Target Policy Frames
The model classifies headlines across 14 policy frames adapted from the Policy Frames Codebook (Boydstun et al.), plus a technical residual category:
1. Economic
2. Capacity and Resources
3. Morality
4. Fairness and Equality
5. Legality, Constitutionality, and Jurisprudence
6. Policy Prescription and Evaluation
7. Crime and Punishment
8. Security and Defense
9. Health and Safety
10. Quality of Life
11. Cultural Identity
12. Public Opinion
13. Political
14. External Regulation and Reputation
15. Other / Null Case

## Repository Structure
pending.

