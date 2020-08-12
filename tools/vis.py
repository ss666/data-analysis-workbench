import pandas as pd

def vis(path):
    df = pd.read_csv(path)
    index = df.iloc[:,0].tolist()
    content = df.iloc[:,1].tolist()
    return index, content