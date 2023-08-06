
from llama.engine.get_engine import get_engine

def metrics():
    return get_engine().get_metrics()

