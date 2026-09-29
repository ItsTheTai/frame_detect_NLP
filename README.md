# Automated Detection of Policy Frames in German News Headlines

News headlines condense complex issues into key words that set the perspective (frame) through which events are interpreted. This repository implements an automated system for detecting policy frames in German news headlines using a fine-tuned transformer model. It combines weak supervision (LLM-based pseudo-labeling with majority voting) and human annotations to classify headlines across 14 policy frames plus a residual category, achieving a micro-F1 of 0.716 on the full dataset and 0.588 on a manually-curated Tagesschau gold standard benchmark.
* Language(s): Python (Jupyter Notebooks, 100%)
* Framework / runtime: Hugging Face Transformers, PyTorch
* Notable libraries: pandas, transformers (AutoTokenizer, AutoModelForSequenceClassification), torch, sklearn (for metrics), BERTopic (for clustering)

## Target Policy Frames & Distribution of LLM title annotated Frames
The model classifies headlines across 14 policy frames adapted from the Policy Frames Codebook (Boydstun et al. 2020), plus a technical residual category:
| Frame | % of Labels |
|-------|------------|
| Policy prescription and evaluation | 17.69% |
| Legality, constitutionality and jurisprudence | 16.92% |
| Political | 13.02% |
| External regulation and reputation | 9.38% |
| Security and defense | 8.06% |
| Economic | 6.99% |
| Crime and punishment | 5.54% |
| Health and safety | 5.12% |
| Morality | 4.54% |
| Capacity and resources | 4.19% |
| Other / Null Case | 3.16% |
| Fairness and equality | 1.71% |
| Public opinion | 1.39% |
| Cultural identity | 1.29% |
| Quality of life | 1.00% |


## Methods Outline
* **Transformer-Based Multi-Label Frame Classifier**: A fine-tuned `LSX-UniWue/ModernGBERT_134M` model trained to detect 14 generic policy frames (plus a residual category) at the headline level.
* **Weak Supervision \& Pseudo-Labeling Pipeline**: An automated annotation strategy combining LLM annotations (GPT-5.6, Claude, Gemini/Mistral) with majority voting and article-reference matching across SemEval-2023, Media Frames Corpus (MFC), and Chinese News Framing Dataset (CHN).
* **Human-Annotated Gold Standard**: A manually curated benchmark set of 70 *Tagesschau* headlines for model evaluation against real-world media.
* **Ground-News-Inspired Prototype**: A BERTopic clustering and inference pipeline designed to group comparable news headlines across German news outlets (*Tagesschau*, *FAZ*, *taz*) and highlight frame distributions.

## Repo Structure
The pipeline flows from (a) the formating + translation of SemEval data and its ground truth, a human and AI annotation pre-study as well as general preprocessing, also leveraging LLMs (GPT, Claude, Gemini, Mistral) for weak supervision on 1400+ headlines with consensus voting. Combined with additional datasets (CHN, MFC), the aggregated training data fine-tunes a Modern GBERT 134M model in (b), which is then evaluated in (c) against real Tagesschau headlines. The classification is multi-label meaning each headline can match 0 to multiple frames from the 15-category taxonomy.
* `a._preprocessing+annotation/`: Data preparation and annotation pipeline
  * `0_data_startingpoint_semeval23_framedetect/`: Raw multilingual SemEval 2023 data (en, fr, ge, it, po)
  * `1_annotationsstudie_pre-study_semeval/`: Pre-study human and llm annotation: Prepared data + Annotated data + Results
  * `2_llm-titel-annotation-aller-1400-titel_semeval/`: LLM-based annotation of ~1400 headlines: Unlabeled set + LLM annotations + Ground truth 
  *  `3_additional_data_chn+mfc/`: Additional datasets and LLM annotation on new data
  *  `Z_Policy_Frames_Codebook.pdf`: Reference codebook (Boydstun et al. 2020)
  *  `preprocessing.ipynb`: further preprocessing after annotation study (semeval, mfc, chn) + llm annotation (semeval, mfc, chn) + normalization and combining to trainingdataset
*  `b._fine_tuning+model_application/2_fine_tuning.ipynb`: Model training and inference using LSX-`UniWue/ModernGBERT_134M` on labeled data
*  `c._real_data_application/`: Evaluation and applied inference
  * `3_realdata_model_application.ipynb`: Tagesschau gold standard evaluation (70 headlines) + Applied combination of real data inference and topic clustering using BERTopic
  * `Goldstandard_Tagesschau/`: Manually annotated benchmark sets + Evaluation
    * `[name]_tagesschau_goldstandard_geprueft_[date]`: three annotation files
    * `Notebook Golstandard Tagesschau.ipynb`: Inter-Rater Agreement Assessment, Adjudication, and Gold Standard Creation
    * `goldstandard_auswertung`: Documentation of Label Discussions and final Gold Standard
  * `all_headlines_260922.xlsx`: Scraped headlines from real news outlets
  * `tagesschau_template_260917.xlsx`: Annotation template
*  `d._paper+appebduces/`: Draft paper, final paper and appendices A and B

## Data Composition
* Starting point: ~1,400 SemEval 2023 headlines
* After LLM annotation: 7,776 rows initially
* After filtering: 2,590 training samples (keeping German/Chinese or those with assigned frames)
* Gold standard: 70 manually annotated Tagesschau headlines

## Key Results
* Full Dataset (Mixed):
  * Micro-F1: 0.716
  * Macro-F1: 0.532
  * Dataset size: 2,590 headlines after filtering
  * Trained on combined SemEval + CHN + MFC data
* Tagesschau Gold Standard Benchmark:
  * Micro-F1: 0.588
  * Macro-F1: 0.379
  * Test set: 70 independently annotated human headlines from Tagesschau (Sept 17, 2026)
  * More realistic evaluation against real-world German news (Sept 22, 2026
 
 The drop-off in macro-F1 (0.532 to 0.379) on the gold standard reflects challenges with underrepresented frames, particularly the rare categories like Quality of Life (1%), Cultural Identity (1.29%), and Fairness & Equality (1.71%).


