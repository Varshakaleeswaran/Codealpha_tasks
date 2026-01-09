import os
import pickle
from datetime import datetime

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_pickle(data, filepath):
    ensure_directory_exists(os.path.dirname(filepath))
    with open(filepath, 'wb') as f:
        pickle.dump(data, f)

def load_pickle(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'rb') as f:
        return pickle.load(f)

def get_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")
