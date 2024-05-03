import pandas as pd

def calculate_split_index(data: pd.DataFrame, split: float):          
    split_idx = int(len(data) * split)
    return split_idx


def get_test_subset(data: pd.DataFrame, split: float):
    split_idx = calculate_split_index(data, split)
    test = data.iloc[split_idx:len(data)]
    return test
    
def get_train_subset(data: pd.DataFrame, split: float):
    split_idx = calculate_split_index(data, split)
    train = data.iloc[0:split_idx]
    return train