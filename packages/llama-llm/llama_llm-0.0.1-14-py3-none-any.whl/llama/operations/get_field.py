
from llama.engine.get_engine import get_engine

def get_field(input, field_name):
    return get_engine().get_field(input, field_name)

