
from llama.engine.hyper_llama_engine import HyperLlamaEngine

global_engine = None

def get_engine():
    global global_engine
    if global_engine is None:
        global_engine = HyperLlamaEngine()

    return global_engine

