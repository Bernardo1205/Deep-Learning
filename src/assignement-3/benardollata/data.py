from pathlib import Path
import pandas as pd

DATASET_DIR = Path("benardollata/dataset")

def load(csv_name):
    return  pd.read_csv(DATASET_DIR / csv_name , sep="," , on_bad_lines='skip')


