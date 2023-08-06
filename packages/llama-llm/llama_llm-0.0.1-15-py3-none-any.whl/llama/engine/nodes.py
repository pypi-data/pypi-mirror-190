from llama.engine.llama import Llama

from llama.specification.base_specification import BaseSpecification
from llama.specification.context import Context

class Node:
    def __init__(self):
        self.graph = None
        self.index = None

    def set_graph(self, graph):
        self.graph = graph
        self.index = len(graph.nodes)

    def get_index(self):
        assert self.index is not None
        return self.index

    def get_predecessors(self):
        predecessors = []

        for predecessor, successor in self.graph.edges:
            if successor == self.get_index():
                predecessors.append(predecessor)

        return predecessors

    def set_inputs(self, input_values):
        self.input_values = input_values

    def get(self):
        self.graph.engine.optimize()
        self.graph.engine.execute(self)
        return self.graph.engine.get_value(self.get_index())


class ValueNode(Node):
    def __init__(self, value_type):
        super().__init__()

        self.value = None
        self.value_type = value_type

    def execute(self):
        assert not self.value is None
        return self.value

    def get_type(self):
        return self.value_type

    def __str__(self):
        return f"Value {self.value} {self.value_type}"


class LlamaNode(Node):
    def __init__(self, input_spec, output_spec):
        super().__init__()

        self.llama = Llama()

        self.input_spec = input_spec
        self.output_spec = output_spec

    def execute(self):

        return self.llama.run(
            input=self.input_values[0],
            output_spec=self.output_spec,
            temperature=self.graph.engine.temperature,
            use_examples=self.graph.engine.use_examples
        )

    def fit(self, examples):
        return self.llama.fit(examples)

    def get_type(self):
        return self.output_spec

    def __str__(self):
        return f"Running LLM on {self.input_spec} to {self.output_spec}"

class MetricNode(LlamaNode):
    def __init__(self, input_spec, output_spec):
        super().__init__(input_spec, output_spec)


class GetFieldNode(Node):
    def __init__(self, input_spec, field_name):
        super().__init__()

        self.input_spec = input_spec
        self.field_name = field_name

    def execute(self):
        return getattr(self.input_values[0], self.field_name)

    def __str__(self):
        return f"Getting field {self.field_name} from {self.input_spec}"


class Match(BaseSpecification):
    a: str = Context("the first string")
    b: str = Context("the second string")


class MatchResult(BaseSpecification):
    similarity: float = Context(
        "a number between 0.0 and 1.0 describing similarity of the input strings.  0.0 is no similarity, and 1.0 is a perfect match."
    )


class CheckMatchNode(Node):
    def __init__(self, a, b):
        super().__init__()

        self.llama = Llama()

        self.a = a
        self.b = b

    def execute(self):
        a = cast(self.input_values[0], str)
        b = cast(self.input_values[1], str)

        #print(f"Comparing: {a} & {b}")

        result = self.llama.run(input=Match(a=a, b=b), output_spec=MatchResult)

        #print("Match result is:", result)
        return result

    def __str__(self):
        return f"Checking {self.a} & {self.b}"


def cast(value, target_type):
    if isinstance(value, target_type):
        return value

    if isinstance(value, BaseSpecification):
        assert len(value.__fields__.keys()) == 1
        field_name = next(iter(value.__fields__.keys()))
        field_value = getattr(value, field_name)
        return cast(field_value, target_type)

    assert False

