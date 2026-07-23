 # Fake News Detector

A simple, practical fake-news classifier built with Python, SQLite, pandas,
scikit-learn, and the News API.

## Stack

- **SQLite** — stores articles (labeled + unlabeled) and predictions
- **pandas** — cleans and reshapes data
- **scikit-learn** — TF-IDF + Logistic Regression classifier
- **News API** — pulls live articles to classify

## Project structure

```
fake_news_detector/
├── db/
│   ├── schema.sql       # table definitions
│   └── db_utils.py      # connection + query helpers
├── data/
│   └── load_dataset.py  # loads a labeled CSV dataset into SQLite
├── models/               # trained model + metrics land here
├── fetch_news.py         # pulls live articles from News API (unlabeled)
├── train.py               # trains TF-IDF + Logistic Regression on labeled data
├── predict.py             # classifies unlabeled articles, saves predictions
└── requirements.txt
```

## Setup

```bash
cd fake_news_detector
pip install -r requirements.txt
```

## 1. Get labeled training data

News API only gives you *current, unlabeled* articles — you need a labeled
dataset to train on. A common choice is Kaggle's "Fake and Real News
Dataset" (ships as `Fake.csv` + `True.csv`).

```bash
python data/load_dataset.py --fake-csv path/to/Fake.csv --real-csv path/to/True.csv
```

Or, if you have a single CSV with an explicit label column (0 = fake, 1 = real):

```bash
python data/load_dataset.py --csv path/to/news.csv --label-col label
```

This creates `db/fake_news.db` and populates the `articles` table.

## 2. Train the model

```bash
python train.py
```

This trains a TF-IDF + Logistic Regression pipeline, prints precision /
recall / F1 and a confusion matrix, and saves the fitted model to
`models/model.joblib`.

## 3. Pull live articles

```bash
export NEWS_API_KEY=your_key_here
python fetch_news.py --query "climate change" --page-size 50
# or
python fetch_news.py --top-headlines --country us
```

Live articles are stored in `articles` with `label = NULL`.

## 4. Classify

```bash
# Classify every unlabeled article currently in the DB
python predict.py

# Or classify an ad-hoc string
python predict.py --text "Scientists confirm the moon is made of cheese"
```

Predictions (label, confidence, model version) are saved to the
`predictions` table, joined to `articles` via `article_id`.

## Notes & next steps

- **Class balance**: `LogisticRegression(class_weight="balanced")` is used
  since fake/real datasets are often imbalanced.
- **Evaluation**: don't rely on accuracy alone — check the confusion matrix
  in the `train.py` output, since false positives (real flagged as fake)
  and false negatives have different real-world costs.
- **Improving the model**: try `PassiveAggressiveClassifier` or
  `LinearSVC` as drop-in replacements in `train.py`'s `build_pipeline()`,
  or add features beyond TF-IDF (e.g. source credibility, article length,
  punctuation/caps ratio for clickbait detection).
- **Retraining**: re-run `train.py` any time you load more labeled data;
  it always retrains from scratch on everything in the `articles` table
  with a non-null `label`.
