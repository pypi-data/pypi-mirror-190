
from llama.engine.get_engine import get_engine

def fit(examples):
    return get_engine().fit(examples)


