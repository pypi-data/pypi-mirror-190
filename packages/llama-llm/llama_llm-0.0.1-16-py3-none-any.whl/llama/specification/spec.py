
from llama.specification.base_specification import BaseSpecification
from llama.engine.nodes import ValueNode

from pydantic import PrivateAttr
import inspect

class Spec(BaseSpecification):
    _node = PrivateAttr()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._node = ValueNode(type(self))

    def __getattribute__(self, name):
        if name.find("_") == 0:
            if name != "_node":
                return super().__getattribute__(name)

        members = inspect.getmembers(Spec)
        for member_name, member in members:
            if member_name == "__dict__":
                _node = member["_node"].__get__(self)

        if name == "_node":
            return _node

        if name in self.__dict__:
            return _node.graph.engine.get_field(_node, name)

        return super().__getattribute__(name)

    def _get_attribute_raw(self, name):
        return super().__getattribute__(name)


