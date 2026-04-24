import os
import json
import pandas as pd

def save_report(results):
    os.makedirs("outputs", exist_ok=True)

    with open("outputs/report.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    df = pd.DataFrame(results)
    df.to_csv("outputs/report.csv", index=False)

    return df