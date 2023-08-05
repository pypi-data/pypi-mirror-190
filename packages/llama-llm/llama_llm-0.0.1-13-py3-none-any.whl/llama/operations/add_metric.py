
from llama.engine.get_engine import get_engine

def add_metric(input, metric_spec, fit : bool=True):
    return get_engine().add_metric(input, metric_spec)


