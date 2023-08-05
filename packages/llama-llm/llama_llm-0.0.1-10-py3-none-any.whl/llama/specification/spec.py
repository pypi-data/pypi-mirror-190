
from llama.specification.base_specification import BaseSpecification
from pydantic import PrivateAttr

from llama.engine.get_engine import get_engine

class Spec(BaseSpecification):
    _node = PrivateAttr()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._node = get_engine().get_value_node(type(self))

