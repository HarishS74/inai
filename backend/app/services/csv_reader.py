import pandas as pd

def read_csv(path: str):
    df = pd.read_csv(path)

    return df.to_string()