from llama.engine.get_engine import get_engine

def predict(input, output_spec):
    return get_engine().run(input, output_spec)

