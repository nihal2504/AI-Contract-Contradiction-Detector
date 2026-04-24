# Contract Contradiction Detector
## Demo

### Main Dashboard
![Home UI](screenshots/home.png)

### Results
![Results UI](screenshots/results.png)

Detect contradictory clauses in contracts using NLP.

## Features
- Clause extraction
- Pair generation
- Bidirectional contradiction scoring
- Risk levels
- CSV + JSON reports
- Streamlit UI

## Install

pip install -r requirements.txt

## Run CLI

python run_pipeline.py --input data/samples/sample_contract.txt

## Run UI

streamlit run app.py
