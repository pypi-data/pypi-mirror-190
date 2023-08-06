
from llama.engine.get_engine import get_engine

from llama.metrics.metric import Metric

def add_metric(input, metric_spec=None, fit : bool=True):
    if isinstance(input, Metric):
        input = input.get_input()
        assert metric_spec is None
        metric_spec = input.get_metric_spec()

    return get_engine().add_metric(input, metric_spec)


